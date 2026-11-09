"""Fabrique le dossier de médias « trop lourds » du Lab 07 (séance 7).

Patrick envoie ses photos, son logo, une carte, un extrait de drone et la grille
des tarifs, chacun dans un format ou une taille qui ne convient pas au Web.
Les images sont des paysages générés (aucune photo réelle, aucun droit à gérer);
elles ont du grain, comme une vraie photo, pour que la compression se comporte
de façon réaliste.

    pip install numpy pillow pillow-heif imageio-ffmpeg
    python outils/medias/generer_envoi_patrick.py

Sortie : docs/public/fiches/lab07-envoi-patrick.zip (et un dossier de travail
dans outils/medias/sortie/, ignoré par git).
"""

from __future__ import annotations

import argparse
import math
import subprocess
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RACINE = Path(__file__).resolve().parents[2]
TRAVAIL = Path(__file__).resolve().parent / "sortie" / "envoi-patrick"
ZIP = RACINE / "docs" / "public" / "fiches" / "lab07-envoi-patrick.zip"
POLICES = Path("C:/Windows/Fonts")


# ---------------------------------------------------------------- bruit et paysages

def bruit_fractal(rng, w, h, octaves=6, base=4, persistance=0.5):
    """Bruit de valeur fractal, entre 0 et 1, de taille (h, w)."""
    total = np.zeros((h, w), np.float32)
    amp, somme = 1.0, 0.0
    for o in range(octaves):
        cw, ch = base * 2**o + 1, max(2, int((base * 2**o) * h / w) + 1)
        petit = rng.random((ch, cw)).astype(np.float32)
        grand = Image.fromarray(petit, mode="F").resize((w, h), Image.BICUBIC)
        total += amp * np.asarray(grand)
        somme += amp
        amp *= persistance
    total /= somme
    return np.clip((total - total.min()) / (np.ptp(total) + 1e-6), 0, 1)


def crete(rng, w, base, hauteur, octaves=7):
    """Ligne de crête (une hauteur en pixels par colonne)."""
    n = bruit_fractal(rng, w, 2, octaves=octaves, base=3)[0]
    return base - n * hauteur


def melange(a, b, t):
    return a + (b - a) * t


def paysage(w, h, seed, ciel_haut, ciel_bas, montagnes, eau, soleil=None, horizon=0.6):
    """Ciel dégradé, nuages, trois plans de montagnes, rivière avec reflet."""
    rng = np.random.default_rng(seed)
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    img = melange(np.array(ciel_haut, np.float32), np.array(ciel_bas, np.float32), y**0.8)
    img = np.broadcast_to(img, (h, w, 3)).copy()
    hz = int(h * horizon)

    if soleil:
        sx, sy, couleur = soleil
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = np.sqrt(((xx - sx * w) / w) ** 2 + ((yy - sy * h) / h) ** 2)
        lueur = np.exp(-d * 7)[..., None]
        img = melange(img, np.array(couleur, np.float32), lueur * 0.85)

    nuages = bruit_fractal(rng, w, h, octaves=7, base=3)
    masque = np.clip((nuages - 0.55) * 3, 0, 1) * np.clip(1 - y[..., 0] / horizon, 0, 1)
    img = melange(img, np.array([250, 235, 225], np.float32), masque[..., None] * 0.55)

    for i, (couleur, base, haut) in enumerate(montagnes):
        ligne = crete(rng, w, base * h, haut * h)
        lignes = np.arange(h, dtype=np.float32)[:, None]
        dedans = (lignes >= ligne[None, :]) & (lignes < hz)
        texture = bruit_fractal(rng, w, h, octaves=8, base=16)
        teinte = np.array(couleur, np.float32) * (0.75 + 0.5 * texture[..., None])
        img = np.where(dedans[..., None], teinte, img)

    # La rivière : reflet du haut de l'image, ondulé et assombri.
    haut = img[:hz][::-1]
    bas_h = h - hz
    reflet = np.zeros((bas_h, w, 3), np.float32)
    ondes = bruit_fractal(rng, 8, bas_h, octaves=3, base=2)[:, 0]
    for r in range(bas_h):
        src = min(hz - 1, int(r * 0.9))
        dec = int((ondes[r] - 0.5) * 60 * (1 + r / bas_h))
        reflet[r] = np.roll(haut[src], dec, axis=0)
    prof = np.linspace(0, 1, bas_h, dtype=np.float32)[:, None, None]
    reflet = melange(reflet * 0.7, np.array(eau, np.float32), 0.35 + 0.4 * prof)
    stries = bruit_fractal(rng, w, bas_h, octaves=5, base=24)
    reflet *= (0.9 + 0.2 * stries[..., None])
    img[hz:] = reflet
    return np.clip(img, 0, 255)


