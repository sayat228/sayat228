from PIL import Image, ImageDraw, ImageFilter
import math
import random

W, H = 1000, 300
FRAMES = 48
random.seed(228)

stars = [
    (random.randint(0, W), random.randint(0, H), random.randint(1, 3))
    for _ in range(75)
]

frames = []

for frame_no in range(FRAMES):
    img = Image.new("RGB", (W, H), (7, 8, 16))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    pulse = (math.sin(frame_no * 2 * math.pi / FRAMES) + 1) / 2

    gd.rounded_rectangle(
        (18, 18, W - 18, H - 18),
        radius=24,
        outline=(255, 0, 45, 180),
        width=3
    )
    gd.ellipse(
        (600, 20, 1030, 330),
        fill=(130, 0, 30, int(35 + pulse * 35))
    )
    glow = glow.filter(ImageFilter.GaussianBlur(35))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img)

    # Аниме-глаза
    for cx in (350, 650):
        cy = 115
        eye_w, eye_h = 100, 43

        d.polygon(
            [
                (cx - eye_w, cy),
                (cx - 45, cy - eye_h),
                (cx + 45, cy - eye_h),
                (cx + eye_w, cy),
                (cx + 40, cy + 22),
                (cx - 40, cy + 22),
            ],
            fill=(15, 10, 22, 255),
            outline=(255, 25, 55, 255)
        )

        iris_y = cy + 2 + int(pulse * 4)
        d.ellipse(
            (cx - 29, iris_y - 30, cx + 29, iris_y + 30),
            fill=(170, 0, 30, 255),
            outline=(255, 40, 60, 255),
            width=3
        )
        d.ellipse(
            (cx - 12, iris_y - 22, cx + 12, iris_y + 22),
            fill=(8, 5, 12, 255)
        )
        d.ellipse(
            (cx - 13, iris_y - 19, cx - 3, iris_y - 9),
            fill=(255, 220, 220, 255)
        )

    # Красный сканирующий луч
    scan_x = int((frame_no / (FRAMES - 1)) * W)
    d.line((scan_x, 25, scan_x - 80, H - 25),
           fill=(255, 25, 55, 220), width=3)

    # Частицы
    for x, y, r in stars:
        yy = (y + frame_no * (r + 1)) % H
        d.ellipse((x, yy, x + r, yy + r),
                  fill=(255, 45, 65, 180))

    # Заголовок
    d.text((W // 2, 205), "SAYAT228",
           anchor="mm", fill=(255, 45, 70, 255),
           stroke_width=1, stroke_fill=(100, 0, 20, 255))
    d.text((W // 2, 238), "CYBERSECURITY  //  DEVELOPMENT",
           anchor="mm", fill=(205, 210, 225, 255))
    d.text((W // 2, 264), "CODE.  SECURE.  BUILD.",
           anchor="mm", fill=(255, 100, 120, 255))

    frames.append(img.convert("RGB"))

frames[0].save(
    "banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=70,
    loop=0,
    optimize=True
)

print("Готово! Создан banner.gif")