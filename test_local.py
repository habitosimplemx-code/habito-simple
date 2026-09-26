"""Prueba LOCAL: genera guion (o usa uno de ejemplo), voz, subtítulos y video.

NO sube nada ni publica. Sirve para confirmar que tu equipo arma bien el mp4.

- Sin GEMINI_API_KEY: usa un guion de ejemplo (no necesitas ninguna cuenta).
- Con GEMINI_API_KEY: genera un guion real con Gemini.
"""
import os

from src import tts, subtitles, video

BUILD = "build"

SAMPLE = {
    "hook": "Dormir mal te pega más de lo que crees.",
    "script": (
        "Mientras descansas, tu cuerpo se repara y tu mente ordena lo del día. "
        "Un hábito simple ayuda un montón: apaga las pantallas media hora antes de dormir. "
        "La luz azul le dice a tu cerebro que aún es de día y te cuesta más conciliar el sueño. "
        "Prueba dejar el celular fuera de la cama una semana y nota la diferencia. "
        "Recuerda: esto es información general, ante dudas checa con tu médico. "
        "Sígueme, mañana va otro hábito."
    ),
}


def main():
    os.makedirs(BUILD, exist_ok=True)

    if os.environ.get("GEMINI_API_KEY"):
        from src import script_gen
        print("Generando guion con Gemini...")
        data = script_gen.generate_script(
            os.environ.get("NICHE", "salud y bienestar")
        )
    else:
        print("Sin GEMINI_API_KEY: uso un guion de ejemplo.")
        data = SAMPLE

    narration = f"{data['hook']} {data['script']}"

    print("Sintetizando voz...")
    audio = os.path.join(BUILD, "audio.mp3")
    boundaries = tts.synthesize(narration, audio)
    print(f"  -> {len(boundaries)} tiempos de edge-tts" + ("" if boundaries else " (vacío: se usará timing estimado)"))

    print("Generando subtítulos...")
    ass = os.path.join(BUILD, "subs.ass")
    subtitles.build_ass(narration, boundaries, ass, audio)

    print("Armando video...")
    out = os.path.join(BUILD, "reel.mp4")
    try:
        dur = subtitles._audio_duration(audio)
    except Exception:
        dur = 40.0
    hook_card = (data.get("hook_card") or "").strip()
    video.build_video(audio, ass, out, duration=dur, hook=hook_card)

    full = os.path.abspath(out)
    print("\nListo. Video en:", full)
    try:
        os.startfile(full)  # abre el video en Windows
    except Exception:
        pass


if __name__ == "__main__":
    main()
