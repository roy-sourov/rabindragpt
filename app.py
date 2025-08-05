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
import re

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

def load_tagore_songs_data():
    """Load Rabindranath Tagore's songs data from pickle file or Google Drive if pickle doesn't exist"""
    pickle_path = "songs/tagore.pkl"
    
    # Try to load from pickle first
    if os.path.exists(pickle_path):
        try:
            df = pd.read_pickle(pickle_path)
            return df
        except Exception as e:
            st.warning(f"Could not load from pickle: {e}")
    
    # If pickle doesn't exist or fails, load from Google Drive and create pickle
    try:
        sheet_id = "14usErsJJZU82Thx1Jl4D93cTPyN0ea8Mq7nsYzgtZP4"
        gid = "0"  # Tagore sheet gid
        
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        
        df = pd.read_csv(csv_url)
        
        # Save to pickle for future use
        try:
            os.makedirs("songs", exist_ok=True)
            df.to_pickle(pickle_path)
            st.success("✅ Tagore songs data loaded from Google Drive and saved locally")
        except Exception as e:
            st.warning(f"Could not save pickle: {e}")
        
        return df
    except Exception as e:
        st.error(f"Could not load Tagore songs from Google Drive: {e}")
        return pd.DataFrame()

def load_dwijendralal_songs_data():
    """Load Dwijendralal Ray's songs data from Google Drive"""
    pickle_path = "songs/dwijendralal.pkl"
    
    # Try to load from pickle first
    if os.path.exists(pickle_path):
        try:
            df = pd.read_pickle(pickle_path)
            return df
        except Exception as e:
            st.warning(f"Could not load from pickle: {e}")
    
    # If pickle doesn't exist or fails, load from Google Drive and create pickle
    try:
        sheet_id = "14usErsJJZU82Thx1Jl4D93cTPyN0ea8Mq7nsYzgtZP4"
        gid = "491922462"  # Dwijendralal Ray sheet gid
        
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        
        df = pd.read_csv(csv_url)
        
        # Save to pickle for future use
        try:
            os.makedirs("songs", exist_ok=True)
            df.to_pickle(pickle_path)
            st.success("✅ Dwijendralal Ray songs data loaded from Google Drive and saved locally")
        except Exception as e:
            st.warning(f"Could not save pickle: {e}")
        
        return df
    except Exception as e:
        st.error(f"Could not load Dwijendralal Ray songs from Google Drive: {e}")
        return pd.DataFrame()

def load_atulprasad_songs_data():
    """Load Atulprasad Sen's songs data from Google Drive"""
    pickle_path = "songs/atulprasad.pkl"
    
    # Try to load from pickle first
    if os.path.exists(pickle_path):
        try:
            df = pd.read_pickle(pickle_path)
            return df
        except Exception as e:
            st.warning(f"Could not load from pickle: {e}")
    
    # If pickle doesn't exist or fails, load from Google Drive and create pickle
    try:
        sheet_id = "14usErsJJZU82Thx1Jl4D93cTPyN0ea8Mq7nsYzgtZP4"
        gid = "1890029073"  # Atulprasad Sen sheet gid
        
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
        
        df = pd.read_csv(csv_url)
        
        # Save to pickle for future use
        try:
            os.makedirs("songs", exist_ok=True)
            df.to_pickle(pickle_path)
            st.success("✅ Atulprasad Sen songs data loaded from Google Drive and saved locally")
        except Exception as e:
            st.warning(f"Could not save pickle: {e}")
        
        return df
    except Exception as e:
        st.error(f"Could not load Atulprasad Sen songs from Google Drive: {e}")
        return pd.DataFrame()

