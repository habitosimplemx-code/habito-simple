"""Prueba local del post de imagen: guion -> fondo IA -> render. No sube ni publica."""
import os
from src import image_script, image_gen, image_render

os.makedirs("build", exist_ok=True)

if os.environ.get("GEMINI_API_KEY"):
    data = image_script.generate_image_post(os.environ.get("NICHE", "salud y bienestar"))
else:
    # Sin API key: datos de ejemplo para probar SOLO el render (cero costo)
    data = {"big": "20-20-20", "small": "cada 20 min, mira 20 seg algo a 20 pies (6 m)",
            "image_prompt": "calm green desk with plant, person resting eyes, soft natural light"}

print("big:", data.get("big"), "| small:", data.get("small"))
print("caption:", data.get("caption", "(sin caption en modo ejemplo)"))

bg = image_gen.fetch_background(data.get("image_prompt", ""), "build/bg.png")
image_render.render_image(data.get("big", ""), data.get("small", ""), "build/post.jpg", bg_path=bg)
print("\nListo -> abre build\\post.jpg")
