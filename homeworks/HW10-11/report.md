# HW10-11 – компьютерное зрение в PyTorch: CNN, transfer learning, detection/segmentation

## 1. Кратко: что сделано

- Для части A выбран датасет `STL10`.
- Для части B выбран датасет `OxfordIIITPet` и трек `segmentation`.
- В части A сравнивались:
  - `C1`: simple CNN без аугментаций
  - `C2`: simple CNN с аугментациями
  - `C3`: pretrained `ResNet18`, обучение только головы
  - `C4`: pretrained `ResNet18`, partial fine-tuning (`layer4 + fc`)
- Во второй части сравнивались:
  - `V1`: базовая бинаризация вероятностной маски
  - `V2`: альтернативная постобработка с более высоким порогом и удалением маленьких компонент

## 2. Среда и воспроизводимость

- Python: `3.12.10`
- torch / torchvision: `2.10.0+cpu` / `0.25.0+cpu`
- Устройство (CPU/GPU): `CPU`
- Seed: `42`
- Как запустить: открыть `HW10-11.ipynb` и выполнить Run All.

## 3. Данные

### 3.1. Часть A: классификация

- Датасет: `STL10`
- Разделение: `train/val/test = 4000 / 1000 / 8000`
- Базовые transforms:
  - `ToTensor()`
- Augmentation transforms:
  - `RandomHorizontalFlip(p=0.5)`
  - `RandomCrop(size=(96, 96), padding=8)`
  - `ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2)`
  - `ToTensor()`
- Комментарий (2-4 предложения):  
  `STL10` содержит 10 классов цветных изображений размером `96x96`. Этот датасет подходит для сравнения простой CNN и transfer learning на pretrained `ResNet18`. На нём удобно наблюдать разницу между обучением с нуля и использованием предобученных признаков.

### 3.2. Часть B: structured vision

- Датасет: `OxfordIIITPet`
- Трек: `segmentation`
- Что считается ground truth:
  - бинарная маска `pet vs background`
  - foreground строится по trimap-значениям `1` и `3`
  - значение `2` считается background
- Какие предсказания использовались:
  - pretrained `DeepLabV3_ResNet50`
  - foreground в предсказании задавался как объединение классов `cat` и `dog`
- Комментарий (2-4 предложения):  
  Для `OxfordIIITPet` разумно использовать постановку `pet vs background`, потому что датасет содержит готовые segmentation-маски. Такая бинарная постановка хорошо согласуется с возможностями pretrained segmentation model и позволяет корректно интерпретировать `IoU`, `precision` и `recall`.

## 4. Часть A: модели и обучение (C1-C4)

- C1 (simple-cnn-base):  
  Простая CNN из трёх блоков `Conv-ReLU-MaxPool`, затем `Flatten -> Linear(18432 -> 256) -> ReLU -> Dropout(0.3) -> Linear(256 -> 10)`. Обучение с нуля без аугментаций.
- C2 (simple-cnn-aug):  
  Та же архитектура `SimpleCNN`, что и в `C1`, но с train-аугментациями.
- C3 (resnet18-head-only):  
  Pretrained `ResNet18`, backbone заморожена, обучается только `fc`.
- C4 (resnet18-finetune):  
  Pretrained `ResNet18`, partial fine-tuning: обучаются `layer4 + fc`.

Дополнительно:

- Loss: `CrossEntropyLoss`
- Optimizer(ы): `Adam`
- Batch size: `64`
- Epochs (макс):
  - `C1`, `C2`: `8`
  - `C3`: `5`
  - `C4`: `5`
- Критерий выбора лучшей модели: `best_val_accuracy`

## 5. Часть B: постановка задачи и режимы оценки (V1-V2)

### Если выбран segmentation track

- Модель: `DeepLabV3_ResNet50 pretrained`
- Что считается foreground:
  - в ground truth: `pet`
  - в предсказании: `cat OR dog`
- V1: базовая постобработка  
  Бинаризация вероятностной карты с порогом `0.5`.
- V2: альтернативная постобработка  
  Бинаризация с порогом `0.6` и удаление маленьких компонент площадью меньше `300` пикселей.
- Как считался mean IoU:  
  Для каждого изображения считалось отношение пересечения к объединению бинарных масок `pred` и `gt`, затем результат усреднялся.
