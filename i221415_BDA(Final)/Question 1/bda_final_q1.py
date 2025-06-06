# -*- coding: utf-8 -*-
"""BDA Final Q1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vgod-0LBsWH2B0x19jx8ZGndWU7uT0Si
"""

# Importing required libraries
from itertools import combinations
import numpy as np
import random
from collections import defaultdict

# Sample input
sessions = [
    ["view_home", "click_ads", "view_product", "add_to_cart", "checkout", "view_home"],
    ["view_product", "add_to_cart", "checkout", "view_home", "click_ads", "view_product"],
    ["view_home", "click_ads", "view_product", "add_to_cart", "view_product", "checkout"],
    ["view_home", "click_ads", "view_product", "add_to_cart", "view_product", "checkout"]
]

# Creating 3-shingles from each session
def create_shingles(sessions, k=3):
    shingles = []
    for session in sessions:
        session_shingles = [tuple(session[i:i+k]) for i in range(len(session) - k + 1)]
        shingles.append(session_shingles)
    return shingles

# Constructing a vocabulary from the unique shingles
def create_vocabulary(shingles):
    vocab = set()
    for session in shingles:
        vocab.update(session)
    vocab = {shingle: idx for idx, shingle in enumerate(vocab)}
    return vocab

# One-hot encoding the shingles based on the vocabulary
def one_hot_encode(shingles, vocab):
    vectors = []
    for session in shingles:
        vector = np.zeros(len(vocab))
        for shingle in session:
            if shingle in vocab:
                vector[vocab[shingle]] = 1
        vectors.append(vector)
    return np.array(vectors)

# Generate MinHash signatures
def minhash(vectors, num_hashes=100):
    num_rows, num_cols = vectors.shape
    max_shingle_id = num_cols
    next_prime = 4294967311

    # Generate random hash functions
    hash_funcs = []
    for _ in range(num_hashes):
        a = random.randint(1, next_prime - 1)
        b = random.randint(0, next_prime - 1)
        hash_funcs.append((a, b))

    # Initialize the signature matrix with infinity
    signatures = np.full((num_hashes, num_rows), np.inf)

    for r in range(max_shingle_id):
        # Hash the row index using each hash function
        for i in range(num_hashes):
            a, b = hash_funcs[i]
            hash_val = (a * r + b) % next_prime
            for j in range(num_rows):
                if vectors[j, r] == 1:
                    if hash_val < signatures[i, j]:
                        signatures[i, j] = hash_val
    return signatures

# Apply LSH to the signatures
def lsh(signatures, num_bands):
    num_rows, num_cols = signatures.shape
    rows_per_band = num_rows // num_bands

    buckets = defaultdict(list)
    for band_idx in range(num_bands):
        for col_idx in range(num_cols):
            band = tuple(signatures[band_idx * rows_per_band:(band_idx + 1) * rows_per_band, col_idx])
            band_hash = (band_idx, hash(band))
            if band_hash not in buckets:
                buckets[band_hash] = []
            buckets[band_hash].append(col_idx)
    return buckets

# Identifying candidate pairs from the buckets
def find_candidate_pairs(buckets):
    candidate_pairs = set()
    for bucket in buckets.values():
        if len(bucket) > 1:
            for pair in combinations(bucket, 2):
                candidate_pairs.add(pair)
    return candidate_pairs

# Compute Dice coefficient for similarity
def dice_coefficient(set1, set2):
    intersection = len(set1 & set2)
    return 2 * intersection / (len(set1) + len(set2))

# Calculate Dice scores for candidate pairs
def calculate_dice_scores(candidate_pairs, shingles):
    scores = []
    for i, j in candidate_pairs:
        set_i = set(shingles[i])
        set_j = set(shingles[j])
        score = dice_coefficient(set_i, set_j)
        scores.append(((i, j), score))
    return scores

# Main function
if __name__ == "__main__":
    # Creating shingles of size 3 from each session
    shingles = create_shingles(sessions)
    print("Shingles:", shingles)

    # Constructing a vocabulary from the unique shingles
    vocab = create_vocabulary(shingles)
    print("Vocabulary:", vocab)

    # One-hot encoding the shingles
    vectors = one_hot_encode(shingles, vocab)
    print("One-hot encoded vectors:\n", vectors)

    # Generate MinHash signatures
    num_hashes = 100
    signatures = minhash(vectors, num_hashes=num_hashes)
    print("MinHash Signatures:\n", signatures)

    # Apply LSH to the signatures with number of bands = 10
    num_bands = 10
    buckets = lsh(signatures, num_bands)
    print("Buckets:\n", buckets)

    # Identifying candidate pairs from the buckets
    candidate_pairs = find_candidate_pairs(buckets)
    print("Candidate Pairs:", candidate_pairs)

    # Finding the Dice Score for similarity between the pairs
    dice_scores = calculate_dice_scores(candidate_pairs, shingles)
    dice_scores.sort(key=lambda x: x[1], reverse=True)

    # Printing the top 5 similar pairs of user sessions if the Dice Score is greater than 0.5
    threshold = 0.8
    top_5_similar_pairs = dice_scores[:5]
    print("Top 5 Similar Pairs of User Sessions:")
    for pair, score in top_5_similar_pairs:
        if score > threshold:
            print(f"Pair: {pair}, Score: {score}")
            session1, session2 = sessions[pair[0]], sessions[pair[1]]
            print(f"Session 1: {session1}")
            print(f"Session 2: {session2}")
            print()