# tests/

В этой папке хранятся тесты сервиса.

---

## Запуск

```bash
cd project
uv run pytest tests -v
```

---

## Файлы

### `test_service.py`

Тесты FastAPI сервиса через `TestClient` — запускаются без поднятия реального сервера.

| Тест | Что проверяет |
|------|---------------|
| `test_health` | `GET /health` возвращает `{"status": "ok"}` |
| `test_predict_valid_input` | Корректный запрос к `POST /predict` возвращает статус 200 |
| `test_predict_probability_range` | Вероятность увольнения всегда в диапазоне [0.0, 1.0] |
| `test_predict_risk_levels` | Уровень риска всегда один из: `low`, `medium`, `high` |
| `test_predict_invalid_input` | Некорректные данные (неверный тип) возвращают статус 422 |
