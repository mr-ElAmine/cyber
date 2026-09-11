FROM python:3.13-slim

RUN pip install --no-cache-dir \
    dissect.hypervisor==3.21 dissect.volume==3.18 \
    dissect.ntfs==3.16 dissect.regf==3.14

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 1000:1000
