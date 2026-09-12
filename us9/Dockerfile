FROM python:3.13-slim

# Lire les fichiers du registre Windows.
RUN pip install --no-cache-dir dissect.regf==3.14

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 1000:1000
