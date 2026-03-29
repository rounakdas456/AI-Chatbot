import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ------------------------
# LOAD DATA
# ------------------------
df = pd.read_csv("Courses.csv")

# ------------------------
# EMBEDDINGS
# ------------------------
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings = np.array(
    df["Description"].apply(lambda x: embed_model.encode(x)).tolist()
).astype("float32")

# ------------------------
# FAISS INDEX
# ------------------------
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# ------------------------
# LLM (CORRECT PIPELINE)
# ------------------------
generator = pipeline("text2text-generation", model="google/flan-t5-base")


# ------------------------
# SEARCH FUNCTION
# ------------------------
def search(query, k=3):
    query_vec = np.array([embed_model.encode(query)]).astype("float32")
    distances, indices = index.search(query_vec, k)
    return df.iloc[indices[0]]


# ------------------------
# RECOMMEND FUNCTION
# ------------------------
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
