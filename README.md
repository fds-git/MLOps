## Проект по обнаружению мошеннических транзакций кредитных карт
Цели проекта:
1) разработать модуль обнаружения мошеннических транзакций кредитных карт на основе алгоритма машинного обучения. Данный модуль будет использоваться как составная часть системы обнаружения мошеннических транзакций кредитных карт;
2) данный модуль должен повысить производительность экспертов, которые занимаются определением, действительно ли транзакция является мошеннической, как минимум в два раза (во внимание экспертов попадает в два раза большее количество мошеннических транзакций).

Метрики проекта:
1) AUC ROC, как стандартная метрика при решении задачи бинарной классификации;
2) Average precision, как метрика, более подходящая чем AUC ROC для решения задач с сильным дисбаллансом классов;
3) Card Precision@k, как метрика, наиболее близко связанная с бизнес-метрикой (производительность экспертов), где k - максимальное количество банковских карт, которое может проверить эксперт.

Задачи:
1) инфраструктура:
а) ыавыва,
2) подготовка данных,
3) моделирование,
4) развертывание,
5) мониторинг,
6) автоматическое переобучение
