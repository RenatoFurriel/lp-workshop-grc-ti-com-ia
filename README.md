# LP — Workshop GRC TI com IA (3ª edição)

Página de captura de **4 dobras** para o workshop de 22/08/2026, montada a partir do
PDF de design `[PÁGINA] WORKSHOP GRC TI COM IA` e da identidade oficial do
**Manual da Marca v1.3** (Google Drive → *Identidade Visual*).

Dobras: **Hero** · **Conteúdo (5 blocos)** · **E você ainda vai receber** · **Quem será o seu mentor**

Feita para ser colada em **um bloco de HTML do GreatPages**.

Existem **duas versões** para teste A/B, geradas da mesma fonte:

| Versão | Fundo | Arquivo | Preview local |
|---|---|---|---|
| **A** | Branco Osso `#F0EBE1` | `dist/greatpages-block.html` | `index.html` |
| **B** | Preto Comando `#0D0D0D` | `dist/greatpages-block-b.html` | `index-b.html` |

A única diferença entre as duas é um bloco de tokens (`body.ix-b`). Estrutura,
copy, layout e JavaScript são idênticos — o que garante que o teste meça a cor
de fundo, e não duas páginas diferentes.

---

## 1. O que entregar no GreatPages

Cada página recebe **um arquivo só**:

```
dist/greatpages-block.html     (versão A)
dist/greatpages-block-b.html   (versão B)
```

1. No GreatPages, inserir **um bloco de HTML / Código** e colar o arquivo inteiro
   (`greatpages-block.html` na página A, `greatpages-block-b.html` na página B).
2. Definir o **fundo da página** igual ao da versão: **`#F0EBE1`** na A e
   **`#0D0D0D`** na B. Sem isso, o bloco aparece como um retângulo emoldurado.
3. Desativar qualquer bloco nativo de hero/título na mesma página — o bloco já traz
   o `<h1>`.
4. **Não reabrir o bloco no editor visual** depois de colado: o editor pode
   reprocessar o HTML e quebrar o conteúdo.

---

## 2. A única coisa que falta preencher

O formulário de inscrição ainda é um placeholder. Quando a URL do form da 3ª edição
existir, trocar em **dois lugares no `index.html`** e rodar o build de novo:

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
(`hero`, `entregaveis`, `mentor`, `sticky`) para rastrear qual botão converteu.

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
| Relatório de peso, com corte em 140 KB | impede que a página engorde sem ninguém perceber |

Peso atual: **~129 KB cru / ~84 KB gzip** em cada versão, com **zero requisições externas**.
Para referência, a LP anterior (`insc-hic-b`) tem 152 KB / 96 KB e ainda baixa
fontes do Google.

---

## 5. Arquivos

```
index.html                  ← FONTE DE VERDADE. Editar aqui. Abre direto no navegador.
build_greatpages.py         ← gera o bloco a partir do index.html
index-b.html                ← preview local da versao B (gerado pelo build)
dist/greatpages-block.html  ← ★ versao A (fundo osso)
dist/greatpages-block-b.html← ★ versao B (fundo preto)
dist/host-simulator.html    ← teste: injeta o bloco num host hostil (ver abaixo)
assets/                     ← fontes da marca + foto (o build otimiza na hora)
copy/                       ← a copy aprovada, em markdown
```

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

- Página: `http://localhost:8753/index.html`
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

**As duas versões passam pelo mesmo QA.** Acrescente `?bloco=b` para testar a B:
`dist/host-simulator.html?bloco=b&utm_source=qa`. O painel checa, além do resto,
se o fundo, a faixa da dobra 2, o símbolo da marca e o negativo do selo estão
corretos **para aquela versão**.

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
