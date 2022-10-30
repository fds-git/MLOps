### Автоматический запуск скриптов на кластере Data Proc через AirFlow

Важно: ВМ с AirFlow и кластер Data Proc должны находиться в одной сети и иметь одну и ту же группу безопасности

1) Создать виртуальную машину (Compute Cloud) с AirFlow
2) При создании группа безопасности должна иметь следующие настройки:

Исходящий трафик:
Протокол	Диапазон портов	Тип назначения			Назначение	Описание
Any			0-65535			Группа безопасности		Self		—
TCP			443				CIDR					0.0.0.0/0 	—
Any			0-65535			CIDR					0.0.0.0/0 	—

Входящий трафик:
Протокол	Диапазон портов	Тип источника			Источник	Описание
Any			0-65535			Группа безопасности		Self		—
TCP			22				CIDR					0.0.0.0/0 	—
ICMP		—				CIDR					0.0.0.0/0 	—
TCP			80				CIDR					0.0.0.0/0 	—

3) Подключиться по SSH с локальной машины и скопировать логин/пароль для подключения к AirFlow через web-интерфейс

		ssh dima@51.250.23.122

4) Переконфигурируем AirFlow, внеся изменения в /etc/airflow/airflow.cfg (чтобы выводилось меньше ненужной информации, напр. примеры DAG'ов)

		sudo nano /etc/airflow/airflow.cfg

	load_examples = False
	load_default_connections = False

	Сохраняем изменения и перезапускаем виртуальную машину

5) Генерирует SSH ключи
	
		ssh-keygen

6) Копируем содержимое открытого ключа (он необходим при создании кластера Data Proc)

		cd .ssh
		cat id_rsa.pub
	Выделяем ключ и ctrl+shift+c

7) Создать кластер Data Proc
8) При создании группа безопасности должна иметь такие же настройки, как и ВМ с AirFlow
9) В качестве SSH ключа использовать открытый ключ ВМ с AirFlow
10) Подключиться к датаноде из консоли AirFlow можно по внутреннему адресу, можно по внешнему, если внешний ip был разрешен при создании кластера

		ssh ubuntu@10.129.0.33

11) Склонировать репозиторий, содержащий необходимый скрипт

		sudo apt update
		sudo apt install git
		git clone https://github.com/fds-git/MLOps.git

12) Установить необходимые библиотеки

		sudo apt install python3-pip
		pip install numpy
		pip install pandas
		
13) Создаем новый DAG

		cd /home/airflow/dags/
		sudo nano run_generate_script.py

	Копируем содержимое run_generate_script.py из репозитория MLOps/airflow_dataproc_gen_data/ в только что созданный run_generate_script.py и сохраняем изменения

13) Сохранить сгенерированные данные в распределенную файловую систему

		python3 MLOps/airflow_dataproc_gen_data/create_data.py
		hdfs dfs -mkdir /user/testdata
		hdfs dfs -copyFromLocal dataframe.csv /user/testdata/dataframe.csv

14) Выполнить проверку результата сохранения

		hdfs dfs -ls /user/testdata


15) Подключиться к AirFlow через web-интерфейс

		http://51.250.23.122:80/

	Здесь должны увидеть новый DAG с dag_id = mks_geo

16) Запускаем переключателем DAG. Через некоторое время можем увидеть выполненные экземпляры DAG'a, в логах будут храниться результаты запросов к сервису.

17) Заменив PythonOperator, например, на PostgresOperator можем сохранять результаты запросов в базу данных.

