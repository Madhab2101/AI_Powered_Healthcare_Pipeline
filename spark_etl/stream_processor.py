import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import *

spark = (SparkSession.builder
         .appName("PredictiveHealthcareETL")
         .config("spark.sql.streaming.schemaInference", "true")
         .config("spark.sql.shuffle.partitions", "2")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "raw-patient"
OUTPUT_PATH = "D:/BDA/AI_Powered_Healthcare_Pipeline/output/cleaned_data"

schema = StructType([
    StructField("patient_id", StringType()),
    StructField("timestamp", StringType()),
    StructField("heart_rate", IntegerType()),
    StructField("systolic_bp", IntegerType()),
    StructField("diastolic_bp", IntegerType()),
    StructField("oxygen_saturation", DoubleType()),
    StructField("body_temp", DoubleType()),
    StructField("glucose_level", IntegerType())
])

raw_stream = (spark.readStream.format("kafka")
              .option("kafka.bootstrap.servers", KAFKA_BROKER)
              .option("subscribe", KAFKA_TOPIC)
              .option("startingOffsets", "latest")
              .load())

json_stream = raw_stream.selectExpr("CAST(value AS STRING) AS json_str")
parsed_stream = json_stream.select(from_json(col("json_str"), schema).alias("data")).select("data.*")

query = (parsed_stream.writeStream
         .format("parquet")
         .option("path", OUTPUT_PATH)
         .option("checkpointLocation", "D:/BDA/AI_Powered_Healthcare_Pipeline/output/checkpoints")
         .outputMode("append")
         .start())


print("Spark streaming started -> writing cleaned Parquet data...")

query.awaitTermination()
