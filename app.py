from __future__ import annotations

import html
import re

import pandas as pd
import streamlit as st

from learner_agent.agent import LearningAgent
from learner_agent.database import initialize_database
from learner_agent.knowledge_base import KnowledgeBase
from learner_agent.recommender import TopicRecommender
from learner_agent.seed import TOPICS


st.set_page_config(page_title="LearnLoop · Learning workspace", page_icon="🧠", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
:root { --ink:#17212f; --muted:#697586; --line:#e7ebf1; --paper:#ffffff; --canvas:#f5f7fa; --blue:#455be9; --mint:#dff6ef; }
.stApp { background:var(--canvas); color:var(--ink); font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(245,247,250,.88); }
.block-container { max-width:1280px; padding-top:2rem; padding-bottom:4rem; }
h1,h2,h3 { font-family:'Manrope',sans-serif; color:var(--ink); letter-spacing:-.035em; }
h1 { font-size:2.2rem!important; }
h2 { font-size:1.55rem!important; }
p, label, li { color:#475467; }
[data-testid="stSidebar"] { background:#fff; border-right:1px solid var(--line); }
[data-testid="stSidebar"] .block-container { padding-top:2rem; }
[data-testid="stMetric"] { background:var(--paper); border:1px solid var(--line); padding:18px 20px; border-radius:14px; box-shadow:0 2px 8px rgba(20,35,60,.025); }
[data-testid="stMetricLabel"] p { color:var(--muted); font-weight:600; }
[data-testid="stMetricValue"] { color:var(--ink); font-family:'Manrope',sans-serif; }
[data-testid="stTabs"] [role="tablist"] { gap:8px; border-bottom:1px solid var(--line); }
[data-testid="stTabs"] button[role="tab"] { padding:12px 16px; color:#667085; font-weight:600; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color:var(--blue); border-bottom:2px solid var(--blue); }
div.stButton > button { border-radius:9px; font-weight:600; min-height:42px; padding:0 18px; }
div.stButton > button[kind="primary"] { background:var(--blue); border-color:var(--blue); }
[data-testid="stProgressBar"] > div > div { background:linear-gradient(90deg,#5368ed,#45b8a0); border-radius:99px; }
[data-testid="stFileUploader"] { background:#fff; border:1px dashed #cbd3df; border-radius:13px; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
.hero { background:linear-gradient(115deg,#17253c 0%,#263d69 58%,#4059bc 100%); border-radius:20px; padding:32px 36px; color:white; margin:4px 0 24px; box-shadow:0 12px 30px rgba(26,43,82,.12); }
.hero-kicker { color:#bdc9ff; font-size:.72rem; font-weight:700; letter-spacing:.13em; text-transform:uppercase; margin-bottom:12px; }
.hero-title { color:white; font:800 1.9rem 'Manrope',sans-serif; letter-spacing:-.045em; line-height:1.2; }
.hero-copy { color:#dbe3f5; font-size:1rem; max-width:680px; margin-top:10px; line-height:1.65; }
.section-label { font-size:.72rem; color:#788395; letter-spacing:.12em; font-weight:700; text-transform:uppercase; margin:8px 0 6px; }
.topic-row { background:white; border:1px solid var(--line); border-radius:12px; padding:14px 16px 9px; margin:10px 0; }
.topic-name { font-weight:700; color:var(--ink); }
.topic-score { color:var(--muted); font-size:.9rem; }
.plan-number { display:inline-block; color:#455be9; font-weight:700; font-size:.78rem; letter-spacing:.08em; text-transform:uppercase; padding:6px 9px; background:#eef0ff; border-radius:7px; margin-bottom:10px; }
.mode-chip { display:inline-block; background:#e8f7f1; color:#24725e; border-radius:99px; padding:5px 10px; font-size:.78rem; font-weight:700; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

initialize_database()
agent = LearningAgent()
recommender = TopicRecommender(TOPICS)
if "knowledge_base" not in st.session_state:
    st.session_state["knowledge_base"] = KnowledgeBase()
knowledge_base: KnowledgeBase = st.session_state["knowledge_base"]

with st.sidebar:
    st.markdown("## LearnLoop")
    st.caption("PERSONAL LEARNING WORKSPACE")
    st.markdown("---")
    st.markdown("#### Your profile")
    learner = st.text_input("Learner name", value="Student", key="learner_name").strip() or "Student"
    st.markdown("---")
    st.markdown("#### Learning engine")
    st.caption("Your practice history informs topic mastery. A similarity model recommends what to focus on next.")
    if knowledge_base.chunks:
        st.success(f"{len({chunk.source for chunk in knowledge_base.chunks})} study file(s) ready")
    else:
        st.caption("No study notes added yet")
    st.markdown("---")
    st.caption("Zero-cost GenAI is optional: run Ollama locally. Without it, the built-in tutor still works.")

topics = list(TOPICS)
history = agent.get_history(learner)
mastery = agent.get_mastery(learner, topics)
average_mastery = sum(mastery.values()) / max(len(mastery), 1)
weakest_topic = min(mastery, key=mastery.get)

safe_name = html.escape(learner)
st.markdown(
    f'<div class="hero"><div class="hero-kicker">Your personal learning workspace</div>'
    f'<div class="hero-title">A smarter next step, {safe_name}.</div>'
    '<div class="hero-copy">LearnLoop connects your study materials, practice, and progress to help you focus on what matters next.</div></div>',
    unsafe_allow_html=True,
)

tab_home, tab_study, tab_quiz, tab_tutor, tab_materials, tab_progress = st.tabs(
    ["Overview", "Study plan", "Practice", "AI tutor", "My materials", "Progress"]
)

with tab_home:
    st.markdown('<div class="section-label">Your learning snapshot</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Topics in your path", len(topics))
    col2.metric("Practice attempts", len(history))
    col3.metric("Average mastery", f"{average_mastery:.0%}")
    col4.metric("Study materials", len({chunk.source for chunk in knowledge_base.chunks}))

    left, right = st.columns([1.4, 1], gap="large")
    with left:
        st.markdown("### Topic mastery")
        st.caption("Your scores update as you practice. Start with a topic that needs attention.")
        for topic, score in sorted(mastery.items(), key=lambda row: row[1]):
            st.markdown(
                f'<div class="topic-row"><span class="topic-name">{html.escape(topic)}</span>'
                f'<span class="topic-score" style="float:right">{score:.0%}</span></div>',
                unsafe_allow_html=True,
            )
            st.progress(int(score * 100))
    with right:
        st.markdown("### Recommended focus")
        ranked = recommender.rank(mastery)
        for rank, (topic, _score, reason) in enumerate(ranked[:3], start=1):
            with st.container(border=True):
                st.markdown(f'<div class="plan-number">Next focus · 0{rank}</div>', unsafe_allow_html=True)
                st.markdown(f"**{topic}**")
                st.caption(reason)
        st.caption(f"A good place to begin: **{weakest_topic}**")

with tab_study:
    st.markdown("### Build a focused session")
    st.caption("Choose the time you have. LearnLoop will use your topic mastery to structure a practical session.")
    controls, action = st.columns([3, 1], vertical_alignment="bottom")
    with controls:
        minutes = st.slider("Available study time", 10, 90, 30, step=5, format="%d minutes")
    with action:
        build_plan = st.button("Create my plan", type="primary", use_container_width=True)
    if build_plan:
        st.session_state["plan"] = agent.make_plan(learner, minutes, recommender)
    plan = st.session_state.get("plan", [])
    if plan:
        st.markdown("#### Your session")
        for index, item in enumerate(plan, start=1):
            with st.container(border=True):
                number_col, details_col = st.columns([1, 7])
                with number_col:
                    st.markdown(f'<div class="plan-number">STEP 0{index}</div>', unsafe_allow_html=True)
                    st.markdown(f"**{item['minutes']} min**")
                with details_col:
                    st.markdown(f"#### {item['topic']}")
                    st.caption(item["reason"])
                    objective, activity = st.columns(2)
                    objective.markdown(f"**Learning objective**  \n{item['objective']}")
                    activity.markdown(f"**Try this**  \n{item['activity']}")
    else:
        st.info("Your study plan will appear here. Start with **Create my plan**.")

with tab_quiz:
    st.markdown("### Practice a topic")
    st.caption("Short checks help LearnLoop understand what you know and shape your next study plan.")
    topic = st.selectbox("Choose a topic", topics, key="quiz_topic")
    questions = agent.get_quiz(topic)
    topic_key = re.sub(r"\W+", "_", topic.lower())
    index_key = f"quiz_index_{topic_key}"
    feedback_key = f"quiz_feedback_{topic_key}"
    if index_key not in st.session_state:
        st.session_state[index_key] = 0
    if st.button("Start over", key=f"restart_{topic_key}"):
        st.session_state[index_key] = 0
        st.session_state.pop(feedback_key, None)
        st.rerun()

    if feedback_key in st.session_state:
        correct, explanation = st.session_state[feedback_key]
        if correct:
            st.success("That's right — nice work.")
        else:
            st.warning("Not quite. Take a moment to review this explanation.")
        st.info(explanation)
        if st.button("Continue", type="primary", key=f"continue_{topic_key}"):
            st.session_state[index_key] += 1
            st.session_state.pop(feedback_key, None)
            st.rerun()
    elif st.session_state[index_key] < len(questions):
        current = st.session_state[index_key]
        question = questions[current]
        st.progress((current + 1) / len(questions), text=f"Question {current + 1} of {len(questions)}")
        with st.container(border=True):
            st.markdown(f"#### {question['question']}")
            answer = st.radio("Select one answer", question["options"], key=f"answer_{topic_key}_{current}", label_visibility="collapsed")
            if st.button("Check answer", type="primary", key=f"check_{topic_key}_{current}"):
                correct = answer == question["answer"]
                agent.record_attempt(learner, topic, correct, question["question"])
                st.session_state[feedback_key] = (correct, question["explanation"])
                st.rerun()
    else:
        st.success("Topic complete. Your practice has been added to your learning history.")
        if st.button("Practice this topic again", type="primary", key=f"again_{topic_key}"):
            st.session_state[index_key] = 0
            st.rerun()

with tab_tutor:
    st.markdown("### Ask your learning coach")
    st.caption("Ask for an explanation, example, or practice question. Add your own notes to get answers grounded in your material.")
    prompt_col, button_col = st.columns([5, 1], vertical_alignment="bottom")
    with prompt_col:
        question = st.text_area("Your question", placeholder="For example: Explain gradient descent using my notes…", height=110, label_visibility="collapsed")
    with button_col:
        ask = st.button("Ask LearnLoop", type="primary", use_container_width=True)
    if ask and question.strip():
        with st.spinner("Thinking through your question…"):
            response, mode = agent.answer(question, learner, mastery, knowledge_base)
        with st.container(border=True):
            st.markdown(response)
        st.markdown(f'<span class="mode-chip">{html.escape(mode)}</span>', unsafe_allow_html=True)
    elif ask:
        st.warning("Type a question first, and I’ll help you work through it.")
    st.markdown("**Quick prompts**")
    st.caption("Explain overfitting · Give me a Python practice problem · Why do train and test sets matter?")

with tab_materials:
    st.markdown("### Your study library")
    st.caption("Add course notes so the tutor can retrieve relevant passages. Files stay in this browser session and are not saved to the database.")
    uploads = st.file_uploader(
        "Choose study files", type=["pdf", "txt", "md"], accept_multiple_files=True,
        help="PDF, plain text, or Markdown · up to 8 MB per file",
    )
    if uploads:
        if st.button("Add to my library", type="primary"):
            existing = {chunk.source for chunk in knowledge_base.chunks}
            for uploaded in uploads:
                if uploaded.name in existing:
                    st.info(f"{uploaded.name} is already in your library.")
                    continue
                try:
                    count = knowledge_base.add_file(uploaded.name, uploaded.getvalue())
                    if count:
                        st.success(f"Added {uploaded.name} · {count} passages ready to search")
                    else:
                        st.warning(f"No readable text found in {uploaded.name}.")
                except ValueError as exc:
                    st.error(str(exc))
    sources = sorted({chunk.source for chunk in knowledge_base.chunks})
    if sources:
        st.markdown("#### Indexed files")
        for source in sources:
            with st.container(border=True):
                st.markdown(f"**{html.escape(source)}**")
                count = sum(chunk.source == source for chunk in knowledge_base.chunks)
                st.caption(f"{count} searchable passage(s)")
        if st.button("Clear my study library"):
            knowledge_base.clear()
            st.rerun()
    else:
        st.info("Your library is empty. Add your notes here, then ask the AI tutor about their content.")

with tab_progress:
    st.markdown("### Your learning progress")
    st.caption("A record of the practice that informs your recommendations.")
    if history:
        df = pd.DataFrame(history)
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%b %d, %Y · %H:%M")
        df["correct"] = df["correct"].map({1: "Correct", 0: "Needs review", True: "Correct", False: "Needs review"})
        df = df.rename(columns={"topic": "Topic", "correct": "Result", "question": "Question", "created_at": "Date"})
        st.dataframe(df[["Date", "Topic", "Question", "Result"]], use_container_width=True, hide_index=True)
    else:
        st.info("Your history will appear here after your first practice question.")
    with st.expander("Reset learner progress"):
        st.caption("This permanently deletes the quiz history for the learner name shown in the sidebar.")
        confirm_reset = st.checkbox("I understand and want to reset this learner’s progress", key="confirm_reset")
        if st.button("Reset progress", disabled=not confirm_reset):
            agent.reset(learner)
            st.session_state.pop("confirm_reset", None)
            st.rerun()
