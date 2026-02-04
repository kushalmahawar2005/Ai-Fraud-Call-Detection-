import streamlit as st
import time
import os
import tempfile
import re
from transcriber import Transcriber
from analyzer import analyze_text, detect_voice_authenticity

# Initialize Transcriber (Cached)
@st.cache_resource
def load_transcriber():
    return Transcriber(model_size="base")

# Page Configuration - Professional & Clean
st.set_page_config(
    page_title="AI Risk Intelligence",
    layout="wide",  # Wide layout for dashboard feel
    initial_sidebar_state="expanded"
)

# Professional Minimalist CSS
st.markdown("""
    <style>
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        color: #f0f2f6;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #aeb5bc;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 5px;
        border: 1px solid #41424b;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar: Project Overview
with st.sidebar:
    st.markdown("### Project Overview")
    st.markdown("""
    **Project Name:**  
    AI-Powered Call Risk Intelligence System
    
    **Objective:**  
    Analyze recorded call audio to assess potential fraud risk using speech understanding and behavioral analysis.
    
    **Core Capabilities:**
    *   Multilingual Speech Analysis (English + Hindi)
    *   Scam Intent Detection
    *   Voice Authenticity Analysis (AI vs Human)
    *   Explainable Risk Scores
    
    **Technology Stack:**
    *   Python & Streamlit
    *   Whisper (ASR)
    *   Rule-based Risk Engine
    
    **Build Status:**  
    Prototype (Hackathon Submission)
    """)
    st.markdown("---")
    st.caption("© 2026 AI Risk Intelligence Prototype")

# Main Page Header
st.markdown('<div class="main-header">AI-Powered Call Risk Intelligence System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Fraud Detection & Voice Analysis Engine</div>', unsafe_allow_html=True)

st.divider()

# --- Section 1: Audio Ingestion ---
st.markdown("## Audio Ingestion")

UPLOAD_DIR = "temp_audio"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

uploaded_file = st.file_uploader("Upload Audio File (WAV/MP3 format supported)", type=["wav", "mp3"])

if uploaded_file is not None:
    # Save file securely
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        file_path = tmp_file.name
    
    st.write(f"**Filename:** {uploaded_file.name}")
    st.audio(uploaded_file)
    st.caption("Status: Audio file successfully ingested for processing.")
    
    st.divider()

    # --- Section 2: Speech Transcription ---
    if st.button("Initiate Analysis", type="primary"):
        st.markdown("## Speech Transcription")
        
        status_container = st.empty()
        status_container.markdown("*Initializing ASR Model & Processing Speech...*")
        
        try:
            # Load & Transcribe
            transcriber = load_transcriber()
            text = transcriber.transcribe(file_path)
            
            if text.startswith("Error:"):
                status_container.markdown(f"**Error during transcription:** {text}")
            else:
                status_container.markdown("**Status:** Transcription process verified.")
                
                # --- Section 3: Risk Assessment ---
                st.divider()
                st.markdown("## Risk Assessment")
                
                # Analyze Text
                analysis = analyze_text(text)
                
                # Map technical labels to professional terms
                risk_score = analysis['risk_score']
                raw_verdict = analysis['verdict']
                
                # Professional Verdict Mapping
                if raw_verdict == "SAFE":
                    pro_verdict = "Low Risk / Verified"
                elif raw_verdict == "SUSPICIOUS":
                    pro_verdict = "Potential Risk Detected"
                else: # SCAM
                    pro_verdict = "High Risk / Fraudulent Pattern"
                
                # Metrics Display
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Confidence Score", f"{risk_score}/100")
                col2.metric("Risk Classification", pro_verdict)
                col3.metric("Risk Indicators Identified", len(analysis['matched_keywords']))
                
                # Risk Meter
                bar_color = "green" if risk_score <= 30 else ("yellow" if risk_score <= 60 else "red")
                st.progress(risk_score / 100, text=f"Calculated Risk Level: {pro_verdict}")
                
                # Matched Keywords (Professional List)
                if analysis['matched_keywords']:
                    st.markdown("**Risk Signals Detected:**")
                    st.markdown(", ".join([f"`{k.upper()}`" for k in analysis['matched_keywords']]))
                else:
                    st.markdown("**Status:** No high-risk indicators detected in the analyzed content.")

                # Transcript with High-Risk Highlight
                st.markdown("### Analyzed Transcript Content")
                formatted_text = text
                for kw in sorted(analysis['matched_keywords'], key=len, reverse=True):
                    # Bold red for professional highlight, no emojis
                    pattern = re.compile(re.escape(kw), re.IGNORECASE)
                    formatted_text = pattern.sub(f":red[**{kw.upper()}**]", formatted_text)
                
                st.markdown(f"> {formatted_text}")
                
                # --- Section 4: Voice Authenticity Analysis ---
                st.divider()
                st.markdown("## Voice Authenticity Analysis")
                
                voice_analysis = detect_voice_authenticity(text)
                
                # Mapping Voice Labels
                raw_label = voice_analysis['label']
                if "Human" in raw_label and "Uncertain" not in raw_label:
                    pro_label = "Voice Classification: Predominantly Human"
                elif "AI" in raw_label:
                    pro_label = "Voice Classification: Automated/Synthetic Pattern"
                else:
                    pro_label = "Voice Classification: Ambiguous / Scripted Pattern"
                
                # Columns for analysis
                v_col1, v_col2 = st.columns([1, 2])
                
                v_col1.metric("Synthesized Speech Likelihood", f"{voice_analysis['score']}%")
                
                with v_col2:
                    st.markdown(f"**{pro_label}**")
                    st.markdown(f"**Analysis Rationale:** {voice_analysis['explanation']}")
                
                st.progress(voice_analysis['score'] / 100, text="Synthetic Probability Index")
                
        except Exception as e:
            st.error(f"System Error: {str(e)}")

    # Footer Disclaimer
    st.divider()
    st.caption("Disclaimer: This system provides a risk-based advisory analysis and does not constitute a definitive legal or financial determination.")

else:
    st.markdown("Waiting for audio ingestion...")
