# OlharDoBrasil

Plataforma web estática para visualização e simulação do Congresso Nacional Brasileiro, com uma interface inspirada em painéis institucionais e foco em leitura espacial, dinâmica política e interação por perfil parlamentar.

O projeto foi construído em um único arquivo HTML e utiliza JavaScript puro, Tailwind via CDN e Font Awesome para compor uma experiência visual rica, responsiva e leve de executar localmente.

## Visão Geral

O objetivo do projeto é representar de forma didática e visual o funcionamento do plenário da Câmara dos Deputados e do Senado Federal, permitindo ao usuário alternar entre casas legislativas, inspecionar parlamentares, simular votações e consultar um dossiê sintético com informações de atuação.

Embora a interface seja inspirada no Congresso Nacional real, os dados exibidos são gerados de forma simulada no próprio front-end. Isso torna o projeto ideal para demonstrações, prototipação de produto, estudos de UX e experimentação com visualização institucional.

## Funcionalidades Atuais

- Alternância entre Câmara dos Deputados e Senado Federal.
- Duas áreas principais de navegação: visualização do plenário e simulação legislativa.
- Renderização vetorial do hemiciclo com assentos distribuídos de acordo com a casa selecionada.
- Seleção de parlamentares por clique ou hover, com tooltip contextual.
- Card de detalhes do parlamentar com partido, UF, espectro político e status.
- Simulador de votação com pautas pré-configuradas e placar em tempo real.
- Indicadores visuais de voto por cadeira, com atualização progressiva do plenário.
- Dossiê detalhado do parlamentar com emendas simuladas e histórico de votações.
- Áudio ambiente opcional e efeitos sonoros para reforçar a imersão.
- Reinicialização do estado do plenário e das votações.

## Como Executar

O projeto não depende de build, bundler ou backend.

1. Abra o arquivo `index.html` diretamente no navegador.
2. Para uma melhor experiência visual, use um navegador moderno com suporte a SVG, Tailwind via CDN e Web Audio API.
3. Como a interface carrega fontes e bibliotecas externas, é recomendável estar conectado à internet.

## Tecnologias Utilizadas

- HTML5
- CSS3 com utilitários do Tailwind CSS
- JavaScript Vanilla
- SVG para a composição do plenário
- Web Audio API para ambiência e efeitos sonoros
- Google Fonts
- Font Awesome

## Estrutura do Projeto

- `index.html`: aplicação principal, interface, estilos e lógica da simulação.
- `README.md`: documentação do projeto.

## Decisões de Produto e UX

- A interface adota uma linguagem institucional, escura e solene para reforçar a proposta temática.
- A separação entre visualização e simulação permite leitura limpa do plenário sem perder a camada analítica.
- A utilização de dados sintéticos evita dependência de APIs externas na versão atual.
- A composição em um único arquivo facilita distribuição, testes rápidos e prototipagem.

## Limitações Atuais

- Os parlamentares, emendas e históricos são simulados em tempo de execução.
- Não há persistência de dados entre sessões.
- Não existe integração com base oficial de dados legislativos.
- Não há autenticação, perfis de usuário ou trilhas de auditoria.

## Projeções Para Futuras Implementações

### Integração com Dados Reais

- Conectar o projeto a APIs públicas ou a uma camada de backend própria para consumir dados oficiais da Câmara e do Senado.
- Substituir os registros gerados localmente por informações verificadas de parlamentares, partidos, votações, presença e emendas.
- Permitir atualização automática por período legislativo, legislatura ou sessão.

### Persistência e Backend

- Criar uma API para armazenar pautas, votações, perfis e histórico de interação.
- Salvar estados de simulação, favoritos e filtros do usuário.
- Permitir auditoria e comparação entre votações reais e simulações.

### Ferramentas Analíticas

- Implementar filtros por partido, UF, espectro político e situação.
- Adicionar busca por nome de parlamentar ou sigla partidária.
- Incluir comparativos entre casas legislativas, bancadas e blocos ideológicos.
- Gerar relatórios exportáveis em PDF, CSV ou JSON.

### Acessibilidade e Experiência

- Melhorar contraste, navegação por teclado e suporte a leitores de tela.
- Incluir descrições acessíveis para elementos SVG e tooltips.
- Oferecer modo de redução de movimento e ajustes visuais para diferentes perfis de uso.

### Evolução da Simulação

- Criar pautas dinâmicas com parâmetros editáveis.
- Adicionar regras de coalizão, disciplina partidária e comportamento por bancada.
- Simular quórum, obstrução, empate e eventos de sessão com maior profundidade.

### Produto e Distribuição

- Transformar a aplicação em SPA ou PWA para uso offline e instalação como aplicativo.
- Criar páginas adicionais para dashboards, perfil de bancada e histórico legislativo.
- Estruturar testes automatizados para preservar a lógica de votação e renderização.

## Possível Próximo Passo

Se o objetivo for evoluir o projeto para uma versão mais robusta, o caminho mais natural é separar interface, dados e regras de negócio em camadas distintas, começando por um backend leve e uma fonte de dados oficial.

## Licença

Defina aqui a licença do projeto caso ele seja distribuído publicamente.
