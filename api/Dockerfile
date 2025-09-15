FROM python:3.10-slim-buster AS base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS dev
COPY . .
ARG API_PORT=8000
ENV API_PORT=${API_PORT}
EXPOSE ${API_PORT}
ENV PYTHONDONTWRITEBYTECODE=1
CMD uvicorn app.main:app --reload --host 0.0.0.0 --port ${API_PORT}

FROM base AS prod
COPY . .
ARG API_PORT=8000
ENV API_PORT=${API_PORT}
EXPOSE ${API_PORT}
CMD uvicorn app.main:app --host 0.0.0.0 --port ${API_PORT}
