"""Fabrique les images de la matière de la séance 7 à partir du dossier de Patrick.

À lancer après generer_envoi_patrick.py (il lit outils/medias/sortie/envoi-patrick) :

    pip install numpy pillow pillow-heif imageio-ffmpeg
    python outils/medias/generer_visuels_seance7.py

Sortie : docs/public/images/seance7/ et, dans la console, les poids mesurés
à recopier dans les composants (DossierPatrick, ComparerQualite, PerteSansPerte).
"""

import io
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ICI = Path(__file__).resolve().parent
SOURCE = ICI / "sortie" / "envoi-patrick"
SORTIE = ICI.parents[1] / "docs" / "public" / "images" / "seance7"

sys.path.insert(0, str(ICI))
import generer_envoi_patrick as envoi  # noqa: E402


def ko(n):
    return f"{n / 1024:.0f} Ko"


def poids_jpeg(im, q):
    tampon = io.BytesIO()
    im.save(tampon, "JPEG", quality=q, optimize=True, progressive=True)
    return tampon.tell()


def vignette(im, nom, largeur=360):
    im = im.copy()
    im.thumbnail((largeur, largeur * 2), Image.LANCZOS)
    im.save(SORTIE / "dossier" / nom, "WEBP", quality=72)


def main():
    import imageio_ffmpeg
    import pillow_heif
    pillow_heif.register_heif_opener()
    (SORTIE / "dossier").mkdir(parents=True, exist_ok=True)

    # 1. Les vignettes du dossier de Patrick ---------------------------------------
    m1 = Image.open(SOURCE / "IMG_4521.JPG").convert("RGB")
    vignette(m1, "m1.webp")
    vignette(Image.open(SOURCE / "IMG_4540.HEIC").convert("RGB"), "m2.webp")
    vignette(Image.open(SOURCE / "via ferrata FALAISE final(2).png").convert("RGB"), "m3.webp")
    logo = Image.open(SOURCE / "logo-ASM-final.png")
    vignette(logo, "m4.webp", 240)
    carte = Image.open(SOURCE / "carte-parcours.png").convert("RGB")
    vignette(carte, "m5.webp")
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    image_video = subprocess.run(
        [ffmpeg, "-loglevel", "error", "-ss", "3", "-i", str(SOURCE / "DJI_0042.MOV"),
         "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
        check=True, capture_output=True,
    ).stdout
    image_drone = Image.open(io.BytesIO(image_video)).convert("RGB")
    vignette(image_drone, "m6.webp")
    page = envoi.page_tarifs(1, envoi.TARIFS[:3], np.random.default_rng(7))
    vignette(page, "m7.webp", 260)

    # 2. Matriciel et vectoriel : le même sommet de montagne, agrandi ---------------
    # Grille du logo : 1000 × 1000. On garde la zone 333-633 × 167-467 (pixels 40-76 × 20-56 sur 120).
    petit = logo.resize((120, 120), Image.LANCZOS)
    petit.crop((40, 20, 76, 56)).save(SORTIE / "logo-pixels.png")
    svg = (SOURCE / "logo-ASM.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<metadata>.*?</metadata>", "", svg, flags=re.S)
    svg = re.sub(r'<g id="Calque_brouillon".*?</g>', "", svg, flags=re.S)
    svg = re.sub(r"<!--.*?-->", "", svg)
    svg = re.sub(r"\n\s*\n", "\n", svg)
    (SORTIE / "logo.svg").write_text(svg, encoding="utf-8")
    zoom = svg.replace('viewBox="0 0 1000 1000"', 'viewBox="333 167 300 300"')
    zoom = zoom.replace("enable-background:new 0 0 1000 1000;", "")
    (SORTIE / "logo-zoom.svg").write_text(zoom, encoding="utf-8")

    # 3. Avec perte, sans perte : le texte de la carte --------------------------------
    carte1200 = carte.resize((1200, 800), Image.LANCZOS)
    zone = (60, 112, 380, 188)  # la légende « Parcours 1 — Les Marmites »
    carte1200.crop(zone).save(SORTIE / "carte-png.png", optimize=True)
    tampon = io.BytesIO()
    carte1200.save(tampon, "JPEG", quality=8)
    Image.open(io.BytesIO(tampon.getvalue())).crop(zone).save(SORTIE / "carte-jpeg.png", optimize=True)
    tampon_png = io.BytesIO()
    carte1200.quantize(128).save(tampon_png, "PNG", optimize=True)
    print("Carte 1200 px : PNG réduit en couleurs", ko(tampon_png.tell()), "· JPEG qualité 8", ko(len(tampon.getvalue())))

    # 4. La qualité JPEG : une portion du coucher de soleil à 100 % -------------------
    m1_1920 = m1.resize((1920, 1280), Image.LANCZOS)
    portion = (900, 300, 1620, 705)  # le soleil et les montagnes, 720 × 405
    for q in (90, 60, 30, 8):
        tampon = io.BytesIO()
        m1_1920.save(tampon, "JPEG", quality=q)
        Image.open(io.BytesIO(tampon.getvalue())).crop(portion).save(SORTIE / f"qualite-{q}.png", optimize=True)
        print(f"Coucher de soleil 1920 px, JPEG qualité {q} :", ko(poids_jpeg(m1_1920, q)))

    # 5. Le contraste : une image du drone (ciel clair), en bannière --------------------
    banniere = image_drone.resize((1200, 675), Image.LANCZOS)
    banniere.save(SORTIE / "banniere.webp", "WEBP", quality=70)
    # Contraste du texte blanc sur la zone du titre (moitié droite, tiers du haut).
    def lum(c):
        c = c / 255
        c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
        return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]
    zone_titre = np.asarray(banniere.crop((540, 60, 1150, 300)), np.float64)
    l = lum(zone_titre)
    voile = lum(zone_titre * 0.28 + np.array([10, 12, 30]) * 0.72)  # même voile que VoileContraste.vue
    print("Contraste du blanc sur la zone du titre : sans voile, pire", f"{1.05 / (l.max() + 0.05):.1f}", "· médian", f"{1.05 / (np.median(l) + 0.05):.1f}",
          "· avec voile, pire", f"{1.05 / (voile.max() + 0.05):.1f}")

    for f in sorted(SORTIE.rglob("*.*")):
        print(f"{f.stat().st_size / 1024:7.1f} Ko  {f.relative_to(SORTIE)}")


if __name__ == "__main__":
    main()
