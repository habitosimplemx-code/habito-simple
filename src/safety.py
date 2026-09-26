"""Barreras de seguridad del nicho de SALUD (fuente única de verdad).

Salud NO es finanzas: un mal consejo puede dañar a una persona y hacer que las
plataformas tumben la cuenta por desinformación médica. Como el guion lo escribe
una IA en automático, estas reglas van METIDAS en el prompt y NO son opcionales.

Se importan desde script_gen.py e image_script.py para que el video y la imagen
compartan exactamente las mismas barreras.
"""
import os

# El disclaimer visible se puede sobreescribir por variable de entorno para que
# el video (video.py) y la imagen (image_render.py) usen el MISMO texto.
DISCLAIMER_TEXT = os.environ.get(
    "DISCLAIMER_TEXT", "Info general · No sustituye a tu médico"
).strip()

# Frase completa para cerrar el caption y la narración.
DISCLAIMER_LARGO = os.environ.get(
    "DISCLAIMER_LARGO",
    "ℹ️ Información general y educativa, no reemplaza a tu médico.",
).strip()

# Bloque que se pega DENTRO del prompt de Gemini (guion e imagen).
REGLAS_SEGURIDAD = """REGLAS DE SEGURIDAD (OBLIGATORIAS — este es un canal de SALUD, no de medicina):
Estás PROHIBIDO de hacer cualquiera de estas cosas. Si un tema no se puede tratar sin
romper una regla, CAMBIA el enfoque a un hábito o prevención general seguro.
- ❌ NADA de diagnósticos ("si tienes X es porque…", "esto que sientes es…").
- ❌ NADA de dosis, nombres de medicamentos como recomendación, ni "toma esto para…".
- ❌ NADA de curas ni "esto cura / elimina / revierte / desinflama X".
- ❌ NADA de suplementos presentados como tratamiento.
- ❌ NADA de dietas específicas para enfermedades (diabetes, tiroides, riñón, etc.).
- ❌ NADA de cifras o estadísticas inventadas. Si no estás seguro, habla en términos generales.
- ❌ NADA de temas sensibles: trastornos alimenticios, autolesión, suicidio, adelgazar rápido,
     ni "detox", "quema grasa", "baja X kilos en Y días".
- ✅ SIEMPRE enmarca como INFORMACIÓN GENERAL Y EDUCATIVA, no consejo médico.
- ✅ Ante señales de alerta o cualquier duda → di claramente "acude con un profesional de salud".
- ✅ Apóyate en el consenso de fuentes serias (OMS, Secretaría de Salud, IMSS).
- ✅ Tono tranquilo y amable: educar y motivar hábitos, NUNCA asustar ni prometer resultados."""


def bloque_remite_medico(remite: bool) -> str:
    """Instrucción extra cuando el pilar del día es sensible (ej. 'Cuándo ir al médico',
    o una fecha de enfermedad)."""
    if not remite:
        return ""
    return ("\nIMPORTANTE HOY: este tema toca señales/condiciones de salud. El ángulo debe ser "
            "de concientización y prevención, y DEBES cerrar remitiendo a un profesional de salud "
            "('agenda con tu médico', 'no lo dejes pasar, consúltalo').\n")
