#!/usr/bin/env python3
"""
Gera o bloco GreatPages (dist/greatpages-block.html) a partir de index.html.

O que este script resolve:
  1. Escopa TODO o CSS em #ix-ws3 (nada vaza para a pagina hospedeira).
  2. Embute fonte e imagens como data URI (zero request de imagem).
  3. Converte tudo para ASCII puro - o GreatPages controla o <head> e o
     charset; sem isso a acentuacao vira mojibake.
  4. Relatorio de peso com limite rigido.

Uso:
    python3 build_greatpages.py            # gera o bloco
    python3 build_greatpages.py --check    # valida o bloco ja gerado
Requer: Pillow
"""

import base64
import gzip
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
OUT_DIR = os.path.join(HERE, "dist")
OUT = os.path.join(OUT_DIR, "greatpages-block.html")

ROOT_ID = "ix-ws3"
ROOT = "#" + ROOT_ID
# Limite rigido de peso. 140 KB deixa folga real sobre os ~129 KB atuais (fontes
# da marca + foto + os tokens das duas versoes). O guard existe para pegar
# regressao - ja pegou duas: a foto embutida em duplicidade e o <head> vazando
# para dentro do bloco.
MAX_RAW = 140 * 1024

# ---------------------------------------------------------------- assets
# receita declarativa: caminho no index.html -> como embutir
ASSETS = {
    # Foto usada no hero (com fade) e no circulo da dobra 4.
    # O asset ja esta cortado no alpha (833x1027) para que o preview local e o
    # bloco final enquadrem a foto exatamente igual - com autocrop so no build,
    # os dois divergiam.
    "assets/arteiro-recorte.png": {
        "kind": "image",
        "resize": (760, None),
        "save": dict(format="WEBP", quality=70, alpha_quality=82, method=6),
        "mime": "image/webp",
    },
    # A dobra 4 reaproveita a MESMA foto, recortada em quadrado por object-fit.
    # Embutir um segundo arquivo custaria ~36 KB de base64 sem ganho visual.

    # fontes oficiais da marca (Manual v1.3), com subset
    "assets/khand-700.woff2": {"kind": "font", "mime": "font/woff2", "subset": True},
    "assets/archivo-var.woff2": {"kind": "font", "mime": "font/woff2", "subset": True},
}

# Glifos preservados no subset: ASCII + acentuacao do portugues + a pontuacao
# usada na pagina. Manter folga aqui e barato; se a copy trouxer um caractere
# novo fora desta lista, ele cai na fonte de fallback.
SUBSET_CHARS = (
    " !\"#$%&'()*+,-./0123456789:;<=>?@"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
    "abcdefghijklmnopqrstuvwxyz{|}~"
    " "                     # espaco insecavel
    "ÀÁÂÃÄÇÈÉÊËÌÍÎÏÑÒÓÔÕÖÙÚÛÜÝ"
    "àáâãäçèéêëìíîïñòóôõöùúûüýÿ"
    "ªº°·—–…“”‘’«»€©®™→↑↓×÷±§¶"
)


def subset_font(raw):
    """Reduz a fonte aos glifos usados. Preserva o eixo de peso das variaveis."""
    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont
    import io as _io

    f = TTFont(_io.BytesIO(raw))
    opts = Options()
    opts.layout_features = ["*"]      # mantem kerning/ligaduras
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    opts.retain_gids = False
    if "fvar" in f:                   # variavel: nao instanciar, manter wght
        opts.drop_tables = []
    sub = Subsetter(options=opts)
    sub.populate(text=SUBSET_CHARS)
    sub.subset(f)
    f.flavor = "woff2"
    out = _io.BytesIO()
    f.save(out)
    return out.getvalue()


def encode_image(path, spec):
    im = Image.open(path).convert("RGBA")
    before = im.size
    if spec.get("autocrop"):
        bbox = im.getchannel("A").getbbox()
        if bbox:
            im = im.crop(bbox)
    if spec.get("resize"):
        w, h = spec["resize"]
        if h is None:
            h = round(w * im.size[1] / im.size[0])
        im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, **spec["save"])
    raw = buf.getvalue()
    print("  %-34s %s -> %s  %6.1f KB" % (
        os.path.basename(path), "x".join(map(str, before)),
        "x".join(map(str, im.size)), len(raw) / 1024))
    return raw


def data_uri(raw, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode())


