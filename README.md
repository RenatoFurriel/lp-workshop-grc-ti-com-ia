# LP — Workshop GRC TI com IA (3ª edição)

Página de captura de **4 dobras** para o workshop de 22/08/2026, montada a partir do
PDF de design `[PÁGINA] WORKSHOP GRC TI COM IA` e da identidade oficial do
**Manual da Marca v1.3** (Google Drive → *Identidade Visual*).

Dobras: **Hero** · **Conteúdo (5 blocos)** · **E você ainda vai receber** · **Quem será o seu mentor**

Feita para ser colada em **um bloco de HTML do GreatPages**.

Existem **três versões** para teste:

| Versão | Fundo | Layout | Arquivo | Preview local |
|---|---|---|---|---|
| **A** | Branco Osso `#F0EBE1` | 4 dobras do PDF | `dist/greatpages-block.html` | `index.html` |
| **B** | Preto Comando `#0D0D0D` | 4 dobras do PDF | `dist/greatpages-block-b.html` | `index-b.html` |
| **C** | Preto Comando `#0D0D0D` | blueprint | `dist/greatpages-block-c.html` | `index-c.html` |

**A e B** saem da mesma fonte (`index.html`); a única diferença entre elas é um
bloco de tokens (`body.ix-b`). Estrutura, copy, layout e JavaScript são
idênticos — o que garante que o teste meça a cor de fundo, e não duas páginas
diferentes.

