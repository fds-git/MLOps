echo ******Hello World from AWS EC2 Instance*******
echo $(hostname -i)
cd /home/ubuntu/MLOps/airflow_dataproc_gen_process_data/for_dataproc
echo $(pwd)

# Стартовую дату для генерации данных считываем из файла
START_DATE=`cat date.txt`

# Остальные параметры для генерации задаются здесь
INCREMENT_DAYS_INTERVAL=7
CUSTOMERS=500
TERMINALS=100
RADIUS=5

# Логируем часть параметров
echo Start generate data from $START_DATE
echo Increment days interval $INCREMENT_DAYS_INTERVAL

# Генерируем новые данные и записываем имя сгенерированного файла в текстовый документ
LAST_DATA_NAME=`python3 create_data.py -c ${CUSTOMERS} -t ${TERMINALS} -d ${INCREMENT_DAYS_INTERVAL} -date ${START_DATE} -r ${RADIUS}`
echo ${LAST_DATA_NAME} > last_data_name.txt
#export LAST_DATA_NAME

# Рассчитываем стартовую дату для следующей итерации и сохраняем в файл (перезаписываем исходный)
NEW_DATE=`python3 increment_date.py -d ${INCREMENT_DAYS_INTERVAL} -date ${START_DATE}`
echo ${NEW_DATE} > date.txt