# ---------- Builder ----------
FROM python:3.11-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.lock.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir \
      --extra-index-url https://download.pytorch.org/whl/cpu \
      -r requirements.lock.txt \
      -w /wheels

# ---------- Runtime ----------
FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . .

EXPOSE 8000
CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8000","--workers","1"]
