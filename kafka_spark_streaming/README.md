# Инференс модели на PySpark и Kafka

## Настроить кластер Kafka

1) В Yandex Cloud создать Managed Service for Kafka (зона доступности - ru-central1-b, выбрать любую сеть или default, выбрать группу безопасности, которая имеет настройки как в проекте airflow_dataproc_mlflow_validation, разрешить публичный доступ)

2) При создании группа безопасности должна иметь следующие настройки (как минимум):

Исходящий трафик:
| Протокол | Диапазон портов | Тип назначения       | Назначение    | Описание    |
|----------|-----------------|----------------------|---------------|-------------|
| Any	   | 0-65535	     |	Группа безопасности |	Self	    |  —          |
| Any	   | 0-65535		 |	CIDR				|	0.0.0.0/0   |  —          |

Входящий трафик:
| Протокол | Диапазон портов |	Тип источника       | Источник      | Описание    |
|----------|-----------------|----------------------|---------------|-------------|
| Any	   | 0-65535		 |	Группа безопасности	|	Self	    | input       |
| TCP	   | 9092    		 |  CIDR				|	0.0.0.0/0   | kafka plain |
| Any	   | 9091			 |  CIDR				|	0.0.0.0/0   | kafka ssl   |
| ICMP	   | —				 |  CIDR				|	0.0.0.0/0   | ping        |

3) Зайти в созданный кластер, нажать кнопку "Подключиться", скопировать FQDN и использовать его в параметрах подключения (18 строка в kafka_consumer.py и 29 строка в kafka_producer.py)

4) Скачать корневой сертификат для обмена данными по SSL (ссылка: https://cloud.yandex.ru/docs/managed-kafka/operations/connect#get-ssl-cert) . Файл YandexCA.crt положить в директорию со скриптами

5) Создать топики "features" и "predictions"

6) Создать пользователя (задать имя "mlops", пароль "otus-mlops", добавить роли consumer и producer для созданных топиков)

7) Установить библиотеку kafka-python

		pip install kafka-python


## Настроить кластер Data Proc

8) В качестве кластра использовать 

9) Склонировать репозиторий

		git clone https://github.com/fds-git/MLOps.git

10) Установить библиотеки

		pip install kafka-python


## Запуск скриптов

11) Запустить client_consumer

		python3 client_consumer.py -g otus

12) Запустить server_consumer

		python3 server_consumer.py -g otus

13) Запустить client_producer

		python3 kafka_producer.py -n 100


Обязательно проверить версию SPARK и SCALA

		spark-submit --version

Если версии такие:

SPARK 3.0.3
Scala 2.12.10

то запускаем приложение такой строкой

spark-submit --jars mlflow-spark-1.27.0.jar --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 predict.py

.option("partition.assignment.strategy", "range") \

--jars mlflow-spark-1.27.0.jar
