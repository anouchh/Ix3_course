# data/

В этой папке хранятся данные, используемые для обучения и тестирования модели.

---

## Файлы

### `WA_Fn-UseC_HR-Employee-Attrition.csv`

Основной датасет проекта.

- **Источник:** IBM HR Analytics Employee Attrition Dataset, опубликован на Kaggle
- **Ссылка:** https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
- **Лицензия:** открытые данные, синтетически сгенерированы IBM — персональных данных не содержит
- **Размер:** 1470 строк, 35 признаков

**Целевая переменная:** `Attrition` — уволился (`Yes`) / остался (`No`)

**Признаки (после очистки используются 31):**

| Признак | Тип | Описание |
|---------|-----|----------|
| `Age` | int | Возраст сотрудника |
| `BusinessTravel` | str | Частота командировок: `Non-Travel`, `Travel_Rarely`, `Travel_Frequently` |
| `DailyRate` | int | Дневная ставка |
| `Department` | str | Отдел: `Sales`, `Research & Development`, `Human Resources` |
| `DistanceFromHome` | int | Удалённость от работы (км) |
| `Education` | int | Уровень образования (1–5) |
| `EducationField` | str | Направление образования |
| `EnvironmentSatisfaction` | int | Удовлетворённость рабочей средой (1–4) |
| `Gender` | str | Пол: `Male`, `Female` |
| `HourlyRate` | int | Почасовая ставка |
| `JobInvolvement` | int | Вовлечённость в работу (1–4) |
| `JobLevel` | int | Уровень должности (1–5) |
| `JobRole` | str | Должность |
| `JobSatisfaction` | int | Удовлетворённость работой (1–4) |
| `MaritalStatus` | str | Семейное положение: `Single`, `Married`, `Divorced` |
| `MonthlyIncome` | int | Ежемесячный доход |
| `MonthlyRate` | int | Ежемесячная ставка |
| `NumCompaniesWorked` | int | Количество предыдущих работодателей |
| `OverTime` | str | Сверхурочная работа: `Yes`, `No` |
| `PercentSalaryHike` | int | Процент повышения зарплаты |
| `PerformanceRating` | int | Оценка производительности (1–4) |
| `RelationshipSatisfaction` | int | Удовлетворённость отношениями на работе (1–4) |
| `StockOptionLevel` | int | Уровень опционов на акции (0–3) |
| `TotalWorkingYears` | int | Общий стаж работы |
| `TrainingTimesLastYear` | int | Количество обучений за последний год |
| `WorkLifeBalance` | int | Баланс работы и личной жизни (1–4) |
| `YearsAtCompany` | int | Лет в компании |
| `YearsInCurrentRole` | int | Лет на текущей должности |
| `YearsSinceLastPromotion` | int | Лет с последнего повышения |
| `YearsWithCurrManager` | int | Лет с текущим руководителем |

**Удалённые при предобработке признаки:**
- `EmployeeCount` — одно значение у всех (1)
- `Over18` — одно значение у всех (Y)
- `StandardHours` — одно значение у всех (80)
- `EmployeeNumber` — просто ID, информации не несёт

---

## Примечание

В репозитории хранится полный датасет — он небольшой (≈ 230 КБ)
и не содержит конфиденциальных данных.
