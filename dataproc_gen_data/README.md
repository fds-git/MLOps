### Ручной запуск скриптов на кластере Data Proc

1) Создать кластер Data Proc

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

3) Подключиться к датаноде

		ssh ubuntu@51.250.21.57

4) Установить Git

		sudo apt update
		sudo apt install git

5) Склонировать репозиторий, содержащий необходимый скрипт

		git clone https://github.com/fds-git/MLOps.git

6) Установить необходимые библиотеки и запустить скрипт

		sudo apt install python3-pip
		pip install numpy
		pip install pandas
		python3 MLOps/dataproc_gen_data/create_data.py

7) Сохранить сгенерированные данные в распределенную файловую систему

		hdfs dfs -mkdir /user/testdata
		hdfs dfs -copyFromLocal dataframe.csv /user/testdata/dataframe.csv

8) Выполнить проверку результата сохранения

		hdfs dfs -ls /user/testdata