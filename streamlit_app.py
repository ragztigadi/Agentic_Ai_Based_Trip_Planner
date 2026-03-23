import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Voyager AI — Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --ink: #0a0a0f;
    --paper: #f5f0e8;
    --sand: #e8dcc8;
    --rust: #c4622d;
    --rust-light: #e07a4a;
    --gold: #b8924a;
    --muted: #7a7060;
    --white: #fdfaf4;
}

* { box-sizing: border-box; }

html, body, .stApp {
    background-color: var(--ink) !important;
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-image: 
        radial-gradient(ellipse at 20% 0%, rgba(196,98,45,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(184,146,74,0.08) 0%, transparent 50%);
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
section[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Hero section */
.hero {
    text-align: center;
    padding: 60px 40px 40px;
    position: relative;
}

.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--rust);
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(52px, 8vw, 88px);
    font-weight: 300;
    line-height: 0.95;
    color: var(--paper);
    margin: 0 0 8px;
    letter-spacing: -0.02em;
}

.hero-title em {
    font-style: italic;
    color: var(--rust-light);
}

.hero-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    font-weight: 300;
    color: var(--muted);
    margin: 20px 0 0;
    letter-spacing: 0.02em;
}

/* Divider */
.divider {
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--rust), transparent);
    margin: 32px auto;
}

/* Input area */
.input-zone {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 40px 40px;
}

/* Override streamlit input */
.stTextInput > div > div > input {
    background: rgba(245,240,232,0.05) !important;
    border: 1px solid rgba(245,240,232,0.12) !important;
    border-radius: 2px !important;
    color: var(--paper) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 300 !important;
    padding: 18px 24px !important;
    letter-spacing: 0.01em !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: rgba(196,98,45,0.5) !important;
    background: rgba(245,240,232,0.08) !important;
    box-shadow: 0 0 0 1px rgba(196,98,45,0.2) !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(122,112,96,0.6) !important;
    font-style: italic !important;
}

.stTextInput label {
    color: var(--muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    background: var(--rust) !important;
    color: var(--paper) !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 14px 40px !important;
    width: 100% !important;
    margin-top: 12px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: var(--rust-light) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(196,98,45,0.3) !important;
}

/* Quick suggestions */
.suggestions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 20px;
}

.suggestion-pill {
    background: rgba(245,240,232,0.05);
    border: 1px solid rgba(245,240,232,0.1);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 12px;
    color: var(--muted);
    font-family: 'DM Sans', sans-serif;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
}

/* Spinner override */
.stSpinner > div {
    border-top-color: var(--rust) !important;
}

/* Response area */
.response-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 40px 80px;
}

.response-card {
    background: rgba(245,240,232,0.04);
    border: 1px solid rgba(245,240,232,0.08);
    border-radius: 4px;
    padding: 48px;
    position: relative;
    overflow: hidden;
}

.response-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--rust), var(--gold));
}

.response-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid rgba(245,240,232,0.08);
}

.response-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--rust);
}

.response-meta {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    color: var(--muted);
    text-align: right;
}

/* Markdown overrides inside response */
.response-card h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 36px !important;
    font-weight: 400 !important;
    color: var(--paper) !important;
    margin-top: 32px !important;
}

.response-card h2 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 26px !important;
    font-weight: 400 !important;
    color: var(--paper) !important;
    margin-top: 28px !important;
    border-bottom: 1px solid rgba(245,240,232,0.08) !important;
    padding-bottom: 8px !important;
}

.response-card h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--rust-light) !important;
    margin-top: 24px !important;
}

.stMarkdown p {
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.8;
    color: rgba(245,240,232,0.75);
    font-weight: 300;
}

.stMarkdown li {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    line-height: 1.8;
    color: rgba(245,240,232,0.7);
    font-weight: 300;
}

.stMarkdown strong {
    color: var(--paper);
    font-weight: 500;
}

/* Status bar at bottom */
.status-bar {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: rgba(10,10,15,0.95);
    border-top: 1px solid rgba(245,240,232,0.06);
    padding: 10px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(10px);
    z-index: 100;
}

