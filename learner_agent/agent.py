from __future__ import annotations

import json
import os
from urllib.error import URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

from learner_agent.database import connect, initialize_database
from learner_agent.seed import QUIZZES, TOPICS

load_dotenv()


class LearningAgent:
    """A bounded tutor workflow: assess -> recommend -> teach -> record feedback."""

    def __init__(self):
        initialize_database()

    def get_history(self, learner: str) -> list[dict]:
        with connect() as db:
            rows = db.execute("SELECT topic, correct, question, created_at FROM attempts WHERE learner=? ORDER BY id DESC LIMIT 100", (learner,)).fetchall()
        return [dict(row) for row in rows]

    def get_mastery(self, learner: str, topics: list[str]) -> dict[str, float]:
        with connect() as db:
            rows = db.execute("SELECT topic, AVG(correct) AS score FROM attempts WHERE learner=? GROUP BY topic", (learner,)).fetchall()
        observed = {row["topic"]: float(row["score"]) for row in rows}
        # Neutral cold-start prior: no evidence is treated as 50% mastery.
        return {topic: observed.get(topic, 0.5) for topic in topics}

    def make_plan(self, learner: str, minutes: int, recommender) -> list[dict]:
        mastery = self.get_mastery(learner, list(TOPICS))
        ranked = recommender.rank(mastery)
        count = max(1, min(4, minutes // 15))
        selected = ranked[:count]
        slot = max(5, minutes // count)
        return [{"topic": name, "minutes": slot, "reason": reason, "objective": TOPICS[name]["objective"], "activity": TOPICS[name]["activity"]} for name, _, reason in selected]

    def get_quiz(self, topic: str) -> list[dict]:
        return QUIZZES.get(topic, QUIZZES["Python fundamentals"])

    def record_attempt(self, learner: str, topic: str, correct: bool, question: str) -> None:
        with connect() as db:
            db.execute("INSERT INTO attempts (learner, topic, correct, question) VALUES (?, ?, ?, ?)", (learner, topic, int(correct), question))

    def answer(self, question: str, learner: str, mastery: dict[str, float], knowledge_base=None) -> tuple[str, str]:
        retrieved = knowledge_base.search(question) if knowledge_base else []
        context = "\n\n".join(
            f"[Source: {chunk.source}" + (f", page {chunk.page}" if chunk.page else "") + f"]\n{chunk.text}"
            for chunk, _score in retrieved
        )
        # Ollama serves an open model on the learner's own computer. No API key
        # or hosted inference provider is called by this project.
        if os.getenv("OLLAMA_ENABLED", "false").lower() not in {"1", "true", "yes"}:
            mode = "Local RAG tutor" if retrieved else "Built-in local tutor"
            return self._local_answer(question, retrieved), mode

        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")
        model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        weak = ", ".join(sorted(mastery, key=mastery.get)[:2])
        instructions = (
            "Use supplied study passages when relevant. Cite filename and page inline. "
            "If passages do not answer the question, say so and label any general explanation. "
            "Never invent a citation. Keep the answer concise, explain with an example, and end with one check-for-understanding question."
        )
        payload = {
            "model": model,
            "stream": False,
            "messages": [
                {"role": "system", "content": f"You are LearnLoop, a patient learning coach. {instructions}"},
                {"role": "user", "content": f"Learner: {learner}. Current focus: {weak}.\nQuestion: {question}\n\nRetrieved study material:\n{context or 'No relevant uploaded material was found.'}"},
            ],
            "options": {"temperature": 0.4},
        }
        request = Request(
            f"{base_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
            answer = result.get("message", {}).get("content", "")
            if answer.strip():
                return answer, "Local LLM + RAG" if retrieved else "Local LLM"
            return self._local_answer(question, retrieved), "Local fallback (empty model response)"
        except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            mode = "Local tutor fallback"
            if retrieved:
                mode = "Local RAG fallback"
            return self._local_answer(question, retrieved), f"{mode} · Ollama unavailable ({type(exc).__name__})"

    @staticmethod
    def _local_answer(question: str, retrieved=()) -> str:
        if retrieved:
            passages = "\n\n".join(
                f"> {chunk.text}\n\n*Source: {chunk.source}" + (f", page {chunk.page}" if chunk.page else "") + "*"
                for chunk, _score in retrieved[:2]
            )
            return f"Here are the most relevant passages from your material:\n\n{passages}\n\nUse these passages as your starting point; I can explain a specific term or ask you a practice question about them."
        q = question.lower()
        if "overfit" in q:
            return "**Overfitting** happens when a model memorizes details of its training examples instead of learning patterns that generalize. For example, a student who memorizes practice answers may struggle with a new question. Use a validation set, simpler models, or regularization to catch and reduce it. **Check:** would lower training error always mean better performance on new data?"
        if "gradient descent" in q:
            return "**Gradient descent** improves model parameters in small steps. Imagine standing on a hill: estimate the steepest downhill direction, take a step, and repeat. In training, the gradient tells us how a change in parameters affects the loss; the learning rate controls the step size. **Check:** what might happen if the learning rate is too large?"
        if "train" in q and "test" in q:
            return "A **training set** teaches the model; a separate **test set** estimates how it performs on unseen examples. If you repeatedly tune decisions using test results, the test set stops being a fair final check. **Check:** which split should you use while selecting model settings?"
        return "Try breaking this into three parts: (1) state the key idea in one sentence, (2) work through a tiny example, and (3) explain what could go wrong. I can give a more targeted answer if you mention the topic and your current level."

    def reset(self, learner: str) -> None:
        with connect() as db:
            db.execute("DELETE FROM attempts WHERE learner=?", (learner,))
