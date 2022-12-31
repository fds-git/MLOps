### Автоматический запуск скриптов на кластере Data Proc через AirFlow

На кластере DataProc Через AirFlow запускаются скрипты: 
- генерации данных
- сохранения данных в HDFS
- предобработки данных с помощью PySpark
- обучения модели логистической регрессии и ее валидация с логгированием в MLFLOW
- обучения модели случайного леса и ее валидация с логгированием в MLFLOW
- построения доверительных интервалов для метрики F1 для каждой модели
- проведения t-test с заключением, показала ли вторая модель результат лучше, чем первая модель 

Важно: ВМ с AirFlow, MLFlow и кластер Data Proc должны находиться в одной сети и иметь одну и ту же группу безопасности

## Настройка MLFlow

1) Создать кластер Managed Service for PostgreSQL (не разрешать внешний IP, имя БД db1, пользователь user1, задать пароль)

2) При создании группа безопасности должна иметь следующие настройки:

Исходящий трафик:
| Протокол | Диапазон портов | Тип назначения       | Назначение    | Описание    |
|----------|-----------------|----------------------|---------------|-------------|
| Any	   | 0-65535	     |	Группа безопасности |	Self	    |  —          |
| Any	   | 0-65535		 |	CIDR				|	0.0.0.0/0   |  —          |

Входящий трафик:
| Протокол | Диапазон портов |	Тип источника       | Источник      | Описание    |
|----------|-----------------|----------------------|---------------|-------------|
| Any	   | 0-65535		 |	Группа безопасности	|	Self	    | input       |
| TCP	   | 22				 |  CIDR				|	0.0.0.0/0   | SSH         |
| ICMP	   | —				 |  CIDR				|	0.0.0.0/0   | ping        |
| TCP	   | 80				 |  CIDR				|	0.0.0.0/0   | HTTP (Air)  |
| TCP	   | 443			 |  CIDR				|	0.0.0.0/0   | HTTPS       |
| Any	   | 8888			 |  CIDR				|	0.0.0.0/0   | Jupyter     |
| Any	   | 4040-4050   	 |  CIDR				|	0.0.0.0/0   | Spark WebUI |
| Any      | 8000            |  CIDR                |   0.0.0.0/0   | MLFlow      |

Или можно создать ВМ и установить PostgreSQL (https://pedro-munoz.tech/how-to-setup-mlflow-in-production/)

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
		[default]
  		region=ru-central1
		MLFLOW_S3_ENDPOINT_URL=https://storage.yandexcloud.net
		MLFLOW_TRACKING_URI=http://10.129.0.26:8000 (внутренний адрес ВМ с MLFlow) (http://localhost:8000)

14) Создать файл:

		mkdir ~/.aws
		nano ~/.aws/credentials

15) И добавить в него credentials для доступа к S3 (см. пункт 5)

		aws_access_key_id = xxxx
		aws_secret_access_key = yyyy

16) Применяем настройки

		conda activate mlflow_env

17) Теперь можно запускать Tracking Server

		mlflow server --backend-store-uri postgresql://user1:заданный_пароль@внутренее_имя_хоста_базы_данных:6432/db1 --default-artifact-root s3://mlflowbucket/artifacts/ -h 0.0.0.0 -p 8000

		внутренее_имя_хоста_базы_данных например = rc1b-xqc7kmhsi8kne1bt.mdb.yandexcloud.net

18) !!!!!!!! ЗАДАТЬ ПАРОЛЬ ДЛЯ ПОЛЬЗОВАТЕЛЯ WEB ИНТЕРФЕЙСА (или пробросить SSH тоннель через 127.0.0.1 - ssh тоннель надо тоже фиксировать через tmux)

19) Подключаемся в web интерфейсу "внешний_IP_ВМ_MLFlow":8000 и в UI MLFlow создать эксперимент Spark_Experiment (ВАЖНО при создании в поле "Artifact Location" ввести s3://mlflowbucket/artifacts (НЕ s3a!!!)

## Настройка AirFlow

20) Создать виртуальную машину (Compute Cloud) с AirFlow (выбрать группу безопасности, настроенную ранее)

