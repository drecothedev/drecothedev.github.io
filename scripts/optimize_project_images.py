"""Generate appropriately sized monochrome WebP assets from preserved M1 originals.
Run with the bundled Python runtime containing Pillow. No runtime image library is needed.
"""
from pathlib import Path
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'submission/ActivityWebserver/static/img/project'
OUTPUT = ROOT/'submission/ActivityWebserver/static/img/project2'
for name in ['gemma','sxmpler']:
    with Image.open(SOURCE/f'{name}.jpg') as source:
        image = ImageOps.grayscale(ImageOps.exif_transpose(source))
        for width in [180,360,720]:
            height = round(image.height * width / image.width)
            image.resize((width,height),Image.Resampling.LANCZOS).save(
                OUTPUT/f'{name}-{width}.webp', 'WEBP', quality=82, method=6)
    print(name, sum(p.stat().st_size for p in OUTPUT.glob(f'{name}-*.webp')), 'bytes across three sizes')
