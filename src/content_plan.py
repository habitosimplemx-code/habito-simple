import datetime

COOLDOWN_DIAS = 5

# --------------------------------------------------------------------------
# Pilares (categorias base) — SALUD Y BIENESTAR.
# El dia que NO es de temporada, se usa esto. Todos acotados a educacion
# general y prevencion (NUNCA diagnostico ni tratamiento).
# --------------------------------------------------------------------------
PILARES = [
    {"id": "habitos", "nombre": "Hábitos diarios",
     "angulos": ["rutina de mañana", "pasos al día", "pausas activas", "constancia"]},
    {"id": "nutricion", "nombre": "Nutrición básica",
     "angulos": ["comer balanceado", "porciones", "leer etiquetas", "plato del bien comer"]},
    {"id": "sueno", "nombre": "Sueño y descanso",
     "angulos": ["higiene del sueño", "pantallas antes de dormir", "siesta corta", "rutina para dormir"]},
    {"id": "movimiento", "nombre": "Movimiento / actividad física",
     "angulos": ["caminar", "estiramientos", "moverse sin gimnasio", "romper el sedentarismo"]},
    {"id": "mental", "nombre": "Salud mental cotidiana",
     "angulos": ["manejo del estrés", "respiración", "desconexión", "descanso mental"]},
    {"id": "hidratacion", "nombre": "Hidratación",
     "angulos": ["cuánta agua", "señales de deshidratación", "mitos del agua", "hidratarte con calor"]},
    {"id": "mitos", "nombre": "Mito vs evidencia",
     "angulos": ["desmontar creencias comunes", "qué dice el consenso serio", "modas sin sustento"]},
    {"id": "prevencion", "nombre": "Prevención y chequeos",
     "angulos": ["qué revisiones tocan por edad", "agenda con tu médico", "prevenir mejor que curar"]},
    {"id": "pantallas", "nombre": "Salud y pantallas",
     "angulos": ["postura", "descanso visual (regla 20-20-20)", "cuello y espalda", "luz azul de noche"]},
    {"id": "azucar", "nombre": "Azúcar y ultraprocesados",
     "angulos": ["cómo identificarlos", "leer etiquetas", "sin satanizar", "azúcares escondidos"]},
    {"id": "trabajo", "nombre": "Salud en el trabajo",
     "angulos": ["ergonomía", "pausas activas", "estar sentado mucho", "estirar en la oficina"]},
    {"id": "corazon", "nombre": "Corazón y hábitos",
     "angulos": ["cuidar la presión con hábitos", "menos sal", "moverte más", "corazón y estilo de vida"]},
    {"id": "envejecer", "nombre": "Envejecer bien",
     "angulos": ["fuerza y equilibrio", "memoria activa", "hábitos a largo plazo", "vida social"]},
    {"id": "higiene", "nombre": "Higiene y cuidado diario",
     "angulos": ["lavado de manos", "cuidado de la piel", "protección solar", "higiene bucal"]},
    {"id": "alerta", "nombre": "Cuándo SÍ ir al médico",
     "angulos": ["señales de alerta generales", "no automedicarse", "cuándo no esperar"],
     "remite_medico": True},
]

# En estos pilares, el prompt SIEMPRE debe cerrar remitiendo a un profesional.
PILARES_REMITE_MEDICO = {p["id"] for p in PILARES if p.get("remite_medico")}

FORMATOS = [
    {"id": "tip", "nombre": "Tip rápido",
     "video": "Da UN consejo de hábito accionable y sencillo que la persona pueda aplicar hoy.",
     "imagen": "'big' = una acción corta en mayúsculas (ej: 'EMPIEZA HOY'). 'small' = qué hábito hacer y para qué."},
    {"id": "howto", "nombre": "Cómo hacerlo (paso a paso)",
     "video": "Explica PASO A PASO cómo adoptar un hábito o cómo prepararse para algo (1, 2, 3). "
              "Apóyate en el consenso de fuentes serias (OMS, Secretaría de Salud, IMSS). NO inventes pasos "
              "ni des dosis, medicamentos ni tratamientos.",
     "imagen": "'big' = 'PASO A PASO' o el resultado (ej: '3 PASOS'). 'small' = el hábito o resultado que se logra."},
    {"id": "dato", "nombre": "El dato que sorprende",
     "video": "Arranca con un hecho o dato concreto y educativo que sorprenda, y explícalo simple. "
              "NO inventes cifras ni estadísticas; si no estás seguro, habla en términos generales.",
     "imagen": "'big' = un hecho corto o '¿SABÍAS?'. 'small' = frase clara que lo explica, sin cifras inventadas."},
    {"id": "error", "nombre": "El error común",
     "video": "Nombra el error o mal hábito concreto que comete la gente y di cómo corregirlo, sin alarmar.",
     "imagen": "'big' = 'EL ERROR #1'. 'small' = el error concreto en una frase clara."},
    {"id": "mito", "nombre": "Mito vs. realidad",
     "video": "Plantea una creencia falsa común de salud y corrígela con el consenso serio, claro y breve.",
     "imagen": "'big' = 'MITO'. 'small' = la creencia falsa entre comillas + la realidad corta."},
    {"id": "comparativa", "nombre": "Comparativa simple",
     "video": "Compara dos opciones o hábitos (A vs B) y di cuál conviene y por qué, en términos generales.",
     "imagen": "'big' = 'A vs B' con dos conceptos cortos. 'small' = cuál conviene y por qué."},
    # Formato extra SOLO para el golpe del día y la reacción (no entra en la rotación normal).
    {"id": "mensaje", "nombre": "Mensaje del día",
     "video": "Mensaje corto y humano para EL día de la fecha: cuida tu bienestar con conciencia, sin sermón; "
              "un recordatorio ligero y amable.",
     "imagen": "'big' = frase corta del día. 'small' = recordatorio ligero y amable, sin regañar."},
]

