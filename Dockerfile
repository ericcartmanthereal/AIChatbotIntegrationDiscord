# Dockerfile

# 1. Verwende ein offizielles Python-Image als Basis
FROM python:3.9-slim

# 2. Setze das Arbeitsverzeichnis im Container
WORKDIR /bot

# 3. Kopiere das Python-Skript in das Arbeitsverzeichnis
COPY bot.py .

# 4. Führe das Python-Skript aus, wenn der Container gestartet wird
CMD ["python", "bot.py"]