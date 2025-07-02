import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="RabindraGPT - Bengali Poetry & Music Generator",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
    # Header
    st.markdown('<h1 class="main-header">🎵 RabindraGPT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Open Source Bengali Poetry and Music Generator</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        st.markdown("---")
        
        # Mode selection
        mode = st.selectbox(
            "Choose Generation Mode",
            ["Poetry Generation", "Music Generation", "Poetry + Music", "Settings"]
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