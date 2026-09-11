# Docker construit nativement pour le processeur du Mac.
# QEMU se charge ensuite d'émuler le PC x64 de Windows.
FROM debian:13-slim AS vm

RUN apt-get update \
    && apt-get install -y --no-install-recommends qemu-system-x86 qemu-utils socat genisoimage \
    && rm -rf /var/lib/apt/lists/* \
    && install -d -o 1000 -g 1000 -m 0700 /storage /run/console

USER 1000:1000
# La commande QEMU est définie directement dans compose.yaml.

# Deuxième image : uniquement l'interface web d'administration.
FROM debian:13-slim AS console

RUN apt-get update \
    && apt-get install -y --no-install-recommends novnc websockify \
    && rm -rf /var/lib/apt/lists/* \
    && install -d -o 1000 -g 1000 -m 0700 /run/console

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 1000:1000
CMD ["websockify", "--web=/usr/share/novnc", "--unix-target=/run/console/vnc.sock", "0.0.0.0:6080"]
