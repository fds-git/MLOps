### Автоматический запуск скриптов на кластере Data Proc

1) Создать кластер Data Proc 
2) Подключиться к датаноде

		ssh ubuntu@51.250.21.57

3) Склонировать репозиторий, содержащий необходимый скрипт

		git clone https://github.com/fds-git/MLOps.git

4) Установить необходимые библиотеки и запустить скрипт

		sudo apt update
		sudo apt install python3-pip
		pip install numpy
		pip install pandas
		python3 MLOps/scripts/create_data.py

5) Сохранить сгенерированные данные в распределенную файловую систему

		hdfs dfs -mkdir /user/testdata
		hdfs dfs -copyFromLocal dataframe.csv /user/testdata/dataframe.csv

6) Выполнить проверку результата сохранения

		hdfs dfs -ls /user/testdata