### Проект по загрузке занных в S3 и Data Proc и работа с данными на кластере Spark


1) Создать кластер Managed Service for PostgreSQL (не разрешать внешний IP, имя БД db1, пользователь user1, задать пароль)

Можно создать ВМ и установить PostgreSQL (https://pedro-munoz.tech/how-to-setup-mlflow-in-production/)

2) Настроить группу безопасности следующим образом:

Исходящий трафик:
| Протокол | Диапазон портов | Тип назначения       | Назначение    | Описание    |
|----------|-----------------|----------------------|---------------|-------------|
| Any	     | 0-65535	       |	Группа безопасности |	Self	        | output      |
| Any	     | 0-65535		     |	CIDR				        |	0.0.0.0/0     | out         |

Входящий трафик:
| Протокол | Диапазон портов |	Тип источника       | Источник      | Описание    |
|----------|-----------------|----------------------|---------------|-------------|
| Any	     | 0-65535		     |	Группа безопасности	|	Self	        | input       |
| TCP	     | 22				       |  CIDR				        |	0.0.0.0/0     | SSH         |
| TCP	     | 443			       |  CIDR				        |	0.0.0.0/0     | HTTPS       |
| Any      | 4040-4050       |  CIDR                | 0.0.0.0/0     | Spark WebUI |
| Any      | 8888            |  CIDR                | 0.0.0.0/0     | Jupyter     |
| Any      | 8000            |  CIDR                | 0.0.0.0/0     | MLFlow      |

3) В Object Storage создать бакет mlflowbucket с приватным доступом и в ACL бакета добавить текущего пользователя Yandex Cloud с правами read и write

4) Создать внутри папку artifacts

5) Сгенерировать и сохранить, если до этого не было сгенерировано, идентификатор и ключ доступа для текушего сервисного аккаунта 

6) Создать виртуальную машину (для MLFlow)

7) Выбрать группу безопасности, настроенную ранее, разрешить внешний IP, выбрать существующий сервисный аккаунт, внести ssh ключ локальной машины, задать имя пользователя

8) Подключиться к ВМ MLFlow через внешний IP

		ssh dima@51.250.21.57

9) Установить и запустить tmux, чтобы сессия не прерывалась и разделить консоль
	
		sudo apt install tmux
		tmux


Порядок настройки MlFlow взят отсюда https://mcs.mail.ru/blog/mlflow-in-the-cloud


10) Установить Conda

		curl -O https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh
		bash Anaconda3-2020.11-Linux-x86_64.sh
		exec bash

11) Создадим и активируем отдельное окружение для MLflow

		conda create -n mlflow_env
		conda activate mlflow_env

12) Устанавливаем необходимые библиотеки

		sudo apt update
		conda install python
		pip install mlflow
		pip install boto3                 # для работы MLFlow с S3 хранилищем
		sudo apt install gcc
		pip install psycopg2-binary

13) Создаем переменные окружения

		sudo nano /etc/environment

		добавить:
		MLFLOW_S3_ENDPOINT_URL=https://storage.yandexcloud.net
		MLFLOW_TRACKING_URI=http://10.129.0.26:5000 (внутренний адрес ВМ с MLFlow)

14) Создать файл:

		mkdir ~/.aws
		nano ~/.aws/credentials

15) И добавить в него credentials для доступа к S3 (см. пункт 5)

		aws_access_key_id = YCA1JE4zVgb2pBpfhDvAPwsfKg3
		aws_secret_access_key = YCO234dQVQXycd1_rok-qUHdwqdq8KsoIsYwcQZPk

16) Применяем настройки

		conda activate mlflow_env

17) Теперь можно запускать Tracking Server

		mlflow server --backend-store-uri postgresql://user1:заданный_пароль@внутренее_имя_хоста_базы_данных:6432/db1 --default-artifact-root s3a://mlflowbucket/artifacts/ -h 0.0.0.0 -p 8000

		внутренее_имя_хоста_базы_данных например = rc1b-xqc7kmhsi8kne1bt.mdb.yandexcloud.net

18) !!!!!!!! ЗАДАТЬ ПАРОЛЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ WEB ИНТЕРФЕЙСА (или пробросить SSH тоннель через 127.0.0.1 - ssh тоннель надо тоже фиксировать через tmux)

19) Подключаемся в web интерфейсу "внешний_IP_ВМ_MLFlow":8000

20) Создать кластер Data Proc, выбрать группу безопасности, настроенную ранее, разрешить внешний IP, выбрать существующий сервисный аккаунт, внести ssh ключ локальной машины, выбрать бакет mlflowbucket

21) Подключиться к мастерноде

		ssh ubuntu@158.160.16.238

22) Установить и запустить tmux, чтобы сессия не прерывалась и разделить консоль
	
		sudo apt install tmux
		tmux

23) Запустить jupyter notebook на мастерноде через активное окно tmux и скорировать токен подключения
		
		jupyter notebook --no-browser --port=8888

24) На локальном хосте пробросить ssh туунель

		ssh -L 8888:localhost:8888 ubuntu@158.160.16.238

25) В браузере подключиться к localhost:8888 и ввести токен

26) На кластере установить git и клонировать репозиторий с примерами

		sudo apt install git
		git clone https://github.com/fds-git/MLOps

27) Устанавливаем клиентскую часть mlflow

		pip install mlflow

28) В UI Spark создать эксперимент Spark_Experiment

27) Переходим в директорию со скриптами и запускаем 

		cd MLOps/mlflow/fixed/
		bash flights_LR_only_solution.sh

28) В UI Spark видим выполнение задачи, в UI MLFlow видим результат эксперимента


Внимательно с именами файлов
Разобрать почему findspark иногда находится, иногда нет

в консоли вкладки
1 - ВМ MLFlow (разбито на 2 части через tmux: запущенный mlflow server и командная строка ВМ MLFlow)
2 - Мастернода DataProc (разбито на 2 части через tmux: запущенный jupyter notebook и командная строка мастерноды)
3 - локальная машина (разбито на 2 части через tmux: тоннель для juputer notebook и для web интерфейса MLFlow)

упражнение flights_LR_only работало
упражнение flights_pipeline_solution не работало
ошибка:

Traceback (most recent call last):
  File "/home/ubuntu/solutions/flights_pipeline_solution.py", line 114, in <module>
    main(args)
  File "/home/ubuntu/solutions/flights_pipeline_solution.py", line 57, in main
    experiment_id = experiment.experiment_id
AttributeError: 'NoneType' object has no attribute 'experiment_id'

Не понятно, как клиент MLFlow находит развернутый сервер

Уточнить, правильно ли:
mlflow server --backend-store-uri postgresql://user1:заданный_пароль@внутренее_имя_хоста_базы_данных:6432/db1 --default-artifact-root s3a://mlflowbucket/artifacts/ -h 0.0.0.0 -p 8000