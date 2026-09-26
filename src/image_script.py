import os
import json
import time
import datetime
from google import genai
from google.genai import types
from google.genai import errors

from src import content_plan
from src import safety
from src.script_gen import _model_ladder, _is_daily_quota


def _extract_json(text: str) -> dict:
    text = text.strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"El modelo no devolvió JSON:\n{text}")
    return json.loads(text[start:end + 1])


def generate_image_post(niche="salud y bienestar", avoid=None, max_retries=6) -> dict:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    today = datetime.date.today()
    plan = content_plan.plan_del_dia(today, offset=0)   # imagen usa offset 0
    evitar = content_plan.avoid_text(avoid)
    cal = content_plan.calendario_linea(plan)
    remite = safety.bloque_remite_medico(plan.get("remite_medico", False))

    prompt = f"""Eres redactor de una cuenta mexicana de SALUD Y BIENESTAR llamada "Hábito Simple".
Tu público: personas normales en México, SIN conocimientos médicos. Escribes claro y directo,
como si le explicaras a un amigo. Nada de jerga. Nada de frases motivacionales vacías. NUNCA alarmas.
Es una SERIE diaria: "Hábito Simple" publica un hábito o consejo corto de salud cada día.

{safety.REGLAS_SEGURIDAD}
{remite}
PILAR DE HOY: {plan['categoria_nombre']} (ángulos posibles: {plan['angulos']}).
FORMATO DE HOY: {plan['formato_nombre']}.
Instrucciones del formato:
{plan['formato_imagen']}
{cal}{evitar}
Genera UN post de UNA imagen sobre el PILAR y el FORMATO de hoy. UNA idea útil y concreta que
cualquiera entienda al instante y pueda aplicar. Usa la fecha como semilla: {today.isoformat()}.

Reglas de longitud:
- "big": máximo ~14 caracteres. El gancho grande de la imagen.
- "small": una FRASE CLARA Y COMPLETA de 8 a 12 palabras (que se entienda sola).
- "caption": explicación útil en 2-3 frases y AL FINAL: un llamado a SEGUIR + guardar (ej: "Sígueme @habitosimplemx para un hábito diario y guarda este."), luego el aviso "{safety.DISCLAIMER_LARGO}", y 3-4 hashtags.
- "title": 3-5 palabras.
- "image_prompt": 1-2 frases EN INGLÉS para un fondo profesional del tema (salud, bienestar, vida cotidiana), SIN texto ni números y SIN escenas clínicas fuertes (nada de hospital, pastillas, sangre).
- "topic": identificador corto del tema en minúsculas con guiones (ej: "regla-20-20-20").
  Sirve para no repetir; hazlo específico al ángulo de HOY.

Reglas de contenido:
- Que cualquier persona lo entienda en 3 segundos.
- NO inventes estadísticas falsas. Usa cifras realistas o habla en términos generales.
- Ortografía correcta en español de México, CON acentos y ñ.

Devuelve SOLO un objeto JSON válido, sin markdown, con estas claves exactas:
"big", "small", "caption", "title", "image_prompt", "topic"."""

    modelos = _model_ladder()
    agotados = []
    last_err = None
    for mi, model in enumerate(modelos):
        for attempt in range(max_retries):
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=1.0,
                        response_mime_type="application/json",
                    ),
                )
                data = _extract_json(resp.text)
                data["categoria"] = plan["categoria_id"]
                data["formato"] = plan["formato_nombre"]
                data["publicar_borrador"] = plan.get("publicar_borrador", False)
                if mi > 0:
                    print(f"    (se usó el modelo de respaldo '{model}')")
                return data
            except errors.APIError as e:
                code = getattr(e, "code", None) or getattr(e, "status_code", None)
                last_err = e

                if code == 429 and _is_daily_quota(e):
                    agotados.append(model)
                    if mi < len(modelos) - 1:
                        print(f"Cuota diaria agotada en '{model}'. Salto a "
                              f"'{modelos[mi + 1]}'...")
                    break

                if code in (429, 500, 502, 503) and attempt < max_retries - 1:
                    wait = 10 * (attempt + 1)
                    print(f"Gemini respondió {code} (transitorio) en '{model}'. "
                          f"Reintento en {wait}s...")
                    time.sleep(wait)
                    continue

                if code in (429, 500, 502, 503):
                    print(f"'{model}' sigue fallando ({code}); pruebo el siguiente.")
                    break

                raise

    if agotados:
        raise RuntimeError(
            "Cuota DIARIA de Gemini agotada en todos los modelos del escalón "
            f"({', '.join(agotados)}). Se resetea a medianoche hora del Pacífico."
        )
    raise last_err
