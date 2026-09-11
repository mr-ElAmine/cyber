FROM python:3.13-slim
# Volatility analyse la RAM ; pyelftools vérifie le format des captures.
RUN pip install --no-cache-dir volatility3==2.28.0 pyelftools==0.32 jsonschema
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 XDG_CACHE_HOME=/cache
USER 1000:1000
