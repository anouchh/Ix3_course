# Итоговый проект по курсу «Инженерия Искусственного Интеллекта»

---

## 1. Паспорт проекта

- **Название проекта:** HR Attrition — сервис предсказания увольнений сотрудников
- **Автор:** Мамасова Анна Сергеевна
- **Группа:** ИКБО-30-24
- **Контакт:** @anouchh

- **Краткое описание:**
  Проект решает задачу предсказания увольнения сотрудника по его профилю.
  Используется открытый датасет IBM HR Analytics Employee Attrition (Kaggle, 1470 сотрудников, 31 признак).
  Обучены и сравнены четыре модели; финальная модель — логистическая регрессия с ROC-AUC 0.807 и Recall 0.77.
  Результат — REST API, который по профилю сотрудника возвращает вероятность увольнения и уровень риска.

---

## 2. Структура проекта

```
project/
  notebooks/                 — EDA и эксперименты с моделями
    README.md                — описание ноутбуков
    01_eda.ipynb             — разведочный анализ данных и обучение моделей
  src/
    README.md                — описание модулей
    data/
      __init__.py
      preprocessor.py        — предобработка входных данных (кодирование категориальных признаков)
    models/
      __init__.py
      predictor.py           — загрузка модели из artifacts/ и выполнение предсказания
    service/
      __init__.py
      app.py                 — FastAPI приложение
  data/                      — датасет (открытые данные, IBM HR Analytics)
    README.md                — описание источника данных и признаков
    WA_Fn-UseC_HR-Employee-Attrition.csv
  artifacts/
    model.pkl                — сохранённая финальная модель (логистическая регрессия)
    README.md                — описание модели: метрики, алгоритм 
  configs/
    .env.example             — описание переменных окружения
    README.md                — описание доступных конфигураций
  tests/
    __init__.py
    README.md                — инструкция по запуску тестов
    test_service.py          — тесты сервиса
  .dockerignore
  .gitignore
  Dockerfile                 — сборка Docker-образа
  pyproject.toml             — зависимости проекта и конфигурация для uv
  uv.lock                    — фиксация точных версий всех зависимостей
  demo.py                    — скрипт-демонстрация: отправляет тестовый запрос к API
  report.md                  — отчёт по проекту
  self-checklist.md          — чеклист самопроверки
```

---

## 3. Требования и установка

### 3.1. Требования

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) — менеджер зависимостей
- Docker (опционально, для запуска в контейнере)

### 3.2. Установка окружения

```bash
# Перейти в папку проекта
cd project

# Установить зависимости через uv (создаст .venv автоматически)
uv sync

# Активировать окружение (Windows)
.venv\Scripts\activate
```

---

## 4. Как запустить проект

### 4.1. Запуск сервиса локально

```bash
cd project
uv run uvicorn src.service.app:app --reload
```

Сервис поднимается на `http://localhost:8000`.

Swagger UI (интерактивная документация): `http://localhost:8000/docs`

### 4.2. Запуск через Docker

```bash
cd project

# Собрать образ
docker build -t hr-attrition .

# Запустить контейнер
docker run -p 8000:8000 hr-attrition
```

### 4.3. Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Проверка работоспособности сервиса |
| POST | `/predict` | Предсказание вероятности увольнения |

Полный список признаков для `/predict` см. в `src/service/app.py` (класс `EmployeeFeatures`)
или в интерактивной документации по адресу `http://localhost:8000/docs`.

Пример минимального запроса:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 28, "BusinessTravel": "Travel_Frequently", "DailyRate": 500,
    "Department": "Sales", "DistanceFromHome": 25, "Education": 2,
    "EducationField": "Life Sciences", "EnvironmentSatisfaction": 1,
    "Gender": "Male", "HourlyRate": 40, "JobInvolvement": 2, "JobLevel": 1,
    "JobRole": "Sales Representative", "JobSatisfaction": 1,
    "MaritalStatus": "Single", "MonthlyIncome": 2500, "MonthlyRate": 5000,
    "NumCompaniesWorked": 5, "OverTime": "Yes", "PercentSalaryHike": 11,
    "PerformanceRating": 3, "RelationshipSatisfaction": 2, "StockOptionLevel": 0,
    "TotalWorkingYears": 3, "TrainingTimesLastYear": 1, "WorkLifeBalance": 1,
    "YearsAtCompany": 1, "YearsInCurrentRole": 0, "YearsSinceLastPromotion": 0,
    "YearsWithCurrManager": 0
  }'
```

Пример ответа:

```json
{
  "attrition_probability": 0.85,
  "risk_level": "high"
}
```

Уровни риска: `low` (< 0.35), `medium` (0.35–0.60), `high` (> 0.60)

### 4.4. Демонстрационный скрипт

```bash
# Сервис должен быть запущен
python demo.py
```

Скрипт отправляет два запроса — сотрудник с высоким риском и стабильный сотрудник —
и выводит результаты в консоль.

---

## 5. Данные

Используется открытый датасет **IBM HR Analytics Employee Attrition** (Kaggle).

- Ссылка: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- Файл: `data/WA_Fn-UseC_HR-Employee-Attrition.csv`
- 1470 строк, 35 признаков (после очистки — 31)
- Целевая переменная: `Attrition` (Yes / No)
- Данные полностью открытые, синтетически сгенерированные IBM — персональных данных нет

Датасет лежит в `data/` — скачивать отдельно не нужно.
Подробное описание признаков см. в `data/README.md`.

---

## 6. Тесты

Реализованы тесты сервиса в `tests/test_service.py`:

- `test_health` — сервис отвечает на `/health`
- `test_predict_valid_input` — корректный запрос возвращает 200
- `test_predict_probability_range` — вероятность всегда в диапазоне [0, 1]
- `test_predict_risk_levels` — уровень риска всегда один из допустимых значений
- `test_predict_invalid_input` — некорректные данные возвращают 422

Запуск:

```bash
cd project
uv run pytest tests -v
```

---

## 7. Демонстрация на защите

На защите я:

1. Покажу структуру проекта и ключевые файлы (`src/`, `notebooks/`, `artifacts/`).
2. Запущу сервис через Docker (`docker run -p 8000:8000 hr-attrition`).
3. Запущу `demo.py` — покажу предсказания для сотрудника с высоким риском и стабильного сотрудника.
4. Покажу ноутбук `notebooks/01_eda.ipynb` — графики EDA и итоговую таблицу сравнения моделей.
5. Обращу внимание на логи сервиса — каждый запрос логируется с результатом.

---

## 8. Ограничения и дальнейшая работа

**Текущие ограничения:**
- Датасет синтетический (IBM), реальные данные компании могут отличаться
- Модель статична — не переобучается при появлении новых данных
- Нет мониторинга дрейфа данных и качества предсказаний в продакшне
- Нет объяснения предсказаний для конкретного сотрудника (SHAP не реализован)

**Дальнейшие шаги:**
- Добавить SHAP-объяснения: почему модель считает сотрудника в зоне риска
- Настроить автоматическое переобучение модели по расписанию
- Добавить мониторинг метрик качества через Prometheus/Grafana
- Реализовать хранение истории предсказаний в базе данных

---

## 9. Оценка проекта

Итоговая оценка за проект выставляется по пятибалльной шкале (2–5).
