import argparse
import findspark
findspark.init()
findspark.find()
import pyspark
from pyspark.sql import SparkSession
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.sql.functions import dayofweek
from pyspark.sql.functions import hour

if __name__=='__main__':

    parser = argparse.ArgumentParser(description="Start date increment")
    parser.add_argument("-name", dest="name", help="name", required=True, type=str)
    args = parser.parse_args()
    name = args.name
    print(f'{name}')
    print(pyspark.__version__)

    spark = SparkSession\
            .builder\
            .appName("Feature")\
            .getOrCreate()


    customers = spark.read.csv(f'/user/testdata/{name}/customers.csv', inferSchema=True, header=True)
    terminals = spark.read.csv(f'/user/testdata/{name}/terminals.csv', inferSchema=True, header=True)
    transactions = spark.read.csv(f'/user/testdata/{name}/transactions.csv', inferSchema=True, header=True)

    # Удаляем лишние столбцы
    customers = customers.drop("available_terminals","nb_terminals")
    transactions = transactions.drop("TX_FRAUD_SCENARIO")
    transactions = transactions.drop("TX_TIME_SECONDS", "TX_TIME_DAYS")

    # Сводим все в одну таблицу
    result = transactions.join(customers, transactions.CUSTOMER_ID == customers.CUSTOMER_ID, "left")
    result = result.join(terminals, result.TERMINAL_ID == terminals.TERMINAL_ID, "left")

    # Работаем с временными признаками
    result = result.withColumn('day_of_week', dayofweek(result.TX_DATETIME))
    result = result.withColumn('hour', hour(result.TX_DATETIME))
    result = result.drop("TX_DATETIME")

    # Удаляем потенциально полезные признаки (надо проверить), чтобы не раздувать пространство
    result = result.drop("TRANSACTION_ID", "CUSTOMER_ID", "TERMINAL_ID")

    # one-hot преобразование hour
    hour_encoder = OneHotEncoder(inputCol="hour", outputCol="hour_encoded")
    hour_encoder_model = hour_encoder.fit(result)
    result = hour_encoder_model.transform(result)

    # one-hot преобразование day_of_week
    day_encoder = OneHotEncoder(inputCol="day_of_week", outputCol="day_of_week_encoded")
    day_encoder_model = day_encoder.fit(result)
    result = day_encoder_model.transform(result)

    # Нормализация оставшихся признаков
    amount_assembler = VectorAssembler(inputCols=["TX_AMOUNT"], outputCol="TX_AMOUNT_v")
    result = amount_assembler.transform(result)

    amount_scaler = MinMaxScaler(inputCol="TX_AMOUNT_v", outputCol="TX_AMOUNT_scaled")
    amount_scaler_model = amount_scaler.fit(result)
    result = amount_scaler_model.transform(result)

    x_cus_assembler = VectorAssembler(inputCols=["x_customer_id"], outputCol="x_customer_id_v")
    result = x_cus_assembler.transform(result)

    x_cus_scaler = MinMaxScaler(inputCol="x_customer_id_v", outputCol="x_customer_id_scaled")
    x_cus_scaler_model = x_cus_scaler.fit(result)
    result = x_cus_scaler_model.transform(result)

    y_cus_assembler = VectorAssembler(inputCols=["y_customer_id"], outputCol="y_customer_id_v")
    result = y_cus_assembler.transform(result)

    y_cus_scaler = MinMaxScaler(inputCol="y_customer_id_v", outputCol="y_customer_id_scaled")
    y_cus_scaler_model = y_cus_scaler.fit(result)
    result = y_cus_scaler_model.transform(result)

    mean_amount_assembler = VectorAssembler(inputCols=["mean_amount"], outputCol="mean_amount_v")
    result = mean_amount_assembler.transform(result)

    mean_amount_scaler = MinMaxScaler(inputCol="mean_amount_v", outputCol="mean_amount_scaled")
    mean_amount_scaler_model = mean_amount_scaler.fit(result)
    result = mean_amount_scaler_model.transform(result)

    std_amount_assembler = VectorAssembler(inputCols=["std_amount"], outputCol="std_amount_v")
    result = std_amount_assembler.transform(result)

    std_amount_scaler = MinMaxScaler(inputCol="std_amount_v", outputCol="std_amount_scaled")
    std_amount_scaler_model = std_amount_scaler.fit(result)
    result = std_amount_scaler_model.transform(result)

    mean_nb_amount_assembler = VectorAssembler(inputCols=["mean_nb_tx_per_day"], outputCol="mean_nb_tx_per_day_v")
    result = mean_nb_amount_assembler.transform(result)

    mean_nb_amount_scaler = MinMaxScaler(inputCol="mean_nb_tx_per_day_v", outputCol="mean_nb_tx_per_day_scaled")
    mean_nb_amount_scaler_model = mean_nb_amount_scaler.fit(result)
    result = mean_nb_amount_scaler_model.transform(result)

    x_ter_assembler = VectorAssembler(inputCols=["x_terminal_id"], outputCol="x_terminal_id_v")
    result = x_ter_assembler.transform(result)

    x_ter_scaler = MinMaxScaler(inputCol="x_terminal_id_v", outputCol="x_terminal_id_scaled")
    x_ter_scaler_model = x_ter_scaler.fit(result)
    result = x_ter_scaler_model.transform(result)

    y_ter_assembler = VectorAssembler(inputCols=["y_terminal_id"], outputCol="y_terminal_id_v")
    result = y_ter_assembler.transform(result)

    y_ter_scaler = MinMaxScaler(inputCol="y_terminal_id_v", outputCol="y_terminal_id_scaled")
    y_ter_scaler_model = y_ter_scaler.fit(result)
    result = y_ter_scaler_model.transform(result)

    # Собираем все признаки вместе
    features_assembler = VectorAssembler(inputCols=[
    "hour_encoded",
    "day_of_week_encoded",
    "TX_AMOUNT_scaled",
    "x_customer_id_scaled",
    "y_customer_id_scaled",
    "mean_amount_scaled",
    "std_amount_scaled",
    "mean_nb_tx_per_day_scaled",
    "x_terminal_id_scaled",
    "y_terminal_id_scaled"
    ],
    outputCol="Features",
    )

    result = features_assembler.transform(result)

    result.write.parquet(f'/user/processed_data/{name}/processed.parquet')
    spark.stop()