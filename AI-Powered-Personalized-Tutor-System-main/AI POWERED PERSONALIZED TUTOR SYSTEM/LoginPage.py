import streamlit as st

# Page Configuration - Full Screen Mode
st.set_page_config(page_title="Student Login", page_icon="🎓", layout="wide")

# Custom CSS for Background Image and Styling
st.markdown("""
    <style>
        [data-testid="stDecoration"] { display: none; }
        .block-container { padding: 0; margin: 0; width: 100vw; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .stApp { 
            background-image: url('https://img.freepik.com/free-vector/hand-drawn-back-school-background_23-2149464866.jpg');
            background-size: cover; 
            background-position: center; 
            color: #333; 
        }
        .login-title { text-align: center; color: #FF6F61; font-size: 40px; font-weight: bold; margin-bottom: 10px; }
        .st-form { background: rgba(255, 255, 255, 0.8); padding: 30px; border-radius: 15px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3); width: 40%; text-align: center; max-height: 70vh; overflow-y: auto; }
        .stButton>button { background: #FF6F61; color: #000; font-size: 18px; padding: 10px; border-radius: 10px; width: 100%; transition: all 0.3s ease; }
        .stButton>button:hover { background: #FF4A37; transform: scale(1.05); }
        .dashboard-title { text-align: center; font-size: 40px; font-weight: bold; color: #6B5B95; margin-top: 20px; }
        .dashboard-container { display: flex; justify-content: center; align-items: center; flex-wrap: wrap; gap: 30px; margin-top: 30px; }
        .box { background: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 15px; text-align: center; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); font-size: 22px; font-weight: bold; color: #333; width: 220px; cursor: pointer; transition: 0.3s ease; }
        .box:hover { background: #D3E0EA; transform: scale(1.05); box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3); }
    </style>
""", unsafe_allow_html=True)

# Session State Setup
if "page" not in st.session_state:
    st.session_state.page = "login"

# Login Page
if st.session_state.page == "login":
    st.markdown('<h1 class="login-title">🎓 Student Login</h1>', unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown('<div class="st-form">', unsafe_allow_html=True)

        st.markdown('<p style="color:#00FFF5;font-weight:600;font-size:18px;">👤 Full Name</p>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="e.g. John Doe")

        st.markdown('<p style="color:#FFD700;font-weight:600;font-size:18px;">🎂 Your Age</p>', unsafe_allow_html=True)
        age = st.number_input("", min_value=3, max_value=18, step=1)

        st.markdown('<p style="color:#ADFF2F;font-weight:600;font-size:18px;">🏫 Education Level</p>', unsafe_allow_html=True)
        level = st.selectbox("", ["Kindergarten", "Elementary", "Middle School", "High School"])

        st.markdown('<p style="color:#FF69B4;font-weight:600;font-size:18px;">📧 Email Address</p>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="e.g. john@email.com")

        submitted = st.form_submit_button("🔓 Login")

        st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            if not name or not email:
                st.warning("⚠ Please enter your name and email to continue!")
            else:
                st.session_state.page = "dashboard"
                st.session_state.user = {"name": name, "age": age, "level": level, "email": email}
                st.success("✅ Login successful!")
                st.rerun()

# Dashboard Page
elif st.session_state.page == "dashboard":
    st.markdown('<h1 class="dashboard-title">📊 Student Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

    # Add boxes as interactive buttons
    if st.button("📈 Predict Assessment Score"):
        st.switch_page("pages/PredictAssesmentScore.py")

    if st.button("📚 Recommendation"):
        st.switch_page("pages/Recommendation.py")

    if st.button("🔍 Retention Analysis"):
        st.switch_page("pages/retentionSkip.py")

    if st.button("🎓 Check Promotion"):
        st.switch_page("pages/Promotion.py")

    if st.button("📦 Doubt"):
        st.switch_page("pages/PdfQuery.py")

    if st.button("EDA"):
        st.switch_page("pages/EDA.py")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚪 Logout"):
        st.session_state.page = "login"
        st.success("✅ Logged out successfully!")
        st.rerun()
