# Multi-stage build: build assets in node stage, then install Python deps and collectstatic

# Node stage (for Tailwind build)
FROM node:20-alpine AS node_builder
WORKDIR /app
COPY ./chaiheadq/theme/package.json ./chaiheadq/theme/package-lock.json* ./
RUN if [ -f package.json ]; then npm ci --legacy-peer-deps || npm install --legacy-peer-deps; fi
# If you add Tailwind inputs, build them here
# COPY ./chaiheadq/theme/src ./chaiheadq/theme/src
# RUN npm run build || true

# Python runtime stage
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash appuser

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /code/

# copy built assets from node stage if present
# COPY --from=node_builder /app/dist /code/static/dist

# collect static for production
RUN python chaiheadq/manage.py collectstatic --noinput || true

# switch to non-root
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD [ "curl", "-f", "http://127.0.0.1:8000/health/" ] || exit 1

CMD ["gunicorn", "chaiheadq.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
