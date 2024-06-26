### Формулировка проблемы

Специфика работы страховой компании предполагает наличие значительного портфеля в fixed-income инструментах (облигации, депозиты). Поэтому для целей бюджетного планирования и управления рисками (стресс-тестов) необходимо решить задачу прогнозирования уровней процентных ставок, которые, в свою очередь, используются для:

- Прогнозирования стоимости портфеля/переоценки в стрессовых сценариях и базовых сценариях.
- Прогнозирования уровня рискового капитала (Риск 1 в методологии 781-П), который участвует в расчёте аналога норматива достаточности капитала — нормативного соотношения (подробнее см. Положение ЦБ 781-П).

Все эти показатели напрямую зависят от уровней ключевой ставки на всей КБД-кривой. Далее будет описан подход к прогнозированию распределения ставок на кривой.

### Подход к решению задачи

Существуют различные подходы к прогнозированию, такие как:

- Использование прогнозов от участников рынка, ЦБ и т. д.
- Чисто эконометрические модели.
- Рыночные модели (расчёт форвардных ставок по сложившейся на дату оценки кривой и т. д., использование short-rate моделей).

Проблема этих моделей в чистом виде заключается в том, что они лишь отражают ожидания в моменте (рыночные модели и прогнозы) либо просто используют исторические данные (эконометрические модели) и не отражают ожидаемые будущие изменения. К тому же, они, как правило, не позволяют сделать сценарный анализ или стресс-тест.

Также особенностью бюджетного планирования в компании является привязка к показателю ключевой ставки ЦБ. С одной стороны, это упрощает прогнозирование инвестиционного дохода (пусть и ценой точности), с другой — упрощает процесс стресс-тестирования: появляется универсальный входной параметр, от которого зависит сценарий стресс-теста (то есть движение кривой ОФЗ). Этот параметр можно презентовать и наглядно объяснить, в отличие от абстрактных движений ставок, вроде параллельного сдвига кривой, роста коротких/снижения длинных и наоборот.

Задача заключается в следующем: нужно спрогнозировать распределение процентной кривой КБД на конец 2024, 2025 и 2026 годов, используя исторические данные и прогноз ключевой ставки. То есть сделать модель, которая прогнозирует изменения кривой ОФЗ при изменении ключевой ставки с учётом временного лага, характерного для конкретного тенора кривой.

### Для решения задачи было решено использовать модификацию модели Халла-Уайта со следующими особенностями:

- Параметры κ (скорость возврата к среднему) и σ (волатильность) калибруются на исторических данных.
- Параметр θ (долгосрочное среднее) является вектором и определяется как ключевая ставка минус средний спред тенора кривой к ключевой ставке на исторических данных.

То есть параметры κ и σ калибруются с учётом переменного θ, динамика которого зависит от ключевой ставки. В качестве θ может выступать прогноз ключевой ставки минус спред.

### Пример результата для бюджетного сценария
![image](https://github.com/SaikNikita/Curve_prediction/assets/124429089/5308c827-a8cc-4a72-9637-1718df7afdc9)

#### Кривые на отчётные даты
![image](https://github.com/SaikNikita/Curve_prediction/assets/124429089/8287bccb-4ee1-43e7-9fb8-513461cd3693)

Подробнее в https://github.com/SaikNikita/Curve_prediction/blob/master/%D0%9F%D1%80%D0%BE%D0%B3%D0%BD%D0%BE%D0%B7%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20IR%20%D0%BA%D1%80%D0%B8%D0%B2%D0%BE%D0%B9.ipynb
