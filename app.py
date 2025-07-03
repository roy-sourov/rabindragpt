import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import os

st.set_page_config(
    page_title="RabindraGPT - Bengali Poetry & Music Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header Banner with Tagore (left), RabindraGPT (center), Lalon (right)
    tagore_img_path = os.path.join("static", "tagore.png")
    lalon_img_path = os.path.join("static", "lalon.png")
    def img_to_base64(path):
        try:
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            return None
    tagore_b64 = img_to_base64(tagore_img_path)
    lalon_b64 = img_to_base64(lalon_img_path)
    banner_html = ''
    if tagore_b64 and lalon_b64:
        banner_html = f'''
        <div style="display: flex; align-items: center; width: 100%; height: 160px; margin-bottom: 2rem; border-radius: 18px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.10); background: #f7f3ed;">
            <img src="data:image/png;base64,{tagore_b64}" style="width: 110px; height: 110px; object-fit: cover; border-radius: 14px; margin-left: 24px; margin-right: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.10); background: #fff;" />
            <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <h1 style="font-size: 2.5rem; font-weight: bold; color: #1f77b4; margin-bottom: 0.5rem; letter-spacing: 2px;">🎵 RabindraGPT</h1>
                <p style="font-size: 1.2rem; color: #444; margin: 0;">Open Source Bengali Poetry and Music Generator</p>
            </div>
            <img src="data:image/png;base64,{lalon_b64}" style="width: 110px; height: 110px; object-fit: cover; border-radius: 14px; margin-right: 24px; margin-left: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.10); background: #fff;" />
        </div>
        '''
    else:
        banner_html = f'<h1 style="color: #b00;">RabindraGPT</h1><p>Banner images not found.</p>'
    st.markdown(banner_html, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # RabindraGPT logo at the top, always centered with equal margins
        rabindragpt_img_path = os.path.join("static", "RabindraGPT.png")
        with open(rabindragpt_img_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f'''
            <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 1.2rem;">
                <img src="data:image/png;base64,{img_base64}" style="width: 180px; max-width: 80%; display: block; margin-left: auto; margin-right: auto; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); background: #fff;" />
            </div>
        ''', unsafe_allow_html=True)
        # Mode dropdown
        st.session_state['active_mode'] = st.selectbox("Mode", ["Search", "Generate"], key="mode_select").lower()

        # Poet name dropdown for search mode
        poet_options = [
            "All",
            "Chandidas",
            "Vidyapati",
            "Michael Madhusudan Dutt",
            "Rabindranath Tagore",
            "Jibanananda Das"
        ]
        if st.session_state['active_mode'] == 'search':
            st.session_state['selected_poet'] = st.selectbox("Poet Name", poet_options, key="poet_name_select")

        if st.session_state['active_mode'] == 'generate':
            st.header("Settings")
            if 'temperature' not in st.session_state:
                st.session_state['temperature'] = 0.8
            if 'max_tokens' not in st.session_state:
                st.session_state['max_tokens'] = 500
            temperature = st.slider("Creativity Level", 0.1, 2.0, st.session_state['temperature'], key="temperature_slider_sidebar")
            max_tokens = st.slider("Max Tokens", 100, 1000, st.session_state['max_tokens'], key="max_tokens_slider_sidebar")

    # Main content area
    if 'active_mode' not in st.session_state:
        st.session_state['active_mode'] = 'search'  # default to search
    # Use only st.session_state['active_mode'] for logic
    if st.session_state['active_mode'] == 'search':
        # Poetry Search tools with additional filters
        st.subheader("Poetry Search")
        keyword = st.text_input("Keyword (Bengali or English)", "", key="poetry_search")
        selected_poet = st.session_state.get('selected_poet', 'All')
        # Mock poetry database
        poetry_db = [
            {
                "title": "আজি এ প্রভাতে রবির কর",
                "content": "আজি এ প্রভাতে রবির কর\nকেমনে পশিল প্রাণের পর?\nকেমনে পশিল হৃদয়-গহনে\nকেমনে পশিল আঁখির স্বপনে?",
                "tags": ["রবি", "আলো", "প্রভাত"],
                "poet": "Rabindranath Tagore"
            },
            {
                "title": "আমার সোনার বাংলা",
                "content": "আমার সোনার বাংলা, আমি তোমায় ভালোবাসি\nচিরদিন তোমার আকাশ, তোমার বাতাস, আমার প্রাণে বাজায় বাঁশি",
                "tags": ["বাংলা", "ভালোবাসা", "দেশ"],
                "poet": "Rabindranath Tagore"
            },
            {
                "title": "বসন্ত এসেছে",
                "content": "বসন্ত এসেছে, ফুলে ফুলে রঙ লেগেছে\nবাতাসে মধুর গন্ধে মন ভরে গেছে",
                "tags": ["বসন্ত", "ফুল", "প্রকৃতি"],
                "poet": "Jibanananda Das"
            },
            {
                "title": "Where the mind is without fear",
                "content": "Where the mind is without fear and the head is held high...",
                "tags": ["Tagore", "English", "Mind"],
                "poet": "Rabindranath Tagore"
            },
        ]
        if st.button("🔍 Search Poetry", key="do_search"):
            if keyword.strip() == "" and (selected_poet is None or selected_poet == "All"):
                st.warning("Please enter a keyword or select a poet to search.")
            else:
                # Search poems (case-insensitive, in title/content/tags/poet)
                results = []
                for poem in poetry_db:
                    poet_match = (selected_poet == "All" or (selected_poet and selected_poet.lower() in poem["poet"].lower()))
                    keyword_match = (
                        keyword.lower() in poem["title"].lower() or
                        keyword.lower() in poem["content"].lower() or
                        any(keyword.lower() in tag.lower() for tag in poem["tags"])
                    ) if keyword.strip() else True
                    if poet_match and keyword_match:
                        results.append(poem)
                if results:
                    st.success(f"Found {len(results)} matching poem(s):")
                    for poem in results:
                        with st.expander(f"{poem['title']} — {poem['poet']}"):
                            st.markdown(f'<div class="bengali-poem">{poem["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.info("No matching poems found. Try another filter!")
            
    elif st.session_state['active_mode'] == 'generate':
        # Show Generation tools (default to Poetry Generation, with options for other modes)
        st.header("📝 Poetry & Music Generation")
        gen_mode = st.radio(
            "Choose Generation Mode",
            ["Poetry Generation", "Music Generation", "Poetry + Music"],
            key="generation_mode_radio"
        )
        if gen_mode == "Poetry Generation":
            poetry_type = st.selectbox(
                "Poetry Type",
                ["Sonnet", "Ghazal", "Free Verse", "Haiku", "Custom"]
            )
            theme = st.text_input("Theme (optional)", placeholder="Nature, Love, Freedom...")
            length = st.slider("Poem Length", 4, 20, 8)
        elif gen_mode == "Music Generation":
            music_style = st.selectbox(
                "Music Style",
                ["Rabindra Sangeet", "Folk", "Classical", "Modern", "Fusion"]
            )
            duration = st.slider("Duration (seconds)", 30, 300, 120)
        elif gen_mode == "Poetry + Music":
            pass
        # Do NOT add settings sliders here (they are only in the sidebar)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Made with ❤️ for Bengali culture and literature</p>
        <p>Powered by Streamlit and AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 