def load_combined_songs_data(selected_lyricist):
    """Load songs data based on selected lyricist"""
    if selected_lyricist == "All":
        # Load all lyricists' data
        tagore_df = load_tagore_songs_data()
        dwijendralal_df = load_dwijendralal_songs_data()
        atulprasad_df = load_atulprasad_songs_data()
        
        # Add lyricist column to each dataframe
        if not tagore_df.empty:
            tagore_df['lyricist'] = 'Rabindranath Tagore'
        if not dwijendralal_df.empty:
            dwijendralal_df['lyricist'] = 'Dwijendralal Ray'
        if not atulprasad_df.empty:
            atulprasad_df['lyricist'] = 'Atulprasad Sen'
        
        # Combine all dataframes
        dataframes = []
        if not tagore_df.empty:
            dataframes.append(tagore_df)
        if not dwijendralal_df.empty:
            dataframes.append(dwijendralal_df)
        if not atulprasad_df.empty:
            dataframes.append(atulprasad_df)
        
        if dataframes:
            combined_df = pd.concat(dataframes, ignore_index=True)
            return combined_df
        else:
            return pd.DataFrame()
    elif selected_lyricist == "Rabindranath Tagore":
        df = load_tagore_songs_data()
        if not df.empty:
            df['lyricist'] = 'Rabindranath Tagore'
        return df
    elif selected_lyricist == "Dwijendralal Ray":
        df = load_dwijendralal_songs_data()
        if not df.empty:
            df['lyricist'] = 'Dwijendralal Ray'
        return df
    elif selected_lyricist == "Atulprasad Sen":
        df = load_atulprasad_songs_data()
        if not df.empty:
            df['lyricist'] = 'Atulprasad Sen'
        return df
    else:
        # For other lyricists, return empty dataframe for now
        return pd.DataFrame()

def load_dictionary_data():
    """Load dictionary data from Google Sheet"""
    try:
        sheet_id = "1WCkGF8wzS3YVACJC9YleFHEkx5K0XGmFja4xteFs2hw"
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(csv_url)
        return df
    except Exception as e:
        st.error(f"Could not load dictionary data: {e}")
        return pd.DataFrame()

