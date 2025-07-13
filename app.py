import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64
import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import random

# Load environment variables
load_dotenv()

# Set favicon to tagoreV1.png for page config
favicon_path = os.path.join("static", "tagoreV1.png")
favicon_img = None
if os.path.exists(favicon_path):
    favicon_img = Image.open(favicon_path)

st.set_page_config(
    page_title="RabindraGPT - Bengali Poetry & Music Generator",
    page_icon=favicon_img if favicon_img else "🎵",
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

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in environment variables. Please create a .env file with your API key.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def gemini_generate(prompt, temperature=0.8, max_tokens=500):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content(prompt, generation_config={
        'temperature': temperature,
        'max_output_tokens': max_tokens
    })
    # Robust error handling for Gemini responses
    try:
        if hasattr(response, 'text') and response.text:
            return response.text
        # Fallback: try to extract from parts
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            return part.text
        # If finish_reason is 2 (SAFETY), show a warning
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'finish_reason') and candidate.finish_reason == 2:
                    return "⚠️ Gemini refused to generate content due to safety filters. Try a different prompt."
        return "⚠️ No response generated. Try a different prompt."
    except Exception as e:
        return f"⚠️ Error: {e}"

def main():
    # Header Banner with TagoreV1 (left), RabindraGPT (center), TagoreV2 (right)
    tagore_v1_img_path = os.path.join("static", "tagoreV1.png")
    tagore_v2_img_path = os.path.join("static", "tagoreV2.png")
    def img_to_base64(path):
        try:
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            return None
    tagore_v1_b64 = img_to_base64(tagore_v1_img_path)
    tagore_v2_b64 = img_to_base64(tagore_v2_img_path)
    banner_html = ''
    if tagore_v1_b64 and tagore_v2_b64:
        banner_html = f'''
        <div style="display: flex; align-items: center; width: 100%; height: 160px; margin-bottom: 2rem; border-radius: 18px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.30); background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);">
            <img src="data:image/png;base64,{tagore_v1_b64}" style="width: 110px; height: 110px; object-fit: cover; border-radius: 14px; margin-left: 24px; margin-right: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.25); background: #2a2a3e; border: 2px solid #3a3a4e;" />
            <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <h1 style="font-size: 2.5rem; font-weight: bold; color: #64b5f6; margin-bottom: 0.5rem; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">RabindraGPT</h1>
                <p style="font-size: 1.2rem; color: #b0bec5; margin: 0; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">Open Source Bengali Poetry and Music Generator</p>
            </div>
            <img src="data:image/png;base64,{tagore_v2_b64}" style="width: 110px; height: 110px; object-fit: cover; border-radius: 14px; margin-right: 24px; margin-left: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.25); background: #2a2a3e; border: 2px solid #3a3a4e;" />
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
                <img src="data:image/png;base64,{img_base64}" style="width: 180px; max-width: 80%; display: block; margin-left: auto; margin-right: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border: 2px solid #3a3a4e; padding: 8px;" />
            </div>
        ''', unsafe_allow_html=True)
        # Mode dropdown
        st.session_state['active_mode'] = st.selectbox("Mode", ["Search Music", "Search Poetry", "Generate"], key="mode_select").lower().replace(' ', '_')

        # Poet name dropdown for search mode
        poet_options = [
            "All",
            "Chandidas",
            "Vidyapati",
            "Michael Madhusudan Dutt",
            "Rabindranath Tagore",
            "Jibanananda Das"
        ]
        if st.session_state['active_mode'] == 'search_poetry':
            st.session_state['selected_poet'] = st.selectbox("Poet Name", poet_options, key="poet_name_select")

        if st.session_state['active_mode'] == 'generate':
            st.header("Settings")
            if 'temperature' not in st.session_state:
                st.session_state['temperature'] = 0.8
            if 'max_tokens' not in st.session_state:
                st.session_state['max_tokens'] = 500
            temperature = st.slider("Creativity Level", 0.1, 2.0, st.session_state['temperature'], key="temperature_slider_sidebar")
            max_tokens = st.slider("Max Tokens", 100, 1000, st.session_state['max_tokens'], key="max_tokens_slider_sidebar")
            
            # Music Generation Settings in Sidebar
            if 'selected_gen_mode' in st.session_state and st.session_state['selected_gen_mode'] == 'Music':
                st.markdown("---")
                st.subheader("🎼 Music Settings")
                
                # Initialize session state for music generation
                if 'music_gen_query' not in st.session_state:
                    st.session_state['music_gen_query'] = ''
                if 'music_gen_style' not in st.session_state:
                    st.session_state['music_gen_style'] = 'Rabindra Sangeet'
                if 'music_gen_raga' not in st.session_state:
                    st.session_state['music_gen_raga'] = ''
                if 'music_gen_tala' not in st.session_state:
                    st.session_state['music_gen_tala'] = ''
                
                # Music Style Selection
                music_style = st.selectbox(
                    "Music Style",
                    ["Rabindra Sangeet", "Folk", "Classical", "Modern", "Fusion"],
                    key="music_gen_style_sidebar",
                    index=["Rabindra Sangeet", "Folk", "Classical", "Modern", "Fusion"].index(st.session_state['music_gen_style']) if st.session_state['music_gen_style'] in ["Rabindra Sangeet", "Folk", "Classical", "Modern", "Fusion"] else 0
                )
                st.session_state['music_gen_style'] = music_style
                
                # Query Input
                query = st.text_input("Enter your query", value=st.session_state['music_gen_query'], placeholder="e.g. Love, Nature, Freedom...", key="music_gen_query_sidebar")
                st.session_state['music_gen_query'] = query
                
                # Raga and Tala Selection (only for Rabindra Sangeet)
                if music_style == "Rabindra Sangeet":
                    st.markdown("**রাগ এবং তাল নির্বাচন করুন:**")
                    try:
                        df = pd.read_excel("data/tagore.xlsx")
                        rag_options = [r for r in sorted(df['রাগ'].dropna().unique().tolist()) if str(r).strip() != '?' and str(r).strip() != 'nan']
                        tal_options = [t for t in sorted(df['তাল'].dropna().unique().tolist()) if str(t).strip() != '?' and str(t).strip() != 'nan']
                    except Exception:
                        rag_options, tal_options = [], []
                    
                    raga = st.selectbox("রাগ (Raga)", rag_options, key="music_gen_raga_sidebar")
                    st.session_state['music_gen_raga'] = raga
                    tala = st.selectbox("তাল (Tala)", tal_options, key="music_gen_tala_sidebar")
                    st.session_state['music_gen_tala'] = tala
                
                # Duration
                duration = st.slider("Duration (seconds)", 30, 300, 120, key="music_gen_duration_sidebar")
                st.session_state['music_gen_duration'] = duration

        # Utility to show available Gemini models in the sidebar for debugging
        # if st.checkbox('Show available Gemini models (debug)', value=False, key='show_models'):
        #     try:
        #         models = genai.list_models()
        #         st.write('Available Gemini models:')
        #         for m in models:
        #             st.write(m.name)
        #     except Exception as e:
        #         st.error(f"Error listing models: {e}")

    # Main content area
    if 'active_mode' not in st.session_state:
        st.session_state['active_mode'] = 'search_poetry'  # default to search poetry
    # Use only st.session_state['active_mode'] for logic
    if st.session_state['active_mode'] == 'search_poetry':
        # Poetry Search tools with additional filters
        st.subheader("Poetry Search")
        keyword = st.text_input("Keyword (Bengali or English)", "", key="poetry_search")
        selected_poet = st.session_state.get('selected_poet', 'All')
        # --- Poetry Search Pagination Refactor ---
        if 'poetry_search_results' not in st.session_state:
            st.session_state['poetry_search_results'] = None
        if 'poetry_total_pages' not in st.session_state:
            st.session_state['poetry_total_pages'] = 0
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 0
        if st.button("🔍 Search Poetry", key="do_search"):
            st.session_state['current_page'] = 0
            try:
                df = pd.read_excel("data/tagore.xlsx")
                if keyword.strip():
                    matches = df[df['lyrics'].str.contains(keyword, case=False, na=False)]
                else:
                    matches = df
                st.session_state['poetry_search_results'] = matches
                st.session_state['poetry_total_pages'] = (len(matches) + 19) // 20
            except Exception as e:
                st.session_state['poetry_search_results'] = None
                st.session_state['poetry_total_pages'] = 0
                st.error(f"Could not load poetry from songs.txt: {e}")
        # Show results if available
        results = st.session_state.get('poetry_search_results', None)
        total_pages = st.session_state.get('poetry_total_pages', 0)
        if results is not None and len(results) > 0:
            st.success(f"Found {len(results)} matching poem(s):")
            page_size = 20
            # --- Custom Page Navigation UI ---
            start_idx = st.session_state['current_page'] * page_size
            end_idx = min(start_idx + page_size, len(results))
            current_page_data = results.iloc[start_idx:end_idx]
            for _, row in current_page_data.iterrows():
                first_line = row['lyrics'].splitlines()[0].rstrip('।.,!?,;: ')
                def safe(val):
                    return 'অজানা' if str(val).strip() == '?' or str(val).strip() == 'nan' else val
                with st.expander(f"{first_line} - Rabindranath Tagore"):
                    st.markdown(f'<div class="bengali-poem">{row["lyrics"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    st.markdown(f"**রাগ:** {safe(row['রাগ'])}  ")
                    st.markdown(f"**তাল:** {safe(row['তাল'])}  ")
                    st.markdown(f"**রচনাকাল (বঙ্গাব্দ):** {safe(row['রচনাকাল (বঙ্গাব্দ)'])}  ")
                    st.markdown(f"**রচনাকাল (খৃষ্টাব্দ):** {safe(row['রচনাকাল (খৃষ্টাব্দ)'])}  ")
                    st.markdown(f"**স্বরলিপিকার:** {safe(row['স্বরলিপিকার'])}  ")
                    st.markdown(f"[View Original]({row['url']})")
            # --- Page Navigation at Bottom ---
            col1, col2, col3 = st.columns([2, 12, 2])
            with col1:
                if st.button("Previous", key="poetry_prev"):
                    if st.session_state['current_page'] > 0:
                        st.session_state['current_page'] -= 1
            with col2:
                st.write("")  # Empty space in the middle
            with col3:
                if st.button("Next", key="poetry_next"):
                    if st.session_state['current_page'] < total_pages-1:
                        st.session_state['current_page'] += 1
        elif results is not None:
            st.info("No matching poems found. Try another filter!")
            
    elif st.session_state['active_mode'] == 'search_music':
        # Music Search: search songs.txt, show lyrics and metadata, filter by রাগ and তাল
        st.subheader("Music Search")
        try:
            df = pd.read_excel("data/tagore.xlsx")
            rag_options = ['All'] + sorted([r for r in df['রাগ'].dropna().unique().tolist() if str(r).strip() != '?' and str(r).strip() != 'nan'])
            tal_options = ['All'] + sorted([t for t in df['তাল'].dropna().unique().tolist() if str(t).strip() != '?' and str(t).strip() != 'nan'])
        except Exception as e:
            st.error(f"Could not load music from songs.txt: {e}")
            rag_options, tal_options = ['All'], ['All']
            df = None
        keyword = st.text_input("Keyword (Bengali or English)", "", key="music_search")
        col_rag, col_tal = st.columns(2)
        with col_rag:
            selected_rag = st.selectbox("রাগ (Raga)", rag_options, key="rag_select")
        with col_tal:
            selected_tal = st.selectbox("তাল (Tala)", tal_options, key="tal_select")
        # --- Music Search Pagination Refactor ---
        if 'music_search_results' not in st.session_state:
            st.session_state['music_search_results'] = None
        if 'music_total_pages' not in st.session_state:
            st.session_state['music_total_pages'] = 0
        if 'current_page_music' not in st.session_state:
            st.session_state['current_page_music'] = 0
        if st.button("Search Music", key="do_search_music"):
            st.session_state['current_page_music'] = 0
            try:
                if df is not None:
                    filtered = df
                    if keyword.strip():
                        filtered = filtered[filtered['lyrics'].str.contains(keyword, case=False, na=False)]
                    if selected_rag != 'All':
                        filtered = filtered[filtered['রাগ'] == selected_rag]
                    if selected_tal != 'All':
                        filtered = filtered[filtered['তাল'] == selected_tal]
                    st.session_state['music_search_results'] = filtered
                    st.session_state['music_total_pages'] = (len(filtered) + 19) // 20
                else:
                    st.session_state['music_search_results'] = None
                    st.session_state['music_total_pages'] = 0
            except Exception as e:
                st.session_state['music_search_results'] = None
                st.session_state['music_total_pages'] = 0
                st.error(f"Could not load music from songs.txt: {e}")
        # Show results if available
        results = st.session_state.get('music_search_results', None)
        total_pages = st.session_state.get('music_total_pages', 0)
        if results is not None and len(results) > 0:
            st.success(f"Found {len(results)} matches!")
            page_size = 20
            # --- Custom Page Navigation UI ---
            start_idx = st.session_state['current_page_music'] * page_size
            end_idx = min(start_idx + page_size, len(results))
            current_page_data = results.iloc[start_idx:end_idx]
            # Accordion behavior: only one expander open at a time
            if 'music_expander_open' not in st.session_state:
                st.session_state['music_expander_open'] = None
            for idx, (_, row) in enumerate(current_page_data.iterrows()):
                lyrics = row['lyrics']
                if not isinstance(lyrics, str) or not lyrics.strip():
                    continue  # Skip rows with missing or invalid lyrics
                first_line = lyrics.splitlines()[0].rstrip('।.,!?,;: ')
                if first_line.strip().lower() == 'youtube_url':
                    continue  # Skip header or malformed row
                def safe(val):
                    return 'অজানা' if str(val).strip() == '?' or str(val).strip() == 'nan' else val
                exp_key = f"music_expander_{start_idx + idx}"
                expanded = st.session_state['music_expander_open'] == exp_key
                exp = st.expander(f"{first_line} - Rabindranath Tagore", expanded=expanded)
                with exp:
                    # If this expander is opened, set it as the open one
                    if expanded is False and st.session_state['music_expander_open'] != exp_key:
                        st.session_state['music_expander_open'] = exp_key
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        # Ensure lyrics is a string and not a list (which would add commas)
                        if isinstance(lyrics, list):
                            lyrics_str = '\n'.join(lyrics)
                        else:
                            lyrics_str = str(lyrics)
                        # Remove only one trailing comma from each line
                        lines = lyrics_str.split('\n')
                        cleaned_lines = []
                        for line in lines:
                            if line.strip().endswith(','):
                                # Remove only one comma from the end
                                cleaned_lines.append(line[:-1] if line.endswith(',') else line)
                            else:
                                cleaned_lines.append(line)
                        lyrics_str = '\n'.join(cleaned_lines)
                        st.markdown(f'<div class="bengali-poem">{lyrics_str.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    with col2:
                        video_url = str(row.get('youtube_url', '')).strip() if 'youtube_url' in row else ''
                        if not video_url or video_url.lower() == 'nan' or not video_url.startswith('http'):
                            video_url = "https://www.youtube.com/watch?v=b8JbxVDzB-k&t=942s"
                        st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)
                        st.video(video_url, format="video/mp4", start_time=0)
                        st.markdown("""
                        <style>
                        .video-wrapper iframe {
                            min-width: 800px !important;
                            min-height: 450px !important;
                            width: 100% !important;
                            height: 450px !important;
                            max-width: 100% !important;
                            margin: 24px 24px 24px 0 !important;
                            border-radius: 12px;
                            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
                        }
                        </style>
                        </div>
                        """, unsafe_allow_html=True)
                    # Horizontal line below both columns
                    st.markdown('---')
                    # Metadata below the line, left-aligned
                    metadata_line = (
                        f"**রাগ:** {safe(row['রাগ'])} &nbsp;|&nbsp; "
                        f"**তাল:** {safe(row['তাল'])} &nbsp;|&nbsp; "
                        f"**রচনাকাল (বঙ্গাব্দ):** {safe(row['রচনাকাল (বঙ্গাব্দ)'])} &nbsp;|&nbsp; "
                        f"**রচনাকাল (খৃষ্টাব্দ):** {safe(row['রচনাকাল (খৃষ্টাব্দ)'])} &nbsp;|&nbsp; "
                        f"**স্বরলিপিকার:** {safe(row['স্বরলিপিকার'])}"
                    )
                    st.markdown(f'<span style=\"font-size: 0.92rem; color: #b0bec5;\">{metadata_line}</span>', unsafe_allow_html=True)
                    st.markdown(f"[View Original]({row['url']})")
                # If this expander is closed, clear the open state
                if not exp.expanded and st.session_state['music_expander_open'] == exp_key:
                    st.session_state['music_expander_open'] = None
            # --- Page Navigation at Bottom ---
            col1, col2, col3 = st.columns([2, 12, 2])
            with col1:
                if st.button("Previous", key="music_prev"):
                    if st.session_state['current_page_music'] > 0:
                        st.session_state['current_page_music'] -= 1
            with col2:
                st.write("")  # Empty space in the middle
            with col3:
                if st.button("Next", key="music_next"):
                    if st.session_state['current_page_music'] < total_pages-1:
                        st.session_state['current_page_music'] += 1
        elif results is not None:
            st.info("No matching songs found. Try another filter!")
    elif st.session_state['active_mode'] == 'generate':
        # Create clickable buttons for generation modes
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #64b5f6; margin-bottom: 1rem;">Choose Your Creative Mode</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Poetry Generation", key="poetry_button", use_container_width=True):
                st.session_state['selected_gen_mode'] = 'Poetry'
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                        border-radius: 15px; padding: 1.5rem; margin: 1rem 0; 
                        border: 2px solid #3a3a4e; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                <p style="color: #b0bec5; font-size: 0.9rem; text-align: center; margin: 0;">Create beautiful Bengali poetry in various styles</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            if st.button("🎼 Music Generation", key="music_button", use_container_width=True):
                st.session_state['selected_gen_mode'] = 'Music'
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                        border-radius: 15px; padding: 1.5rem; margin: 1rem 0; 
                        border: 2px solid #3a3a4e; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                <p style="color: #b0bec5; font-size: 0.9rem; text-align: center; margin: 0;">Compose Bengali music lyrics and melodies</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show generation UI based on selected mode
        if 'selected_gen_mode' in st.session_state:
            gen_mode = st.session_state['selected_gen_mode']
            
            # Add a back button
            if st.button("← Back to Mode Selection", key="back_button"):
                del st.session_state['selected_gen_mode']
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            result = None
            if gen_mode == "Poetry":
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                            border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                            border: 1px solid #3a3a4e;">
                    <h4 style="color: #64b5f6; margin-bottom: 1rem;">📝 Poetry Settings</h4>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    poetry_type = st.selectbox(
                        "Poetry Type",
                        ["Sonnet", "Ghazal", "Free Verse", "Haiku", "Custom"]
                    )
                    query = st.text_input("Enter your query", placeholder="e.g. Love, Nature, Freedom...")
                with col2:
                    length = st.slider("Poem Length", 4, 20, 8)
                    if st.button("🎵 Generate Poetry", key="do_generate_poetry", use_container_width=True):
                        with st.spinner("✨ Generating poetry with Gemini..."):
                            prompt = f"Generate a Bengali poetry on theme: {query if query else 'Any'} of length {length} lines. Type: {poetry_type}."
                            result = gemini_generate(prompt, st.session_state['temperature'], st.session_state['max_tokens'])
                
                if result:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); 
                                border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                                border: 1px solid #3a3a4e;">
                        <h4 style="color: #64b5f6; margin-bottom: 1rem;">✨ Generated Poetry</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f'<div class="bengali-poem">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            elif gen_mode == "Music":
                st.markdown("""
                <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                            border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                            border: 1px solid #3a3a4e;">
                    <h4 style="color: #64b5f6; margin-bottom: 1rem;">🎼 Music Generation</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("Configure your music settings in the sidebar, then click the generate button below.")
                
                # Generate Button in main area
                if st.button("🎼 Generate Music Lyrics", key="do_generate_music", use_container_width=True):
                    with st.spinner("🎵 Generating music lyrics with Gemini..."):
                        music_style = st.session_state.get('music_gen_style', 'Rabindra Sangeet')
                        duration = st.session_state.get('music_gen_duration', 120)
                        if music_style == "Rabindra Sangeet" and st.session_state.get('music_gen_raga') and st.session_state.get('music_gen_tala'):
                            try:
                                df = pd.read_excel("data/tagore.xlsx")
                                filtered = df[(df['রাগ'] == st.session_state['music_gen_raga']) & (df['তাল'] == st.session_state['music_gen_tala'])]
                                if not filtered.empty:
                                    ref_row = filtered.sample(1).iloc[0]
                                    ref_lyrics = ref_row['lyrics']
                                    prompt = f"Write a Bengali song similar to the following, using raga: {st.session_state['music_gen_raga']} and tala: {st.session_state['music_gen_tala']}. Reference lyrics: {ref_lyrics}"
                                else:
                                    st.warning(f"No matching Rabindra Sangeet found for রাগ: {st.session_state['music_gen_raga']} and তাল: {st.session_state['music_gen_tala']}.")
                                    prompt = None
                            except Exception as e:
                                st.warning(f"Error loading songs.txt: {e}")
                                prompt = None
                        else:
                            prompt = f"Generate Bengali music lyrics in style: {music_style} on theme: {st.session_state.get('music_gen_query', 'Any')} of length suitable for {duration} seconds."
                        result = gemini_generate(prompt, st.session_state['temperature'], st.session_state['max_tokens']) if prompt else None
                
                if result:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); 
                                border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                                border: 1px solid #3a3a4e;">
                        <h4 style="color: #64b5f6; margin-bottom: 1rem;">🎵 Generated Music Lyrics</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f'<div class="bengali-poem">{result.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Made with ❤️ for Bengali culture and literature</p>
        <p>Powered by Sourov Roy and Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 