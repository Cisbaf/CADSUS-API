# Etapa 1: builder
FROM python:3.12-slim AS builder

# Evita prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia e instala dependências em ambiente isolado
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# Etapa 2: imagem final minimalista
FROM python:3.12-slim

ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app

# Copia apenas o que for necessário do builder
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app

# Copia código da aplicação
COPY src /app/src/
COPY .certificate-cisbaf.pfx /app

# Porta usada pela FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "src.view.main:app", "--host", "0.0.0.0", "--port", "8000"]
