// Olhar do Brasil · presença em tempo real (online + ponteiros anônimos)
// Nada é gravado: o servidor só repassa a posição do ponteiro (0 a 1) para os outros visitantes.

export class Sala {
  constructor(ctx, env) {
    this.ctx = ctx;
    this.env = env;
  }

  async fetch(req) {
    if (req.headers.get("Upgrade") !== "websocket") return new Response("Esperava WebSocket", { status: 400 });
    if (this.ctx.getWebSockets().length >= 300) return new Response("Lotado", { status: 503 }); // protege o limite grátis
    const [client, server] = Object.values(new WebSocketPair());
    this.ctx.acceptWebSocket(server); // API de hibernação: não cobra tempo parado
    server.serializeAttachment({ id: crypto.randomUUID().slice(0, 8), t: 0 });
    this.broadcast({ t: "n", n: this.ctx.getWebSockets().length });
    return new Response(null, { status: 101, webSocket: client });
  }

  broadcast(obj, skip) {
    const txt = JSON.stringify(obj);
    for (const w of this.ctx.getWebSockets()) {
      if (w === skip) continue;
      try { w.send(txt); } catch (_) {}
    }
  }

  webSocketMessage(ws, msg) {
    if (typeof msg !== "string" || msg.length > 100) return;
    const a = ws.deserializeAttachment() || {};
    const agora = Date.now();
    if (agora - (a.t || 0) < 100) return; // no máximo ~10 mensagens por segundo por pessoa
    let m;
    try { m = JSON.parse(msg); } catch (_) { return; }
    if (typeof m.x !== "number" || typeof m.y !== "number" || (m.c !== "cam" && m.c !== "sen")) return; // ignora o "ping"
    a.t = agora;
    ws.serializeAttachment(a);
    const lim = (v) => Math.min(1, Math.max(0, v));
    this.broadcast({ t: "m", id: a.id, x: lim(m.x), y: lim(m.y), c: m.c }, ws);
  }

  saiu(ws) {
    const a = ws.deserializeAttachment() || {};
    this.broadcast({ t: "b", id: a.id }, ws);
    this.broadcast({ t: "n", n: this.ctx.getWebSockets().filter((w) => w !== ws).length }, ws);
  }
  webSocketClose(ws) { this.saiu(ws); }
  webSocketError(ws) { this.saiu(ws); }
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (url.pathname !== "/ws") return new Response("Olhar do Brasil · presença", { status: 200 });
    const origem = req.headers.get("Origin") || "";
    const permitidas = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim());
    if (!permitidas.includes(origem)) return new Response("Origem não permitida", { status: 403 });
    return env.SALA.get(env.SALA.idFromName("global")).fetch(req);
  },
};
