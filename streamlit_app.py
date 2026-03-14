import streamlit as st
import requests

st.set_page_config(page_title="AutoVal — Car Price Predictor", page_icon="🚗", layout="centered")

API_URL = "https://car-prediction-model-x7o6.onrender.com"

# ── INJECT CUSTOM CSS + ANIMATIONS ──
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<style>
/* Hide Streamlit default chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 720px; }

:root {
  --accent: #e8ff00;
  --accent2: #00d4ff;
  --red: #ff3c3c;
  --bg: #060810;
  --muted: #888;
}

/* Full page dark background */
.stApp {
  background: var(--bg) !important;
  color: #f0f0f0 !important;
}

/* ── BACKGROUND SCENE ── */
.bg-scene {
  position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden;
}
.stars {
  position: absolute; inset: 0;
  background-image:
    radial-gradient(1px 1px at 10% 20%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 30% 10%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 50% 30%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 15%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 40%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 20% 60%, rgba(255,255,255,0.2) 0%, transparent 100%),
    radial-gradient(1.5px 1.5px at 60% 55%, rgba(255,255,255,0.4) 0%, transparent 100%),
    radial-gradient(1px 1px at 90% 70%, rgba(255,255,255,0.3) 0%, transparent 100%),
    radial-gradient(1px 1px at 75% 85%, rgba(255,255,255,0.3) 0%, transparent 100%);
}
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px); opacity: 0.22;
  animation: orbfloat 8s ease-in-out infinite;
}
.orb1 { width:500px;height:500px;background:#00d4ff;top:-100px;left:-100px;animation-delay:0s; }
.orb2 { width:400px;height:400px;background:#e8ff00;bottom:100px;right:-80px;animation-delay:-3s; }
.orb3 { width:300px;height:300px;background:#ff3c3c;top:40%;left:40%;animation-delay:-5s; }
@keyframes orbfloat {
  0%,100%{transform:translateY(0) scale(1);}
  50%{transform:translateY(-30px) scale(1.08);}
}
.grid-floor {
  position:absolute;bottom:0;left:0;right:0;height:280px;
  background-image:linear-gradient(rgba(0,212,255,0.07) 1px,transparent 1px),linear-gradient(90deg,rgba(0,212,255,0.07) 1px,transparent 1px);
  background-size:60px 60px;
  transform:perspective(400px) rotateX(60deg);
  transform-origin:bottom center;
  mask-image:linear-gradient(to top,rgba(0,0,0,0.8) 0%,transparent 100%);
}
.road-strip {
  position:absolute;bottom:0;left:0;right:0;height:100px;
  background:linear-gradient(to top,#111318 0%,transparent 100%);
}
.road-line {
  position:absolute;bottom:40px;left:-200px;
  height:3px;width:100px;background:rgba(232,255,0,0.5);border-radius:2px;
  animation:roadline 2.2s linear infinite;
}
.road-line:nth-child(2){animation-delay:-0.73s;}
.road-line:nth-child(3){animation-delay:-1.46s;}
@keyframes roadline{from{left:-200px;}to{left:calc(100% + 200px);}}
.speed-line {
  position:absolute;height:1.5px;
  background:linear-gradient(90deg,transparent,rgba(0,212,255,0.6),transparent);
  border-radius:1px;animation:speedline 1.8s linear infinite;opacity:0;
}
@keyframes speedline{
  0%{left:-300px;opacity:0;width:80px;}
  10%{opacity:1;}90%{opacity:0.6;}
  100%{left:110%;opacity:0;width:180px;}
}
.car-svg {
  position:absolute;bottom:45px;left:-320px;
  animation:carDrive 12s linear infinite;
  filter:drop-shadow(0 10px 40px rgba(0,212,255,0.5));
}
@keyframes carDrive{
  0%{left:-320px;opacity:0;}5%{opacity:1;}
  90%{opacity:1;}100%{left:calc(100% + 320px);opacity:0;}
}

/* ── HERO HEADER ── */
.hero {
  text-align:center;padding:48px 0 32px;position:relative;z-index:10;
  animation:fadeDown 0.8s ease both;
}
.badge {
  display:inline-flex;align-items:center;gap:8px;
  background:rgba(232,255,0,0.1);border:1px solid rgba(232,255,0,0.3);
  border-radius:100px;padding:6px 16px;
  font-family:'Space Mono',monospace;font-size:11px;
  color:var(--accent);letter-spacing:2px;text-transform:uppercase;
  margin-bottom:18px;
}
.badge-dot{width:6px;height:6px;background:var(--accent);border-radius:50%;animation:blink 1.5s ease infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
.hero h1 {
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(56px,10vw,100px);
  letter-spacing:4px;line-height:0.95;
  background:linear-gradient(135deg,#fff 30%,#00d4ff 70%,#e8ff00 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.hero p { color:var(--muted);font-size:14px;font-weight:300;margin-top:10px; }

/* ── CARD ── */
.pred-card {
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:24px;
  backdrop-filter:blur(20px);
  padding:36px;
  box-shadow:0 40px 80px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.07);
  position:relative;z-index:10;
  animation:fadeUp 0.9s ease both;animation-delay:0.15s;
  margin-bottom:32px;
}
.sec-title {
  font-family:'Space Mono',monospace;font-size:10px;
  letter-spacing:3px;text-transform:uppercase;color:var(--accent2);
  margin-bottom:18px;display:flex;align-items:center;gap:10px;
}
.sec-title::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(0,212,255,0.3),transparent);}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.08),transparent);margin:20px 0;}

/* ── Streamlit input overrides ── */
.stTextInput input, .stNumberInput input, .stSelectbox select,
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div > input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  border-radius: 10px !important;
  color: #f0f0f0 !important;
  font-family: 'DM Sans', sans-serif !important;
}
div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {
  border-color: rgba(0,212,255,0.5) !important;
  box-shadow: 0 0 0 3px rgba(0,212,255,0.1) !important;
}
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
  font-family: 'Space Mono', monospace !important;
  font-size: 11px !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  color: #888 !important;
}
div[data-baseweb="select"] li { background: #0f1117 !important; color: #f0f0f0 !important; }

/* ── BUTTON ── */
.stButton > button {
  width:100% !important;
  background:linear-gradient(135deg,#e8ff00,#a8c700) !important;
  color:#060810 !important;
  border:none !important;
  border-radius:12px !important;
  font-family:'Bebas Neue',sans-serif !important;
  font-size:20px !important;
  letter-spacing:3px !important;
  padding:16px !important;
  box-shadow:0 4px 30px rgba(232,255,0,0.25) !important;
  transition:transform 0.15s,box-shadow 0.2s !important;
}
.stButton > button:hover {
  transform:translateY(-2px) !important;
  box-shadow:0 8px 40px rgba(232,255,0,0.4) !important;
  filter:brightness(1.08) !important;
}

/* ── PAYLOAD BOX ── */
.payload-box {
  background:rgba(0,0,0,0.4);
  border:1px solid rgba(232,255,0,0.15);
  border-radius:12px;padding:16px;margin:12px 0;
}
.payload-title {
  font-family:'Space Mono',monospace;font-size:10px;
  color:var(--accent);letter-spacing:2px;text-transform:uppercase;margin-bottom:10px;
}
.payload-line { font-family:'Space Mono',monospace;font-size:12px;line-height:1.8; }
.pk { color:#888; } .pv { color:#e8ff00; }

/* ── RESULT ── */
.result-success {
  background:rgba(232,255,0,0.07);border:1px solid rgba(232,255,0,0.3);
  border-radius:14px;padding:24px;margin-top:16px;
  animation:popIn 0.4s cubic-bezier(0.34,1.56,0.64,1) both;
}
.result-error {
  background:rgba(255,60,60,0.08);border:1px solid rgba(255,60,60,0.3);
  border-radius:14px;padding:24px;margin-top:16px;
}
.result-label { font-family:'Space Mono',monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;margin-bottom:6px; }
.result-price { font-family:'Bebas Neue',sans-serif;font-size:52px;color:var(--accent);line-height:1;letter-spacing:2px; }
.result-sub { font-size:13px;color:var(--muted);margin-top:4px; }
.result-err-msg { font-family:'Space Mono',monospace;font-size:12px;color:var(--red);line-height:1.7; }

/* footer */
.footer-txt {
  text-align:center;font-family:'Space Mono',monospace;font-size:10px;
  letter-spacing:2px;color:rgba(255,255,255,0.12);padding:32px 0;
  position:relative;z-index:10;
}

@keyframes fadeDown{from{opacity:0;transform:translateY(-24px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeUp{from{opacity:0;transform:translateY(24px);}to{opacity:1;transform:translateY(0);}}
@keyframes popIn{from{opacity:0;transform:scale(0.92);}to{opacity:1;transform:scale(1);}}
</style>

<!-- BACKGROUND SCENE -->
<div class="bg-scene">
  <div class="stars"></div>
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
  <div class="grid-floor"></div>
  <div class="road-strip">
    <div class="road-line"></div>
    <div class="road-line"></div>
    <div class="road-line"></div>
  </div>
  <div class="speed-line" style="bottom:60px;animation-delay:0s;animation-duration:2s;"></div>
  <div class="speed-line" style="bottom:72px;animation-delay:-0.6s;animation-duration:2.3s;"></div>
  <div class="speed-line" style="bottom:48px;animation-delay:-1.2s;animation-duration:1.9s;"></div>
  <svg class="car-svg" width="280" height="110" viewBox="0 0 280 110" fill="none" xmlns="http://www.w3.org/2000/svg">
    <ellipse cx="140" cy="85" rx="120" ry="16" fill="rgba(0,212,255,0.2)" filter="url(#glow)"/>
    <path d="M20 70 Q24 55 60 50 L80 32 Q100 18 140 18 Q180 18 200 32 L220 50 Q256 55 260 70 L260 82 Q260 88 254 88 L26 88 Q20 88 20 82 Z" fill="#1a1e2e" stroke="rgba(0,212,255,0.6)" stroke-width="1.5"/>
    <path d="M82 34 Q100 20 140 20 Q180 20 198 34 L218 50 L80 50 Z" fill="rgba(255,255,255,0.06)"/>
    <path d="M88 34 L102 22 Q120 14 140 14 Q162 14 178 22 L192 34 L162 34 Q150 50 130 50 L96 50 Z" fill="rgba(0,212,255,0.15)" stroke="rgba(0,212,255,0.4)" stroke-width="1"/>
    <line x1="130" y1="14" x2="134" y2="50" stroke="rgba(0,212,255,0.3)" stroke-width="0.8"/>
    <rect x="246" y="56" width="16" height="7" rx="3" fill="#e8ff00" opacity="0.9"/>
    <ellipse cx="262" cy="59.5" rx="12" ry="5" fill="rgba(232,255,0,0.3)" filter="url(#headglow)"/>
    <rect x="18" y="60" width="12" height="7" rx="3" fill="#ff3c3c" opacity="0.9"/>
    <circle cx="72" cy="88" r="18" fill="#0f1117" stroke="rgba(0,212,255,0.5)" stroke-width="2"/>
    <circle cx="72" cy="88" r="10" fill="#1a1e2e" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <circle cx="72" cy="88" r="4" fill="rgba(0,212,255,0.5)"/>
    <circle cx="208" cy="88" r="18" fill="#0f1117" stroke="rgba(0,212,255,0.5)" stroke-width="2"/>
    <circle cx="208" cy="88" r="10" fill="#1a1e2e" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <circle cx="208" cy="88" r="4" fill="rgba(0,212,255,0.5)"/>
    <line x1="72" y1="78" x2="72" y2="98" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="62" y1="88" x2="82" y2="88" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="65" y1="81" x2="79" y2="95" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="65" y1="95" x2="79" y2="81" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="208" y1="78" x2="208" y2="98" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="198" y1="88" x2="218" y2="88" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="201" y1="81" x2="215" y2="95" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <line x1="201" y1="95" x2="215" y2="81" stroke="rgba(0,212,255,0.4)" stroke-width="1.5"/>
    <path d="M30 70 Q100 64 140 66 Q180 64 250 70" stroke="rgba(0,212,255,0.4)" stroke-width="1.5" fill="none"/>
    <defs>
      <filter id="glow"><feGaussianBlur stdDeviation="8"/></filter>
      <filter id="headglow"><feGaussianBlur stdDeviation="4"/></filter>
    </defs>
  </svg>
</div>

<!-- HERO -->
<div class="hero">
  <div class="badge"><span class="badge-dot"></span> ML Powered</div>
  <h1>AutoVal</h1>
  <p>Enter your car specs · Get instant AI price prediction</p>
</div>

<!-- CARD TOP -->
<div class="pred-card">
  <div class="sec-title">Vehicle Details</div>
</div>
""", unsafe_allow_html=True)

# ── INPUTS (pure Streamlit) ──
car_name = st.text_input("Car_Name (e.g. swift, ritz, sx4)", value="swift")
year = st.number_input("Year", min_value=1990, max_value=2026, value=2014, step=1)
present_price = st.number_input("Present_Price (in lakhs)", min_value=0.0, value=5.59, step=0.1)
kms_driven = st.number_input("Kms_Driven", min_value=0, value=40000, step=1000)

st.markdown('<div class="divider"></div><div class="sec-title" style="position:relative;z-index:10;font-family:Space Mono,monospace;font-size:10px;letter-spacing:3px;text-transform:uppercase;color:#00d4ff;margin:12px 0;">Configuration</div>', unsafe_allow_html=True)

fuel_type = st.selectbox("Fuel_Type", ["Petrol", "Diesel", "CNG"])
seller_type = st.selectbox("Seller_Type", ["Dealer", "Individual"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner_label = st.selectbox("Owner", ["0 (First Owner)", "1 (Second Owner)", "3 (Third Owner)"])
owner = int(owner_label.split()[0])

# ── PAYLOAD ──
payload = {
    "Car_Name": str(car_name),
    "Year": int(year),
    "Present_Price": float(present_price),
    "Kms_Driven": int(kms_driven),
    "Fuel_Type": str(fuel_type),
    "Seller_Type": str(seller_type),
    "Transmission": str(transmission),
    "Owner": int(owner),
}

lines_html = "".join(
    f'<div class="payload-line"><span class="pk">"{k}"</span>: <span class="pv">{repr(v) if isinstance(v, str) else v}</span></div>'
    for k, v in payload.items()
)
st.markdown(f"""
<div class="payload-box" style="position:relative;z-index:10;">
  <div class="payload-title">▸ Payload Preview</div>
  {lines_html}
</div>
""", unsafe_allow_html=True)

# ── PREDICT BUTTON ──
if st.button("💰  Predict Price"):
    try:
        res = requests.post(API_URL, json=payload, timeout=20)
        if res.status_code == 200:
            data = res.json()
            pred = data.get("prediction", data.get("predicted_price", data.get("prediction_price", None)))
            if pred is None:
                st.markdown(f"""
                <div class="result-error">
                  <div class="result-label" style="color:#ff3c3c;">⚠ Key Not Found</div>
                  <div class="result-err-msg">API responded but prediction key not found.<br><br>{data}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result-success">
                  <div class="result-label" style="color:#e8ff00;">✓ Predicted Selling Price</div>
                  <div class="result-price">₹ {float(pred):.2f}</div>
                  <div class="result-sub">Lakhs — estimated resale value</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-error">
              <div class="result-label" style="color:#ff3c3c;">✗ API Error {res.status_code}</div>
              <div class="result-err-msg">{res.text}</div>
            </div>""", unsafe_allow_html=True)
    except requests.exceptions.RequestException as e:
        st.markdown(f"""
        <div class="result-error">
          <div class="result-label" style="color:#ff3c3c;">✗ Connection Failed</div>
          <div class="result-err-msg">Could not connect to API. Is FastAPI running?<br><br>{e}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="footer-txt">AUTOVAL ENGINE · POWERED BY ML · © 2025</div>', unsafe_allow_html=True)