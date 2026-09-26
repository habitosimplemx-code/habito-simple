import os
import json
import time
import datetime
from google import genai
from google.genai import types
from google.genai import errors

from src import content_plan
from src import safety

def _model_ladder():
    lista = os.environ.get("GEMINI_MODELS", "").strip()
    if lista:
        modelos = [m.strip() for m in lista.split(",") if m.strip()]
    else:
        modelos = [os.environ.get("GEMINI_MODEL", "gemini-3.6-flash").strip()]
    # sin duplicados, conservando el orden
    vistos, out = set(), []
    for m in modelos:
        if m and m not in vistos:
            vistos.add(m)
            out.append(m)
    return out


_DAILY_QUOTA_MARKS = ("PerDay", "GenerateRequestsPerDay", "free_tier_requests",
                      "RequestsPerDay")


def _is_daily_quota(err) -> bool:
    msg = str(err)
    return any(mark in msg for mark in _DAILY_QUOTA_MARKS)


def _extract_json(text: str) -> dict:
    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"El modelo no devolvió JSON:\n{text}")
    return json.loads(text[start:end + 1])


def generate_script(niche: str = "salud y bienestar",
                    avoid=None, max_retries: int = 4) -> dict:
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    today = datetime.date.today()
    plan = content_plan.plan_del_dia(today, offset=7)   # video usa offset 7
    evitar = content_plan.avoid_text(avoid)
    cal = content_plan.calendario_linea(plan)
    remite = safety.bloque_remite_medico(plan.get("remite_medico", False))

    prompt = f"""Eres guionista de Reels/Shorts en español de México para una cuenta
de SALUD Y BIENESTAR llamada "Hábito Simple". Tu público: personas normales en
México, SIN conocimientos médicos. Hablas claro y directo, como a un amigo.
Nada de jerga, nada de frases motivacionales vacías, NUNCA alarmas.

IDENTIDAD DE LA CUENTA (refuérzala, es una SERIE diaria): "Hábito Simple" publica
UN hábito o consejo corto de salud CADA DÍA para que la gente en México se sienta
mejor con pequeños cambios sostenibles. Que se sienta parte de una serie continua
("hoy te toca…", "el hábito de hoy…"), para dar razón de seguir y esperar el de mañana.

{safety.REGLAS_SEGURIDAD}
{remite}
PILAR DE HOY: {plan['categoria_nombre']} (ángulos posibles: {plan['angulos']}).
FORMATO DE HOY: {plan['formato_nombre']}. {plan['formato_video']}
{cal}{evitar}
Genera UN guion para un video vertical de 30 a 45 segundos sobre el PILAR y el FORMATO
de hoy, con un ángulo fresco, concreto y poco obvio. Usa la fecha como semilla: {today.isoformat()}.

MUY IMPORTANTE — cómo se usa el guion:
El "hook" y el "script" se CONCATENAN y se narran JUNTOS, en ese orden, como una
sola voz continua. Por eso:
- El "script" debe CONTINUAR justo después del hook, SIN repetirlo y SIN parafrasearlo.
- NO empieces el "script" retomando la idea del hook; entra directo al desarrollo.
- Leídos seguidos (hook + " " + script), NO debe haber ninguna frase ni idea repetida
  al inicio. Debe sonar natural, como si una persona hablara de corrido.

Ejemplo de lo que NO se debe hacer:
  hook:   "Dormir mal te afecta más de lo que crees."
  script: "Dormir mal te afecta mucho. El sueño..."  <-- MAL, repite el hook
Ejemplo correcto:
  hook:   "Dormir mal te afecta más de lo que crees."
  script: "Tu cuerpo repara y ordena la memoria mientras descansas, y sin eso todo cuesta más..."  <-- BIEN, continúa

Devuelve SOLO un objeto JSON válido, sin markdown ni texto adicional, con estas claves EXACTAS:
{{
  "hook": "primera frase de 1 línea que enganche en los primeros 2 segundos (sin alarmar)",
  "hook_card": "versión MUY CORTA del hook para mostrarla GRANDE en pantalla los primeros ~2.5s: 3-6 palabras, tipo pregunta/afirmación que FRENE el scroll (ej: '¿DUERMES MAL?', 'MUÉVETE 5 MIN', 'MITO DEL AGUA')",
  "script": "texto corrido que CONTINÚA después del hook (NO lo repitas), 90-130 palabras, frases cortas. Debe cerrar con: (1) un recordatorio de que es info general y ante dudas se consulta al médico, y (2) un llamado a seguir MUY corto (ej: 'Recuerda: esto es info general, ante dudas checa con tu médico. Sígueme, mañana va otro.'). Ese cierre cuenta dentro del límite de palabras.",
  "caption": "descripción para el post en 2-3 frases útiles y educativas, y AL FINAL: un llamado claro a SEGUIR + guardar (ej: 'Sígueme @habitosimplemx para un hábito diario y guarda este.'), luego el aviso '{safety.DISCLAIMER_LARGO}', y 3-5 hashtags relevantes en español de México (ej: #salud #bienestar #hábitossaludables #méxico)",
  "title": "título corto de 3-7 palabras",
  "topic": "identificador corto del tema en minúsculas con guiones (ej: 'higiene-del-sueno'); específico al ángulo de HOY",
  "broll_keywords": "2-4 palabras EN INGLÉS para el video de fondo (Pexels). Debe ser una escena CONCRETA de salud, bienestar o vida cotidiana RELACIONADA con el tema de hoy, y variar entre videos. Ejemplos válidos: 'person stretching morning', 'drinking water glass', 'walking in park', 'healthy vegetables cutting', 'person sleeping bed', 'meditation breathing', 'washing hands sink', 'running outdoors', 'family cooking kitchen'. PROHIBIDO: (a) escenas médicas o clínicas fuertes (nada de 'hospital', 'surgery', 'pills', 'injection', 'blood'); (b) escenas genéricas sin relación con salud (nada de 'texting', 'shopping', 'cafe coffee')",
  "cards": [
    {{"big": "texto grande, máx ~14 caracteres", "small": "frase corta que lo explica"}}
  ],
  "graphics": []
}}

Reglas para "cards": 0 a 2 elementos. Son rótulos que refuerzan la narración. Si no aportan, deja [].

Reglas para "graphics": 0 o 1 elemento, SOLO si tienes un dato numérico REAL y NO médico
que valga la pena animar (ej: 'camina 30 min', '7-9 horas de sueño', 'regla 20-20-20').
NUNCA cifras médicas (dosis, presión, glucosa) ni inventadas. Si no aplica, deja [].
Cada gráfico debe ser EXACTAMENTE uno de estos dos formatos, con números planos (sin comas ni signos):
- Contador que sube:
  {{"type": "countup", "value": 30, "prefix": "", "suffix": " MIN", "label": "DE CAMINATA AL DÍA"}}
- Barras comparativas (A vs B):
  {{"type": "bars", "title": "PASOS AL DÍA", "a_label": "SEDENTARIO", "a_value": 3000,
    "b_label": "META", "b_value": 8000, "a_color": "red", "b_color": "green", "money": false}}
No uses otros tipos ni omitas claves de estos formatos."""

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
                        print(f"Cuota diaria agotada en '{model}'. Salto al siguiente "
                              f"modelo: '{modelos[mi + 1]}'...")
                    break  # rompe el bucle de intentos -> siguiente modelo

                if code in (429, 500, 502, 503) and attempt < max_retries - 1:
                    wait = 8 * (attempt + 1)
                    print(f"Gemini respondió {code} (transitorio) en '{model}'. "
                          f"Reintento en {wait}s...")
                    time.sleep(wait)
                    continue

                if code in (429, 500, 502, 503):
                    print(f"'{model}' sigue fallando ({code}); pruebo el siguiente modelo.")
                    break

                raise

    if agotados:
        raise RuntimeError(
            "Cuota DIARIA del free tier de Gemini agotada en TODOS los modelos del "
            f"escalón ({', '.join(agotados)}). Se resetea a medianoche hora del "
            "Pacífico (~08:00 UTC / ~01:00 CDMX). Opciones: ampliar GEMINI_MODELS con "
            "otro modelo/flash-lite, o habilitar billing."
        )
    raise last_err