def grain(img_u8, rng, sigma):
    """Ajoute un grain de capteur, par bandes pour ménager la mémoire."""
    out = img_u8.copy()
    pas = 500
    for y0 in range(0, out.shape[0], pas):
        bloc = out[y0:y0 + pas].astype(np.int16)
        bloc += rng.normal(0, sigma, bloc.shape).astype(np.int16)
        out[y0:y0 + pas] = np.clip(bloc, 0, 255).astype(np.uint8)
    return out


def agrandir(arr, w, h):
    return np.asarray(Image.fromarray(arr.astype(np.uint8)).resize((w, h), Image.LANCZOS))


def police(nom, taille):
    for f in (nom, "segoeuib.ttf", "arialbd.ttf", "arial.ttf"):
        p = POLICES / f
        if p.exists():
            return ImageFont.truetype(str(p), taille)
    return ImageFont.load_default()


# ---------------------------------------------------------------- les fichiers

def m1_coucher_soleil(dossier, rng):
    """Photo de reflex, 6000 × 4000, JPEG qualité 97 : pour la bannière d'accueil."""
    base = paysage(
        3000, 2000, seed=11,
        ciel_haut=(52, 60, 110), ciel_bas=(250, 160, 90),
        montagnes=[((95, 80, 110), 0.40, 0.12), ((55, 60, 75), 0.48, 0.10), ((25, 35, 35), 0.55, 0.08)],
        eau=(40, 45, 70), soleil=(0.62, 0.55, (255, 210, 140)), horizon=0.6,
    )
    img = grain(agrandir(base, 6000, 4000), rng, 3)
    Image.fromarray(img).save(dossier / "IMG_4521.JPG", quality=95, subsampling=0)


def m2_kayak_adapte(dossier, rng):
    """Photo d'iPhone en HEIC, 4032 × 3024 : le kayak adapté au quai."""
    import pillow_heif
    pillow_heif.register_heif_opener()
    base = paysage(
        2016, 1512, seed=22,
        ciel_haut=(90, 150, 215), ciel_bas=(200, 225, 240),
        montagnes=[((90, 120, 110), 0.38, 0.10), ((45, 85, 55), 0.47, 0.08), ((25, 60, 35), 0.53, 0.05)],
        eau=(30, 70, 90), horizon=0.55,
    ).astype(np.uint8)
    im = Image.fromarray(base)
    d = ImageDraw.Draw(im)
    # Coque jaune, siège à dossier haut et deux stabilisateurs.
    cx, cy = 1008, 1150
    d.ellipse([cx - 560, cy - 70, cx + 560, cy + 70], fill=(240, 190, 30), outline=(120, 90, 10), width=6)
    d.rectangle([cx - 90, cy - 230, cx + 10, cy - 30], fill=(30, 40, 60))
    d.rectangle([cx - 800, cy + 120, cx + 800, cy + 135], fill=(160, 160, 165))
    for sx in (cx - 800, cx + 800):
        d.ellipse([sx - 140, cy + 100, sx + 140, cy + 160], fill=(230, 230, 230), outline=(90, 90, 90), width=4)
    d.rectangle([cx - 30, cy - 330, cx - 10, cy + 60], fill=(70, 70, 75))
    im = im.filter(ImageFilter.GaussianBlur(1.2))
    img = grain(agrandir(np.asarray(im), 4032, 3024), rng, 3)
    hf = pillow_heif.from_pillow(Image.fromarray(img))
    hf.save(str(dossier / "IMG_4540.HEIC"), quality=55)


