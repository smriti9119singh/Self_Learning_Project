"""Small, local retrieval layer for learner supplied study material."""
from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import PurePath

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Chunk:
    source: str
    page: int | None
    text: str


class KnowledgeBase:
    """Extract, chunk, and retrieve relevant passages with TF-IDF similarity."""

    MAX_BYTES = 8 * 1024 * 1024

    def __init__(self, chunk_size: int = 900, overlap: int = 140):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks: list[Chunk] = []
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix = None

    def add_file(self, name: str, content: bytes) -> int:
        if len(content) > self.MAX_BYTES:
            raise ValueError("Each file must be smaller than 8 MB.")
        suffix = PurePath(name).suffix.lower()
        if suffix == ".pdf":
            try:
                from pypdf import PdfReader
                reader = PdfReader(BytesIO(content))
                pages = [(index + 1, page.extract_text() or "") for index, page in enumerate(reader.pages)]
            except Exception as exc:
                raise ValueError(f"Could not read {name} as a PDF: {exc}") from exc
        elif suffix in {".txt", ".md"}:
            pages = [(None, content.decode("utf-8", errors="replace"))]
        else:
            raise ValueError("Supported file types: PDF, TXT, and Markdown.")

        before = len(self.chunks)
        for page, text in pages:
            for part in self._split(text):
                if part.strip():
                    self.chunks.append(Chunk(name, page, part.strip()))
        self._rebuild()
        return len(self.chunks) - before

    def _split(self, text: str):
        words = text.split()
        step = max(1, self.chunk_size - self.overlap)
        for start in range(0, len(words), step):
            section = words[start:start + self.chunk_size]
            if section:
                yield " ".join(section)

    def _rebuild(self) -> None:
        if not self.chunks:
            self._vectorizer, self._matrix = None, None
            return
        self._vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=20_000)
        self._matrix = self._vectorizer.fit_transform([chunk.text for chunk in self.chunks])

    def search(self, query: str, limit: int = 4) -> list[tuple[Chunk, float]]:
        if not self.chunks or not query.strip():
            return []
        query_vector = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self._matrix)[0]
        indices = scores.argsort()[::-1]
        return [(self.chunks[index], float(scores[index])) for index in indices[:limit] if scores[index] > 0]

    def clear(self) -> None:
        self.chunks.clear()
        self._rebuild()
