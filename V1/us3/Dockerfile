FROM debian:13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pefile binutils-mingw-w64-i686 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
USER 65534:65534
ENTRYPOINT ["python3", "/analyse.py"]
