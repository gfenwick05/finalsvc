import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import difflib
import os

class BookRecommender:
    def __init__(self, data_path="assets/books.csv"):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Books CSV not found: {data_path}")
        self.df = pd.read_csv(data_path)
        self.df["content"] = (
            self.df["title"].fillna("") + " " +
            self.df["author"].fillna("") + " " +
            self.df["description"].fillna("")
        )
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=2000)
        self.matrix = self.vectorizer.fit_transform(self.df["content"])

    def _find_match(self, title):
        titles = self.df["title"].astype(str).tolist()
        match = difflib.get_close_matches(title, titles, n=1, cutoff=0.5)
        if match:
            return self.df.index[self.df["title"] == match[0]].tolist()[0]
        lower = self.df["title"].str.lower()
        match_idx = lower[lower.str.contains(title.lower())]
        if not match_idx.empty:
            return match_idx.index[0]
        raise ValueError("No matching title found.")

    def recommend(self, title, top_k=5):
        idx = self._find_match(title)
        sims = linear_kernel(self.matrix[idx:idx+1], self.matrix).flatten()
        sims[idx] = -1
        top = sims.argsort()[::-1][:top_k]
        return [
            {
                "title": str(self.df.loc[i, "title"]),
                "author": str(self.df.loc[i, "author"]),
                "score": float(sims[i])
            }
            for i in top
        ]
