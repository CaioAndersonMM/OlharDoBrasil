#!/usr/bin/env python3
"""Olhar do Brasil: coleta mensal (Câmara + Senado).
Gera data/*.json, páginas estáticas por partido e parlamentar (SEO), sitemap.xml e robots.txt.
Só usa a biblioteca padrão do Python. Coloque em coleta/coletar.py no repositório."""
import json, os, re, time, unicodedata, urllib.request
from datetime import date, timedelta
from html import escape as E
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = os.environ.get("SITE_URL", "https://olhardobrasil.caioandersonmartins.workers.dev").rstrip("/")
CAM = "https://dadosabertos.camara.leg.br/api/v2"
SEN = "https://legis.senado.leg.br/dadosabertos"

CSS = ("body{font-family:Inter,system-ui,sans-serif;max-width:860px;margin:0 auto;padding:0 20px 40px;color:#0b1f4d;background:#fff}"
       ".s{height:5px;background:linear-gradient(90deg,#009c3b 34%,#f2b705 34% 66%,#002776 66%);margin:0 -20px}"
       "h1{font-size:34px;margin:28px 0 6px;color:#002776}a{color:#009c3b}.m{color:#6a7592}ul{columns:2;padding-left:18px}"
       "img{width:96px;height:120px;object-fit:cover;border-radius:10px;float:left;margin:0 18px 10px 0}"
       ".b{display:inline-block;margin-top:18px;background:#002776;color:#fff;padding:10px 18px;border-radius:10px;text-decoration:none}")


def get(url, tries=4):
    """GET JSON com novas tentativas e pausa (a API da Câmara pode devolver 429)."""
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                        "User-Agent": "OlharDoBrasil/1.0 (coleta mensal)"})
            with urllib.request.urlopen(req, timeout=40) as r:
                time.sleep(0.4)
                return json.load(r)
        except Exception as e:
            print("falha:", url, e)
            time.sleep(2 * (i + 1))
    return None


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "x"


def deputados():
    out, url = [], CAM + "/deputados?itens=100&ordem=ASC&ordenarPor=nome"
    while url:
        d = get(url)
        if not d:
            break
        out += d.get("dados", [])
        url = next((l["href"] for l in d.get("links", []) if l.get("rel") == "next"), None)
    return [{"id": x["id"], "nome": x["nome"], "partido": x.get("siglaPartido") or "S/Partido",
             "uf": x.get("siglaUf", ""), "foto": x.get("urlFoto", ""), "casa": "Câmara"} for x in out]


def senadores():
    d = get(SEN + "/senador/lista/atual") or {}
    try:
        lista = d["ListaParlamentarEmExercicio"]["Parlamentares"]["Parlamentar"]
    except (KeyError, TypeError):
        return []
    if isinstance(lista, dict):
        lista = [lista]
    out = []
    for p in lista:
        i = p.get("IdentificacaoParlamentar", {})
        out.append({"id": i.get("CodigoParlamentar"), "nome": i.get("NomeParlamentar", ""),
                    "partido": i.get("SiglaPartidoParlamentar") or "S/Partido", "uf": i.get("UfParlamentar", ""),
                    "foto": i.get("UrlFotoParlamentar", ""), "casa": "Senado"})
    return out


def diagnostico():
    """Testa se a API da Câmara devolve votos individuais de votações recentes."""
    fim = date.today()
    ini = fim - timedelta(days=120)
    d = get(f"{CAM}/votacoes?dataInicio={ini}&dataFim={fim}&ordem=DESC&ordenarPor=dataHoraRegistro&itens=8") or {}
    res = []
    for v in d.get("dados", []):
        votos = get(f"{CAM}/votacoes/{v['id']}/votos") or {}
        res.append({"id": v["id"], "data": v.get("data"), "descricao": (v.get("descricao") or "")[:120],
                    "votos_individuais": len(votos.get("dados", []))})
    return {"executado_em": str(fim), "camara_votacoes_testadas": res}


def page(path, title, desc, body, ld=None):
    url = f"{SITE}/{path}"
    j = '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False) if ld else ""
    html = ('<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}</title><meta name="description" content="{E(desc)}">'
            f'<link rel="canonical" href="{url}"><meta property="og:title" content="{E(title)}">'
            f'<meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website">'
            f'<meta property="og:url" content="{url}"><style>{CSS}</style>{j}</head><body><div class="s"></div>'
            f'{body}<p><a class="b" href="{SITE}/">Abrir o plenário interativo</a></p>'
            f'<p class="m"><a href="{SITE}/partidos/">Partidos</a> · <a href="{SITE}/parlamentares/">Parlamentares</a>'
            ' · Dados: Câmara dos Deputados e Senado Federal (dados abertos).</p></body></html>')
    f = ROOT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(html, encoding="utf-8")
    return url


