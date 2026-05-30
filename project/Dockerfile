FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY pyproject.toml .
RUN pip install uv && uv sync --no-dev

# Копируем весь проект
COPY . .

# Запускаем сервис
CMD ["uv", "run", "uvicorn", "src.service.app:app", "--host", "0.0.0.0", "--port", "8000"]