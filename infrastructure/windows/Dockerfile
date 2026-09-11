# Image de la VM : les outils tournent sur le processeur du Mac.
# QEMU émule ensuite le PC x64 nécessaire à Windows.
FROM debian:13-slim AS vm

# qemu-utils gère le disque ; socat accède au moniteur QEMU.
# genisoimage prépare les DVD virtuels utilisés pour apporter des fichiers.
RUN apt-get update \
    && apt-get install -y --no-install-recommends qemu-system-x86 qemu-utils socat genisoimage \
    && rm -rf /var/lib/apt/lists/* \
    && install -d -o 1000 -g 1000 -m 0700 /storage /run/console

USER 1000:1000
# La commande QEMU est définie directement dans compose.yaml.

# Image de la console : noVNC affiche le bureau dans le navigateur.
# websockify relie cette page au socket VNC de QEMU.
FROM debian:13-slim AS console

RUN apt-get update \
    && apt-get install -y --no-install-recommends novnc websockify \
    && rm -rf /var/lib/apt/lists/* \
    && install -d -o 1000 -g 1000 -m 0700 /run/console

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 1000:1000
CMD ["websockify", "--web=/usr/share/novnc", "--unix-target=/run/console/vnc.sock", "0.0.0.0:6080"]
