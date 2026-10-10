from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TopicRecommender:
    """Content-based recommender using TF-IDF and cosine similarity."""

    def __init__(self, topics: dict):
        self.topics = topics
        self.names = list(topics)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([f"{t['objective']} {t['tags']}" for t in topics.values()])

    def rank(self, mastery: dict[str, float]) -> list[tuple[str, float, str]]:
        weak = sorted(self.names, key=lambda name: mastery.get(name, 0.0))[:2]
        profile = " ".join(f"{self.topics[name]['tags']} {self.topics[name]['objective']}" for name in weak)
        profile_vector = self.vectorizer.transform([profile])
        similarities = cosine_similarity(profile_vector, self.matrix)[0]
        ranked = []
        for idx, name in enumerate(self.names):
            weakness = 1 - mastery.get(name, 0.0)
            relevance = float(similarities[idx])
            score = 0.65 * weakness + 0.35 * relevance
            reason = f"Mastery is {mastery.get(name, 0.0):.0%}; recommendation also reflects content similarity to your current focus."
            ranked.append((name, score, reason))
        return sorted(ranked, key=lambda row: row[1], reverse=True)