def m3_falaise_png(dossier, rng):
    """Photo enregistrée en PNG « pour la qualité », 2400 × 1800."""
    w, h = 1600, 1200
    roche = bruit_fractal(rng, w, h, octaves=9, base=6)
    fissures = bruit_fractal(rng, w, h, octaves=6, base=40)
    img = np.empty((h, w, 3), np.float32)
    img[..., 0] = 120 + 90 * roche - 40 * fissures
    img[..., 1] = 105 + 80 * roche - 40 * fissures
    img[..., 2] = 90 + 70 * roche - 35 * fissures
    # Coin de ciel en haut à gauche et câble de la via ferrata.
    yy, xx = np.mgrid[0:h, 0:w]
    ciel = (yy < 380 - xx * 0.45)
    img[ciel] = np.array([150, 190, 230], np.float32) + 20 * roche[ciel][:, None]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    pts = [(200 + i * 60, 1100 - i * 38 + int(12 * math.sin(i))) for i in range(22)]
    d.line(pts, fill=(60, 60, 65), width=7)
    for x, y in pts[::3]:
        d.rectangle([x - 10, y - 4, x + 10, y + 26], fill=(200, 200, 205))
    img = grain(agrandir(np.asarray(im), 2400, 1800), rng, 4)
    Image.fromarray(img).save(dossier / "via ferrata FALAISE final(2).png", optimize=False, compress_level=6)


def geometrie_logo(t):
    """Le logo sur une grille de 1000 × 1000 ; t convertit en pixels."""
    return {
        "cercle": (500, 400, 330),
        "montagne": [(230, 470), (390, 250), (470, 360), (560, 200), (770, 470)],
        "vague1": [(170, 470 + 25 * math.sin(i / 3)) for i in range(0, 661, 20)],
    }