- Считались ли дополнительные pixel-level метрики:  
  Да, считались `precision` и `recall`.

## 6. Результаты

Ссылки на файлы в репозитории:

- Таблица результатов: `./artifacts/runs.csv`
- Лучшая модель части A: `./artifacts/best_classifier.pt`
- Конфиг лучшей модели части A: `./artifacts/best_classifier_config.json`
- Кривые лучшего прогона классификации: `./artifacts/figures/classification_curves_best.png`
- Сравнение C1-C4: `./artifacts/figures/classification_compare.png`
- Визуализация аугментаций: `./artifacts/figures/augmentations_preview.png`
- Визуализации второй части:
  - `./artifacts/figures/segmentation_examples.png`
  - `./artifacts/figures/segmentation_metrics.png`

Короткая сводка (6-10 строк):

- Лучший эксперимент части A: `C4`
- Лучшая `val_accuracy`: `0.9512`
- Итоговая `test_accuracy` лучшего классификатора: `0.9481`
- Что дали аугментации (C2 vs C1): в данной конфигурации аугментации не улучшили результат
- Что дал transfer learning (C3/C4 vs C1/C2): transfer learning дал сильное улучшение качества
- Что оказалось лучше: head-only или partial fine-tuning: лучше оказался `partial fine-tuning`
- Что показал режим V1 во второй части: `mean_iou = 0.8150`, `precision = 0.9805`, `recall = 0.8290`
- Что показал режим V2 во второй части: `mean_iou = 0.7975`, `precision = 0.9856`, `recall = 0.8079`
- Как интерпретируются метрики второй части: `IoU` оценивает качество перекрытия масок, `precision` — точность foreground-пикселей, `recall` — полноту покрытия foreground

Примечание: для ускорения расчёта segmentation-метрики оценивались на подмножестве из 200 тестовых изображений.

## 7. Анализ

Простая CNN на `STL10` показала существенно более слабый результат, чем pretrained `ResNet18`. В `C1` модель достигла `val_accuracy ≈ 0.58`, что ожидаемо для обучения с нуля на сравнительно небольшом наборе данных. В `C2` аугментации не дали улучшения: результат оказался ниже, чем у `C1`. Вероятно, при выбранной архитектуре и числе эпох модель не успела получить пользу от дополнительного разнообразия данных.

Pretrained `ResNet18` дал сильное улучшение качества. Уже в режиме `head-only` (`C3`) качество выросло до `val_accuracy ≈ 0.93`, что намного лучше результатов простой CNN. Это показывает, что предобученные признаки хорошо переносятся на `STL10`. При переходе к partial fine-tuning (`C4`) качество стало ещё выше, так как часть backbone смогла адаптироваться под текущую задачу. В итоге `C4` оказался лучшим и по `val_accuracy`, и по итоговой `test_accuracy`.

Во второй части метрика `mean_iou` подходит для segmentation, потому что она оценивает качество перекрытия предсказанной и истинной масок. Дополнительные `precision` и `recall` позволяют понять, насколько модель склонна к ложным срабатываниям или к потере части объекта. При переходе от `V1` к `V2` выросла `precision`, но снизились `recall` и `mean_iou`. Это означает, что более жёсткая постобработка сделала маски более консервативными: уменьшилось число лишних foreground-пикселей, но часть истинного объекта стала теряться.

## 8. Итоговый вывод

В качестве базового классификационного конфига я бы выбрала `C4`, потому что он дал наилучшие `val_accuracy` и `test_accuracy`. Главный вывод по transfer learning состоит в том, что pretrained признаки дают очень большое преимущество по сравнению с обучением простой CNN с нуля. Во второй части стало видно, что для segmentation важно смотреть не только на `IoU`, но и на `precision` и `recall`. Также стало понятно, что постобработка может улучшать одни метрики и ухудшать другие, поэтому её нужно оценивать количественно.

## 9. Приложение

- кривые лучшего классификационного прогона: `./artifacts/figures/classification_curves_best.png`
- сравнение экспериментов `C1-C4`: `./artifacts/figures/classification_compare.png`
- визуализация аугментаций: `./artifacts/figures/augmentations_preview.png`
- примеры segmentation-предсказаний: `./artifacts/figures/segmentation_examples.png`
- сравнение метрик `V1` и `V2`: `./artifacts/figures/segmentation_metrics.png`