def find_suffix_matches(query_word, tokens_df, top_n=20):
    """Find tokens with longest suffix match to the query word"""
    if query_word.strip() == "":
        return []
    
    matches = []
    query_word = query_word.strip()
    
    for _, row in tokens_df.iterrows():
        token = str(row['token']).strip()
        if token == "" or token == "nan":
            continue
            
        # Find the longest common suffix
        max_suffix_length = 0
        for i in range(1, min(len(query_word), len(token)) + 1):
            if query_word[-i:] == token[-i:]:
                max_suffix_length = i
            else:
                break
        
        if max_suffix_length > 0:
            matches.append({
                'token': token,
                'token_length': row['token_length'],
                'suffix_length': max_suffix_length,
                'suffix': token[-max_suffix_length:]
            })
    
    # Sort by suffix length (longest first), then by token length
    matches.sort(key=lambda x: (x['suffix_length'], x['token_length']), reverse=True)
    
    return matches[:top_n]

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
    # Header Banner with RabindraGPT (center only)
    banner_html = '''
        <div style="display: flex; align-items: center; width: 100%; height: 180px; margin-bottom: 2rem; border-radius: 18px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.30); background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);">
            <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <h1 style="font-size: 2.5rem; font-weight: bold; color: #64b5f6; margin-bottom: 0.5rem; letter-spacing: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">RabindraGPT</h1>
            </div>
        </div>
        '''
    st.markdown(banner_html, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # TagoreV1 image at the top, always centered with equal margins
        tagore_v1_img_path = os.path.join("static", "tagoreV1.png")
        def img_to_base64(path):
            try:
                with open(path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            except Exception:
                return None
        tagore_v1_b64 = img_to_base64(tagore_v1_img_path)
        if tagore_v1_b64:
            st.markdown(f'''
                <div style="display: flex; justify-content: center; align-items: center; width: 100%; margin-bottom: 1.2rem;">
                        <img src="data:image/png;base64,{tagore_v1_b64}" style="width: 180px; max-width: 80%; display: block; margin-left: auto; margin-right: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.25); background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border: 2px solid #3a3a4e; padding: 8px;" />
                </div>
            ''', unsafe_allow_html=True)
        # Remove Admin Portal from the mode dropdown
        st.session_state['active_mode'] = st.selectbox("Mode", ["Search Music", "Search Poetry", "Generate", "Read Blog", "Dictionary"], key="mode_select").lower().replace(' ', '_')

        # Poet name dropdown for search mode
        poet_options = [
            "All",
            "Chandidas",
            "Vidyapati",
            "Michael Madhusudan Dutt",
            "Rabindranath Tagore",
            "Jibanananda Das"
        ]
        
        # Lyricist name dropdown for search mode
        lyricist_options = [
            "All",
            "Rabindranath Tagore",
            "Dwijendralal Ray",
            "Atulprasad Sen",
            "Rajnikant Sen",
            "Kazi Nazrul Islam",
            "Salil Chowdhury",
            "Hemanta Mukhopadhyay"
        ]
        
        if st.session_state['active_mode'] == 'search_poetry':
            st.session_state['selected_poet'] = st.selectbox("Poet Name", poet_options, key="poet_name_select")

        if st.session_state['active_mode'] == 'search_music':
            st.session_state['selected_lyricist'] = st.selectbox("Lyricist Name", lyricist_options, key="lyricist_name_select")

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
                        df = load_tagore_songs_data()
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


        
        # Place Access Level dropdown at the absolute bottom of the sidebar
        access_level_placeholder = st.sidebar.empty()
        with access_level_placeholder:
            st.markdown("<hr style='margin:1rem 0;'>", unsafe_allow_html=True)
            if 'access_level' not in st.session_state:
                st.session_state['access_level'] = 'User'
            access_level = st.selectbox('Access Level', ['User', 'Admin'], key='access_level_select', index=0 if st.session_state['access_level'] == 'User' else 1)
            if access_level != st.session_state['access_level']:
                st.session_state['access_level'] = access_level
                if access_level == 'User':
                    st.session_state['show_admin_portal'] = False
                    st.session_state['admin_logged_in'] = False
                else:
                    st.session_state['show_admin_portal'] = True
        # Keep show_admin_portal in sync with access_level
        if st.session_state['access_level'] == 'Admin':
            st.session_state['show_admin_portal'] = True
        else:
            st.session_state['show_admin_portal'] = False

    # Main content area
    if 'active_mode' not in st.session_state:
        st.session_state['active_mode'] = 'search_poetry'  # default to search poetry
    # Use only st.session_state['active_mode'] for logic

    # Show admin login form as a modal or at the top of main area if admin portal is triggered
    if st.session_state.get('show_admin_portal', False) and not st.session_state.get('admin_logged_in', False):
        st.subheader("Admin Portal Login")
        with st.form("admin_login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if username == "sourovroy" and password == "SourovBairagi@1998":
                    st.session_state['admin_logged_in'] = True
                    st.success("Logged in as admin!")
                else:
                    st.error("Invalid credentials.")
        st.stop()

    if st.session_state.get('admin_logged_in', False):
        st.subheader("Edit YouTube Links (Admin)")
        try:
            df = load_tagore_songs_data()
        except Exception as e:
            st.error(f"Could not load songs: {e}")
            df = None
        if df is not None:
            for idx, row in df.iterrows():
                # Determine if YouTube link is missing
                current_url = row.get('youtube_url', '') if 'youtube_url' in row else ''
                url_missing = not current_url or str(current_url).lower() == 'nan' or not str(current_url).startswith('http')
                expander_label = f"ID#{idx}"
                if url_missing:
                    expander_label = f"🟠 {expander_label} (No YouTube Link)"
                with st.expander(expander_label):
                    # Show lyrics above the YouTube URL
                    lyrics = row.get('lyrics', '')
                    if isinstance(lyrics, list):
                        lyrics_str = '\n'.join(lyrics)
                    else:
                        lyrics_str = str(lyrics)
                    style = "background: #fffde7; border: 2px solid #ff9800; border-radius: 8px; padding: 8px; margin-bottom: 1rem; color: #333;" if url_missing else "margin-bottom: 1rem; color: #333;"
                    st.markdown(f'<div class="bengali-poem" style="{style}">{lyrics_str.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                    st.markdown(f"**Current YouTube URL:** {current_url}")

                    edit_btn_key = f"edit_yt_btn_{idx}"
                    edit_state_key = f"edit_yt_state_{idx}"
                    url_key = f"yturl_{idx}"
                    update_key = f"update_{idx}"

                    if edit_state_key not in st.session_state:
                        st.session_state[edit_state_key] = False
                    if url_key not in st.session_state:
                        st.session_state[url_key] = str(current_url)

                    if not st.session_state[edit_state_key]:
                        if st.button("Edit", key=edit_btn_key):
                            st.session_state[edit_state_key] = True
                    else:
                        new_url = st.text_input("New YouTube URL", value=st.session_state[url_key], key=url_key)
                        if st.button("Update", key=update_key):
                            # Note: Google Drive updates require Google Sheets API
                            # For now, this functionality is disabled
                            st.warning("⚠️ YouTube URL updates are currently disabled. Google Drive integration requires additional API setup.")
                            st.info("To enable updates, you'll need to implement Google Sheets API integration.")
                            st.session_state[edit_state_key] = False
                            # Do NOT assign to st.session_state[url_key] here
            if st.button("Logout (Admin)"):
                st.session_state['admin_logged_in'] = False
                st.session_state['show_admin_portal'] = False
        st.stop()
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
                df = load_tagore_songs_data()
                if keyword.strip():
                    matches = df[df['lyrics'].str.contains(keyword, case=False, na=False)]
                else:
                    matches = df
                st.session_state['poetry_search_results'] = matches
                st.session_state['poetry_total_pages'] = (len(matches) + 19) // 20
            except Exception as e:
                st.session_state['poetry_search_results'] = None
                st.session_state['poetry_total_pages'] = 0
                st.error(f"Could not load poetry from Google Drive: {e}")
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
                
                # Determine the lyricist name from the data
                if 'lyricist' in row:
                    lyricist_name = row['lyricist']
                else:
                    # Fallback to selected poet if lyricist column doesn't exist
                    selected_poet = st.session_state.get('selected_poet', 'All')
                    if selected_poet == 'Rabindranath Tagore':
                        lyricist_name = "Rabindranath Tagore"
                    elif selected_poet == 'Dwijendralal Ray':
                        lyricist_name = "Dwijendralal Ray"
                    elif selected_poet == 'Atulprasad Sen':
                        lyricist_name = "Atulprasad Sen"
                    else:
                        lyricist_name = "Rabindranath Tagore"  # Default fallback
                
                with st.expander(f"{first_line} - {lyricist_name}"):
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
                if st.button("Previous", key="poetry_prev", use_container_width=True):
                    if st.session_state['current_page'] > 0:
                        st.session_state['current_page'] -= 1
            with col2:
                st.write("")  # Empty space in the middle
            with col3:
                if st.button("Next", key="poetry_next", use_container_width=True):
                    if st.session_state['current_page'] < total_pages-1:
                        st.session_state['current_page'] += 1
        elif results is not None:
                    st.info("No matching poems found. Try another filter!")
            
    elif st.session_state['active_mode'] == 'search_music':
        # Music Search: search Google Drive, show lyrics and metadata, filter by রাগ and তাল
        st.subheader("Music Search")
        
        # Get selected lyricist
        selected_lyricist = st.session_state.get('selected_lyricist', 'All')
        
        try:
            # Load data based on selected lyricist
            df = load_combined_songs_data(selected_lyricist)
            
            # Get raga and tala options from the loaded data
            if not df.empty:
                rag_options = ['All'] + sorted([r for r in df['রাগ'].dropna().unique().tolist() if str(r).strip() != '?' and str(r).strip() != 'nan'])
                tal_options = ['All'] + sorted([t for t in df['তাল'].dropna().unique().tolist() if str(t).strip() != '?' and str(t).strip() != 'nan'])
            else:
                rag_options, tal_options = ['All'], ['All']
        except Exception as e:
            st.error(f"Could not load music from Google Drive: {e}")
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
        # Initialize search status in session state
        if 'music_search_status' not in st.session_state:
            st.session_state['music_search_status'] = ''
        
        col_btn, col_msg = st.columns([2, 3])
        with col_btn:
            search_clicked = st.button("Search Music", key="do_search_music")
        with col_msg:
            # Show search status or results count
            if search_clicked:
                st.session_state['music_search_status'] = 'Searching...'
                st.markdown(
                    f"<div style='color: #388e3c; font-weight: bold; text-align: right; font-size: 1.1rem;'>{st.session_state['music_search_status']}</div>",
                    unsafe_allow_html=True
                )
            else:
                results = st.session_state.get('music_search_results', None)
                if results is not None and len(results) > 0:
                    st.session_state['music_search_status'] = f"Found {len(results)} matches!"
                    st.markdown(
                        f"<div style='color: #388e3c; font-weight: bold; text-align: right; font-size: 1.1rem;'>{st.session_state['music_search_status']}</div>",
                        unsafe_allow_html=True
                    )
                elif st.session_state['music_search_status']:
                    st.markdown(
                        f"<div style='color: #388e3c; font-weight: bold; text-align: right; font-size: 1.1rem;'>{st.session_state['music_search_status']}</div>",
                        unsafe_allow_html=True
                    )
        if search_clicked:
            st.session_state['current_page_music'] = 0
            try:
                if df is not None and not df.empty:
                    filtered = df
                    if keyword.strip():
                        filtered = filtered[filtered['lyrics'].str.contains(keyword, case=False, na=False)]
                    if selected_rag != 'All':
                        filtered = filtered[filtered['রাগ'] == selected_rag]
                    if selected_tal != 'All':
                        filtered = filtered[filtered['তাল'] == selected_tal]
                    
                    st.session_state['music_search_results'] = filtered
                    st.session_state['music_total_pages'] = (len(filtered) + 19) // 20
                    
                    # Update search status
                    if len(filtered) > 0:
                        st.session_state['music_search_status'] = f"Found {len(filtered)} matches!"
                    else:
                        st.session_state['music_search_status'] = "No matches found"
                else:
                    st.session_state['music_search_results'] = None
                    st.session_state['music_total_pages'] = 0
                    st.session_state['music_search_status'] = "No data available"
            except Exception as e:
                st.session_state['music_search_results'] = None
                st.session_state['music_total_pages'] = 0
                st.session_state['music_search_status'] = "Search failed"
                st.error(f"Could not load music from Google Drive: {e}")
        # Show results if available
        results = st.session_state.get('music_search_results', None)
        total_pages = st.session_state.get('music_total_pages', 0)
        if results is not None and len(results) > 0:
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
                
                # Determine the lyricist name from the data
                if 'lyricist' in row:
                    lyricist_name = row['lyricist']
                else:
                    # Fallback to selected lyricist if lyricist column doesn't exist
                    selected_lyricist = st.session_state.get('selected_lyricist', 'All')
                    if selected_lyricist == 'Rabindranath Tagore':
                        lyricist_name = "Rabindranath Tagore"
                    elif selected_lyricist == 'Dwijendralal Ray':
                        lyricist_name = "Dwijendralal Ray"
                    elif selected_lyricist == 'Atulprasad Sen':
                        lyricist_name = "Atulprasad Sen"
                    else:
                        lyricist_name = "Rabindranath Tagore"  # Default fallback
                
                exp_key = f"music_expander_{start_idx + idx}"
                expanded = st.session_state['music_expander_open'] == exp_key
                exp = st.expander(f"{first_line} - {lyricist_name}", expanded=expanded)
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
                    st.markdown(f'<span style="font-size: 0.92rem; color: #b0bec5;">{metadata_line}</span>', unsafe_allow_html=True)
                    st.markdown(f"[View Original]({row['url']})")
                    # Song ID at bottom right (universally unique, based on Excel row)
                    song_id = row.name + 1  # DataFrame index is 0-based, so add 1 for display
                    st.markdown(f'''<div style="position: relative; height: 24px;">
                        <span style="position: absolute; right: 0; bottom: 0; font-size: 1.1rem; color: #90caf9; opacity: 0.85; font-weight: bold;">#{song_id}</span>
                    </div>''', unsafe_allow_html=True)
                # If this expander is closed, clear the open state
                if not exp.expanded and st.session_state['music_expander_open'] == exp_key:
                    st.session_state['music_expander_open'] = None
            # --- Page Navigation at Bottom ---
            col1, col2, col3 = st.columns([2, 12, 2])
            with col1:
                if st.button("Previous", key="music_prev", use_container_width=True):
                    if st.session_state['current_page_music'] > 0:
                        st.session_state['current_page_music'] -= 1
            with col2:
                st.write("")  # Empty space in the middle
            with col3:
                if st.button("Next", key="music_next", use_container_width=True):
                    if st.session_state['current_page_music'] < total_pages-1:
                        st.session_state['current_page_music'] += 1
        elif results is not None:
            selected_lyricist = st.session_state.get('selected_lyricist', 'All')
            if selected_lyricist != 'All' and selected_lyricist not in ['Rabindranath Tagore', 'Dwijendralal Ray', 'Atulprasad Sen']:
                st.info(f"No songs available for {selected_lyricist} yet. Currently only Rabindranath Tagore, Dwijendralal Ray, and Atulprasad Sen's songs are available in our database.")
            else:
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
                                df = load_tagore_songs_data()
                                filtered = df[(df['রাগ'] == st.session_state['music_gen_raga']) & (df['তাল'] == st.session_state['music_gen_tala'])]
                                if not filtered.empty:
                                    ref_row = filtered.sample(1).iloc[0]
                                    ref_lyrics = ref_row['lyrics']
                                    prompt = f"Write a Bengali song similar to the following, using raga: {st.session_state['music_gen_raga']} and tala: {st.session_state['music_gen_tala']}. Reference lyrics: {ref_lyrics}"
                                else:
                                    st.warning(f"No matching Rabindra Sangeet found for রাগ: {st.session_state['music_gen_raga']} and তাল: {st.session_state['music_gen_tala']}.")
                                    prompt = None
                            except Exception as e:
                                st.warning(f"Error loading from Google Drive: {e}")
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

    elif st.session_state['active_mode'] == 'dictionary':
        # Dictionary Section
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #64b5f6; margin-bottom: 1rem;">📚 বাংলা অভিধান</h3>
            <p style="color: #888; font-size: 1.1rem;">Find Bengali words with longest suffix matches</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load dictionary data
        tokens_df = load_dictionary_data()
        
        if not tokens_df.empty:
            # Input section
            col1, col2 = st.columns([3, 1])
            with col1:
                query_word = st.text_input("Enter a Bengali word", placeholder="e.g. ভালো, মানুষ, প্রেম...", key="dictionary_search")
            with col2:
                search_clicked = st.button("🔍 Search", key="do_dictionary_search", use_container_width=True)
            
            if search_clicked and query_word.strip():
                with st.spinner("🔍 Finding suffix matches..."):
                    matches = find_suffix_matches(query_word, tokens_df, top_n=20)
                    
                    if matches:
                        st.markdown("""
                        <div style="background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); 
                                    border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                                    border: 1px solid #3a3a4e;">
                            <h4 style="color: #64b5f6; margin-bottom: 1rem;">📖 Top 20 Suffix Matches</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Create a table with the results
                        results_data = []
                        for i, match in enumerate(matches, 1):
                            results_data.append({
                                "Rank": i,
                                "Token": match['token'],
                                "Token Length": match['token_length'],
                                "Suffix Length": match['suffix_length'],
                                "Common Suffix": match['suffix']
                            })
                        
                        results_df = pd.DataFrame(results_data)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Show detailed analysis
                        st.markdown("### 📊 Analysis")
                        st.markdown(f"**Query Word:** {query_word}")
                        st.markdown(f"**Total Matches Found:** {len(matches)}")
                        if matches:
                            st.markdown(f"**Longest Suffix Match:** {matches[0]['suffix']} ({matches[0]['suffix_length']} characters)")
                    else:
                        st.info("No suffix matches found for the given word. Try a different word!")
            elif search_clicked and not query_word.strip():
                st.warning("Please enter a Bengali word to search.")
        else:
            st.error("Could not load dictionary data. Please try again later.")

    elif st.session_state['active_mode'] == 'read_blog':
        # Blog Section (Multiple Blogs)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3 style="color: #64b5f6; margin-bottom: 1rem;">বাংলা ব্লগ পড়ুন</h3>
        </div>
        """, unsafe_allow_html=True)

        # Blog entries data
        blogs = [
            {
                "title": "রবীন্দ্রনাথ ঠাকুর: ভালোবাসা, নৈতিকতা, শিল্প ও অর্থবোধ নিয়ে ৭টি চিরন্তন ভাবনা",
                "summary": "নোবেলজয়ী কবি, লেখক, চিত্রশিল্পী ও সংগীতজ্ঞ রবীন্দ্রনাথ ঠাকুরের দর্শন ও সাহিত্য নিয়ে অসাধারণ বিশ্লেষণ। ভালোবাসা, নৈতিকতা, শিল্পের উদ্দেশ্য, অর্থবোধ, ক্ষমতার প্রকৃতি ও জাতীয়তাবাদ নিয়ে তাঁর চিরন্তন ভাবনা নিয়ে পড়ুন এই ব্লগে।",
                "url": "https://medium.com/the-east-berry/the-best-of-rabindranath-tagore-7-timeless-ideas-about-love-morality-art-and-meaning-2faa1146057b",
                "author": "Rushie J.",
                "bullets": [
                    "ভালোবাসা ও নৈতিকতা নিয়ে রবীন্দ্রচিন্তা",
                    "শিল্প ও অর্থবোধের দর্শন",
                    "ক্ষমতা ও জাতীয়তাবাদ নিয়ে বিশ্লেষণ",
                    "মানবতা ও শিক্ষার গুরুত্ব",
                    "রবীন্দ্রনাথের সাহিত্য ও জীবনের গভীর দিক"
                ]
            },
            {
                "title": "The Problem of Evil (অশুভের সমস্যা)",
                "summary": "'অশুভের সমস্যা' প্রবন্ধে রবীন্দ্রনাথ সৃষ্টি ও জীবনের অপূর্ণতা, দুঃখ ও অশুভের অর্থ, এবং এগুলোর মধ্য দিয়ে মানবতার এগিয়ে চলার দর্শন ব্যাখ্যা করেছেন। তিনি দেখিয়েছেন, সীমাবদ্ধতা ও দুঃখই আমাদের অগ্রগতির অনুপ্রেরণা, এবং অশুভ চূড়ান্ত সত্য নয়—এটি পূর্ণতারই প্রকাশ।",
                "url": "https://tagoreweb.in/Essays/sadhana-214/the-problem-of-evil-2612/1",
                "author": "Rabindranath Tagore",
                "bullets": [
                    "সৃষ্টি ও জীবনের অপূর্ণতার অর্থ",
                    "দুঃখ ও অশুভের দর্শন",
                    "মানবতার অগ্রগতিতে সীমাবদ্ধতার ভূমিকা",
                    "আত্মোন্নতি ও চিরন্তন সত্যের সন্ধান",
                    "রবীন্দ্র-দর্শনে অশুভের স্থান"
                ]
            },
            {
                "title": "Rabindranath Tagore and Indian Aesthetics",
                "summary": "রবীন্দ্রনাথ ঠাকুরের জীবন, সাহিত্যকর্ম এবং ভারতীয় নন্দনতত্ত্বে তাঁর অবদানের উপর আলোকপাত। তাঁর প্রবন্ধ 'What is Art?' ও 'The Realization of Beauty' সহ নন্দনতত্ত্ব, শিল্প ও সৌন্দর্য বিষয়ে তাঁর দৃষ্টিভঙ্গি এবং ভারতীয় কাব্যতত্ত্বে তাঁর প্রভাব নিয়ে আলোচনা।",
                "url": "https://ebooks.inflibnet.ac.in/engp11/chapter/rabindranath-tagore-and-indian-aesthetics/",
                "author": "Mr. Abu Saleh",
                "bullets": [
                    "রবীন্দ্রনাথের জীবন ও সাহিত্যকর্মের সংক্ষিপ্ত পরিচিতি",
                    "'What is Art?' ও 'The Realization of Beauty' প্রবন্ধের মূল ভাবনা",
                    "নন্দনতত্ত্ব ও শিল্প বিষয়ে রবীন্দ্র-দর্শন",
                    "সৌন্দর্য ও অনুভূতির ভূমিকা",
                    "ভারতীয় কাব্যতত্ত্বে রবীন্দ্রনাথের অবদান"
                ]
            }
        ]

        for blog in blogs:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                        border-radius: 15px; padding: 2rem; margin: 1.5rem 0; 
                        border: 2px solid #3a3a4e; box-shadow: 0 4px 20px rgba(0,0,0,0.2);">
                <h4 style="color: #64b5f6; margin-bottom: 0.5rem; text-align: center;">{blog['title']}</h4>
                <p style="color: #b0bec5; font-size: 1.1rem; text-align: center; margin-bottom: 0.5rem;">{blog['summary']}</p>
                <p style="color: #b0bec5; font-size: 0.95rem; text-align: center; margin-bottom: 1.2rem;">
                    <b>✍️ লেখক:</b> {blog['author']}
                </p>
                <div style="text-align: center; margin-bottom: 1.2rem;">
                    <a href="{blog['url']}" target="_blank" style="
                        display: inline-block;
                        background: linear-gradient(135deg, #64b5f6 0%, #1976d2 100%);
                        color: white;
                        padding: 12px 30px;
                        text-decoration: none;
                        border-radius: 25px;
                        font-weight: bold;
                        font-size: 1.1rem;
                        box-shadow: 0 4px 15px rgba(100, 181, 246, 0.3);
                        transition: all 0.3s ease;
                    " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(100, 181, 246, 0.4)'" 
                       onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(100, 181, 246, 0.3)'">
                        ব্লগ পড়ুন
                    </a>
                </div>
                <div style="background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); 
                            border-radius: 12px; padding: 1.2rem; margin: 1rem 0 0 0; 
                            border: 1px solid #3a3a4e;">
                    <h5 style="color: #64b5f6; margin-bottom: 1rem;">📝 ব্লগে যা পাবেন:</h5>
                    <ul style="color: #b0bec5; font-size: 1rem;">
                        {''.join([f'<li>{point}</li>' for point in blog['bullets']])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Celebrating Bengali Culture, Creativity, and Soul</p>
        <p>Powered by <a href="https://www.linkedin.com/in/sourovroy-ai/" target="_blank" style="color: #666; text-decoration: underline;">Sourov Roy</a> and Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 