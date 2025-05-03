# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

from backend import process_text
from database import init_db, fetch_comments

# ─── Initialization ───────────────────────────────────────────────────────────
init_db()
st.set_page_config(
    page_title="Sentiment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔍 Sentiment Dashboard")
    st.write("Enter text below to analyze its sentiment.")
    st.markdown("---")
    # color palette selector
    palette = st.selectbox(
        "Choose color palette",
        ["Plotly", "Viridis", "Cividis", "Plasma", "Rainbow"]
    )

# ─── Main UI ──────────────────────────────────────────────────────────────────
st.header("💬 Give Your Comment")
user_input = st.text_area(
    "Share your thoughts here…",
    placeholder="Type or paste text and click **Submit**",
    height=120
)
if st.button("Submit"):
    if user_input.strip():
        sentiment, score = process_text(user_input)
        st.success(f"**{sentiment}** (Confidence: {score:.2f})")
    else:
        st.warning("Please enter some text first.")

# ─── Fetch & Prepare Data ────────────────────────────────────────────────────
data = fetch_comments()
if data:
    df = pd.DataFrame(
        data,
        columns=["ID", "Text", "Sentiment", "Score", "Timestamp"]
    )
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df_recent = df.sort_values("ID", ascending=False).head(50)

    # ─── Data Table ────────────────────────────────────────────────────────────
    st.subheader("📄 Recent Comments")
    st.dataframe(
        df_recent[["Text", "Sentiment", "Score", "Timestamp"]],
        use_container_width=True,
        hide_index=True
    )

    # ─── Charts ────────────────────────────────────────────────────────────────
    st.subheader("📈 Sentiment Trends")

    # 1) Bar: sentiment counts
    counts = df["Sentiment"].value_counts().reset_index()
    counts.columns = ["Sentiment", "Count"]
    fig1 = px.bar(
        counts, x="Sentiment", y="Count",
        title="Sentiment Distribution",
        color="Sentiment", 
        color_discrete_sequence=px.colors.qualitative.__dict__[palette]
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 2) Pie: percentage share
    fig2 = px.pie(
        counts, names="Sentiment", values="Count",
        title="Sentiment Share",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.__dict__[palette]
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3) Line: score over time (daily avg)
    daily = df.resample('D', on='Timestamp').mean(numeric_only=True).reset_index()
    fig3 = px.line(
        daily, x="Timestamp", y="Score",
        title="Average Confidence Over Time",
        markers=True,
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # 4) Scatter: sentiment timeline
    fig4 = px.strip(
        df, x="Timestamp", y="Sentiment",
        title="Sentiment Over Time",
        color="Sentiment",
        color_discrete_sequence=px.colors.qualitative.__dict__[palette]
    )
    st.plotly_chart(fig4, use_container_width=True)

else:
    st.info("No comments yet — submit one above!")
