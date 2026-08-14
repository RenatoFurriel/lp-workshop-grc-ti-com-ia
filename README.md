# LP — Workshop GRC TI com IA (3ª edição)

Página de captura de **4 dobras** para o workshop de 22/08/2026, montada a partir do
PDF de design `[PÁGINA] WORKSHOP GRC TI COM IA` e da identidade oficial do
**Manual da Marca v1.3** (Google Drive → *Identidade Visual*).

Dobras: **Hero** · **Conteúdo (5 blocos)** · **E você ainda vai receber** · **Quem será o seu mentor**

Feita para ser colada em **um bloco de HTML do GreatPages**.

| | |
|---|---|
| Fonte de verdade | `index-c.html` |
| Bloco para colar | `dist/greatpages-block-c.html` |
| Fundo da página | Preto Comando `#0D0D0D` |
| Layout | "blueprint de sala de comando" — ver [§9](#9-o-layout-blueprint-de-sala-de-comando) |

> **Versões A e B removidas.** O projeto tinha três layouts: A e B (as 4 dobras do
> PDF, em fundo claro e escuro, saindo de um `index.html` comum) e a C. A e B foram
> **descartadas** — nada neste repositório as gera mais. Se precisar delas, estão
> inteiras no histórico do git, até o commit `7dde696`:
>
> ```bash
> git show 7dde696:index.html                     > index.html
> git show 7dde696:dist/greatpages-block.html     > bloco-a.html
> git show 7dde696:dist/greatpages-block-b.html   > bloco-b.html
> ```
>
> Elas nunca receberam a URL do formulário (ficaram no placeholder), então não
> estavam prontas para tráfego.

---

## 1. O que entregar no GreatPages

Um arquivo só: **`dist/greatpages-block-c.html`**.

1. No GreatPages, inserir **um bloco de HTML / Código** e colar o arquivo inteiro.
2. Definir o **fundo da página** como **`#0D0D0D`**. Sem isso, o bloco aparece como
   um retângulo emoldurado.
3. Desativar qualquer bloco nativo de hero/título na mesma página — o bloco já traz
   o `<h1>`.
4. **Não reabrir o bloco no editor visual** depois de colado: o editor pode
   reprocessar o HTML e quebrar o conteúdo.

---

## 2. O formulário de inscrição

A URL mora em **dois lugares** de cada HTML de origem, de propósito: a constante
`FORM_URL` no `<script>` e o `href` de cada link `data-form`. O `href` real
garante que o botão funcione mesmo com o JavaScript desligado; o JS só acrescenta
os parâmetros de campanha.

A URL atual é `https://link.itxpro.com.br/insc-grcti-ia-form`.

Cada um dos 5 CTAs leva a sua referência no **`utm_term`**, para dar para ver no
formulário qual botão converteu:

| `data-form` | `utm_term` | Onde |
|---|---|---|
| `topo` | `01-topo` | barra do cabeçalho |
| `hero` | `02-hero` | primeira dobra |
| `entregaveis` | `03-entregaveis` | depois do workbook e do certificado |
| `mentor` | `04-mentor` | fecha a dobra do mentor |
| `sticky` | `05-sticky-mobile` | barra fixa do mobile |

Numerado com zero à esquerda para ordenar certo em relatório que trate o campo
como texto.

> **⚠️ O `utm_term` do botão sobrescreve o que vier na URL da página.** Se os seus
> anúncios usam `utm_term` para palavra-chave, essa palavra-chave **se perde** ao
> clicar no CTA. Foi implementado assim porque foi o campo pedido; se você usa
> `utm_term` para keyword, o campo natural para a referência do botão seria o
> `utm_content` — é trocar o nome em uma linha no `index-c.html`
> (`u.searchParams.set("utm_term", ref)`).

> **`link.itxpro.com.br` é um encurtador.** Quem precisa repassar a query string no
> redirecionamento é ele. Se descartar, o lead chega sem origem **e sem a referência
> do botão**. Vale abrir a página com `?utm_source=teste` e conferir o que chega no
> formulário.

O `utm_term` também está nos `href` estáticos do HTML, então a referência do
botão funciona **mesmo com o JavaScript desligado** — nesse caso só as UTMs da
página não são propagadas.

**Atribuição de campanha:** os CTAs propagam automaticamente `utm_*`, `gclid`,
`fbclid`, `ttclid`, `msclkid`, `src` e `sck` da URL da página para o formulário.
Sem isso o lead chega sem origem.

---

## 3. Identidade da marca aplicada

Tudo vem do Manual da Marca v1.3. As três cores e a proporção 70/20/10:

| Cor | HEX | Papel |
|---|---|---|
| Preto Comando | `#0D0D0D` | fundo de toda a página |
| Branco Osso | `#F0EBE1` | títulos e texto |
| Laranja Núcleo | `#F26101` | CTA, marca-texto, logo, ícones, círculo do mentor |

**Tipografia:** **Khand Bold** em títulos (sempre caixa-alta, peso 700, como manda o
manual) e **Archivo** em todo o texto corrido. Ambas auto-hospedadas em WOFF2 e
embutidas no bloco — **zero requisição externa de fonte**. Os arquivos vêm do Google
Fonts (as mesmas famílias do kit), com subset para os glifos usados.

### A regra de contraste que não deve ser desfeita

O próprio manual mede **laranja sobre osso em 2,7:1** e proíbe texto corrido. Medi
aqui: **2,73:1** — reprova até para texto grande (mínimo 3,0). Por isso:

| Uso | Cor | Contraste |
|---|---|---|
| Preenchimento (CTA, marca-texto, logo, ícones, círculo) | `#F26101` | — |
| Texto laranja sobre Preto Comando | `#F26101` | 6,00:1 ✓ AA |
| Osso sobre Preto Comando | `#F0EBE1` | 16,4:1 ✓ AAA |
| Corpo (osso 80%) sobre Preto Comando | — | 10,8:1 ✓ AAA |

Como a página é toda escura, o laranja **puro da marca** pode ser texto. Onde ele
cai sobre superfície clara — só no certificado — vai em tinta escura `#0D0D0D`,
porque sobre fundo claro o laranja rende 2,73:1 e o próprio manual o proíbe como
texto corrido.

---

## 4. Como gerar o bloco

```bash
python3 build_greatpages.py
```

Requer Pillow e fontTools (`pip3 install Pillow fonttools brotli`).
Para validar um bloco já gerado:

```bash
python3 build_greatpages.py --check
```

O que o build faz — e por que cada passo existe:

| Passo | Motivo |
|---|---|
| Escopa todo o CSS em `#ix-ws3` | nada do bloco vaza para a página do GreatPages |
| Embute fontes e a foto como data URI | zero request de imagem/fonte; o bloco é autossuficiente |
| Faz **subset** das fontes | Khand 7,4→5,8 KB · Archivo 34,1→25,7 KB |
| Converte tudo para **ASCII puro** | o GreatPages controla o `<head>` e o charset; sem isso a acentuação vira mojibake |
| Remove os **comentários HTML** do bloco | documentam a fonte (por que cada decisão existe, como trocar o mockup por um render); não têm o que fazer numa página servida ao público |
| Relatório de peso, com corte em 175 KB | impede que a página engorde sem ninguém perceber |

Peso atual, com **zero requisições externas**: **~169 KB cru / ~93 KB gzip**.

São ~118 KB de assets embutidos (fontes com subset + foto) e ~51 KB de CSS/HTML.
Para referência, a LP anterior (`insc-hic-b`) tem 152 KB / 96 KB e ainda baixa
fontes do Google.

> **O build não é determinístico.** O `fontTools` grava a data da modificação
> dentro da fonte, então o base64 das duas fontes muda a cada rodada e o
> arquivo de `dist/` sempre aparece como modificado no `git status`, mesmo
> sem nenhuma mudança de conteúdo. Para comparar dois builds de verdade, ignore
> os `data:font/woff2;base64,...`.

---

## 5. Arquivos

```
index-c.html                 ← FONTE DE VERDADE. Editar aqui. Abre direto no navegador.
build_greatpages.py          ← gera o bloco a partir do index-c.html
dist/greatpages-block-c.html ← ★ o que vai para o GreatPages
dist/host-simulator.html     ← teste: injeta o bloco num host hostil (ver abaixo)
assets/                      ← fontes da marca + foto + logo (o build otimiza na hora)
copy/                        ← a copy aprovada, em markdown
criativos/                   ← criativos de anúncio (fora do escopo da LP)

dashboard-leads-grcti-ia.html ← painel de leads deste workshop (ver §10)
agente-limpeza-leads-ia.gs    ← agente de limpeza da base, roda no Google Apps Script
regras-negocio-dashboard.md   ← regras do painel. NÃO versionado (critérios comerciais)
```

O `index-c.html` referencia `assets/` por caminho, não por base64 — assim continua
legível e com diff limpo. O base64 existe apenas em `dist/`.

`assets/logo-x-512.png` não é usado pela página (é o símbolo isolado do X, do kit da
marca). Fica como referência.

**A foto do Arteiro entra uma única vez** no bloco, via variável CSS `--foto`, e é
reaproveitada no hero (com fade) e no círculo do mentor (recortada por
`background-position`). Como duas tags `<img>`, o mesmo base64 seria embutido duas
vezes — 48 KB jogados fora. O arquivo em `assets/` já está cortado no alpha
(833×1027) para que o preview local e o bloco final enquadrem a foto igual.

---

## 6. Teste antes de publicar

```bash
python3 -m http.server 8753
```

- Página: `http://localhost:8753/index-c.html`
- QA: `http://localhost:8753/dist/host-simulator.html?utm_source=qa`

O host-simulator reproduz de propósito um host hostil (reset `content-box`, fonte
serifada global, `img{width:100%!important}`, `svg{width:50px!important}`,
`section{background:#0f0!important}`, `footer{background:#600!important}`, estilos em
`.btn`/`.card`, container de 1170px e um ancestral com `transform`, que quebra
`position:fixed`). Ele injeta o bloco, **percorre a página inteira em passos** (o reveal é disparado
por rolagem) e imprime **29 verificações** no canto — entre elas: nenhum overflow
horizontal, os elementos do host intactos, Khand e Archivo aplicadas, o fundo e a
dobra 2 mantendo as cores da marca, os ícones não esmagados, a logo no tamanho
certo, o círculo do mentor redondo, todo o conteúdo revelado e a UTM propagada.

Testar em 390px e em ≥1180px: a CTA fixa só aparece abaixo de 880px.

> **Auditar com a aba na frente.** Aba em segundo plano não roda
> `requestAnimationFrame` nem entrega `IntersectionObserver`, então a varredura do
> reveal fica parada e o viewport pode colapsar para 0×0 — o painel reporta
> `reveal: N/A` nesse caso, mas as medidas de largura viram lixo.

---

## 7. Decisões que não devem ser desfeitas sem motivo

**O `!important` em imagens, SVG e nos fundos das superfícies é proposital.**
Construtores injetam `img{width:100%!important}`, `svg{width:50px!important}` e
estilizam `section`/`footer` por tag com `!important`. Sem isso a foto estoura, os
ícones viram selos de 50px e as dobras perdem a cor da marca. As três falhas
foram observadas no host-simulator antes da correção.

**A animação de entrada tem duas redes de segurança.** O `opacity:0` só é armado
quando o JS confirma que rodou (classe `.ix-js`), e se o `IntersectionObserver` não
entregar nada em 1,4s o conteúdo aparece de uma vez. Sem isso, JS quebrado ou
observer inerte deixaria a página **em branco** — risco real dentro de iframes e
navegadores embutidos.

**O mockup do Workbook e o selo do certificado são CSS/SVG, não imagens.** O kit da
marca não tem esses assets. Feitos em código, custam ~0 KB, escalam sem borrar e se
ajustam se a data mudar (a capa lê `22/08/26` como texto).

**Os 5 ícones dos blocos são SVG inline**, desenhados com traço uniforme de 1,7px.
Não há dependência de biblioteca de ícones.

---

## 8. Pendências de copy

- A copy dos 5 blocos veio do PDF de design e **difere** da versão em
  `copy/copy-lp-workshop-grc-ti-ia-v3.md` (que descrevia 3 dobras, sem os blocos
  numerados). O PDF é a versão mais recente e foi a seguida. Vale consolidar as duas.
- **Depoimentos.** Duas edições, centenas de participantes, nenhum depoimento na
  página. Continua sendo o maior ganho de conversão disponível.
- Corrigi um erro de digitação do PDF no bloco 1: *"infraestrurua"* → *"infraestrutura"*.
  No bloco 5, *"sistematica"* → *"sistemática"*.

---

## 9. O layout "blueprint de sala de comando"

Referência de estilo: a home da **asimov.academy** (dark premium, luz, movimento).
Mas a página não copia o layout de lá — ela tem uma ideia própria, e é dela que sai
tudo:

> **O símbolo da ITXPRO já é um diagrama de nós** — o "diagrama de orquestração" do
> manual. Se o produto é *arquitetura cognitiva*, a página é o **blueprint** dela.

Daí saem todas as decisões visuais: rede de nós no hero, painéis com cantos em
colchete, numeração de seção, rótulos técnicos com tracking largo, os 5 blocos como
uma **pilha de arquitetura** com espinha e nós numerados, e grão fotográfico sobre
tudo. Cantos quase retos (4px) nos painéis e pílula só nos CTAs: superfície
técnica, ação macia.

### O hero no mobile não tem a foto

Na primeira dobra, o mobile **não** mostra a foto do mentor: ela ocupava 441px de
altura numa tela de 667px e a dobra pedia duas rolagens para ser lida. No lugar
dela o H1 cresce (19vw, ~71px em 375px de tela, quebrando em duas linhas como no
desktop) e a atmosfera fica por conta da cena de fundo, que já existia — a rede de
nós, as auras e a grade do horizonte.

O que garante "uma visualização só" é `min-height:calc(100svh - 66px)` no hero:
66px é a altura medida do cabeçalho, e **`svh`** (não `vh`) é a altura que sobra com
a barra do navegador móvel aberta. Com `vh` o hero ficava mais alto que a tela útil
e voltava a exigir rolagem. Medido — a primeira dobra fecha exatamente na altura da
tela em 320×568, 360×640, 375×667 e 430×932.

No **desktop nada mudou**: a foto continua na dobra 1 e no círculo da dobra 4.

### O que veio do PDF de design e não deve mudar

Este layout nasceu como alternativa às versões A e B (as 4 dobras do PDF, hoje
removidas). Estes quatro pontos foram mantidos por contrato:

| Mantido | Onde |
|---|---|
| **A copy**, palavra por palavra | verificada, enquanto A/B existiam, por diff de contagem de palavras — zero perdas |
| **Tipografia da marca** | Khand Bold caixa-alta nos títulos, Archivo no corpo |
| **Paleta** | Preto Comando · Branco Osso · Laranja Núcleo |
| **Foto do mentor no hero** | mesmo recorte com fade — **só no desktop**, ver acima |
| **Foto do mentor na última dobra** | mesmo círculo com fundo Laranja Núcleo |

A barra do topo e a ficha técnica reaproveitam strings que já existiam na CTA fixa
(`Quero minha vaga` e `Sáb 22/08 · 9h–18h`). Nada de copy nova foi inventada.

### As peças novas

| Peça | Como funciona |
|---|---|
| **Rede de nós** no hero | SVG inline: 22 arestas, 16 nós, 2 anéis e **7 pulsos** correndo as arestas por `stroke-dashoffset` com atrasos diferentes. Zero asset, zero biblioteca. |
| **Grão fotográfico** | `feTurbulence` inline (~0,4 KB) em `mix-blend-mode:overlay` a 5%. É o que impede o bandeamento dos gradientes numa tela toda escura. |
| **Pilha de arquitetura** | Espinha vertical + nós numerados que acendem. No desktop pelo hover; no mobile, pela camada que passa no meio da tela (`IntersectionObserver` com `rootMargin:-45%`). |
| **Luz que segue o ponteiro** | JS escreve `--mx/--my` no painel sob o cursor. Só com `(hover:hover) and (pointer:fine)`. |
| **Cantos em colchete** | 8 gradientes de fundo posicionados, não `border` — construtores injetam `border:6px solid!important` e um border próprio perderia a briga. |
| **Progresso de leitura** | 2px de laranja no fio inferior da barra do topo, via `scaleX`. |
| **Numerais fantasma** | `content:attr(data-n)` a 3% de opacidade, cortado no canto do painel. Peso editorial a custo zero. |
| **Logo em mascara CSS** | A logo oficial (`assets/marca-itxpro-escuro.png`) foi vetorizada com potrace (**traçando `alpha<=128`**: o potracer trata `True` como *fundo*, então traçar `alpha>128` produz o negativo — um bloco laranja com as letras vazadas) e entra como `mask-image` em data URI — 5,3 KB contra 15 KB do raster em base64, e nitida em qualquer tamanho. Como o arquivo e preto sobre transparente, quem pinta e o `background-color`: **um arquivo serve as quatro cores** de que a pagina precisa (laranja no topo e no rodape, tinta escura no certificado, osso apagado na marca d'agua). Efeito colateral util: nao sendo `<img>` nem `<svg>`, passa ilesa por `img{width:100%!important}` e `svg{width:50px!important}` do host. |
| **Ficha tecnica** | No desktop, 3 celulas divididas por fio. No mobile viram uma **esteira** que corre devagar: o conteudo entra duas vezes e a trilha anda `-50%`, entao o loop e continuo e sem salto (empilhadas, as 3 celulas comiam 180px de altura). |
| **Credenciais como números** | As duas primeiras viram `40.000` e `200` em corpo grande. O texto é o mesmo — só a hierarquia tipográfica muda. |

### Os dois objetos em 3D

Nem o workbook nem o certificado existem como asset no kit da marca. Os dois são
construídos em CSS, com `transform-style: preserve-3d`.

**Workbook** — 5 faces reais (capa, lombada, corte das folhas, topo e contracapa).
Duas coisas foram descobertas na tentativa e erro e não devem ser desfeitas:

1. **A câmera importa mais que a rotação.** `perspective-origin` com **Y negativo**
   (`55% -12%`) põe o observador *acima* do topo do livro. Sem isso a face de topo
   fica de costas e o livro é uma capa chapada — por mais que se aumente o
   `rotateX`. Com ela, o bloco de folhas aparece e o objeto ganha espessura.
2. **`rotateY` positivo** traz a lombada para o lado visível. Com negativo aparece
   o corte das folhas e a lombada fica escondida atrás.
   E `perspective:2400px`, não 1500: com a perspectiva curta o keystone virava
   olho-de-peixe e a tipografia da capa entortava.

Cada face lateral gira em torno da **sua** aresta (`transform-origin` na aresta) e
depois é empurrada meia profundidade para trás — `translateZ(-d/2) rotateY(-90deg)`,
aplicado da direita para a esquerda, encaixa a face exatamente entre contracapa e
capa.

**Certificado** — folha em perspectiva com moldura dupla, linha de nome em branco
(como num certificado de verdade), rubrica em SVG, data e o selo em alto-relevo
(duas `drop-shadow`: uma clara acima, uma escura abaixo). A moldura dupla é
`border` + `outline` com `outline-offset`: com `box-shadow` e spread eu tinha uma
faixa cinza **cheia**, porque o spread pinta o anel inteiro e não a borda dele.

Toda palavra na folha já existe na página (*Certificado de participação*, *Workshop
GRC TI com IA*, *22/08/26*, *Roberto Arteiro*, *ITXPRO*) — nenhuma copy nova.

Os dois têm o caminho de troca documentado no HTML: quando os renders reais
chegarem, é salvar em `assets/`, trocar o bloco pelo `<img>` e registrar em
`ASSETS` no build.

**Escala de laranja:** os efeitos de luz pedem tons acima e abaixo do `#F26101`.
Os dois tons derivados (`--laranja-luz`, `--laranja-fundo`) aparecem **só** em
brilho, gradiente e halo — nunca como cor de texto ou preenchimento sólido. Texto
e CTA seguem no `#F26101` puro (6,00:1 sobre o Preto Comando, AA).

### Duas armadilhas de escala que custaram caro

**O certificado ficava em branco no mobile.** Tudo dentro da folha e medido em
`cqw` (largura do proprio container), entao quando a folha encolhe o texto
encolhe junto: em 375px de tela os rotulos caiam para **5,7px** e a folha parecia
vazia, com so a rubrica (vetor) visivel. A correcao nao e "aumentar a fonte" e
sim **subir a escala tipografica inteira no mobile**, dar toda a largura util a
folha e reduzir a rotacao para o texto nao entortar.

**O reveal podia deixar conteudo invisivel para sempre.** O
`IntersectionObserver` amostra o estado por frame: num SALTO de rolagem
(arrastar a barra, tecla End, deep link com `#ancora`) o elemento entra e sai
entre duas amostras e nunca recebe callback — e como o reveal usa `opacity:0`,
aquele bloco nao aparece nunca mais. Medido com saltos de 600px: **4 de 26
elementos** ficavam invisiveis. A C ganhou uma varredura de retaguarda no mesmo
`requestAnimationFrame` do progresso de leitura: se o topo do elemento ja passou
pela base da viewport, ele tem de estar visivel. A lista se esvazia sozinha.

> O host-simulator tambem estava medindo isso errado: auditava a pagina **parada**
> e por isso acusava "reveal visiveis (4/26)". Agora ele percorre a pagina inteira
> em passos, como um usuario, e so depois audita.

**Sem `@property`** em nenhum lugar: o build o trataria como seletor e o quebraria.

<a id="o-bug-da-cta-fixa-que-a-c-corrigiu"></a>
### O bug da CTA fixa

Quando um ancestral com `transform` quebra o `position:fixed`, o JS reancora a
barra no `<body>`. Só que **todo** o CSS do bloco é escopado em `#ix-ws3` — ao sair
da raiz, a barra perdia cada uma das suas regras e virava um `<div>` estático, sem
cor, no fim da página. O host-simulator não pegava isso porque a verificação
aceitava `parentNode === body` como prova de sucesso.

Aqui o reancoramento injeta no mesmo instante uma folha com as regras
equivalentes **sem escopo**, todas presas a `#ix-sticky` (id que só existe no
bloco, então não toca em nada do host). E a verificação do QA agora mede o que
importa: barra colada na viewport **e** ainda estilizada.

As versões A e B carregavam esse bug até serem removidas — o mesmo trecho de JS,
sem a folha sem escopo. Se alguém ressuscitar aquele código do histórico, é isto
que precisa ser portado.

---

## 10. Painel de leads

`dashboard-leads-grcti-ia.html` — painel interno de acompanhamento da captação deste
workshop, publicado junto com a LP:

**https://renatofurriel.github.io/lp-workshop-grc-ti-com-ia/dashboard-leads-grcti-ia.html**

| | |
|---|---|
| Fonte | Planilha do Respondi, lida direto pelo endpoint `gviz` do Google |
| Contatos | **Não trafegam**: a URL seleciona só as colunas sem nome/e-mail/WhatsApp |
| Atualização | Relê a planilha a cada 5 min |
| Regras de negócio | `regras-negocio-dashboard.md` (local, fora do repo — critérios comerciais) |

O painel mostra total de leads, MQL START e MQL PRO, % de MQL contra a meta de 80%,
linha do tempo diária e 12 gráficos de perfil e de aquisição (incluindo `utm_term`,
que mostra **qual botão da LP converte** — é o mesmo `utm_term` que o `index-c.html`
carimba em cada CTA). Abaixo dos KPIs há uma fileira de cards de **presença ao vivo** (um por resposta da pergunta "você poderá participar no dia 22/Ago?"), com quantidade e percentual.

Todos os gráficos filtram uns aos outros ao clique, estilo BI — e **os cards do topo também**: clicar em MQL PRO, por exemplo, filtra o painel inteiro por esse público e zera os demais cards; o card Total limpa os filtros.

Ele nasceu como cópia do painel do workshop de julho (projeto `O_novo_profissional_de_TI`,
repositório `Workshop-HIC`), que continua no ar com a base antiga. **Correção estrutural
feita lá não chega aqui sozinha**, e vice-versa.

`agente-limpeza-leads-ia.gs` roda dentro da planilha (Extensões → Apps Script), de hora
em hora, e **pinta de vermelho** — nunca apaga — três coisas: cadastros duplicados (mesmo
e-mail ou WhatsApp), formulários em branco e cadastros sem e-mail nem telefone. O painel
desconta essas linhas do total. O motivo fica escrito na coluna `Limpeza` da planilha.

**Para abrir o painel localmente**, use o servidor da §6 (`python3 -m http.server 8753`) e
acesse `/dashboard-leads-grcti-ia.html`. Abrir por duplo clique não funciona: o navegador
bloqueia a leitura da planilha.
