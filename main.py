import streamlit as st
import os

# ================= CONFIG =================
APP_TITLE = "Efham sah"

ADMIN_PASSWORD = "ADMIN123"   # change this
USER_PASSWORD  = "IECES"      # students

VIDEO_ROOT = "videos"
SECTIONS = ["IE352", "IE360", "IE314", "IE339"]

st.set_page_config(page_title=APP_TITLE, layout="wide")

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ================= TITLE =================
st.title("🎓 Efham sah")
st.caption("Educational video platform")

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.subheader("🔐 Login")

    password = st.text_input("Password", type="password")

    if st.button("Enter"):
        if password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.is_admin = True
            st.rerun()
        elif password == USER_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.is_admin = False
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()

# ================= SETUP =================
os.makedirs(VIDEO_ROOT, exist_ok=True)
for sec in SECTIONS:
    os.makedirs(os.path.join(VIDEO_ROOT, sec), exist_ok=True)

st.success("Access granted")

# ================= LAYOUT =================
left, center, right = st.columns([2, 5, 2])

# ---------- LEFT: SECTIONS ----------
with left:
    st.subheader("📚 Sections")
    selected_section = st.radio("Choose subject", SECTIONS)

# ---------- CENTER: VIDEOS ----------
with center:
    section_path = os.path.join(VIDEO_ROOT, selected_section)
    videos = [
        v for v in os.listdir(section_path)
        if v.lower().endswith((".mp4", ".mov", ".mkv"))
    ]

    if not videos:
        st.info("No videos in this section yet.")
    else:
        selected_video = st.selectbox("🎬 Select lesson", videos)
        st.video(os.path.join(section_path, selected_video))

# ---------- RIGHT: ADMIN ONLY ----------
with right:
    st.subheader("ℹ️ Info")
    st.write(f"Section: **{selected_section}**")
    st.write("View-only for students")

    if st.session_state.is_admin:
        st.divider()
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

# ================= FOOTER =================
st.markdown(
    "<div style='position:fixed; bottom:10px; left:20px; font-size:12px; color:gray;'>"
    "Built by <strong>Saad Alshafi</strong></div>",
    unsafe_allow_html=True
)
