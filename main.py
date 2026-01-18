import streamlit as st
import os

# ============== CONFIG ==============
APP_TITLE = "Efham sah"
ACCESS_PASSWORD = "IECES"
VIDEO_ROOT = "videos"

SECTIONS = ["IE352", "IE360", "IE314", "IE339"]

st.set_page_config(page_title=APP_TITLE, layout="wide")

# ============== SESSION ==============
if "auth" not in st.session_state:
    st.session_state.auth = False

# ============== TITLE ==============
st.title("🎓 Efham sah")
st.caption("Educational video platform")

# ============== LOGIN ==============
if not st.session_state.auth:
    st.subheader("🔐 Enter Access Password")
    pw = st.text_input("Password", type="password")

    if st.button("Enter"):
        if pw == ACCESS_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong password")

    st.stop()

# ============== MAIN APP ==============
st.success("Access granted")

# Ensure folders exist
os.makedirs(VIDEO_ROOT, exist_ok=True)
for sec in SECTIONS:
    os.makedirs(os.path.join(VIDEO_ROOT, sec), exist_ok=True)

# ============== LAYOUT ==============
left, center, right = st.columns([2, 5, 2])

# ---------- LEFT: SECTIONS ----------
with left:
    st.subheader("📚 Sections")
    selected_section = st.radio("Choose a subject", SECTIONS)

# ---------- CENTER: VIDEOS ----------
with center:
    section_path = os.path.join(VIDEO_ROOT, selected_section)
    videos = [
        f for f in os.listdir(section_path)
        if f.lower().endswith((".mp4", ".mov", ".mkv"))
    ]

    if not videos:
        st.info("No videos in this section yet.")
    else:
        selected_video = st.selectbox("🎬 Select lesson", videos)
        st.video(os.path.join(section_path, selected_video))

# ---------- RIGHT: INFO + UPLOAD ----------
with right:
    st.subheader("⬆️ Admin Upload")
    uploaded = st.file_uploader(
        f"Upload video to {selected_section}",
        type=["mp4", "mov", "mkv"]
    )

    if uploaded:
        save_path = os.path.join(section_path, uploaded.name)
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())
        st.success("Video uploaded")
        st.rerun()

    st.divider()
    st.subheader("ℹ️ Info")
    st.write(f"Section: **{selected_section}**")
    st.write("Password protected")
    st.write("View-only access")

# ============== FOOTER ==============
st.markdown(
    "<div style='position:fixed; bottom:10px; left:20px; font-size:12px; color:gray;'>"
    "Built by <strong>Saad Alshafi</strong></div>",
    unsafe_allow_html=True
)

