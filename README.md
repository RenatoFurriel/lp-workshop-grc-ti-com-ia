# LP — Workshop GRC TI com IA (3ª edição)

Página de captura de **3 dobras** (Hero · Construção · Quem monta) para o workshop
de 22/08/2026. Feita para ser colada em **um bloco de HTML do GreatPages**.

---

## 1. O que entregar no GreatPages

O arquivo a colar é **um só**:

```
dist/greatpages-block.html
```

Passo a passo:

1. No GreatPages, inserir **um bloco de HTML / Código** e colar o arquivo inteiro.
2. Definir o **fundo da página como `#F6F3EC`** (mesma cor de base do bloco).
   Sem isso, o bloco claro aparece como um retângulo emoldurado dentro da página.
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
Sem isso o lead chega sem origem.

---

## 3. Pendências de copy

- **Número da demonstração.** A copy previa `X controles em Y minutos`. O bloco foi
  montado para fechar bem **sem** o número. Quando ele existir, há um slot pronto e
  comentado no `index.html`, entre `<!-- METRICA:INICIO` e `METRICA:FIM -->`:
  basta descomentar e preencher. Nada colapsa no layout.
- **Depoimentos.** Duas edições, centenas de participantes, nenhum depoimento na
  página. É o maior ganho disponível para a dobra 2.

---

## 4. Como gerar o bloco

```bash
python3 build_greatpages.py
```

Requer Pillow (`pip3 install Pillow`). Para validar um bloco já gerado:

```bash
python3 build_greatpages.py --check
```

O que o build faz — e por que cada passo existe:

| Passo | Motivo |
|---|---|
| Escopa todo o CSS em `#ix-ws3` | nada do bloco vaza para a página do GreatPages |
| Embute fonte e imagens como data URI | zero request de imagem; o bloco é autossuficiente |
| Converte tudo para **ASCII puro** | o GreatPages controla o `<head>` e o charset; sem isso a acentuação vira mojibake |
| Relatório de peso, com corte em 130 KB | impede que a página engorde sem ninguém perceber |

Peso atual: **~113 KB cru / ~70 KB gzip**, com 2 requests de fonte e **nenhum** de
imagem. Para referência, a LP anterior (`insc-hic-b`) tem 152 KB / 96 KB.

---

## 5. Arquivos

```
index.html                  ← FONTE DE VERDADE. Editar aqui. Abre direto no navegador.
build_greatpages.py         ← gera o bloco a partir do index.html
dist/greatpages-block.html  ← ★ o arquivo que vai para o GreatPages
dist/host-simulator.html    ← teste: injeta o bloco num host hostil (ver abaixo)
assets/                     ← imagens e fonte de origem (o build otimiza na hora)
copy/                       ← a copy aprovada, em markdown
```

O `index.html` referencia `assets/` por caminho, não por base64 — assim continua
legível e com diff limpo. O base64 existe apenas em `dist/`.

---

## 6. Teste antes de publicar

```bash
python3 -m http.server 8753
```

Depois abrir `http://localhost:8753/dist/host-simulator.html?utm_source=qa`.

Essa página simula de propósito um host hostil (reset diferente, fonte serifada,
`img{width:100%!important}`, `svg{width:50px!important}`, estilos em `.btn`/`.hero`,
container de 1170px e um ancestral com `transform`, que quebra `position:fixed`).
Ela injeta o bloco e imprime um painel de verificação no canto — 20 checagens,
entre elas: nenhum overflow horizontal, os elementos do host intactos, o bloco
resistindo ao CSS do host, a foto no tamanho certo, todo o conteúdo visível e
**uma única faixa escura** na página.

Testar em 390px e em ≥1010px: a CTA fixa só aparece abaixo de 880px.

---

## 7. Decisões de design que não devem ser desfeitas sem motivo

**Base clara predominante, uma única faixa escura.** O creme `#F6F3EC` domina as 3
dobras. Só o bloco de auditabilidade é escuro (`#141618`). O teste automatizado
verifica que existe exatamente **um** bloco escuro.

**Laranja por função — esta é a regra mais importante.** O laranja da marca
`#FF5C00` sobre creme rende apenas **2,79:1** de contraste: reprova em qualquer
texto. Por isso ele é usado só como **preenchimento e grafismo**, nunca como texto
no claro. Para texto existem variações escurecidas:

| Uso | Cor | Contraste |
|---|---|---|
| Preenchimento (botão, marca-texto, nós) | `#FF5C00` | — |
| Texto pequeno e ícones no claro | `#9A3100` | 6,74:1 ✓ |
| Texto grande (≥24px) e bordas | `#C23F00` | 4,73:1 ✓ |
| Texto laranja **sobre** a faixa escura | `#FF7A1A` | 6,95:1 ✓ |

Toda a rampa de tinta (`#141618`, `#383E45`, `#5A6270`) aprova AA sobre o creme.
`#7D848B` — usado na LP escura — **reprova** no claro (3,42:1) e não deve voltar.

**As 5 camadas não são cards.** São uma pilha com espinha contínua, nós em losango
e uma coluna de taxonomia à direita. Cinco itens numa grade sempre sobra um; a
pilha resolve isso e comunica arquitetura, que é o argumento da página.

**O `!important` nas imagens e no SVG é proposital.** Construtores injetam
`img{width:100%!important}` e `svg{width:50px!important}`. Sem o `!important` a
foto estoura e o diagrama vira um selo de 50px. Confirmado no host-simulator.

**A animação de entrada tem duas redes de segurança.** O `opacity:0` só é armado
quando o JS confirma que rodou (classe `.ix-js`), e se o `IntersectionObserver` não
entregar nada em 1,4s o conteúdo aparece de uma vez. Sem isso, JS quebrado ou
observer inerte deixaria a página **em branco** — risco real dentro de iframes e
navegadores embutidos.
