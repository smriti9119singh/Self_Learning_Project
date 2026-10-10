# LearnLoop AI

**A zero-cost-to-run adaptive learning agent** built with Python, scikit-learn, Streamlit, SQLite, local open models, and retrieval-augmented generation (RAG).

LearnLoop helps a learner choose what to study, practice concepts, and ask questions grounded in their own notes. No paid API, hosted database, or subscription is required. The built-in learning coach and local TF-IDF retrieval work without any model download. For richer generative answers, the app can connect to Ollama running an open model on the learner's own computer. On the free hosted demo, it uses the built-in tutor because the cloud app cannot access Ollama on your personal computer.

## Cost-free architecture

- **Python libraries:** install from `requirements.txt` using pip.
- **Machine learning:** scikit-learn TF-IDF and cosine similarity run inside the app.
- **RAG:** uploaded PDF/TXT/Markdown notes are chunked and searched locally with TF-IDF.
- **GenAI:** optional Ollama local inference; requests go to `localhost`, not a paid API.
- **Persistence:** SQLite database stored with the app for local use.
- **Free public demo:** GitHub repository + Streamlit Community Cloud. Community Cloud deploys directly from GitHub and provides a `streamlit.app` URL. Cloud storage is temporary, so treat it as a demo, not durable learner storage.

## Features

- Topic mastery estimated from quiz answers.
- Explainable study-topic ranking from content similarity and learner mastery.
- Time-boxed, personalized study plans.
- Practice quizzes with feedback recorded for the next recommendation.
- Document-grounded tutor with filename and page references when relevant passages are retrieved.
- Local open-model tutor or built-in fallback.
- Learner progress dashboard and local reset control.

## Run locally at no API cost

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The app works right away with its built-in local tutor. Quiz history is stored in `data/learnloop.db`; uploaded study files stay in session memory.

### Optional: use a local GenAI model

This is optional. It uses your computer's CPU/GPU and disk space; it does not require a paid API key. Install Ollama from its official download page, then download/run a model:

```powershell
ollama run llama3.2:3b
```

Keep Ollama running, then copy `.env.example` to `.env`. The included settings enable local Ollama and select `llama3.2:3b`:

```env
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
```

If you do not want to download/run a model, leave Ollama disabled or omit `.env`; the app still works. Do not use Ollama cloud models if your goal is to avoid inference charges.

## Deploy a free public demo

The simplest zero-hosting-charge route is Streamlit Community Cloud. It deploys an app from a GitHub repository and assigns a `streamlit.app` URL. A public repository means the project source is public, so remove private notes, credentials, and personal data before pushing.

1. Create a GitHub account and a **public** repository named `learnloop-ai`.
2. In PowerShell, from this project folder, publish the files (replace `YOUR_GITHUB_NAME`):

   ```powershell
   git init
   git add .
   git commit -m "Build LearnLoop AI learning agent"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_NAME/learnloop-ai.git
   git push -u origin main
   ```

   Do not add `.env`, `.venv`, or `data/learnloop.db`; `.gitignore` excludes them.
3. Open [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
4. Choose **Create app**, select `learnloop-ai`, branch `main`, and entrypoint `app.py`, then deploy.
5. The hosted app runs its built-in coach and local document retrieval. Do not set `OLLAMA_ENABLED=true` in the cloud deployment: its `localhost` is the cloud container, not your PC.

### Important free-hosting limits

- Free hosted resources can sleep, restart, or reach resource limits.
- The app's local SQLite file on a hosted container is not durable storage; history can disappear after a restart/redeploy. Use the hosted version as a demo with non-sensitive data.
- Local Ollama inference is available when running the project on your own computer, not on the hosted demo.
- Keep the dependency list small and avoid uploading large documents to the public demo.
- A GitHub account and Streamlit Community Cloud account are required; availability or terms may change. Check the current service terms before deployment.

## Demo walkthrough

1. Review the mastery snapshot and recommended topics.
2. Complete a practice question, then build a study plan.
3. Upload a lecture PDF or Markdown note in **My materials**.
4. Ask the tutor about the note. With no model, it displays retrieved passages; with local Ollama enabled, it generates a grounded explanation.
5. Open **Progress** to inspect recorded practice.

## Architecture

```text
app.py                         Streamlit interface
learner_agent/agent.py         Adaptive workflow and local tutor
learner_agent/database.py      SQLite attempt history
learner_agent/knowledge_base.py PDF/text extraction and TF-IDF RAG
learner_agent/recommender.py   scikit-learn topic recommendation
learner_agent/seed.py          Sample curriculum and quizzes
```

## Evaluation plan

The demo curriculum is small and is not a validated learning assessment. To make a credible major-project report, compare the hybrid recommender to a mastery-only baseline with consenting learners. Measure Precision@3 against learner-selected next topics, pre/post quiz score changes, citation relevance, latency, and how often local inference falls back. Report the sample size and limitations; do not claim outcomes before measuring them.

## Resume entry

**LearnLoop AI — Adaptive, Document-Grounded Learning Agent** | Python, scikit-learn, Streamlit, SQLite, RAG, Ollama

- Built a personalized study application that estimates topic mastery from quiz evidence and ranks next topics with a TF-IDF/cosine similarity recommender.
- Implemented a local RAG pipeline that extracts and retrieves passages from learner notes and supports page-aware citations.
- Connected an open model through Ollama for local GenAI tutoring, with a no-key fallback and no paid inference dependency.
- Deployed a public demonstration using Streamlit Community Cloud and documented its storage and compute limitations.

Only claim the deployment after you publish it. Report measured results only after evaluating the system.
