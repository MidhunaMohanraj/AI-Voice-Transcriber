"""
app.py — AI Voice Transcriber
Upload audio/video → Get accurate transcript + summary + speaker stats
100% free using OpenAI Whisper (runs locally, no API key needed)
"""
 
import streamlit as st
import whisper
import tempfile
import os
import time
import re
import math
from pathlib import Path
from datetime import timedelta

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Voice Transcriber",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .main { background: #08090e; }

  .hero {
    background: linear-gradient(135deg, #0f0a1e 0%, #08090e 55%, #001a10 100%);
    border: 1px solid #1e1e30;
    border-radius: 16px;
    padding: 38px 40px;
    text-align: center;
    margin-bottom: 24px;
  }
  .hero h1 { font-size: 42px; font-weight: 700; color: #fff; margin: 0 0 8px; }
  .hero p  { color: #64748b; font-size: 15px; margin: 0; }

  .transcript-box {
    background: #0b0c14;
    border: 1px solid #1e1e30;
    border-radius: 12px;
    padding: 24px 28px;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.9;
    color: #d4d8f0;
    max-height: 480px;
    overflow-y: auto;
    white-space: pre-wrap;
  }

  .segment-block {
    border-left: 3px solid #7c3aed;
    padding: 10px 16px;
    margin: 8px 0;
    background: #0d0e1a;
    border-radius: 0 8px 8px 0;
  }
  .segment-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #7c3aed;
    font-weight: 600;
    margin-bottom: 4px;
  }
  .segment-text { font-size: 14px; color: #c4c8e8; line-height: 1.7; }

  .stat-card {
    background: linear-gradient(135deg, #0d0e1a, #080910);
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 18px;
    text-align: center;
  }
  .stat-val   { font-size: 28px; font-weight: 700; color: #a78bfa; }
  .stat-label { font-size: 11px; color: #475569; text-transform: uppercase;
                letter-spacing: 1.5px; margin-top: 4px; }

  .summary-box {
    background: #0a0f1a;
    border-left: 4px solid #06b6d4;
    border-radius: 0 10px 10px 0;
    padding: 18px 22px;
    font-size: 14px;
    line-height: 1.8;
    color: #94a3b8;
    margin: 12px 0;
  }

  .badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin: 3px;
    letter-spacing: 0.5px;
  }

  div.stButton > button {
    background: linear-gradient(135deg, #6d28d9, #7c3aed);
    color: white;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 13px 28px;
    font-size: 15px;
    width: 100%;
    transition: opacity 0.2s;
  }
  div.stButton > button:hover { opacity: 0.85; }
  .stSelectbox div, .stTextArea textarea {
    background: #0d0e1a !important;
    border-color: #1e1e30 !important;
    color: #e2e8f0 !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Model options ──────────────────────────────────────────────────────────────
WHISPER_MODELS = {
    "tiny   (39M  — fastest, ~32x realtime)":   "tiny",
    "base   (74M  — good balance)":             "base",
    "small  (244M — more accurate)":            "small",
    "medium (769M — high accuracy)":            "medium",
    "large  (1.5G — best accuracy, slowest)":   "large",
}

LANGUAGES = [
    "Auto-detect", "English", "Hindi", "Spanish", "French", "German",
    "Italian", "Portuguese", "Russian", "Japanese", "Korean", "Chinese",
    "Arabic", "Dutch", "Polish", "Turkish", "Swedish", "Danish",
]

SUPPORTED_FORMATS = [
    "mp3", "mp4", "wav", "m4a", "ogg", "flac",
    "aac", "wma", "webm", "mkv", "avi", "mov",
]

# ── Helpers ────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading Whisper model...")
def load_whisper(model_name: str):
    return whisper.load_model(model_name)

def format_timestamp(seconds: float) -> str:
    td = timedelta(seconds=int(seconds))
    h  = td.seconds // 3600
    m  = (td.seconds % 3600) // 60
    s  = td.seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def words_per_minute(text: str, duration_sec: float) -> int:
    words = len(text.split())
    mins  = max(duration_sec / 60, 0.01)
    return int(words / mins)

def count_sentences(text: str) -> int:
    return len(re.findall(r'[.!?]+', text))

def estimate_reading_time(text: str) -> str:
    words = len(text.split())
    mins  = math.ceil(words / 200)
    return f"{mins} min read"

def build_timestamped_transcript(segments) -> str:
    lines = []
    for seg in segments:
        ts   = format_timestamp(seg["start"])
        text = seg["text"].strip()
        if text:
            lines.append(f"[{ts}]  {text}")
    return "\n".join(lines)

def simple_summary(text: str) -> str:
    """Rule-based summary: first sentence + key stats."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if not sentences:
        return text[:300]
    opener = sentences[0]
    word_count  = len(text.split())
    sent_count  = len(sentences)
    return (
        f"{opener}\n\n"
        f"The transcript contains {word_count:,} words across {sent_count} sentences. "
        f"Estimated reading time: {estimate_reading_time(text)}."
    )

def export_srt(segments) -> str:
    """Generate SRT subtitle file content."""
    lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg["start"]).replace(":", ":").replace(".", ",")
        end   = format_timestamp(seg["end"]).replace(":", ":").replace(".", ",")
        # SRT needs HH:MM:SS,mmm format
        def to_srt_time(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            ms = int((sec - int(sec)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
        lines.append(str(i))
        lines.append(f"{to_srt_time(seg['start'])} --> {to_srt_time(seg['end'])}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)

def export_vtt(segments) -> str:
    """Generate WebVTT subtitle file content."""
    lines = ["WEBVTT", ""]
    for seg in segments:
        def to_vtt_time(sec):
            h = int(sec // 3600)
            m = int((sec % 3600) // 60)
            s = int(sec % 60)
            ms = int((sec - int(sec)) * 1000)
            return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
        lines.append(f"{to_vtt_time(seg['start'])} --> {to_vtt_time(seg['end'])}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎙️ Voice Transcriber")
    st.markdown("---")

    st.markdown("### 🤖 Whisper Model")
    model_label = st.selectbox("Select model", list(WHISPER_MODELS.keys()), index=1)
    model_name  = WHISPER_MODELS[model_label]

    st.markdown("### 🌍 Language")
    language = st.selectbox("Audio language", LANGUAGES)

    st.markdown("### ⚙️ Options")
    show_timestamps = st.checkbox("Show timestamps", value=True)
    show_segments   = st.checkbox("Show segment view", value=False)
    word_timestamps = st.checkbox("Word-level timestamps", value=False)

    st.markdown("---")
    st.markdown("### 📂 Supported Formats")
    fmt_text = "  ".join([f"`{f}`" for f in SUPPORTED_FORMATS])
    st.markdown(fmt_text)

    st.markdown("---")
    st.markdown("### 💡 Model Guide")
    st.markdown("""
| Model | Best For |
|---|---|
| tiny | Quick drafts |
| base | Everyday use |
| small | Better accuracy |
| medium | Interviews |
| large | Best quality |
    """)

    st.markdown("---")
    st.markdown("### 🔒 Privacy")
    st.markdown("Everything runs **100% locally**. Your audio never leaves your machine.")

# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🎙️ AI Voice Transcriber</h1>
  <p>Upload any audio or video file → Get an accurate transcript, timestamps, subtitles & stats — 100% offline</p>
</div>
""", unsafe_allow_html=True)

# ── File upload ────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📂 Upload audio or video file",
    type=SUPPORTED_FORMATS,
    help="Max recommended size: ~500MB. Larger files may be slow on CPU.",
)

if uploaded_file:
    file_size_mb = len(uploaded_file.getvalue()) / 1_000_000
    st.markdown(
        f'<span class="badge" style="background:#1e1e30;color:#a78bfa;">📁 {uploaded_file.name}</span>'
        f'<span class="badge" style="background:#1e1e30;color:#64748b;">{file_size_mb:.1f} MB</span>'
        f'<span class="badge" style="background:#1e1e30;color:#64748b;">{uploaded_file.type or "audio"}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    transcribe_clicked = st.button("🎙️ Transcribe Now")

    if transcribe_clicked:
        # Save uploaded file to temp
        suffix = Path(uploaded_file.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        try:
            # Load model
            with st.spinner(f"Loading Whisper {model_name} model..."):
                model = load_whisper(model_name)

            # Transcribe
            t_start = time.time()
            with st.spinner("🔊 Transcribing... (this may take a moment for longer files)"):
                options = {
                    "word_timestamps": word_timestamps,
                    "verbose":         False,
                }
                if language != "Auto-detect":
                    options["language"] = language.lower()

                result = model.transcribe(tmp_path, **options)

            elapsed     = time.time() - t_start
            segments    = result.get("segments", [])
            full_text   = result.get("text", "").strip()
            detected_lang = result.get("language", "unknown").upper()
            duration    = segments[-1]["end"] if segments else 0

            st.success(f"✅ Transcribed in {elapsed:.1f}s")

            # ── Stats ──────────────────────────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            stats = [
                (len(full_text.split()), "Words"),
                (len(segments),          "Segments"),
                (format_timestamp(duration), "Duration"),
                (words_per_minute(full_text, duration), "WPM"),
                (detected_lang,          "Language"),
            ]
            for col, (val, label) in zip([c1,c2,c3,c4,c5], stats):
                with col:
                    st.markdown(
                        f'<div class="stat-card"><div class="stat-val">{val}</div>'
                        f'<div class="stat-label">{label}</div></div>',
                        unsafe_allow_html=True,
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Tabs ───────────────────────────────────────────────────────────
            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "📜 Transcript", "⏱️ Segments", "📋 Summary", "📥 Export", "🔍 Search"
            ])

            # Tab 1 — Full transcript
            with tab1:
                st.markdown("### 📜 Full Transcript")
                if show_timestamps:
                    display_text = build_timestamped_transcript(segments)
                else:
                    display_text = full_text
                st.markdown(f'<div class="transcript-box">{display_text}</div>', unsafe_allow_html=True)

                # Plain text copy area
                st.text_area(
                    "Copy-ready transcript:",
                    value=full_text,
                    height=140,
                    label_visibility="visible",
                )

            # Tab 2 — Segment view
            with tab2:
                st.markdown("### ⏱️ Timestamped Segments")
                st.markdown(f"*{len(segments)} segments detected*")
                for seg in segments:
                    start_ts = format_timestamp(seg["start"])
                    end_ts   = format_timestamp(seg["end"])
                    text     = seg["text"].strip()
                    if text:
                        st.markdown(f"""
<div class="segment-block">
  <div class="segment-time">{start_ts} → {end_ts}</div>
  <div class="segment-text">{text}</div>
</div>""", unsafe_allow_html=True)

            # Tab 3 — Summary
            with tab3:
                st.markdown("### 📋 Quick Summary")
                summary = simple_summary(full_text)
                st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

                st.markdown("### 📊 Text Analysis")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total characters",  f"{len(full_text):,}")
                    st.metric("Sentences",          count_sentences(full_text))
                    st.metric("Avg words/segment",  f"{len(full_text.split())//max(len(segments),1)}")
                with col_b:
                    st.metric("Speaking pace",       f"{words_per_minute(full_text, duration)} WPM")
                    st.metric("Reading time",         estimate_reading_time(full_text))
                    st.metric("Model used",           model_name)

            # Tab 4 — Export
            with tab4:
                st.markdown("### 📥 Download Your Transcript")
                fname_base = Path(uploaded_file.name).stem

                col_dl1, col_dl2, col_dl3, col_dl4 = st.columns(4)

                with col_dl1:
                    st.download_button(
                        "⬇️ Plain Text (.txt)",
                        data=full_text,
                        file_name=f"{fname_base}_transcript.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                with col_dl2:
                    timestamped = build_timestamped_transcript(segments)
                    st.download_button(
                        "⬇️ With Timestamps (.txt)",
                        data=timestamped,
                        file_name=f"{fname_base}_timestamped.txt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                with col_dl3:
                    srt_content = export_srt(segments)
                    st.download_button(
                        "⬇️ Subtitles (.srt)",
                        data=srt_content,
                        file_name=f"{fname_base}.srt",
                        mime="text/plain",
                        use_container_width=True,
                    )
                with col_dl4:
                    vtt_content = export_vtt(segments)
                    st.download_button(
                        "⬇️ WebVTT (.vtt)",
                        data=vtt_content,
                        file_name=f"{fname_base}.vtt",
                        mime="text/plain",
                        use_container_width=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                st.info("💡 **.srt** and **.vtt** files can be uploaded directly to YouTube, VLC, or any video player as subtitles.")

            # Tab 5 — Search
            with tab5:
                st.markdown("### 🔍 Search Transcript")
                search_query = st.text_input("Search for a word or phrase", placeholder="e.g.  machine learning")
                if search_query.strip():
                    matches = [
                        seg for seg in segments
                        if search_query.lower() in seg["text"].lower()
                    ]
                    if matches:
                        st.success(f"Found **{len(matches)}** segment(s) containing '{search_query}'")
                        for seg in matches:
                            highlighted = seg["text"].replace(
                                search_query,
                                f"<mark style='background:#7c3aed33;color:#c4b5fd;'>{search_query}</mark>",
                            )
                            st.markdown(f"""
<div class="segment-block">
  <div class="segment-time">{format_timestamp(seg['start'])}</div>
  <div class="segment-text">{highlighted}</div>
</div>""", unsafe_allow_html=True)
                    else:
                        st.warning(f"No matches found for '{search_query}'")

        except Exception as e:
            st.error(f"Transcription failed: {str(e)}")
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

else:
    # Empty state
    st.markdown("""
<div style="text-align:center;padding:60px 20px;">
  <div style="font-size:72px;margin-bottom:16px;">🎙️</div>
  <h3 style="color:#475569;">Upload an audio or video file to get started</h3>
  <p style="color:#334155;font-size:14px;max-width:520px;margin:0 auto 28px;">
    Transcribes meetings, lectures, podcasts, interviews, YouTube videos and more.
    Supports 99 languages. Runs 100% on your machine — no API key, no cost, no upload limits.
  </p>
</div>
""", unsafe_allow_html=True)

    use_cases = [
        "🎙️ Podcast episodes", "📹 YouTube videos", "🎓 Lectures",
        "💼 Meeting recordings", "🎤 Interviews", "🎬 Film/TV subtitles",
    ]
    cols = st.columns(3)
    for i, uc in enumerate(use_cases):
        with cols[i % 3]:
            st.markdown(
                f'<div style="background:#0d0e1a;border:1px solid #1e1e30;border-radius:8px;'
                f'padding:10px 14px;text-align:center;font-size:13px;color:#64748b;margin:4px 0;">'
                f'{uc}</div>',
                unsafe_allow_html=True,
            )
