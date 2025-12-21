# HW04: HTTP-сервис качества датасетов

## Выполненные задания:

### 1. Основной HTTP-сервис на FastAPI
- Создан файл `api.py` с FastAPI приложением
- Реализованы базовые эндпоинты из семинара S04
- Подключены зависимости `fastapi`, `uvicorn[standard]`, `python-multipart`

### 2. Эндпоинты из семинара (готовые)

#### `GET /health` - проверка работоспособности сервиса
#### `POST /quality` - оценка качества по агрегированным признакам  
#### `POST /quality-from-csv` - оценка качества по CSV-файлу

### 3. Новый эндпоинт

#### `POST /quality-flags-from-csv` - полный набор флагов качества
- Использует все эвристики качества из HW03
- Возвращает только булевы флаги в формате JSON
- Включает мои кастомные проверки:
  - Проверка константных колонок
  - Проверка дубликатов в ID-колонках

## Примеры запросов к API

### 1. Проверка работоспособности
**Запрос:**
```bash
GET http://127.0.0.1:8000/health
```

**Ответ:**
```json
{
  "status": "ok",
  "service": "dataset-quality",
  "version": "0.2.0"
}
```

### 2. Оценка качества по статистикам
**Запрос:**
```bash
POST http://127.0.0.1:8000/quality
Content-Type: application/json

{
  "n_rows": 1000,
  "n_cols": 10,
  "max_missing_share": 0.05,
  "numeric_cols": 7,
  "categorical_cols": 3
}
```

**Ответ:**
```json
{
  "ok_for_model": true,
  "quality_score": 0.85,
  "message": "Данных достаточно, модель можно обучать (по текущим эвристикам).",
  "latency_ms": 12.5,
  "flags": {
    "too_few_rows": false,
    "too_many_columns": false,
    "too_many_missing": false,
    "no_numeric_columns": false,
    "no_categorical_columns": false
  },
  "dataset_shape": {
    "n_rows": 1000,
    "n_cols": 10
  }
}
```

### 3. Оценка качества по CSV-файлу
**Запрос:**
```bash
POST http://127.0.0.1:8000/quality-from-csv
Content-Type: multipart/form-data

file: data/example.csv
```

**Ответ:**
```json
{
  "ok_for_model": true,
  "quality_score": 0.92,
  "message": "CSV выглядит достаточно качественным для обучения модели (по текущим эвристикам).",
  "latency_ms": 45.2,
  "flags": {
    "too_few_rows": false,
    "too_many_columns": false,
    "too_many_missing": false,
    "has_constant_columns": false,
    "has_suspicious_id_duplicates": false
  },
  "dataset_shape": {
    "n_rows": 150,
    "n_cols": 5
  }
}
```

### 4. Все флаги качества из CSV (мой новый эндпоинт)
**Запрос:**
```bash
POST http://127.0.0.1:8000/quality-flags-from-csv
Content-Type: multipart/form-data

file: data/example.csv
```

**Ответ:**
```json
{
  "flags": {
    "too_few_rows": false,
    "too_many_columns": false,
    "too_many_missing": false,
    "has_constant_columns": false,
    "has_suspicious_id_duplicates": false
  }
}
```

## Мои кастомные флаги качества (из HW03)

1. **`has_constant_columns`** - проверяет, есть ли в датасете колонки, где все значения одинаковы
2. **`has_suspicious_id_duplicates`** - проверяет дубликаты в колонках, которые могут быть идентификаторами (содержат "id", "uuid", "guid" в названии)

## Тестирование проекта

```bash
# Установка зависимостей
uv sync

# Запуск сервера
uv run uvicorn eda_cli.api:app --port 8000

# Проверка CLI (из HW03)
uv run eda-cli overview data/example.csv
uv run eda-cli report data/example.csv --out-dir reports

# Запуск тестов
uv run pytest -q
```