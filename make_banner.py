from PIL import Image, ImageDraw, ImageFilter
import math

W, H = 1200, 300
FRAMES = 36
frames = []

for i in range(FRAMES):
    image = Image.new("RGB", (W, H), (5, 5, 9))
    draw = ImageDraw.Draw(image, "RGBA")

    # Красное пульсирующее свечение
    pulse = (math.sin(i * 2 * math.pi / FRAMES) + 1) / 2
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse(
        (650, -100, 1250, 400),
        fill=(255, 0, 45, int(35 + pulse * 65))
    )
    glow = glow.filter(ImageFilter.GaussianBlur(65))
    image = Image.alpha_composite(image.convert("RGBA"), glow)

    draw = ImageDraw.Draw(image, "RGBA")

    # Неоновые линии
    x = int((i / FRAMES) * (W + 250)) - 125
    draw.line((x, 0, x - 180, H), fill=(255, 25, 65, 180), width=3)
    draw.line((x + 20, 0, x - 160, H), fill=(255, 25, 65, 60), width=1)

    # Частицы
    for j in range(28):
        px = (j * 173 + i * 13) % W
        py = (j * 67 + i * 7) % H
        draw.ellipse((px, py, px + 3, py + 3), fill=(255, 50, 80, 180))

    # Рамка
    draw.rounded_rectangle(
        (12, 12, W - 12, H - 12),
        radius=16,
        outline=(255, 25, 65, int(90 + pulse * 120)),
        width=2
    )

    # Текст
    draw.text((W // 2, 82), "CYBERSECURITY  /  DEVELOPMENT",
              anchor="mm", fill=(255, 100, 125, 255), stroke_width=0)
    draw.text((W // 2, 145), "SAYAT228",
              anchor="mm", fill=(255, 255, 255, 255),
              stroke_width=1, stroke_fill=(255, 20, 60, 180))
    draw.text((W // 2, 205), "CODE. SECURE. BUILD.",
              anchor="mm", fill=(255, 45, 80, 255))

    frames.append(image.convert("RGB"))

frames[0].save(
    "banner.gif",
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0,
    optimize=True
)

print("Готово! Создан banner.gif")