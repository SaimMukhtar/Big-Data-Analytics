from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import TrainValidationSplit, ParamGridBuilder

# Step 1: Connect to MongoDB and retrieve the audio features data
spark = SparkSession.builder \
    .appName("MusicRecommendationModel") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/music_recommendation.audio_features") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/music_recommendation.recommendations") \
    .getOrCreate()

# Load audio features data from MongoDB
audio_features_df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()

# Feature engineering and assembling
feature_columns = audio_features_df.columns  # Assuming all columns except 'track_id' are features
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
data = assembler.transform(audio_features_df)

# Splitting the data into training and testing sets
train_data, test_data = data.randomSplit([0.8, 0.2], seed=123)

# Scaling the features
scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
scaler_model = scaler.fit(train_data)
train_data_scaled = scaler_model.transform(train_data)
test_data_scaled = scaler_model.transform(test_data)

# Step 2: Training the music recommendation model with hyperparameter tuning
# Initialize ALS model
als = ALS(userCol="track_id", itemCol="track_id", ratingCol="play_count",
          coldStartStrategy="drop", nonnegative=True)

# Create ParamGrid for hyperparameter tuning
param_grid = ParamGridBuilder() \
    .addGrid(als.rank, [10, 20, 30]) \
    .addGrid(als.maxIter, [10, 20]) \
    .addGrid(als.regParam, [0.01, 0.1]) \
    .build()

# Define evaluator
evaluator = RegressionEvaluator(metricName="rmse", labelCol="play_count", predictionCol="prediction")

# Create TrainValidationSplit
tvs = TrainValidationSplit(estimator=als,
                            estimatorParamMaps=param_grid,
                            evaluator=evaluator,
                            trainRatio=0.8)

# Fit TrainValidationSplit
model = tvs.fit(train_data_scaled)

# Step 3: Evaluating the recommendation model
# Make predictions
predictions = model.transform(test_data_scaled)

# Evaluate the model
rmse = evaluator.evaluate(predictions)
print("Root Mean Squared Error (RMSE) = " + str(rmse))

# Print best parameters
best_model = model.bestModel
print("Best Rank:", best_model.rank)
print("Best MaxIter:", best_model._java_obj.parent().getMaxIter())
print("Best RegParam:", best_model._java_obj.parent().getRegParam())

# Print success message
print("Music recommendation model trained and evaluated successfully!")
