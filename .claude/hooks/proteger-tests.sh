#!/usr/bin/env bash
# Guardrail: se pueden AGREGAR tests, no debilitar los que ya existen.
#
# Regla:
#   - Edit sobre tests/  -> solo se permite si el cambio es puramente aditivo
#                           (el texto viejo sigue intacto dentro del nuevo).
#   - Write sobre tests/ -> solo se permite si el archivo todavia no existe.
#
# Recibe el JSON del PreToolUse por stdin y responde con una decision de permiso.

exec python3 -c '
import json, os, sys, unicodedata

# Ante cualquier entrada inesperada el guardrail se abre, nunca se cierra:
# un hook roto no debe bloquear el trabajo.
try:
    evento = json.load(sys.stdin)
except Exception:
    sys.exit(0)

entrada = evento.get("tool_input", {})
herramienta = evento.get("tool_name", "")
ruta = entrada.get("file_path", "")


def normalizar(p):
    """macOS mezcla NFC y NFD en los paths: sin normalizar, una tilde
    convierte dos rutas identicas en cadenas distintas."""
    return unicodedata.normalize("NFC", os.path.realpath(p)) if p else ""


raiz = normalizar(os.environ.get("CLAUDE_PROJECT_DIR", ""))
absoluta = normalizar(ruta)

if raiz and absoluta.startswith(raiz + os.sep):
    relativa = absoluta[len(raiz) + 1 :]
else:
    relativa = absoluta

def permitir():
    sys.exit(0)

def denegar(motivo):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": motivo,
        }
    }))
    sys.exit(0)

if not relativa.startswith("tests/"):
    permitir()

if herramienta == "Edit":
    viejo = entrada.get("old_string", "")
    nuevo = entrada.get("new_string", "")
    if viejo and viejo in nuevo:
        permitir()
    denegar(
        f"Guardrail del repo: no se pueden modificar ni eliminar tests existentes "
        f"({relativa}). Puedes AGREGAR tests nuevos, pero no debilitar los que ya "
        f"estan. Si crees que este test esta mal, explicalo y pide autorizacion "
        f"al humano en vez de editarlo."
    )

if herramienta == "Write" and os.path.exists(ruta):
    denegar(
        f"Guardrail del repo: {relativa} ya existe y Write lo sobrescribiria "
        f"por completo. Usa Edit para agregar tests al final del archivo."
    )

permitir()
'
