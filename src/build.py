"""Gera ../index.html autocontido (CSS, JS, fontes, logo e fotos embutidos)."""
import base64, re, pathlib, urllib.request, io
from PIL import Image

here = pathlib.Path(__file__).parent
root = here.parent
b64 = lambda b: base64.b64encode(b).decode()

# Fontes: apenas o subconjunto latin (cobre português), em woff2
css_fonts = (here / "fonts" / "fonts.css").read_text(encoding="utf8")
blocks = re.findall(r"/\* (latin) \*/\s*(@font-face \{.*?\})", css_fonts, re.S)
fonts = ""
for _, blk in blocks:
    url = re.search(r"url\((https[^)]+)\)", blk).group(1)
    cache = here / "fonts" / url.split("/")[-1]
    if not cache.exists():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        cache.write_bytes(urllib.request.urlopen(req).read())
    fonts += blk.replace(url, "data:font/woff2;base64," + b64(cache.read_bytes())) + "\n"

# Logo recortada (sem margens) e selo para o disco do hero
src = Image.open(root / "assets" / "logo.jpeg").convert("RGB")
def enc(box, w, q=84, whiten=False):
    c = src.crop(box); c.thumbnail((w, w))
    if whiten:  # leva o fundo do JPEG a branco, para o multiply sumir com o retângulo
        px = c.load(); W, H = c.size
        edge = [px[x, y] for x in range(0, W, 8) for y in (0, H - 1)] + [px[x, y] for y in range(0, H, 8) for x in (0, W - 1)]
        bg = [sorted(p[i] for p in edge)[len(edge) // 2] for i in range(3)]
        c = c.point(lambda v, i=[0]: v)  # placeholder para manter o tipo
        r, g, b_ = c.split()
        c = Image.merge("RGB", [ch.point(lambda v, k=k: min(255, round(v * 255 / k))) for ch, k in zip((r, g, b_), bg)])
    buf = io.BytesIO(); c.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + b64(buf.getvalue())
logo = enc((40, 320, 1230, 710), 900, whiten=True)
mark = enc((850, 325, 1230, 705), 560)
css = (here / "styles.css").read_text(encoding="utf8")
css = ":root{--mark:url(" + mark + ")}" + chr(10) + css
js = (here / "script.js").read_text(encoding="utf8")

html = (here / "index.html").read_text(encoding="utf8")
html = html.replace("/*@CSS*/", fonts + css).replace("/*@JS*/", js)
html = re.sub(r"@IMG:(\w+)", lambda m: "data:image/jpeg;base64," + b64((here / "img" / f"{m[1]}.jpg").read_bytes()), html)
html = html.replace("@LOGO", logo)
(root / "index.html").write_text(html, encoding="utf8")
print("index.html:", round(len(html) / 1024), "KB")
