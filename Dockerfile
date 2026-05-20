FROM python:3.12-slim
RUN apt-get update && apt-get install -y \
  libgtk-3-0 libx11-xcb1 libdbus-glib-1-2 libxt6 \
  ca-certificates --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y libasound2 && rm -rf /var/lib/apt/lists/*
RUN python -m camoufox fetch
COPY server.py .
EXPOSE 3000
CMD ["python", "server.py"]