21) Подключиться по SSH с локальной машины и скопировать логин/пароль для подключения к AirFlow через web-интерфейс

		ssh dima@51.250.23.122

22) Переконфигурируем AirFlow, внеся изменения в /etc/airflow/airflow.cfg (чтобы выводилось меньше ненужной информации, напр. примеры DAG'ов)

		sudo nano /etc/airflow/airflow.cfg

	load_examples = False
	load_default_connections = False

	Сохраняем изменения и перезапускаем виртуальную машину (если веб интерфейс недоступен, пробуем другой браузер)

23) Генерируем SSH ключи на ВМ с AirFlow
	
		ssh-keygen

24) Переносим приватный ключ на директорию выше и присваиваем полный доступ (чтобы AirFlow мог его считать)

		cp .ssh/id_rsa ./
		sudo chmod 777 id_rsa

25) Копируем содержимое открытого ключа (он необходим при создании кластера Data Proc)

		cat .ssh/id_rsa.pub

	Выделяем ключ и ctrl+shift+c

26) Устанавливаем SSH провайдер

		sudo apt install python3-pip
		sudo pip install apache-airflow-providers-ssh (через sudo, иначе в веб интерфейте ошибка, что provider не обнаружен, т.к. AirFlow запущен от пользователя airflow)

	Если после последней команды веб-интерфейс станет недоступным, надо ввести команду:

		airflow webserver -p 80

	И затем отключиться от ВМ и снова в ней подключиться, веб интерфейс должен заработать.

	То же самое надо сделать с командой

		airflow scheduler - (Чтобы DAG запускался)

27) Проверяем, что провайдер установился
		
		sudo airflow providers list
		
28) Создаем новый DAG

		sudo nano /home/airflow/dags/run_generate_script.py

	Копируем содержимое run_generate_script.py из репозитория MLOps/airflow_dataproc_mlflow/for_airflow в только что созданный run_generate_script.py и сохраняем изменения

29) Через WEB-интерфейс AirFlow в разделе Admin Variables задаем переменные окружения

- DATAPROC_IP 10.129.0.13
- DATAPROC_PORT 22
- KEY_FILE /home/dima/id_rsa
- USERNAME ubuntu

## Настройка Hadoop-кластера (DataProc)

30) Создать кластер Data Proc, выбрать группу безопасности, настроенную ранее, разрешить внешний IP, выбрать существующий сервисный аккаунт, внести ssh ключ локальной машины, выбрать бакет mlflowbucket, в качестве SSH ключей использовать открытые ключи ВМ с AirFlow и своего ПК;

31) Подключиться к мастерноде из консоли AirFlow можно по внутреннему IP адресу, можно по внешнему, если внешний ip был разрешен при создании кластера

		ssh ubuntu@10.129.0.33

32) Установить и запустить tmux, чтобы сессия не прерывалась и разделить консоль
	
		sudo apt install tmux
		tmux

33) Склонировать репозиторий, содержащий необходимые скрипты

		sudo apt update
		sudo apt install git
		git clone https://github.com/fds-git/MLOps.git

34) Установить необходимые библиотеки (через sudo, иначе скрипт генерации run_generate_script.py не запустится на кластере так как не увидит numpy, pandas и т.д.)

		sudo apt install python3-pip
		sudo pip install numpy
		sudo pip install pandas
		sudo pip install fastparquet
		#sudo pip install findspark

35) Создаем директорию в hdfs для сохранения данных, которые будут генерироваться

		hdfs dfs -mkdir /user/testdata
		hdfs dfs -mkdir /user/processed_data

36) Правим переменные окружения

		sudo nano /etc/environment

		MLFLOW_S3_ENDPOINT_URL=https://storage.yandexcloud.net
		MLFLOW_TRACKING_URI=http://10.129.0.30:8000 (внутренний адрес ВМ с MLFlow)
		WORKPATH="/home/ubuntu/MLOps/airflow_dataproc_mlflow/for_dataproc/scripts"

