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

# El proyecto Python vive en Backend/: pyproject.toml esta ahi y pytest lo
# necesita para resolver testpaths y pythonpath.
cd Backend 2>/dev/null || exit 0

# Si hay un entorno activo (conda o venv) se respeta ese; si no, se busca
# un .venv/ en el repo. Asi el hook funciona con cualquiera de los dos.
if [ -n "$CONDA_PREFIX" ] || [ -n "$VIRTUAL_ENV" ]; then
  piton=python3
elif [ -x .venv/bin/python ]; then
  piton=.venv/bin/python
else
  piton=python3
fi

"$piton" -m pytest -q --tb=line 2>&1 | tail -15
exit 0