# ---------------------------------------------------------------- CSS scoping
def prefix_selector_list(sel_list):
    out = []
    for s in sel_list.split(","):
        s = s.strip()
        if not s:
            continue
        if s == "*":
            out.append(ROOT)
            out.append(ROOT + " *")
        elif re.match(r"^(?:html|body|:root)(?=[\s.:\[>+~]|$)", s):
            # a raiz do bloco assume o papel de body/html, inclusive em
            # seletores compostos como "body.ix-js .reveal"
            out.append(re.sub(r"^(?:html|body|:root)", ROOT, s))
        else:
            out.append(ROOT + " " + s)
    return ",".join(out)


def transform(css_text):
    """Prefixa cada regra. Nenhum seletor passa sem escopo."""
    result, i, n = [], 0, len(css_text)
    while i < n:
        if css_text[i].isspace():
            i += 1
            continue
        brace = css_text.find("{", i)
        if brace == -1:
            break
        selector = css_text[i:brace].strip()
        depth, j = 1, brace + 1
        while j < n and depth:
            if css_text[j] == "{":
                depth += 1
            elif css_text[j] == "}":
                depth -= 1
            j += 1
        inner = css_text[brace + 1:j - 1]
        if selector.startswith("@font-face"):
            result.append(selector + "{" + inner + "}")
        elif selector.startswith("@keyframes"):
            result.append(selector + "{" + inner + "}")
        elif selector.startswith("@media") or selector.startswith("@supports"):
            result.append(selector + "{" + transform(inner) + "}")
        else:
            result.append(prefix_selector_list(selector) + "{" + inner + "}")
        i = j
    return "\n".join(result)


# ---------------------------------------------------------------- checagens
def validate(block):
    errs = []
    if not block.isascii():
        bad = sorted({c for c in block if ord(c) > 127})[:12]
        errs.append("bloco contem nao-ASCII: %r" % bad)
    # ignora comentarios HTML: as instrucoes de "como trocar pelo asset real"
    # citam caminhos assets/... de proposito e nao sao referencias de verdade
    sem_comentario = re.sub(r"<!--.*?-->", "", block, flags=re.S)
    if re.search(r'src="assets/|url\(assets/', sem_comentario):
        errs.append("sobrou referencia a assets/ nao embutida")
    if "SUBSTITUIR" in block:
        print("  AVISO: FORM_URL ainda e o placeholder SUBSTITUIR.")
    # nenhum seletor fora de escopo dentro do <style>
    css = re.search(r"<style>(.*?)</style>", block, re.S)
    if css:
        for m in re.finditer(r"(?m)^([^@{}\n][^{}\n]*)\{", css.group(1)):
            sel = m.group(1).strip()
            if sel and not all(p.strip().startswith(ROOT) for p in sel.split(",") if p.strip()):
                errs.append("seletor sem escopo: %s" % sel[:70])
                break
    return errs


def report(block):
    raw = len(block.encode())
    gz = len(gzip.compress(block.encode(), 9))
    print("\n  bloco: %.1f KB cru / %.1f KB gzip" % (raw / 1024, gz / 1024))
    print("  limite: %.0f KB cru" % (MAX_RAW / 1024))
    if raw > MAX_RAW:
        sys.exit("ERRO: bloco acima do limite de peso (%.1f KB)." % (raw / 1024))


# ---------------------------------------------------------------- main
if "--check" in sys.argv:
    alvos = [("A (fundo osso)", OUT),
             ("B (fundo preto)", os.path.join(OUT_DIR, "greatpages-block-b.html"))]
    problemas = []
    for nome, caminho in alvos:
        if not os.path.exists(caminho):
            sys.exit("nada para checar: %s nao existe" % caminho)
        bloco = open(caminho, encoding="utf-8").read()
        print("\n  --- versao %s ---" % nome)
        errs = validate(bloco)
        report(bloco)
        if errs:
            problemas.append("%s: %s" % (nome, "; ".join(errs)))
    if problemas:
        sys.exit("FALHOU:\n  - " + "\n  - ".join(problemas))
    print("  OK: ASCII puro, tudo embutido, CSS 100% escopado nas duas versoes.")
    sys.exit(0)

from PIL import Image  # noqa: E402  (so necessario para gerar)

html = open(SRC, encoding="utf-8").read()

# Corta o documento no </head> ANTES de procurar o corpo. Sem isso, uma tag
# escrita dentro de um comentario no <head> (ex.: citar "<body>" num comentario)
# faz o regex casar no lugar errado e arrastar o head inteiro para o bloco.
_split = re.search(r"</head\s*>", html, re.I)
head = html[:_split.start()] if _split else html
after_head = html[_split.end():] if _split else html

