import streamlit as st

# Page Config
st.set_page_config(page_title="🎓 AI Tutor Login", page_icon="🤖", layout="wide")

# Custom CSS for background and design
st.markdown("""
    <style>
        [data-testid="stDecoration"] { display: none; }
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1581092160617-df59c0bf855f?auto=format&fit=crop&w=1470&q=80');
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
            color: #fff;
        }
        .glass-box {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            margin: auto;
            margin-top: 100px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            color: #fff;
        }
        .title {
            font-size: 42px;
            text-align: center;
            font-weight: bold;
            background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }
        .login-label {
            color: #FFDDC1;
            font-weight: 600;
            font-size: 18px;
            margin-top: 15px;
        }
        .stButton>button {
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: white;
            border: none;
            padding: 12px;
            font-size: 18px;
            border-radius: 12px;
            margin-top: 20px;
            width: 100%;
            transition: transform 0.2s ease;
        }
        .stButton>button:hover {
            transform: scale(1.03);
            background: linear-gradient(to right, #43e97b, #38f9d7);
            color: #000;
        }
        .quote {
            margin-top: 30px;
            font-style: italic;
            text-align: center;
            color: #dcdcdc;
        }
    </style>
""", unsafe_allow_html=True)

# Session state for navigation
if "page" not in st.session_state:
    st.session_state.page = "login"

# Login Page
if st.session_state.page == "login":
    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<div class="title">🚀 AI-Powered Tutor Login</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown('<p class="login-label">👤 Full Name</p>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="e.g. John Doe")

        st.markdown('<p class="login-label">🎂 Age</p>', unsafe_allow_html=True)
        age = st.number_input("", min_value=3, max_value=18, step=1)

        st.markdown('<p class="login-label">🏫 Education Level</p>', unsafe_allow_html=True)
        level = st.selectbox("", ["Kindergarten", "Elementary", "Middle School", "High School"])

        st.markdown('<p class="login-label">📧 Email</p>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="e.g. john@email.com")

        submitted = st.form_submit_button("🔓 Login")

        if submitted:
            if not name or not email:
                st.warning("⚠️ Please enter your name and email.")
            else:
                st.session_state.page = "dashboard"
                st.session_state.user = {"name": name, "age": age, "level": level, "email": email}
                st.success("✅ Login successful!")
                st.rerun()

    st.markdown('<p class="quote">“Learning is a treasure that will follow its owner everywhere.”</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Dashboard Page
elif st.session_state.page == "dashboard":
    name = st.session_state.user["name"]
    st.markdown(f"<h1 style='text-align:center; color:#FFFFFF;'>🎓 Welcome, {name}!</h1>", unsafe_allow_html=True)
    # Continue your dashboard code here...

   # render_navbar()

    st.markdown('<div class="dashboard-title">📊 Student Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

    if st.button("📈 Predict Score"):
        st.switch_page("pages/PredictAssesmentScore.py")

    if st.button("📚 Recommendations"):
        st.switch_page("pages/Recommendation.py")

    if st.button("🔍 Retention Analysis"):
        st.switch_page("pages/retentionSkip.py")

    if st.button("🎓 Check Promotion"):
        st.switch_page("pages/Promotion.py")

    if st.button("📦 Ask Doubt"):
        st.switch_page("pages/PdfQuery.py")

    if st.button("📊 EDA"):
        st.switch_page("pages/EDA.py")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚪 Logout", key="logout", help="Click to logout"):
        st.session_state.page = "login"
        st.session_state.user = {}
        st.success("✅ Logged out successfully!")