**C** é um terceiro layout, com fonte própria (`index-c.html`) — ver a seção
[§9](#9-versão-c--blueprint-de-sala-de-comando). Ela mantém copy, tipografia, paleta e as duas
fotos do mentor, e troca todo o resto.

---

## 1. O que entregar no GreatPages

Cada página recebe **um arquivo só**:

```
dist/greatpages-block.html     (versão A)
dist/greatpages-block-b.html   (versão B)
dist/greatpages-block-c.html   (versão C)
```

1. No GreatPages, inserir **um bloco de HTML / Código** e colar o arquivo inteiro
   (`greatpages-block.html` na página A, `-b` na B, `-c` na C).
2. Definir o **fundo da página** igual ao da versão: **`#F0EBE1`** na A e
   **`#0D0D0D`** na B e na C. Sem isso, o bloco aparece como um retângulo
   emoldurado.
3. Desativar qualquer bloco nativo de hero/título na mesma página — o bloco já traz
   o `<h1>`.
4. **Não reabrir o bloco no editor visual** depois de colado: o editor pode
   reprocessar o HTML e quebrar o conteúdo.

---

## 2. A única coisa que falta preencher

O formulário de inscrição ainda é um placeholder. Quando a URL do form da 3ª edição
existir, trocar em **dois lugares no `index.html` e nos mesmos dois lugares no
`index-c.html`** (a C tem 5 CTAs, contando o do topo) e rodar o build de novo:

1. No `<script>`, a constante no topo:
   ```js
   var FORM_URL = "https://form.respondi.app/SUBSTITUIR";
   ```
2. Nos 4 links `data-form` (`href="https://form.respondi.app/SUBSTITUIR"`).
   O `href` real no HTML é intencional: garante que o botão funcione mesmo com o
   JavaScript desligado. O JS apenas acrescenta os parâmetros de campanha.

O build avisa enquanto o placeholder existir:
`AVISO: FORM_URL ainda e o placeholder SUBSTITUIR.`

**Atribuição de campanha:** os CTAs propagam automaticamente `utm_*`, `gclid`,
`fbclid`, `ttclid`, `msclkid`, `src` e `sck` da URL da página para o formulário.
Sem isso o lead chega sem origem. Cada CTA tem um `data-form` próprio
para rastrear qual botão converteu: `hero`, `entregaveis`, `mentor` e `sticky` em
A/B; `topo`, `hero`, `entregaveis`, `mentor` e `sticky` na C.

---

## 3. Identidade da marca aplicada

Tudo vem do Manual da Marca v1.3. As três cores e a proporção 70/20/10:

| Cor | HEX | Papel |
|---|---|---|
| Preto Comando | `#0D0D0D` | dobra 2 e rodapé |
| Branco Osso | `#F0EBE1` | base das dobras 1, 3 e 4 |
| Laranja Núcleo | `#F26101` | CTA, marca-texto, ícones, círculo do mentor |

**Tipografia:** **Khand Bold** em títulos (sempre caixa-alta, peso 700, como manda o
manual) e **Archivo** em todo o texto corrido. Ambas auto-hospedadas em WOFF2 e
embutidas no bloco — **zero requisição externa de fonte**. Os arquivos vêm do Google
Fonts (as mesmas famílias do kit), com subset para os glifos usados.

### Por que a versão B é mais fiel à marca

O manual proíbe laranja como texto sobre o osso — e com razão: são 2,73:1. Sobre o
Preto Comando, o mesmo `#F26101` rende **6,00:1 e passa AA**. Por isso a versão B
usa o **laranja puro da marca no texto**, enquanto a A precisa do `#B84300`
escurecido. Contrastes medidos na B:

| Elemento | Sobre `#0D0D0D` | |
|---|---|---|
| Títulos em Branco Osso | 16,36:1 | AAA |
| Corpo (osso 82%) | 11,06:1 | AAA |
| Laranja da marca como texto | 6,00:1 | AA |
| Osso sobre card `#1F1F1F` | 14,03:1 | AAA |

### A regra de contraste que não deve ser desfeita

O próprio manual mede **laranja sobre osso em 2,7:1** e proíbe texto corrido. Medi
aqui: **2,73:1** — reprova até para texto grande (mínimo 3,0). Por isso:

| Uso | Cor | Contraste |
|---|---|---|
| Preenchimento (CTA, marca-texto, ícones, círculo) | `#F26101` | — |
| **Texto** laranja sobre fundo claro | `#B84300` | 4,60:1 ✓ AA |
| Texto laranja sobre Preto Comando | `#F26101` | 6,00:1 ✓ AA |
| Osso sobre Preto Comando | `#F0EBE1` | 16,4:1 ✓ AAA |

O `#B84300` é a **única** licença tomada em relação ao PDF: no PDF os títulos
"Workbook com o passo a passo" e "Certificado de participação" e a palavra
"WORKSHOP" usam o laranja puro sobre o osso, o que é ilegível para parte do público.
Se preferir fidelidade absoluta ao PDF, troque uma linha no `index.html`:
`--laranja-texto:#B84300` → `--laranja-texto:#F26101`.

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

Peso atual, com **zero requisições externas**:

| Versão | Cru | Gzip |
|---|---|---|
| A / B | ~130 KB | ~84 KB |
| C | ~168 KB | ~93 KB |

Os ~118 KB de assets embutidos (fontes + foto) são os mesmos nas três; a
diferença é só o CSS/HTML de cada layout. Para referência, a LP anterior
(`insc-hic-b`) tem 152 KB / 96 KB e ainda baixa fontes do Google.

> **O build não é determinístico.** O `fontTools` grava a data da modificação
> dentro da fonte, então o base64 das duas fontes muda a cada rodada e os
> arquivos de `dist/` sempre aparecem como modificados no `git status`, mesmo
> sem nenhuma mudança de conteúdo. Para comparar dois builds de verdade, ignore
> os `data:font/woff2;base64,...`.

---

## 5. Arquivos

```
index.html                  ← FONTE DE VERDADE de A e B. Editar aqui. Abre no navegador.
index-c.html                ← FONTE DE VERDADE da C. Editar aqui. Abre no navegador.
build_greatpages.py         ← gera os 3 blocos a partir dos 2 HTMLs
index-b.html                ← preview local da versao B (gerado pelo build)
dist/greatpages-block.html  ← ★ versao A (fundo osso)
dist/greatpages-block-b.html← ★ versao B (fundo preto)
dist/greatpages-block-c.html← ★ versao C (blueprint)
dist/host-simulator.html    ← teste: injeta o bloco num host hostil (ver abaixo)
assets/                     ← fontes da marca + foto (o build otimiza na hora)
copy/                       ← a copy aprovada, em markdown
```

`index-b.html` é **gerado** — não editar. `index.html` e `index-c.html` são as
duas fontes de verdade.

O `index.html` referencia `assets/` por caminho, não por base64 — assim continua
legível e com diff limpo. O base64 existe apenas em `dist/`.

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

- Páginas: `http://localhost:8753/index.html` · `index-b.html` · `index-c.html`
- QA: `http://localhost:8753/dist/host-simulator.html?utm_source=qa`

O host-simulator reproduz de propósito um host hostil (reset `content-box`, fonte
serifada global, `img{width:100%!important}`, `svg{width:50px!important}`,
`section{background:#0f0!important}`, `footer{background:#600!important}`, estilos em
`.btn`/`.card`, container de 1170px e um ancestral com `transform`, que quebra
`position:fixed`). Ele injeta o bloco e imprime **27 verificações** no canto — entre
elas: nenhum overflow horizontal, os elementos do host intactos, Khand e Archivo
aplicadas, a dobra preta e o rodapé mantendo o Preto Comando, os ícones não
esmagados, o círculo do mentor redondo, todo o conteúdo visível e a UTM propagada.

Testar em 390px e em ≥1180px: a CTA fixa só aparece abaixo de 880px.

**As três versões passam pelo mesmo QA.** Acrescente `?bloco=b` ou `?bloco=c`:
`dist/host-simulator.html?bloco=c&utm_source=qa`. O painel checa, além do resto,
se o fundo, a faixa da dobra 2, o raio do CTA, o símbolo da marca e o negativo do
selo estão corretos **para aquela versão**.

> **A e B falham três verificações — todas pré-existentes, nenhuma é regressão da C:**
>
> | Verificação | O que acontece | Correção |
> |---|---|---|
> | `sticky colada na viewport` (390px) | ver [§9, ao final](#o-bug-da-cta-fixa-que-a-c-corrigiu) | portar `CSS_SOLTO` + `anchor` de `index-c.html` |
> | `sticky manteve o estilo fora da raiz` (390px) | idem | idem |
> | `logo com tamanho util` | o host força `svg{width:50px!important}` e o símbolo do cabeçalho infla de 30px para **50×50** — `.ix-marca svg` em `index.html` não tem `!important` no tamanho | `width:30px!important;height:30px!important` |
>
> A C não tem nenhum dos três: a CTA fixa injeta as regras sem escopo, e a logo
> não é `<svg>` (é máscara CSS), então o `svg{50px}` do host não a alcança.

---

## 7. Decisões que não devem ser desfeitas sem motivo

**O `!important` em imagens, SVG e nos fundos das superfícies é proposital.**
Construtores injetam `img{width:100%!important}`, `svg{width:50px!important}` e
estilizam `section`/`footer` por tag com `!important`. Sem isso a foto estoura, os
ícones viram selos de 50px e a dobra preta perde a cor da marca. As três falhas
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

## 9. Versão C — blueprint de sala de comando

Terceiro layout, com fonte própria em `index-c.html`. Referência de estilo: a home
da **asimov.academy** (dark premium, luz, movimento). Mas a C não copia o layout de
lá — ela tem uma ideia própria, e é dela que sai tudo:

> **O símbolo da ITXPRO já é um diagrama de nós** — o "diagrama de orquestração" do
> manual. Se o produto é *arquitetura cognitiva*, a página é o **blueprint** dela.

Daí saem todas as decisões visuais: rede de nós no hero, painéis com cantos em
colchete, numeração de seção, rótulos técnicos com tracking largo, os 5 blocos como
uma **pilha de arquitetura** com espinha e nós numerados, e grão fotográfico sobre
tudo. Cantos quase retos (4px) nos painéis e pílula só nos CTAs: superfície
técnica, ação macia.

### O que a C mantém (e não deve mudar)

| Mantido | Onde |
|---|---|
| **A copy**, palavra por palavra | verificado por diff de contagem de palavras contra `index.html` — zero perdas |
| **Tipografia da marca** | Khand Bold caixa-alta nos títulos, Archivo no corpo |
| **Paleta** | Preto Comando · Branco Osso · Laranja Núcleo |
| **Foto do mentor no hero** | mesmo recorte com fade da A/B |
| **Foto do mentor na última dobra** | mesmo círculo com fundo Laranja Núcleo |

Além dos textos de A/B, a C reaproveita strings que já existiam (`Quero minha vaga`
e `Sáb 22/08 · 9h–18h`, da CTA fixa) na barra do topo e na ficha técnica. Os
numerais de seção `01`–`04` são navegação, não copy.

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
### O bug da CTA fixa que a C corrigiu

Quando um ancestral com `transform` quebra o `position:fixed`, o JS reancora a
barra no `<body>`. Só que **todo** o CSS do bloco é escopado em `#ix-ws3` — ao sair
da raiz, a barra perdia cada uma das suas regras e virava um `<div>` estático, sem
cor, no fim da página. O host-simulator não pegava isso porque a verificação
aceitava `parentNode === body` como prova de sucesso.

Na C, o reancoramento injeta no mesmo instante uma folha com as regras
equivalentes **sem escopo**, todas presas a `#ix-sticky` (id que só existe no
bloco, então não toca em nada do host). E a verificação do QA agora mede o que
importa: barra colada na viewport **e** ainda estilizada.

**A e B continuam com o bug** — mesmo trecho de JS, em `index.html`. A correção é
portar o bloco `CSS_SOLTO` + `anchor` de `index-c.html` para lá e regerar. Não foi
feito para não alterar as duas páginas do teste A/B em andamento.
