Music Recommendation System Report

Introduction
The objective of this project was to develop a music recommendation system that provides personalized music recommendations to users based on their preferences and listening history. Leveraging big data technologies and machine learning algorithms, the system aims to enhance user experience by offering relevant and diverse music suggestions.

Methodology
Extract, Transform, Load (ETL) Pipeline:
The ETL pipeline involved preprocessing the Free Music Archive (FMA) dataset, comprising 106,574 tracks spanning 161 genres.
Features such as Mel-Frequency Cepstral Coefficients (MFCC), spectral centroid, and zero-crossing rate were extracted from audio files using librosa in Python.
MongoDB was used to store the preprocessed audio features in a scalable and accessible manner.

Recommendation Model:
Collaborative filtering and Approximate Nearest Neighbours (ANN) algorithms were explored for recommendation generation.
Apache Spark's MLlib library was used for training recommendation models on the preprocessed dataset.

Deployment Architecture:
A Flask web application was developed to serve as the music streaming service.
Apache Kafka was integrated to handle real-time data streaming for user activity and recommendation generation.
Recommendations were dynamically generated based on user interactions and preferences, leveraging historical playback data.

Data
The FMA dataset, comprising audio tracks and metadata such as title, artist, and genres, was used for training the recommendation model. The dataset provided a rich source of music content, enabling the extraction of diverse features for recommendation generation.

Results

Evaluation Metrics:
Evaluation of the recommendation system was based on metrics such as Root Mean Square Error (RMSE) for collaborative filtering models and precision/recall for ANN models.
Comparative analysis of different recommendation algorithms revealed their respective strengths and weaknesses in terms of accuracy and scalability.

System Performance:
The system demonstrated scalability and efficiency in handling large volumes of user activity data and generating real-time recommendations.
Accuracy of recommendations improved over time as the system learned from user interactions and adapted to changing preferences.
Implementation

Technologies Used:
Python for ETL pipeline, recommendation model training, and web application development.
Apache Spark for distributed processing and training of recommendation models.
Flask for building the web application interface.
Apache Kafka for real-time data streaming and recommendation generation.

Code Organization:
The project code was organized into modules for data preprocessing, model training, web application development, and Kafka integration.
Detailed documentation and comments were provided to facilitate understanding and maintenance of the codebase.

System Setup:
Instructions for setting up and running the system were provided in the README.md file of the GitHub repository.
Dependencies and environment configuration were clearly specified to ensure seamless deployment.

Future Work
Integration of additional data sources and features to enhance recommendation accuracy and diversity.
Experimentation with advanced machine learning models and algorithms for further optimization.
Exploration of emerging big data technologies such as Apache Arrow and Microsoft Azure Cloud for improved performance and scalability.

Conclusion
The music recommendation system developed in this project represents a scalable and efficient solution for delivering personalized music recommendations to users. By leveraging big data technologies and machine learning algorithms, the system is able to provide accurate and diverse recommendations tailored to individual preferences. Further enhancements and experimentation with cutting-edge technologies hold the potential to enhance the system's performance and user experience.

Installation
Clone the repository:
bash

git clone <repository-url>
cd music-recommendation-system
Install dependencies:

pip install -r requirements.txt
Ensure Apache Kafka is installed and running.
Usage
Preprocess the dataset:

python etl_pipeline.py
Train the recommendation model:

python train_model.py
Run the Flask web application:

python app.py
Access the web application at http://localhost:5000.
Directory Structure

music-recommendation-system/
│
├── data/
│   ├── fma_dataset/          # Extracted FMA dataset
│   ├── fma_metadata.zip     # Metadata zip file
│   └── tracks.csv           # Metadata CSV file
│
├── models/                  # Trained recommendation models
│   ├── collaborative_filtering_model.pkl
│   └── ann_model.pkl
│
├── etl_pipeline.py          # ETL pipeline script
├── train_model.py           # Model training script
├── app.py                   # Flask web application
│
├── templates/               # HTML templates for web app
│   ├── index.html
│   └── recommendations.html
│
└── README.md                # Project documentation


References
Free Music Archive (FMA) dataset
librosa: Audio and Music Signal Analysis in Python
Apache Kafka Documentation
Flask Documentation
Apache Spark MLlib Documentation


I221415 Saim Mukhtar
I221997 Sarmad Ali
I222056 Abyaz Israr