css = re.search(r"<style[^>]*>(.*?)</style>", head, re.S).group(1)
_b = re.search(r"<body[^>]*>(.*)</body\s*>", after_head, re.S)
if not _b:
    sys.exit("nao encontrei o <body> depois do </head>")
body = _b.group(1)

# hints de fonte do <head> seguem no fragmento (validos no body)
font_hints = "".join(
    m.group(0) + "\n" for m in re.finditer(
        r'<link rel="(?:preconnect|preload)"[^>]*fonts\.gstatic\.com[^>]*>', head)
)

print("assets:")
for path, spec in ASSETS.items():
    full = os.path.join(HERE, path)
    if not os.path.exists(full):
        sys.exit("asset ausente: " + path)
    if spec["kind"] == "image":
        raw = encode_image(full, spec)
    else:
        raw = open(full, "rb").read()
        antes = len(raw)
        if spec.get("subset"):
            raw = subset_font(raw)
        print("  %-34s %6.1f KB%s" % (
            os.path.basename(path), len(raw) / 1024,
            "  (subset de %.1f KB)" % (antes / 1024) if spec.get("subset") else ""))
    uri = data_uri(raw, spec["mime"])
    body = body.replace('src="%s"' % path, 'src="%s"' % uri)
    css = css.replace("url(%s)" % path, "url(%s)" % uri)

# comentarios /* */ fora, depois escopo
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
css = transform(css)

# ASCII: CSS usa \XX (com espaco final), HTML usa entidades, JS usa \uXXXX
css = re.sub(r"[^\x00-\x7F]", lambda m: "\\%X " % ord(m.group()), css)

# ASCII no body: cada <script> escapa com \uXXXX, o resto com entidades HTML.
# Percorre regiao por regiao para suportar varios blocos de script.
def escape_body(text):
    parts, pos = [], 0
    for m in re.finditer(r"<script\b[^>]*>.*?</script>", text, re.S):
        chunk = text[pos:m.start()]
        parts.append(chunk.encode("ascii", "xmlcharrefreplace").decode())
        parts.append(re.sub(r"[^\x00-\x7F]",
                            lambda c: "\\u%04x" % ord(c.group()), m.group(0)))
        pos = m.end()
    parts.append(text[pos:].encode("ascii", "xmlcharrefreplace").decode())
    return "".join(parts)


body = escape_body(body)

def montar(classe, fundo_pagina):
    """Monta o bloco. A unica diferenca entre A e B e a classe no elemento raiz."""
    cls = (' class="%s"' % classe) if classe else ""
    return (
        "<!-- ===== INICIO DO BLOCO GREATPAGES - LP WORKSHOP GRC TI COM IA (3a ed.) ===== -->\n"
        "<!-- Versao %s. Colar em UM bloco de HTML/Codigo; nao reabrir no editor visual. -->\n"
        "<!-- Fundo da pagina no GreatPages deve ser %s.                              -->\n"
        % (classe or "A (fundo claro)", fundo_pagina)
        + font_hints
        + "<style>\n" + css + "\n</style>\n"
        + '<div id="' + ROOT_ID + '"' + cls + ' lang="pt-BR">' + body + "</div>\n"
        "<!-- ===== FIM DO BLOCO GREATPAGES ===== -->\n"
    )


# A = fundo Branco Osso (padrao) . B = fundo Preto Comando
VARIANTES = [
    ("", "#F0EBE1", OUT),
    ("ix-b", "#0D0D0D", os.path.join(OUT_DIR, "greatpages-block-b.html")),
]

os.makedirs(OUT_DIR, exist_ok=True)
falhas = []
for classe, fundo, destino in VARIANTES:
    bloco = montar(classe, fundo)
    open(destino, "w", encoding="utf-8").write(bloco)
    nome = "B (fundo preto)" if classe else "A (fundo osso)"
    print("\n  --- versao %s ---" % nome)
    errs = validate(bloco)
    report(bloco)
    print("  escrito: %s" % os.path.relpath(destino, HERE))
    if errs:
        falhas.append("%s: %s" % (nome, "; ".join(errs)))

# preview local da B: mesma fonte, so com a classe no <body>
prev_b = os.path.join(HERE, "index-b.html")
open(prev_b, "w", encoding="utf-8").write(
    html.replace("<body>", '<body class="ix-b">', 1))
print("\n  preview local da B: %s" % os.path.relpath(prev_b, HERE))

if falhas:
    sys.exit("FALHOU:\n  - " + "\n  - ".join(falhas))
print("  OK: ASCII puro, tudo embutido, CSS 100% escopado nas duas versoes.")
