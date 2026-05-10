import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CineMind",
    layout="wide"
)

st.title("🎬 CineMind")
st.subheader("AI Scene Intelligence Engine")

st.markdown(
    """
Search movie scenes using semantic similarity and transformer embeddings.
"""
)

query = st.text_input(
    "Enter a semantic query",
    placeholder="e.g. chaos, sacrifice, emotional conflict"
)

if st.button("Search"):

    with st.spinner("Searching scenes..."):

        response = requests.get(
            f"{API_URL}/search",
            params={"query": query}
        )

        data = response.json()

        results = data["results"]

        if not results:
            st.warning("No matching scenes found.")

        for result in results:

            st.markdown("---")

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(
                    f"## 🎥 {result['movie']}"
                )

            with col2:
                st.metric(
                    "Similarity",
                    result["score"]
                )

            st.markdown(
                f"**Timestamp:** {result['timestamp']}"
            )

            st.write(result["scene"])