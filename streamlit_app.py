import numpy as np
import streamlit as st
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.resnet import preprocess_input
from keras.layers import TFSMLayer
import plotly.graph_objects as go
import plotly.express as px
import time
import os
import shutil
import zipfile
import gdown

from nutrisi import CLASS_NAMES, NUTRISI_DATA

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🍎 FruitScan AI",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS - Modern Glassmorphism Design
# ═══════════════════════════════════════════════════════════════════════════════
CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-attachment: fixed;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 1.5rem;
        box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
    }
    
    .glass-card-dark {
        background: rgba(30, 41, 59, 0.9);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        color: white;
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        text-align: center;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    
    /* Result Display */
    .result-box {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        text-align: center;
        color: white;
        margin: 0.75rem 0;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.35);
    }
    
    .result-label {
        font-size: 0.75rem;
        font-weight: 500;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .result-value {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0.25rem 0;
    }
    
    .result-confidence {
        font-size: 0.95rem;
        font-weight: 600;
        opacity: 0.95;
    }
    
    /* Confidence Bar */
    .confidence-bar-container {
        background: #e2e8f0;
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .confidence-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
    }
    
    /* Nutrition Card */
    .nutrition-item {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 12px;
        padding: 0.6rem 0.9rem;
        margin: 0.35rem 0;
        border-left: 3px solid #667eea;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .nutrition-item:hover {
        transform: translateX(5px);
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.15);
    }
    
    .nutrition-label {
        font-size: 0.7rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .nutrition-value {
        font-size: 0.95rem;
        color: #1e293b;
        font-weight: 700;
    }
    
    /* Top Predictions */
    .prediction-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 1rem;
        background: #f8fafc;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .prediction-rank {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        color: white;
    }
    
    .rank-1 { background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); }
    .rank-2 { background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%); }
    .rank-3 { background: linear-gradient(135deg, #d97706 0%, #b45309 100%); }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(30, 41, 59, 0.95);
        backdrop-filter: blur(20px);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Upload Area */
    [data-testid="stFileUploader"] {
        background: rgba(102, 126, 234, 0.05);
        border: 2px dashed #667eea;
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Radio Buttons - Force dark text */
    [data-testid="stRadio"] > div {
        background: #ffffff !important;
        border-radius: 12px;
        padding: 0.75rem 1.25rem;
        border: 1px solid #e2e8f0;
    }
    
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] label span,
    [data-testid="stRadio"] label p,
    [data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stRadio"] * {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    .stRadio > label {
        color: #1e293b !important;
    }
    
    div[role="radiogroup"] label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    div[role="radiogroup"] label div p {
        color: #1e293b !important;
    }
    
    /* Image Preview */
    [data-testid="stImage"] {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    }
    
    /* Metric */
    [data-testid="stMetric"] {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 16px;
        padding: 1rem;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    .animate-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Divider */
    .fancy-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        border: none;
        margin: 1.5rem 0;
        border-radius: 2px;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        color: white;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 800;
    }
    
    .stat-label {
        font-size: 0.85rem;
        opacity: 0.9;
        margin-top: 0.25rem;
    }
</style>
"""

MODEL_DIR = "resnet50_50classes_20251210_155750"

def _find_saved_model_dir(search_root: str = "."):
    for root, _dirs, files in os.walk(search_root):
        if "saved_model.pb" in files:
            return root
    return None


def _safe_extract_zip(zip_path: str, dest_dir: str = "."):
    dest_dir_abs = os.path.abspath(dest_dir)
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            # Normalize path separators (some ZIPs created on Windows may use backslashes)
            member_name = info.filename.replace("\\", "/")
            if member_name.endswith("/"):
                continue

            target_path = os.path.abspath(os.path.join(dest_dir, member_name))
            if not target_path.startswith(dest_dir_abs + os.sep) and target_path != dest_dir_abs:
                raise RuntimeError("Unsafe ZIP path detected")

            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with z.open(info, "r") as src, open(target_path, "wb") as dst:
                shutil.copyfileobj(src, dst)

MODEL_PB_PATH = os.path.join(MODEL_DIR, "saved_model.pb")

# Google Drive file ID for model.zip (provided by user)
GOOGLE_DRIVE_ID = "1Y7qZlm1RltgzOg3ZDcXLxaL-cpIjhD0D"

# Ensure model is present and valid by downloading and extracting if necessary
if not os.path.exists(MODEL_PB_PATH):
    # If a partial/invalid folder exists from a previous run, remove it
    if os.path.isdir(MODEL_DIR):
        try:
            shutil.rmtree(MODEL_DIR)
        except Exception as e:
            st.error(f"Gagal membersihkan folder model yang tidak lengkap: {e}")
            st.stop()

    zip_path = "model.zip"
    # Remove any cached zip to force re-download of the latest Drive file
    if os.path.exists(zip_path):
        try:
            os.remove(zip_path)
        except Exception as e:
            st.error(f"Gagal menghapus cache model.zip: {e}")
            st.stop()

    try:
        st.info("Mengunduh model dari Google Drive...")
        gdown.download(id=GOOGLE_DRIVE_ID, output=zip_path, quiet=False)
    except Exception as e:
        st.error(f"Gagal mengunduh model: {e}")
        st.stop()

    if not zipfile.is_zipfile(zip_path):
        try:
            file_size = os.path.getsize(zip_path)
        except Exception:
            file_size = None
        st.error(f"File yang terunduh bukan ZIP yang valid. Ukuran file: {file_size}")
        st.stop()

    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            zip_names = z.namelist()
    except Exception as e:
        st.error(f"Gagal membaca ZIP: {e}")
        st.stop()

    zip_has_saved_model = any(n.endswith("saved_model.pb") for n in zip_names)
    if not zip_has_saved_model:
        preview = "\n".join(zip_names[:30])
        st.error(
            "ZIP berhasil diunduh, tapi tidak berisi saved_model.pb. "
            "Contoh isi ZIP (30 pertama):\n" + preview
        )
        st.stop()

    try:
        _safe_extract_zip(zip_path, ".")
    except Exception as e:
        st.error(f"Gagal mengekstrak model: {e}")
        st.stop()

    found_dir = _find_saved_model_dir(".")
    if found_dir is None:
        try:
            pb_member = next(n for n in zip_names if n.endswith("saved_model.pb"))
            pb_dir = os.path.dirname(pb_member)
            expected_dir = "." if pb_dir == "" else os.path.normpath(pb_dir)
            expected_pb = os.path.join(expected_dir, "saved_model.pb")
            if os.path.exists(expected_pb):
                found_dir = expected_dir
        except Exception:
            found_dir = None

    if found_dir is None:
        st.error(
            "Model sudah diunduh dan diekstrak, tapi saved_model.pb masih tidak ditemukan. "
            "Pastikan ZIP berisi file saved_model.pb"
        )
        st.stop()

    MODEL_DIR = found_dir
    MODEL_PB_PATH = os.path.join(MODEL_DIR, "saved_model.pb")

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL LOADING
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    try:
        return TFSMLayer(MODEL_DIR, call_endpoint="serving_default")
    except Exception:
        return TFSMLayer(MODEL_DIR)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def preprocess_image(image: Image.Image, target_size=(64, 64)):
    image = image.convert("RGB")
    image = image.resize(target_size)
    img_array = tf.keras.utils.img_to_array(image)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


def get_display_name(class_name: str) -> str:
    """Hapus angka di akhir nama kelas untuk tampilan lebih rapi."""
    tokens = class_name.split()
    if tokens and tokens[-1].isdigit():
        return " ".join(tokens[:-1])
    return class_name


def get_fruit_emoji(name: str) -> str:
    """Return emoji berdasarkan nama buah."""
    name_lower = name.lower()
    emoji_map = {
        "apple": "🍎",
        "banana": "🍌",
        "avocado": "🥑",
        "blueberry": "🫐",
        "blackberry": "🫐",
        "apricot": "🍑",
        "beans": "🫘",
        "beetroot": "🥬",
        "cabbage": "🥬",
    }
    for key, emoji in emoji_map.items():
        if key in name_lower:
            return emoji
    return "🍇"


def get_fruit_color(name: str) -> str:
    """Return warna dominan (CSS gradient) berdasarkan nama buah."""
    name_lower = name.lower()
    
    # --- 1. MERAH (Red) ---
    if any(x in name_lower for x in [
        'apple red', 'apple crimson', 'apple hit', 'apple rotten', 
        'banana red', 'blackberrie not rippen', 'cherry', 'strawberry', 'tomato',
        'cabbage red', 'onion red'
    ]):
        color1, color2 = "#ef4444", "#b91c1c" # Red to Dark Red
        shadow_color = "rgba(239, 68, 68, 0.4)"
        
    # --- 2. HIJAU (Green) ---
    elif any(x in name_lower for x in [
        'apple granny', 'avocado', 'beans', 'cabbage white', 'apple green', 
        'kiwi', 'lime', 'pear', 'cucumber', 'watermelon'
    ]):
        color1, color2 = "#10b981", "#059669" # Emerald to Green
        shadow_color = "rgba(16, 185, 129, 0.4)"

    # --- 3. KUNING / ORANYE (Yellow/Orange) ---
    elif any(x in name_lower for x in [
        'apple golden', 'apricot', 'banana', 'lemon', 'orange', 
        'cantaloupe', 'papaya', 'mango', 'peach', 'corn'
    ]):
        # Cek khusus Banana Red sudah dihandle di atas, jadi aman
        color1, color2 = "#f59e0b", "#d97706" # Amber to Orange
        shadow_color = "rgba(245, 158, 11, 0.4)"

    # --- 4. UNGU / BIRU (Purple/Blue) ---
    elif any(x in name_lower for x in [
        'blueberry', 'blackberrie', 'beetroot', 
        'grape', 'plum', 'eggplant'
    ]):
        # Cek khusus Blackberry not rippen sudah dihandle di atas
        # Khusus Blackberry half rippen mungkin agak kemerahan/ungu, masuk sini ok
        color1, color2 = "#8b5cf6", "#7c3aed" # Violet to Purple
        shadow_color = "rgba(139, 92, 246, 0.4)"

    # --- 5. PINK (Pink) ---
    elif any(x in name_lower for x in ['apple pink lady', 'peach', 'pitaya']):
        color1, color2 = "#ec4899", "#be185d" # Pink to Rose
        shadow_color = "rgba(236, 72, 153, 0.4)"
        
    # --- 6. COKLAT / PUTIH (Brown/White/Others) ---
    elif any(x in name_lower for x in ['potato', 'ginger', 'chestnut', 'coconut']):
        color1, color2 = "#a8a29e", "#78716c" # Stone to Warm Gray
        shadow_color = "rgba(168, 162, 158, 0.4)"
        
    else:
        # Default (jika nama buah lain/generic Apple)
        # Apple 10-19 dll yang tidak spesifik warnanya, kita anggap Merah (umum)
        if 'apple' in name_lower:
             color1, color2 = "#ef4444", "#b91c1c"
             shadow_color = "rgba(239, 68, 68, 0.4)"
        else:
             # Fallback Hijau
             color1, color2 = "#10b981", "#059669"
             shadow_color = "rgba(16, 185, 129, 0.4)"
        
    return color1, color2, shadow_color


def create_confidence_chart(scores: np.ndarray, top_k: int = 5):
    """Buat chart horizontal bar untuk top predictions."""
    top_indices = np.argsort(scores)[-top_k:][::-1]
    top_scores = scores[top_indices] * 100
    top_names = [get_display_name(CLASS_NAMES[i]) for i in top_indices]
    
    colors = ['#10b981', '#667eea', '#8b5cf6', '#a855f7', '#d946ef']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_names[::-1],
        x=top_scores[::-1],
        orientation='h',
        marker=dict(
            color=colors[::-1],
            cornerradius=8
        ),
        text=[f'{s:.1f}%' for s in top_scores[::-1]],
        textposition='outside',
        textfont=dict(size=14, color='#1e293b', family='Inter')
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=0, r=40, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,
            gridcolor='#e2e8f0',
            range=[0, 110],
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=13, color='#1e293b', family='Inter')
        ),
        showlegend=False
    )
    
    return fig


def create_nutrition_chart(nutrisi: dict):
    """Buat donut chart untuk komposisi nutrisi."""
    # Extract numeric values
    kalori = float(nutrisi.get("Kalori (100g)", "0 kcal").replace(" kcal", ""))
    serat = float(nutrisi.get("Serat", "0 g").replace(" g", ""))
    
    fig = go.Figure(data=[go.Pie(
        labels=['Kalori', 'Serat', 'Lainnya'],
        values=[kalori, serat * 10, 100 - kalori - serat * 10],
        hole=0.6,
        marker=dict(colors=['#667eea', '#10b981', '#e2e8f0']),
        textinfo='label+percent',
        textfont=dict(size=12, family='Inter'),
        hovertemplate='%{label}: %{value:.1f}<extra></extra>'
    )])
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        annotations=[dict(
            text=f'{kalori:.0f}<br>kcal',
            x=0.5, y=0.5,
            font=dict(size=20, family='Inter', color='#1e293b'),
            showarrow=False
        )]
    )
    
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    # Inject CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────────────────────────────────────
    with st.sidebar:
        # SVG Icons (White Outline)
        icon_info = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px; vertical-align:text-bottom;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>"""
        icon_cpu = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px; vertical-align:text-bottom;"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>"""
        icon_book = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:8px; vertical-align:text-bottom;"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg>"""
        
        st.markdown(f"<h3 style='color: white; margin-bottom:1.5rem; display:flex; align-items:center;'>{icon_info} Tentang Aplikasi</h3>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style='background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 12px; margin-bottom: 2rem;'>
                <p style='color: #cbd5e1; font-size: 0.9rem; line-height: 1.6;'>
                Aplikasi ini membantu Anda mengenali jenis buah dan sayuran secara otomatis, serta memberikan informasi nutrisi yang bermanfaat untuk kesehatan Anda.
                </p>
            </div>
            """
            , unsafe_allow_html=True)

        st.markdown(f"<h4 style='color: white; font-size: 1rem; margin-bottom: 0.5rem; display:flex; align-items:center;'>{icon_cpu} Spesifikasi Model</h4>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 2rem;'>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;'>
                    <span>Arsitektur</span>
                    <span style='color: white;'>ResNet50</span>
                </div>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;'>
                    <span>Dataset</span>
                    <span style='color: white;'>Fruits-360</span>
                </div>
                <div style='display: flex; justify-content: space-between; margin-bottom: 0.5rem;'>
                    <span>Kemampuan</span>
                    <span style='color: white;'>50 Jenis Buah</span>
                </div>
            </div>
            """
            , unsafe_allow_html=True)
            
        st.markdown(f"<h4 style='color: white; font-size: 1rem; margin-bottom: 0.5rem; display:flex; align-items:center;'>{icon_book} Panduan Penggunaan</h4>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style='color: #cbd5e1; font-size: 0.85rem; line-height: 1.6;'>
                <p style='margin-bottom: 0.5rem;'>• Gunakan pencahayaan yang cukup</p>
                <p style='margin-bottom: 0.5rem;'>• Pastikan objek buah terlihat jelas</p>
                <p>• Background polos memberikan hasil terbaik</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")
        st.markdown(
            "<div style='text-align:center; opacity:0.7; font-size:0.85rem;'>"
            "Made with ❤️ using Streamlit"
            "</div>",
            unsafe_allow_html=True
        )
    
    # ─────────────────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown(
        "<div class='glass-card animate-fade-in'>"
        "<h1 class='hero-title'>🍎 FruitScan AI</h1>"
        "<p class='hero-subtitle'>"
        "Deteksi buah secara instan dengan AI dan dapatkan informasi nutrisi lengkap"
        "</p>"
        "</div>",
        unsafe_allow_html=True
    )
    
    # ─────────────────────────────────────────────────────────────────────────
    # INPUT SECTION
    # ─────────────────────────────────────────────────────────────────────────
    col_input, col_result = st.columns([1, 1.3], gap="large")
    
    with col_input:
        st.markdown(
            "<div class='glass-card'>"
            "<div class='section-header'>Input Gambar</div>",
            unsafe_allow_html=True
        )
        
        # Gunakan columns untuk tombol pilihan
        btn_col1, btn_col2 = st.columns(2)
        
        if "input_mode" not in st.session_state:
            st.session_state.input_mode = "upload"
        
        with btn_col1:
            if st.button("Upload File", use_container_width=True, 
                        type="primary" if st.session_state.input_mode == "upload" else "secondary"):
                st.session_state.input_mode = "upload"
                st.rerun()
        
        with btn_col2:
            if st.button("Kamera", use_container_width=True,
                        type="primary" if st.session_state.input_mode == "kamera" else "secondary"):
                st.session_state.input_mode = "kamera"
                st.rerun()
        
        sumber = "Upload" if st.session_state.input_mode == "upload" else "Kamera"
        
        uploaded_file = None
        if "Upload" in sumber:
            uploaded_file = st.file_uploader(
                "Drag & drop atau klik untuk upload",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed",
                key="file_input"
            )
        else:
            uploaded_file = st.camera_input(
                "Ambil foto",
                label_visibility="collapsed",
                key="cam_input"
            )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.markdown("<div class='section-header' style='margin-top:1rem;'>Preview</div>", unsafe_allow_html=True)
            st.image(image, use_column_width=True)
        else:
            st.markdown(
                "<div style='text-align:center; padding:3rem 1rem; color:#64748b;'>"
                "<p>Upload atau ambil foto buah untuk memulai analisis</p>"
                "</div>",
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ─────────────────────────────────────────────────────────────────────────
    # RESULT SECTION
    # ─────────────────────────────────────────────────────────────────────────
    with col_result:
        if uploaded_file is not None:
            st.markdown(
                "<div class='glass-card animate-fade-in'>",
                unsafe_allow_html=True
            )
            
            # Loading animation
            with st.spinner("Menganalisis gambar..."):
                status = st.empty()
                status.info("Memuat model...")
                model = load_model()

                status.info("Menyiapkan gambar...")
                img_batch = preprocess_image(image, target_size=(64, 64))

                status.info("Menjalankan prediksi...")
                preds = model(img_batch)
                if isinstance(preds, dict):
                    preds = next(iter(preds.values()))

                scores = tf.nn.softmax(preds[0]).numpy()
                status.empty()
            
            predicted_index = int(np.argmax(scores))
            confidence = float(np.max(scores) * 100.0)
            predicted_name = CLASS_NAMES[predicted_index] if predicted_index < len(CLASS_NAMES) else f"Index {predicted_index}"
            display_name = get_display_name(predicted_name)
            fruit_emoji = get_fruit_emoji(display_name)
            
            # Ambil warna dinamis
            color1, color2, shadow_color = get_fruit_color(display_name)
            
            # ── Main Result ──
            # Kita override style result-box secara inline/langsung di elemen
            st.markdown(
                f"""
                <div class='result-box animate-pulse' style='background: linear-gradient(135deg, {color1} 0%, {color2} 100%); box-shadow: 0 8px 25px {shadow_color};'>
                    <div class='result-label'>Buah Terdeteksi</div>
                    <div class='result-value'>{fruit_emoji} {display_name}</div>
                    <div class='result-confidence'>Confidence: {confidence:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # ── Confidence Bar ──
            # Bar color juga mengikuti warna buah (ambil color1)
            bar_color = color1
            
            st.markdown(
                f"""
                <div style='margin: 1rem 0;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
                        <span style='font-weight:600; color:#1e293b;'>Tingkat Keyakinan</span>
                        <span style='font-weight:700; color:{bar_color};'>{confidence:.1f}%</span>
                    </div>
                    <div class='confidence-bar-container'>
                        <div class='confidence-bar' style='width:{confidence}%; background:{bar_color};'></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<hr style='border:none; border-top:1px solid #e2e8f0; margin:1rem 0;'>", unsafe_allow_html=True)
            
            st.markdown("<div class='section-header'>Informasi Nutrisi (per 100g)</div>", unsafe_allow_html=True)
            
            nutrisi = NUTRISI_DATA.get(predicted_name)
            if nutrisi is None:
                base_name = predicted_name.split()[0]
                nutrisi = NUTRISI_DATA.get(base_name)
            
            if nutrisi:
                # Display nutrition items
                ncol1, ncol2 = st.columns(2)
                
                items = list(nutrisi.items())
                half = len(items) // 2 + len(items) % 2
                
                with ncol1:
                    for key, value in items[:half]:
                        # icon = "🔥" if "Kalori" in key else "🌿" if "Serat" in key else "" if "Vitamin" in key else "📝"
                        icon = "" # Hapus icon biar minimalis
                        st.markdown(
                            f"""
                            <div class='nutrition-item'>
                                <div class='nutrition-label'>{key}</div>
                                <div class='nutrition-value'>{value}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                with ncol2:
                    for key, value in items[half:]:
                        # icon = "🔥" if "Kalori" in key else "🌿" if "Serat" in key else "💊" if "Vitamin" in key else "📝"
                        icon = "" # Hapus icon biar minimalis
                        st.markdown(
                            f"""
                            <div class='nutrition-item'>
                                <div class='nutrition-label'>{key}</div>
                                <div class='nutrition-value'>{value}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                
                # Nutrition chart
                st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
                fig_nutrition = create_nutrition_chart(nutrisi)
                st.plotly_chart(fig_nutrition, use_container_width=True, config={'displayModeBar': False})
                
            else:
                st.info("Data nutrisi untuk buah ini belum tersedia dalam database.")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
        else:
            # Empty state
            st.markdown(
                "<div class='glass-card' style='text-align:center; padding:4rem 2rem;'>"
                "<h3 style='color:#1e293b; margin-bottom:0.5rem;'>Menunggu Input</h3>"
                "<p style='color:#64748b;'>Upload atau ambil foto buah di panel kiri untuk memulai analisis AI</p>"
                "</div>",
                unsafe_allow_html=True
            )


if __name__ == "__main__":
    main()