def m4_logo(dossier):
    """Deux logos : un PNG de 3000 × 3000 et un SVG gonflé de métadonnées."""
    vert, bleu, sable = (31, 94, 72), (31, 94, 120), (238, 226, 200)
    s = 3
    im = Image.new("RGBA", (1000 * s, 1000 * s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([170 * s, 70 * s, 830 * s, 730 * s], fill=sable + (255,), outline=vert + (255,), width=18 * s)
    d.polygon([(230 * s, 470 * s), (390 * s, 250 * s), (470 * s, 360 * s), (560 * s, 200 * s), (770 * s, 470 * s)], fill=vert + (255,))
    d.polygon([(390 * s, 250 * s), (430 * s, 305 * s), (410 * s, 300 * s), (375 * s, 272 * s)], fill=(255, 255, 255, 255))
    d.polygon([(560 * s, 200 * s), (600 * s, 255 * s), (575 * s, 250 * s), (545 * s, 225 * s)], fill=(255, 255, 255, 255))
    for k, dy in enumerate((480, 540, 600)):
        pts = [((190 + i) * s, (dy + 18 * math.sin(i / 40 + k)) * s) for i in range(0, 621, 10)]
        d.line(pts, fill=bleu + (255,), width=22 * s, joint="curve")
    titre, sous = police("segoeuib.ttf", 110 * s), police("segoeui.ttf", 70 * s)
    d.text((500 * s, 820 * s), "AVENTURE", font=titre, fill=vert + (255,), anchor="mm")
    d.text((500 * s, 920 * s), "SAINT-MAURICE", font=sous, fill=bleu + (255,), anchor="mm")
    im.save(dossier / "logo-ASM-final.png")

    vagues = []
    for k, dy in enumerate((480, 540, 600)):
        pts = " ".join(f"{190 + i},{dy + 18 * math.sin(i / 40 + k):.1f}" for i in range(0, 621, 10))
        vagues.append(f'    <polyline points="{pts}" fill="none" stroke="#1F5E78" stroke-width="22" stroke-linecap="round"/>')
    # Un export typique d'un logiciel de dessin : commentaires, métadonnées et calques inutiles.
    xmp = "\n".join(
        f'      <rdf:li stEvt:action="saved" stEvt:instanceID="xmp.iid:{i:04d}a7f3-c1e2-4b9d-8f00-{i * 7919:012d}" stEvt:when="2019-05-{1 + i % 28:02d}T14:{i % 60:02d}:00-04:00" stEvt:softwareAgent="Logiciel de dessin 23.0 (Windows)" stEvt:changed="/"/>'
        for i in range(260)
    )
    svg = f"""<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Logiciel de dessin 23.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Calque_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:stEvt="http://ns.adobe.com/xap/1.0/sType/ResourceEvent#"
  x="0px" y="0px" viewBox="0 0 1000 1000" style="enable-background:new 0 0 1000 1000;" xml:space="preserve">
  <metadata>
    <rdf:RDF><rdf:Description><rdf:Seq>
{xmp}
    </rdf:Seq></rdf:Description></rdf:RDF>
  </metadata>
  <style type="text/css">
    .st0{{fill:#EEE2C8;stroke:#1F5E48;stroke-width:18;}}
    .st1{{fill:#1F5E48;}}
    .st2{{fill:#FFFFFF;}}
    .st3{{display:none;}}
  </style>
  <g id="Calque_brouillon" class="st3">
    <rect x="0" y="0" width="1000" height="1000" fill="#FF00FF"/>
  </g>
  <g id="Logo">
    <circle class="st0" cx="500" cy="400" r="321"/>
    <polygon class="st1" points="230,470 390,250 470,360 560,200 770,470"/>
    <polygon class="st2" points="390,250 430,305 410,300 375,272"/>
    <polygon class="st2" points="560,200 600,255 575,250 545,225"/>
{chr(10).join(vagues)}
    <text x="500" y="858" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-weight="700" font-size="110" fill="#1F5E48">AVENTURE</text>
    <text x="500" y="945" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="70" fill="#1F5E78">SAINT-MAURICE</text>
  </g>
</svg>
"""
    (dossier / "logo-ASM.svg").write_text(svg, encoding="utf-8")


def m5_carte(dossier):
    """La carte des parcours, exportée de PowerPoint en PNG 24 bits, 3600 × 2400."""
    s = 3
    W, H = 1200 * s, 800 * s
    im = Image.new("RGB", (W, H), (226, 236, 214))
    d = ImageDraw.Draw(im)
    for k in range(14):  # courbes de niveau
        r = 80 + k * 45
        d.ellipse([(760 - r) * s, (330 - r * 0.7) * s, (760 + r) * s, (330 + r * 0.7) * s], outline=(196, 212, 186), width=2 * s)
    d.polygon([(0, 600 * s), (1200 * s, 520 * s), (1200 * s, 640 * s), (0, 720 * s)], fill=(140, 190, 220))
    d.text((80 * s, 660 * s), "Rivière Saint-Maurice", font=police("segoeuii.ttf", 26 * s), fill=(30, 80, 120))
    p1 = [(180, 520), (260, 470), (340, 440), (430, 430), (500, 400), (560, 360), (540, 300), (470, 290)]
    p2 = [(180, 520), (300, 500), (440, 470), (600, 430), (700, 360), (790, 260), (880, 200), (980, 170), (1040, 230)]
    d.line([(x * s, y * s) for x, y in p1], fill=(46, 125, 50), width=9 * s, joint="curve")
    d.line([(x * s, y * s) for x, y in p2], fill=(198, 40, 40), width=9 * s, joint="curve")
    d.rectangle([150 * s, 500 * s, 210 * s, 545 * s], fill=(80, 60, 40))
    gras, normal = police("segoeuib.ttf", 30 * s), police("segoeui.ttf", 24 * s)
    d.text((120 * s, 555 * s), "Accueil", font=gras, fill=(40, 40, 40))
    d.text((60 * s, 410 * s), "Stationnement", font=normal, fill=(40, 40, 40))
    d.line([(760 * s, 300 * s), (820 * s, 240 * s)], fill=(90, 70, 50), width=6 * s)
    d.text((830 * s, 250 * s), "Pont suspendu", font=normal, fill=(40, 40, 40))
    d.rounded_rectangle([40 * s, 40 * s, 560 * s, 250 * s], radius=16 * s, fill=(255, 255, 255), outline=(150, 150, 150), width=2 * s)
    d.text((70 * s, 60 * s), "Via ferrata — les deux parcours", font=gras, fill=(30, 30, 30))
    d.line([(70 * s, 140 * s), (130 * s, 140 * s)], fill=(46, 125, 50), width=9 * s)
    d.text((145 * s, 122 * s), "Parcours 1 — Les Marmites", font=gras, fill=(46, 125, 50))
    d.text((145 * s, 158 * s), "1,2 km · environ 2 h · facile, dès 10 ans", font=normal, fill=(50, 50, 50))
    d.line([(70 * s, 210 * s), (130 * s, 210 * s)], fill=(198, 40, 40), width=9 * s)
    d.text((145 * s, 192 * s), "Parcours 2 — La Falaise", font=gras, fill=(198, 40, 40))
    d.text((145 * s, 228 * s), "2,0 km · environ 3 h 30 · difficile, dès 14 ans", font=normal, fill=(50, 50, 50))
    im.save(dossier / "carte-parcours.png", compress_level=1)


def m6_drone(dossier, rng):
    """Extrait de drone, 3840 × 2160, 30 i/s, 8 s, avec le bruit du vent, en .MOV."""
    import imageio_ffmpeg
    W, H, IPS, DUREE = 3840, 2160, 30, 8
    fond = paysage(
        2700, 1080, seed=66,
        ciel_haut=(70, 120, 190), ciel_bas=(205, 220, 230),
        montagnes=[((100, 125, 120), 0.36, 0.12), ((50, 90, 60), 0.45, 0.10), ((30, 65, 40), 0.52, 0.06)],
        eau=(35, 70, 85), horizon=0.58,
    ).astype(np.uint8)
    fond = np.asarray(Image.fromarray(fond).resize((5400, 2160), Image.BICUBIC))
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    tmp_video = dossier / "_video.mp4"
    gen = imageio_ffmpeg.write_frames(
        str(tmp_video), (W, H), fps=IPS, codec="libx264", quality=None, bitrate="15M",
        macro_block_size=8, pix_fmt_out="yuv420p", output_params=["-preset", "faster"],
    )
    gen.send(None)
    n = IPS * DUREE
    for i in range(n):
        x = int((5400 - W) * i / (n - 1))
        cadre = fond[:, x:x + W]
        bruit = rng.integers(-6, 7, size=(H // 2, W // 2, 1), dtype=np.int16)
        bruit = np.repeat(np.repeat(bruit, 2, axis=0), 2, axis=1)
        gen.send(np.clip(cadre.astype(np.int16) + bruit, 0, 255).astype(np.uint8))
    gen.close()
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-i", str(tmp_video),
         "-f", "lavfi", "-i", f"anoisesrc=color=brown:amplitude=0.25:duration={DUREE}:sample_rate=48000",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-shortest", str(dossier / "DJI_0042.MOV")],
        check=True,
    )
    tmp_video.unlink()


TARIFS = [
    ("Location de kayak", [("Kayak simple, à l'heure", "25 $"), ("Kayak simple, à la journée", "65 $"), ("Kayak double, à la journée", "90 $"), ("Kayak adapté (sur réservation)", "65 $")]),
    ("Excursions guidées", [("Kayak, 3 h — adulte", "79 $"), ("Kayak, 3 h — enfant (8 à 15 ans)", "59 $"), ("Rabaska, 2 h — par personne", "49 $"), ("Coucher de soleil en rabaska, 2 h 30", "59 $")]),
    ("Via ferrata", [("Parcours 1 — Les Marmites (dès 10 ans)", "69 $"), ("Parcours 2 — La Falaise (dès 14 ans)", "99 $"), ("Location du casque et du harnais", "incluse")]),
    ("Prêt-à-camper", [("Tente, par nuit (4 personnes)", "145 $"), ("Tente, fin de semaine (2 nuits)", "260 $")]),
    ("Groupes (10 personnes et plus)", [("Rabais", "15 %"), ("Dépôt à la réservation", "30 %"), ("Soumission", "sur demande")]),
]


def page_tarifs(numero, sections, rng):
    W, H = 2550, 3300  # lettre à 300 ppp
    im = Image.new("L", (W, H), 246)
    d = ImageDraw.Draw(im)
    titre, sous, txt = police("arialbd.ttf", 92), police("arialbd.ttf", 62), police("arial.ttf", 54)
    y = 250
    d.text((220, y), "AVENTURE SAINT-MAURICE", font=titre, fill=25)
    y += 130
    d.text((220, y), f"Tarifs 2027 — page {numero} de 2 (taxes en sus)", font=txt, fill=60)
    y += 160
    for nom, lignes in sections:
        d.text((220, y), nom, font=sous, fill=20)
        y += 100
        for libelle, prix in lignes:
            d.text((280, y), libelle, font=txt, fill=35)
            d.text((2330, y), prix, font=txt, fill=35, anchor="ra")
            d.line([(280, y + 72), (2330, y + 72)], fill=200, width=2)
            y += 95
        y += 70
    d.text((220, 3050), "Prix en vigueur du 1er juin au 12 octobre 2027. Sujets à changement.", font=police("ariali.ttf", 44), fill=80)
    arr = np.asarray(im).astype(np.int16)
    arr += rng.normal(0, 7, arr.shape).astype(np.int16)  # grain du papier et du numériseur
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).rotate(0.8, fillcolor=235, resample=Image.BICUBIC)
    return im.convert("RGB")


def m7_tarifs(dossier, rng):
    """La feuille des tarifs, numérisée en couleur à 300 ppp : un PDF fait d'images."""
    pages = [page_tarifs(1, TARIFS[:3], rng), page_tarifs(2, TARIFS[3:], rng)]
    pages[0].save(dossier / "Tarifs 2027 SCAN.pdf", save_all=True, append_images=pages[1:], resolution=300, quality=85)


MESSAGE = """Salut l'équipe!

Voici une première sélection pour le site. J'ai mis ce que j'avais de plus beau.

- IMG_4521.JPG : le coucher de soleil sur la rivière, pris avec mon reflex. Pour le haut de la page d'accueil, en grand, sur toute la largeur.
- IMG_4540.HEIC : notre nouveau kayak adapté, au quai (pris avec mon iPhone). Pour la page de l'offre adaptée. Le programme d'aide veut que l'information soit accessible à tout le monde.
- via ferrata FALAISE final(2).png : la falaise du parcours 2, vue du pont suspendu. Pour la page Via ferrata. Karine l'a mise en PNG pour que ce soit de meilleure qualité.
- logo-ASM-final.png et logo-ASM.svg : le neveu m'a envoyé deux fichiers pour le logo. Je ne sais pas lequel est le bon. Il va en haut de chaque page.
- carte-parcours.png : la carte des deux parcours de via ferrata qu'on imprime pour le comptoir. Pour la page Via ferrata aussi.
- DJI_0042.MOV : un extrait de mes vidéos de drone. C'est ça que je veux en plein écran sur l'accueil, en boucle, comme les stations de ski. Le reste fait 60 Go, je vous l'apporte sur une clé.
- Tarifs 2027 SCAN.pdf : Mélanie a numérisé la feuille des prix de l'été prochain. Pour la page des tarifs.

Dites-moi si c'est correct!

Patrick
"""


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--seulement", help="ne refaire qu'un fichier : m1 à m7")
    args = p.parse_args()
    rng = np.random.default_rng(2026)
    if not args.seulement and TRAVAIL.exists():
        for f in TRAVAIL.iterdir():
            f.unlink()
    TRAVAIL.mkdir(parents=True, exist_ok=True)
    etapes = {
        "m1": lambda: m1_coucher_soleil(TRAVAIL, rng),
        "m2": lambda: m2_kayak_adapte(TRAVAIL, rng),
        "m3": lambda: m3_falaise_png(TRAVAIL, rng),
        "m4": lambda: m4_logo(TRAVAIL),
        "m5": lambda: m5_carte(TRAVAIL),
        "m6": lambda: m6_drone(TRAVAIL, rng),
        "m7": lambda: m7_tarifs(TRAVAIL, rng),
    }
    for cle, faire in etapes.items():
        if args.seulement and cle != args.seulement:
            continue
        print("…", cle, flush=True)
        faire()
    (TRAVAIL / "Message de Patrick.txt").write_text(MESSAGE, encoding="utf-8")

    ZIP.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_STORED) as z:  # déjà compressés : on ne recompresse pas
        for f in sorted(TRAVAIL.iterdir()):
            z.write(f, f"envoi-patrick/{f.name}")
    for f in sorted(TRAVAIL.iterdir()):
        print(f"{f.stat().st_size / 1e6:8.2f} Mo  {f.name}")
    print(f"{ZIP.stat().st_size / 1e6:8.2f} Mo  {ZIP.relative_to(RACINE)}")


if __name__ == "__main__":
    main()
