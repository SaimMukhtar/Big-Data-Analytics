# Importing required libraries
import pandas as pd
from pyspark.sql import SparkSession

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("MongoDB RDD Analysis") \
        .getOrCreate()

    # Input MongoDB Atlas password
    password = input("Enter your MongoDB Atlas password: ")

    # Update the MongoDB connection URI with the password
    spark.conf.set("spark.mongodb.input.uri", f"mongodb+srv://i221415:{password}@cluster0.erypqf7.mongodb.net/ecommerce.customers")
    spark.conf.set("spark.mongodb.output.uri", f"mongodb+srv://i221415:{password}@cluster0.erypqf7.mongodb.net/ecommerce.customers")

    # Reading customer data from MongoDB
    customer_df = spark.read.format("mongo").load()

    # Register the DataFrame as a table
    customer_df.createOrReplaceTempView("customers")

    # Printing information about the DataFrame schema
    print("DataFrame Schema:")
    customer_df.printSchema()

    # Stop SparkSession
    spark.stop()

if __name__ == "__main__":
    main()
