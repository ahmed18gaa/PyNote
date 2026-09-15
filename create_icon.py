from PIL import Image

image = Image.open("PyNote.png").convert("RGBA")

sizes = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]

image.save(
    "PyNote.ico",
    format="ICO",
    sizes=sizes
)

print("PyNote.ico created successfully!")