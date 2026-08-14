# quantcrypt 1.0.1 embute binários *.cpython-311-x86_64-linux-gnu.so precompilados:
# exige base glibc (Debian/Ubuntu, não Alpine/musl), CPython 3.11 e x86_64.
FROM --platform=linux/amd64 python:3.11-slim

WORKDIR /app

# Instala dependências primeiro para manter o cache de camada em edições só de código.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN useradd -m -u 1000 appuser
USER appuser
ENV HOME=/home/appuser \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENTRYPOINT ["python", "src/index.py"]
CMD ["--algorithm", "KEM", "--volume", "1000"]
