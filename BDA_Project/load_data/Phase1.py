import numpy as np
import pandas as pd
import pymongo
import librosa
import os
import zipfile
import urllib.request
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Step 1: Download and Extract the Dataset
# Define the URL and filename of the dataset
dataset_url = "https://www.kaggle.com/datasets/aaronyim/fma-small"
dataset_filename = "fma_small.zip"

# Define the directory to extract the dataset
extract_dir = "fma_small"

# Check if the dataset zip file already exists
if not os.path.exists(dataset_filename):
    # If the dataset zip file does not exist, download it
    print("Downloading dataset...")
    urllib.request.urlretrieve(dataset_url, dataset_filename)
    print("Download complete.")

# Check if the extraction directory already exists
if not os.path.exists(extract_dir):
    # If the extraction directory does not exist, create it
    os.makedirs(extract_dir)

# Extract the dataset
print("Extracting dataset...")
with zipfile.ZipFile(fma_small, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print("Extraction complete.")

# Step 2: Load the Dataset
with zipfile.ZipFile('fma_metadata.zip', 'r') as zip_ref:
    zip_ref.extractall('fma_small')

# Load metadata
metadata_df = pd.read_csv('fma_small/tracks.csv')

# Step 3: Feature Extraction
def extract_features(audio_file):
    # Load audio file
    y, sr = librosa.load(audio_file)

    # Extract MFCC (Mel-Frequency Cepstral Coefficients)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Extract 13 MFCC coefficients

    # Extract spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    return mfcc, spectral_centroid

# Apply feature extraction to each audio file and store in a DataFrame
features_df = pd.DataFrame(columns=['track_id', 'mfcc', 'spectral_centroid'])
for track_id, audio_file in metadata_df[['track_id', 'path']].iterrows():
    mfcc, spectral_centroid = extract_features(os.path.join('fma_dataset', 'fma_small', 'fma_small', '{:06d}'.format(track_id), '{:06d}.mp3'.format(track_id)))
    features_df = features_df.append({'track_id': track_id, 'mfcc': mfcc.tolist(), 'spectral_centroid': spectral_centroid.tolist()}, ignore_index=True)

# Step 4: Normalization or Standardization
# Apply normalization or standardization to the extracted features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features_df['features'].values.tolist())
features_df['features'] = scaled_features.tolist()

# Step 5: Dimensionality Reduction
# Apply dimensionality reduction techniques
pca = PCA(n_components=50)
reduced_features = pca.fit_transform(features_df['features'].values.tolist())
features_df['features'] = reduced_features.tolist()

# Step 6: Storage in MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['music_recommendation']
collection = db['audio_features']

# Convert DataFrame to JSON format and insert into MongoDB collection
for row in features_df.itertuples():
    collection.insert_one({'track_id': row.track_id, 'mfcc': row.mfcc, 'spectral_centroid': row.spectral_centroid})

# Print success message
print("Data stored in MongoDB successfully!")
