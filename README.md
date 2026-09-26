# Hábito Simple — contenido automático de salud y bienestar (IG + YouTube + FB + TikTok)

Pipeline que cada día: genera un guion con Gemini → le pone voz (edge-tts) →
crea subtítulos sincronizados → arma un video vertical 1080×1920 con FFmpeg →
lo sube a un Release del repo (URL pública) → lo publica en Instagram y YouTube.
Facebook y TikTok se suben a mano desde el borrador que llega por Telegram.

Es el **mismo motor** que "Dinero Simple", re-marcado para **salud y bienestar** y
con **barreras de seguridad** propias del nicho médico.

## ⚠️ Regla no negociable (léela)

Este canal es de **educación general y prevención**, NUNCA de diagnóstico ni tratamiento.
Las reglas duras están cableadas en `src/safety.py` y se inyectan en cada guion/imagen:

- ❌ Nada de diagnósticos, dosis, medicamentos, curas, suplementos como tratamiento.
- ❌ Nada de dietas médicas, cifras inventadas, ni temas sensibles (adelgazar rápido, etc.).
- ✅ Siempre marco de "información general, no reemplaza a tu médico" (disclaimer FIJO en video e imagen).
- ✅ Ante señales de alerta → "acude con un profesional de salud".
- ✅ Apoyo en consenso de fuentes serias (OMS, Secretaría de Salud, IMSS).

El disclaimer se dibuja SIEMPRE (no depende de que la IA lo recuerde): en el video como
un chip inferior (`DISCLAIMER_TEXT`) y en la imagen como una pastilla al pie. Además el
prompt obliga a cerrar el caption y la narración con el aviso.

## Estructura

```
habito-simple/
├── main.py                 # pipeline de VIDEO (reel)
├── image_main.py           # pipeline de IMAGEN
├── test_local.py           # prueba local del video (sin publicar)
├── image_test.py           # prueba local de la imagen (sin publicar)
├── index.html / privacy.html  # landing + aviso de privacidad (GitHub Pages)
├── brand/                  # logo, foto de perfil, portada, favicon
├── src/
│   ├── safety.py           # ← barreras de seguridad (fuente única)
│   ├── content_plan.py     # 15 pilares de salud + calendario de fechas fuertes
│   ├── script_gen.py       # guion (Gemini) con reglas de seguridad
│   ├── image_script.py     # texto de imagen (Gemini) con reglas de seguridad
│   ├── video.py            # FFmpeg: video vertical + disclaimer fijo (paleta verde)
│   ├── image_render.py     # Pillow: imagen 4:5 + disclaimer fijo (paleta verde)
│   ├── graphics.py, subtitles.py, tts.py, broll.py, image_gen.py
│   ├── uploader.py, publisher.py, image_post.py, youtube_upload.py
│   ├── history.py, notify.py
└── .github/workflows/      # cron diario + ejecución manual (video e imagen)
```

## Probar en local (sin publicar)

1. `python -m venv .venv` y actívalo.
2. `pip install -r requirements.txt` (necesitas FFmpeg instalado).
3. Copia `run_test.ps1.example` → `run_test.ps1`, pon tu `GEMINI_API_KEY`, y corre `.\run_test.ps1`.
   - Sin API key también corre: usa un guion de ejemplo (cero costo).
4. Para la imagen: `run_image_test.ps1.example` → `run_image_test.ps1`.

**Revisa CADA borrador con lupa por el tema de seguridad** antes de publicar.

## Publicar

- Automático: los workflows corren por cron y mandan un **borrador** por Telegram (`PUBLISH: "false"`).
- Apruebas desde Telegram: GitHub → Actions → "Publicar Reel diario" → Run workflow → pega el `publicar_id`.
- Marca / voz / disclaimer se controlan por variables de entorno (ver `.env.example`).

## Marca

- Nombre: **Hábito Simple** · Handle: **@habitosimplemx**
- Tagline: *Tu vida sana, un hábito a la vez*
- Voz TTS: `es-MX-DaliaNeural` (femenina, para diferenciar de "Dinero Simple" = Jorge)
- Paleta: verde salud (`#1FA37A` / `#2FC892`) sobre verde profundo (`#0E2A28`)
