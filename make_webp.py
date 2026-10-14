# Лёгкие версии фото: img/<name>.jpg → img/w/<name>-800.webp и -1600.webp (запускать после добавления новых фото)
import os
from PIL import Image
SRC = 'img'; OUT = 'img/w'
os.makedirs(OUT, exist_ok=True)
for f in sorted(os.listdir(SRC)):
    if not f.endswith('.jpg') or f.startswith('p-'):
        continue
    name = f[:-4]
    im = Image.open(os.path.join(SRC, f)).convert('RGB')
    for w in (800, 1600):
        dst = f'{OUT}/{name}-{w}.webp'
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(os.path.join(SRC, f)):
            continue
        x = im.copy()
        if x.width > w:
            x = x.resize((w, round(x.height * w / x.width)), Image.LANCZOS)
        x.save(dst, 'WEBP', quality=78, method=6)
print('ok', len(os.listdir(OUT)))