37) Создать файл:

		mkdir ~/.aws
		nano ~/.aws/credentials

38) И добавить в него credentials для доступа к S3 (см. пункт 5)

		aws_access_key_id = xxxx
		aws_secret_access_key = yyyy

39) Устанавливаем клиентскую часть mlflow (хотя можно conda не утсанавливать на клиенте)
		conda create -n mlflow_env
		conda activate mlflow_env
		conda install python
		pip install mlflow
		pip install matplotlib
		pip install sklearn
		pip install boto3
		conda install -c anaconda ipykernel
		python -m ipykernel install --user --name ex --display-name "Python (mlflow)"


## Завершение настройки и запуск всей системы

40) Запускаем переключателем DAG. Через некоторое время можем увидеть выполненные экземпляры DAG'a, внутри будут выполненные таски run_generate, в логах можно посмотреть результаты работы.

41) Через консоль мастерноды проверим, что сгенерированыые данные появляются в HDFS

		hdfs dfs -ls /user/testdata - сырые данные (сгенерированные)
		hdfs dfs -ls /user/processed_data - предобработанные данные

42) В UI Spark видим выполненные и текущие spark-задачи

43) в UI MLFlow видим результаты экспериментов (метрики, гиперпараметры и модели)

44) В S3-хранилище YC в папке artifacts видим сериализованные модели

## Дополнительно

45) Обратить внимание на AirFlow:
- провайдеры в AirFlow устанавливать только через sudo, т.к. web-интерфейс, запускается через пользователя airflow и в противном случае не подтянет новые провайдеры;
- если в AirFlow в качестве команды хотим передать через SSHOperator запуск скрипта, например ('bash generate.sh '), то после .sh всегда пробел, иначе - ошибка;
- в date.txt после даты не должно быть пробелов, иначе - ошибка;
- Если при выполнении DAG получена ошибка "SSH command timed out", то попробовать помимо параметров timeout в SSHHook и conn_timeout в SSHOperator увеличить значение cmd_timeout в SSHOperator.

46) Обратить внимание на DataProc:

- Если необходимо запустить jupyter notebook на кластере, то необходим внешний IP на местерноде и чтобы открытый ключ локального компа лежал на местерноде, далее вводим команду в консоли мастерноды:

		jupyter notebook --no-browser --port=8888

- Сохраняем токен и на локальном компе пробросим ssh туннель

		ssh -L 8888:localhost:8888 ubuntu@51.250.21.57

- Подключаемся к jupyter на своей машине по 127.0.0.1:8888 для отладки, проведения экспериментов и анализа, если необходимо (нужно ввести запомненный токен)

- Чтобы в jupyter notebook запустить spark, необходимо установить и импортировать библиотеку 

		pip install findspark

- для отладки скриптов запускаем их вручную на кластере, перед этим отключив DAG в AirFlow

47) Общие рекомендации

- активно пользуемся tmux, в консоли должны быть следующие вкладки:
1. - ВМ MLFlow (разбито на 2 части через tmux: запущенный mlflow server и командная строка ВМ MLFlow)
2. - Мастернода DataProc (разбито на 2 части через tmux: запущенный jupyter notebook и командная строка мастерноды)
3. - ВМ AirFlow (командная строка AirFlow)
3. - локальная машина (разбито на 2 части через tmux: тоннель для juputer notebook и для web интерфейса MLFlow)

- в браузере следующие вкладки:

- использовать mlflow.pyspark.ml.autolog для логирования всех промежуточных значений гиперпараметров при поиске гиперпараметров с помощью pyspark
- использовать systemd для того, чтобы элементы продолжали работать и после отключения от локального компа

## To Do

48) Разобраться, как открывать веб интерфейс MLFlow, не открывая доступ к серверу со всего мира