def main():
    dep, sen = deputados(), senadores()
    if not dep and not sen:
        raise SystemExit("Nenhum dado coletado: arquivos anteriores mantidos.")
    (ROOT / "data").mkdir(exist_ok=True)
    for nome, dados in (("camara", dep), ("senado", sen)):
        if dados:  # nunca sobrescreve com lista vazia
            (ROOT / "data" / f"{nome}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROOT / "data" / "diagnostico.json").write_text(json.dumps(diagnostico(), ensure_ascii=False, indent=1), encoding="utf-8")

    todos = dep + sen
    urls = [SITE + "/"]
    partidos = {}
    for p in todos:
        p["pagina"] = f"parlamentares/{slug(p['nome'])}-{p['casa'][0].lower()}{p['id']}.html"
        partidos.setdefault(p["partido"], []).append(p)

    for p in todos:
        cargo = "Deputado(a) federal" if p["casa"] == "Câmara" else "Senador(a)"
        foto = f'<img src="{E(p["foto"])}" alt="Foto de {E(p["nome"])}">' if p["foto"] else ""
        body = (f'{foto}<h1>{E(p["nome"])}</h1><p class="m">{cargo} · {E(p["partido"])} · {E(p["uf"])}</p>'
                f'<p>Veja a bancada do <a href="{SITE}/partidos/{slug(p["partido"])}.html">{E(p["partido"])}</a> '
                'e a posição de cada cadeira no plenário.</p><div style="clear:both"></div>')
        ld = {"@context": "https://schema.org", "@type": "Person", "name": p["nome"], "jobTitle": cargo,
              "affiliation": {"@type": "Organization", "name": p["partido"]}}
        if p["foto"]:
            ld["image"] = p["foto"]
        urls.append(page(p["pagina"], f'{p["nome"]} ({p["partido"]}-{p["uf"]}) | Olhar do Brasil',
                         f'{cargo} {p["nome"]} ({p["partido"]}-{p["uf"]}): partido, bancada e posição no plenário do Congresso.', body, ld))

    lista_p = []
    for sigla, ms in sorted(partidos.items()):
        nc = sum(m["casa"] == "Câmara" for m in ms)
        ns = len(ms) - nc
        itens = "".join(f'<li><a href="{SITE}/{m["pagina"]}">{E(m["nome"])}</a> ({E(m["uf"])})</li>' for m in ms)
        body = f'<h1>{E(sigla)}</h1><p class="m">{nc} deputados e {ns} senadores em exercício.</p><ul>{itens}</ul>'
        u = page(f"partidos/{slug(sigla)}.html", f"{sigla}: deputados e senadores | Olhar do Brasil",
                 f"Veja os {len(ms)} parlamentares do {sigla} no Congresso Nacional: {nc} na Câmara e {ns} no Senado.", body)
        urls.append(u)
        lista_p.append(f'<li><a href="{u}">{E(sigla)}</a> ({len(ms)})</li>')
    urls.append(page("partidos/index.html", "Partidos do Congresso Nacional | Olhar do Brasil",
                     "Lista de partidos com deputados e senadores em exercício.", f"<h1>Partidos</h1><ul>{''.join(lista_p)}</ul>"))
    lista = "".join(f'<li><a href="{SITE}/{m["pagina"]}">{E(m["nome"])}</a> ({E(m["partido"])}-{E(m["uf"])})</li>'
                    for m in sorted(todos, key=lambda m: m["nome"]))
    urls.append(page("parlamentares/index.html", "Deputados e senadores | Olhar do Brasil",
                     "Lista de todos os deputados federais e senadores em exercício.", f"<h1>Parlamentares</h1><ul>{lista}</ul>"))

    hoje = str(date.today())
    sm = "".join(f"<url><loc>{u}</loc><lastmod>{hoje}</lastmod></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + sm + "</urlset>", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"ok: {len(dep)} deputados, {len(sen)} senadores, {len(urls)} páginas")


if __name__ == "__main__":
    main()
