"""Comprueba la sintaxis de los scripts .sh con `bash -n` (no los ejecuta)."""

import shutil
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
SCRIPTS = sorted(RAIZ.glob("[0-9][0-9]_*/**/*.sh"))


@pytest.mark.skipif(shutil.which("bash") is None, reason="bash no está instalado")
@pytest.mark.parametrize("script", SCRIPTS, ids=lambda p: p.relative_to(RAIZ).as_posix())
def test_sintaxis_bash(script):
    contenido = script.read_bytes()
    assert contenido.startswith(b"#!/bin/bash"), "falta el shebang #!/bin/bash"
    assert b"\r\n" not in contenido, "finales de línea CRLF: bash fallaría en Linux"
    resultado = subprocess.run(["bash", "-n"], input=contenido, capture_output=True)
    assert resultado.returncode == 0, resultado.stderr.decode(errors="replace")
