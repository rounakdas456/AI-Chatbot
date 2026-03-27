import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load dataset
df = pd.read_csv("C:\\Users\\rouna\\OneDrive\\Desktop\\Courses\\Courses.csv")

# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings
embeddings = np.array(
    df["Description"].apply(lambda x: embed_model.encode(x)).tolist()
).astype("float32")

# FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Correct model pipeline
generator = pipeline("text2text-generation", model="google/flan-t5-base")


# Search function
def search(query, k=3):
    query_vec = np.array([embed_model.encode(query)]).astype("float32")
    distances, indices = index.search(query_vec, k)
    return df.iloc[indices[0]]


# Recommendation function
def recommend(user_query):
    results = search(user_query)

    context = "\n".join(
        results["Course Name"] + " - " + results["Link"]
    )

    prompt = f"""
    User wants to learn: {user_query}

    Recommend top 2 courses from below:
    {context}

    Explain briefly and include links.
    """

    response = generator(prompt, max_length=200)[0]['generated_text']
    return response