.status-left {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    color: rgba(122,112,96,0.6);
    letter-spacing: 0.05em;
}

.status-right {
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    color: rgba(122,112,96,0.4);
}

.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4caf50;
    margin-right: 8px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Error */
.error-box {
    background: rgba(196,98,45,0.1);
    border: 1px solid rgba(196,98,45,0.3);
    border-radius: 2px;
    padding: 16px 24px;
    color: var(--rust-light);
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    max-width: 760px;
    margin: 0 auto;
}

/* Thinking animation */
.thinking {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 24px;
    color: var(--muted);
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    max-width: 760px;
    margin: 0 auto;
    font-style: italic;
}

.dot-flashing {
    display: flex;
    gap: 4px;
    align-items: center;
}

.dot-flashing span {
    width: 4px; height: 4px;
    border-radius: 50%;
    background: var(--rust);
    animation: dotFlash 1.4s infinite;
}
.dot-flashing span:nth-child(2) { animation-delay: 0.2s; }
.dot-flashing span:nth-child(3) { animation-delay: 0.4s; }

@keyframes dotFlash {
    0%, 80%, 100% { opacity: 0.2; transform: scale(0.8); }
    40% { opacity: 1; transform: scale(1); }
}

/* Form styling */
.stForm {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# --- HERO ---
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered Travel Intelligence</div>
    <div class="hero-title">Plan your<br><em>perfect journey</em></div>
    <div class="divider"></div>
    <div class="hero-subtitle">Bespoke itineraries, curated experiences, real-time insights —<br>crafted by AI, tailored for you.</div>
</div>
""", unsafe_allow_html=True)

# --- INPUT ZONE ---
st.markdown('<div class="input-zone">', unsafe_allow_html=True)

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your Destination",
        placeholder="e.g. Plan a 7-day trip to Kyoto in spring...",
    )
    submit = st.form_submit_button("✦ Plan My Journey")

st.markdown("""
<div class="suggestions">
    <span class="suggestion-pill">🏯 Kyoto, Japan</span>
    <span class="suggestion-pill">🏖️ Santorini, Greece</span>
    <span class="suggestion-pill">🌿 Bali, Indonesia</span>
    <span class="suggestion-pill">🗼 Paris, France</span>
    <span class="suggestion-pill">🏔️ Patagonia</span>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- RESPONSE ---
if submit and user_input.strip():
    st.markdown('<div class="response-wrapper">', unsafe_allow_html=True)

    with st.spinner("Crafting your bespoke travel plan..."):
        try:
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload, timeout=120)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                now = datetime.datetime.now().strftime('%B %d, %Y · %H:%M')

                st.markdown(f"""
                <div class="response-card">
                    <div class="response-header">
                        <div class="response-label">✦ Your Travel Plan</div>
                        <div class="response-meta">
                            Generated {now}<br>
                            <span style="color:rgba(122,112,96,0.5)">Voyager AI Travel Agent</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(answer)

                st.markdown("""
                <div style="margin-top:32px; padding-top:24px; border-top:1px solid rgba(245,240,232,0.08);
                     font-family:'DM Sans',sans-serif; font-size:11px; color:rgba(122,112,96,0.5);
                     font-style:italic; text-align:center;">
                    This travel plan was generated by AI. Please verify prices, operating hours,
                    and travel requirements before your trip.
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f'<div class="error-box">⚠ {response.json().get("error", response.text)}</div>', unsafe_allow_html=True)

        except requests.exceptions.Timeout:
            st.markdown('<div class="error-box">⚠ Request timed out. Your query may be complex — please try again.</div>', unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f'<div class="error-box">⚠ {str(e)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- STATUS BAR ---
st.markdown(f"""
<div class="status-bar">
    <div class="status-left">
        <span class="status-dot"></span>
        Backend connected · {BASE_URL}
    </div>
    <div class="status-right">Voyager AI © {datetime.datetime.now().year}</div>
</div>
""", unsafe_allow_html=True)