#!/usr/bin/env bash
# Corre la suite despues de cada edicion, para que Claude vea el resultado
# sin tener que acordarse de invocar pytest.
#
# Solo se ejecuta si el archivo tocado es codigo Python del proyecto.

ruta=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')

case "$ruta" in
  *.py) ;;
  *) exit 0 ;;
esac

if [ -x .venv/bin/python ]; then
  piton=.venv/bin/python
else
  piton=python3
fi

"$piton" -m pytest -q --tb=line 2>&1 | tail -15
exit 0