_FORMATO_POR_ID = {f["id"]: f for f in FORMATOS}


# --------------------------------------------------------------------------
# EVENTOS FUERTES de salud: cada uno con su fecha objetivo (mes, dia = el "mero dia").
# En fechas de enfermedades (diabetes, cancer, hipertension) el angulo SIEMPRE es
# prevencion / habitos / concientizacion + "consulta a tu medico", NUNCA tratamiento.
# --------------------------------------------------------------------------
EVENTOS = [
    {"id": "retomar", "mes": 1, "dia": 3,
     "tema": "retomar hábitos en el año nuevo: moverte más y comer mejor sin dietas milagro"},
    {"id": "frio", "mes": 2, "dia": 1,
     "tema": "la temporada de frío: prevenir resfriados y gripe con lavado de manos e higiene"},
    {"id": "sueno_mundial", "mes": 3, "dia": 13,
     "tema": "el Día Mundial del Sueño: higiene del sueño para dormir mejor"},
    {"id": "salud_oms", "mes": 4, "dia": 7,
     "tema": "el Día Mundial de la Salud: chequeos y prevención general (agenda con tu médico)"},
    {"id": "hipertension", "mes": 5, "dia": 17,
     "tema": "cuidar la presión con hábitos (menos sal, más movimiento) — sin tratamiento; consulta a tu médico"},
    {"id": "sin_tabaco", "mes": 5, "dia": 31,
     "tema": "el Día Mundial Sin Tabaco: por dónde empezar para dejar de fumar"},
    {"id": "verano", "mes": 7, "dia": 15,
     "tema": "el calor del verano: hidratación y protección solar"},
    {"id": "corazon", "mes": 9, "dia": 29,
     "tema": "el Día Mundial del Corazón: hábitos para cuidar tu corazón (no tratamiento)"},
    {"id": "salud_mental", "mes": 10, "dia": 10,
     "tema": "el Día Mundial de la Salud Mental: manejo del estrés cotidiano (sin diagnósticos)"},
    {"id": "cancer_mama", "mes": 10, "dia": 19,
     "tema": "la concientización sobre el cáncer de mama: autoexploración y chequeo — remite a tu médico"},
    {"id": "diabetes", "mes": 11, "dia": 14,
     "tema": "el Día Mundial de la Diabetes: azúcar y hábitos, educativo, sin dietas médicas; consulta a tu médico"},
    {"id": "fiestas", "mes": 12, "dia": 24,
     "tema": "las fiestas decembrinas: comer con equilibrio y sin culpa"},
]

# Golpes de temporada = DÍAS PARA el evento (positivo = falta; 0 = el mero día;
# negativo = ya pasó). Espaciado ~3 días + el mero día + una reacción 2 días después.
RAMPA_OFFSETS = [10, 7, 4, 1, 0, -2]

# Rol de cada golpe: (etiqueta, formato_id, instruccion_extra_para_el_prompt).
BEATS = {
    10:  ("arranque", "dato",
          "Presenta por qué esta fecha importa para tu salud o bienestar (sin inventar cifras y sin asustar). "
          "Es el primer aviso: pon el tema sobre la mesa de forma educativa."),
    7:   ("prepárate", "howto",
          "Enseña un hábito o paso de prevención accionable para empezar YA. Algo concreto, no teoría."),
    4:   ("mito/error", "mito",
          "Desmonta un mito o error MUY común de estas fechas con el consenso serio (OMS/Secretaría de Salud/IMSS)."),
    1:   ("recordatorio", "tip",
          "Mini-checklist o recordatorio de hábito para la fecha. Amable y práctico."),
    0:   ("el día", "mensaje",
          "Es el día: mensaje corto y humano. Cuida tu bienestar con conciencia; sin regañar."),
    -2:  ("reacción", "mensaje",
          "Reacciona a la fecha con un ángulo de bienestar y hábitos. REQUIERE revisión humana."),
}

# Ventana en dias para considerar que un evento 'aplica' al buscar su ocurrencia.
_VENTANA_BUSQUEDA = 40


