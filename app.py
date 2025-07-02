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
        st.header("🎛️ Controls")
        st.markdown("---")
        
        # Mode selection
        mode = st.selectbox(
            "Choose Generation Mode",
            ["Poetry Generation", "Music Generation", "Poetry + Music", "Poetry Search", "Settings"]
        )
        
        if mode == "Poetry Generation":
            poetry_type = st.selectbox(
                "Poetry Type",
                ["Sonnet", "Ghazal", "Free Verse", "Haiku", "Custom"]
            )
            
            theme = st.text_input("Theme (optional)", placeholder="Nature, Love, Freedom...")
            
            length = st.slider("Poem Length", 4, 20, 8)
            
        elif mode == "Music Generation":
            music_style = st.selectbox(
                "Music Style",
                ["Rabindra Sangeet", "Folk", "Classical", "Modern", "Fusion"]
            )
            
            duration = st.slider("Duration (seconds)", 30, 300, 120)
            
        elif mode == "Settings":
            st.subheader("⚙️ Configuration")
            temperature = st.slider("Creativity Level", 0.1, 2.0, 0.8)
            max_tokens = st.slider("Max Tokens", 100, 1000, 500)
            
    # Main content area
    if mode == "Poetry Generation":
        st.header("📝 Poetry Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Generated Poetry")
            
            # Placeholder for generated poetry
            if st.button("🎭 Generate Poetry", type="primary"):
                with st.spinner("Creating beautiful poetry..."):
                    # Placeholder content
                    st.success("Poetry generated successfully!")
                    st.markdown("""
                    **Sample Generated Poem:**
                    
                    *সকালের আলোয় জেগে উঠে*
                    *নতুন দিনের স্বপ্ন নিয়ে*
                    *বাংলার মাটিতে বাঙালির হৃদয়*
                    *গান গায় প্রাণের সুরে*
                    """)
        
        with col2:
            st.subheader("📊 Statistics")
            st.metric("Poems Generated", "1,234")
            st.metric("Total Words", "5,678")
            st.metric("Avg. Rating", "4.2 ⭐")
            
    elif mode == "Music Generation":
        st.header("🎼 Music Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Generated Music")
            
            if st.button("🎵 Generate Music", type="primary"):
                with st.spinner("Composing beautiful music..."):
                    st.success("Music generated successfully!")
                    st.audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.wav", format="audio/wav")
        
        with col2:
            st.subheader("🎵 Music Info")
            st.write("**Style:** Rabindra Sangeet")
            st.write("**Duration:** 2:30")
            st.write("**Key:** C Major")
            st.write("**Tempo:** 80 BPM")
            
    elif mode == "Poetry + Music":
        st.header("🎭 Poetry + Music Fusion")
        
        st.info("Generate poetry and music together for a complete artistic experience!")
        
        if st.button("🎨 Generate Fusion", type="primary"):
            with st.spinner("Creating artistic fusion..."):
                st.success("Fusion generated successfully!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Generated Poetry")
                    st.markdown("""
                    *মেঘের কোলে রোদ*
                    *বৃষ্টির পরে ফুল*
                    *জীবনের গল্প*
                    *হৃদয়ের সুর*
                    """)
                
                with col2:
                    st.subheader("Generated Music")
                    st.audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.wav", format="audio/wav")
                    
    elif mode == "Poetry Search":
        st.header("🔎 Bengali Poetry Search Catalogue")
        st.markdown("Search for Bengali poems by keyword. Enter a word or phrase (in Bengali or English) and discover matching poetry from our collection.")

        # Custom CSS for Bengali font
        st.markdown("""
        <style>
        .bengali-poem {
            font-family: 'Noto Serif Bengali', 'SolaimanLipi', 'Bangla', serif;
            font-size: 1.2rem;
            color: #222;
            background: #f9f6f2;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        </style>
        """, unsafe_allow_html=True)

        # Mock poetry database
        poetry_db = [
            {
                "title": "আজি এ প্রভাতে রবির কর",
                "content": "আজি এ প্রভাতে রবির কর\nকেমনে পশিল প্রাণের পর?\nকেমনে পশিল হৃদয়-গহনে\nকেমনে পশিল আঁখির স্বপনে?",
                "tags": ["রবি", "আলো", "প্রভাত"]
            },
            {
                "title": "আমার সোনার বাংলা",
                "content": "আমার সোনার বাংলা, আমি তোমায় ভালোবাসি\nচিরদিন তোমার আকাশ, তোমার বাতাস, আমার প্রাণে বাজায় বাঁশি",
                "tags": ["বাংলা", "ভালোবাসা", "দেশ"]
            },
            {
                "title": "বসন্ত এসেছে",
                "content": "বসন্ত এসেছে, ফুলে ফুলে রঙ লেগেছে\nবাতাসে মধুর গন্ধে মন ভরে গেছে",
                "tags": ["বসন্ত", "ফুল", "প্রকৃতি"]
            },
            {
                "title": "Where the mind is without fear",
                "content": "Where the mind is without fear and the head is held high...",
                "tags": ["Tagore", "English", "Mind"]
            },
        ]

        # Search input
        keyword = st.text_input("Enter poetry keyword (Bengali or English)", "", key="poetry_search")
        if st.button("🔍 Search Poetry"):
            if keyword.strip() == "":
                st.warning("Please enter a keyword to search.")
            else:
                # Search poems (case-insensitive, in title/content/tags)
                results = []
                for poem in poetry_db:
                    if (keyword.lower() in poem["title"].lower() or
                        keyword.lower() in poem["content"].lower() or
                        any(keyword.lower() in tag.lower() for tag in poem["tags"])):
                        results.append(poem)
                if results:
                    st.success(f"Found {len(results)} matching poem(s):")
                    for poem in results:
                        with st.expander(poem["title"]):
                            st.markdown(f'<div class="bengali-poem">{poem["content"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                else:
                    st.info("No matching poems found. Try another keyword!")
            
    elif mode == "Settings":
        st.header("⚙️ Application Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Model Settings")
            st.write(f"**Temperature:** {temperature}")
            st.write(f"**Max Tokens:** {max_tokens}")
            
        with col2:
            st.subheader("User Preferences")
            language = st.selectbox("Preferred Language", ["Bengali", "English", "Both"])
            save_history = st.checkbox("Save Generation History", value=True)
            
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