def _between(today, m1, d1, m2, d2) -> bool:
    """¿(mes,día) de hoy cae en el rango [m1/d1 .. m2/d2]? Maneja cruce de año."""
    x = (today.month, today.day)
    a, b = (m1, d1), (m2, d2)
    if a <= b:
        return a <= x <= b
    return x >= a or x <= b


def _delta_a_evento(today, mes, dia):
    """Días de HOY a la fecha objetivo más cercana (maneja cruce de año).
    Positivo = la fecha aún no llega; negativo = ya pasó."""
    candidatos = []
    for y in (today.year - 1, today.year, today.year + 1):
        try:
            f = datetime.date(y, mes, dia)
        except ValueError:
            continue
        candidatos.append((f - today).days)
    dentro = [c for c in candidatos if -_VENTANA_BUSQUEDA <= c <= _VENTANA_BUSQUEDA]
    if not dentro:
        return None
    return min(dentro, key=abs)


def evento_del_dia(today=None):
    """¿Hoy es un golpe de temporada? Devuelve dict o None."""
    today = today or datetime.date.today()
    for ev in EVENTOS:
        delta = _delta_a_evento(today, ev["mes"], ev["dia"])
        if delta is None:
            continue
        if delta in RAMPA_OFFSETS:
            etiqueta, fmt_id, instr = BEATS[delta]
            return {
                "evento_id": ev["id"],
                "tema": ev["tema"],
                "offset": delta,
                "etiqueta": etiqueta,
                "formato_id": fmt_id,
                "instruccion": instr,
                "es_borrador": delta < 0,   # la 'reacción' post-fecha nunca se autopublica
            }
    return None


def calendario_hint(today=None):
    """Compat: devuelve (tema, peso)."""
    ev = evento_del_dia(today)
    if ev:
        return (ev["tema"], "Fuerte")
    return (None, None)


def plan_del_dia(today=None, offset=0):
    """Elige categoría (enfriamiento de COOLDOWN_DIAS), formato (sin repetir los
    últimos 2) y, si hoy toca golpe de temporada, sobreescribe el formato con el
    del golpe y marca el tema. Devuelve un dict con todo lo que el prompt necesita."""
    today = today or datetime.date.today()

    recientes_pilares, recientes_formatos = [], []
    try:
        from src import history
        recientes_pilares = history.recent_pilares(COOLDOWN_DIAS)   # ids
        recientes_formatos = history.recent_formatos(2)             # nombres
    except Exception:
        pass

    disponibles = [p for p in PILARES if p["id"] not in recientes_pilares] or PILARES
    cat = disponibles[(today.toordinal() + offset) % len(disponibles)]

    fmts = [f for f in FORMATOS if f["nombre"] not in recientes_formatos and f["id"] != "mensaje"] or FORMATOS
    fmt = fmts[today.toordinal() % len(fmts)]

    ev = evento_del_dia(today)
    beat_instr = ""
    es_borrador = False
    if ev:
        fmt = _FORMATO_POR_ID.get(ev["formato_id"], fmt)
        beat_instr = ev["instruccion"]
        es_borrador = ev["es_borrador"]

    tema, peso = (ev["tema"], "Fuerte") if ev else (None, None)
    return {
        "categoria_id": cat["id"],
        "categoria_nombre": cat["nombre"],
        "angulos": ", ".join(cat["angulos"]),
        "remite_medico": cat["id"] in PILARES_REMITE_MEDICO,
        "formato_nombre": fmt["nombre"],
        "formato_video": fmt["video"],
        "formato_imagen": fmt["imagen"],
        "cal_tema": tema,
        "cal_peso": peso,
        "evento_id": ev["evento_id"] if ev else None,
        "evento_beat": ev["etiqueta"] if ev else None,
        "evento_instruccion": beat_instr,
        "publicar_borrador": es_borrador,
    }


def calendario_linea(plan) -> str:
    """Línea lista para el prompt. En un golpe de temporada, además del tema le pasa
    el ROL del golpe para que cada uno sea distinto."""
    tema, peso = plan.get("cal_tema"), plan.get("cal_peso")
    if not tema:
        return ""
    instr = plan.get("evento_instruccion", "")
    beat = plan.get("evento_beat", "")
    linea = f"TEMA DE TEMPORADA (hoy PRIORÍZALO por encima del pilar): {tema}.\n"
    if beat:
        linea += f"Rol de hoy en la cuenta regresiva ({beat}): {instr}\n"
    return linea


def pilar_del_dia(today=None, offset=0):
    return plan_del_dia(today, offset)["categoria_nombre"]


def avoid_text(recientes, limite=40):
    """Bloque de texto para el prompt con los temas a NO repetir."""
    if not recientes:
        return ""
    lista = "; ".join(recientes[-limite:])
    return ("\nTEMAS YA PUBLICADOS RECIENTEMENTE (está PROHIBIDO repetirlos; "
            f"elige un ángulo o subtema claramente distinto):\n{lista}\n")
