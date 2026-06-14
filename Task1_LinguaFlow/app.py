import streamlit as st
from googletrans import Translator, LANGUAGES
import time, html as html_module

st.set_page_config(
    page_title="LinguaFlow - AI Language Translator",
    page_icon="x",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #080818 !important; min-height: 100vh; overflow-x: hidden; }
.stApp::before { content:''; position:fixed; top:-200px; left:-200px; width:600px; height:600px; background:radial-gradient(circle,rgba(124,58,237,.18) 0%,transparent 70%); border-radius:50%; pointer-events:none; z-index:0; animation:orb1 8s ease-in-out infinite; }
.stApp::after  { content:''; position:fixed; bottom:-150px; right:-150px; width:500px; height:500px; background:radial-gradient(circle,rgba(59,130,246,.15) 0%,transparent 70%); border-radius:50%; pointer-events:none; z-index:0; animation:orb2 10s ease-in-out infinite; }
@keyframes orb1 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(40px,30px)} }
@keyframes orb2 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-30px,-40px)} }
#MainMenu,footer,header,.stDeployButton { visibility:hidden !important; }
.block-container { padding: 0 3rem 2rem !important; max-width:1400px !important; }
.hero-wrap { text-align:center; padding:3rem 1rem 2rem; position:relative; z-index:1; }
.hero-badge { display:inline-block; background:rgba(124,58,237,.15); border:1px solid rgba(124,58,237,.4); color:#a78bfa; font-size:.72rem; font-weight:600; letter-spacing:.15em; text-transform:uppercase; padding:.35rem 1rem; border-radius:50px; margin-bottom:1.2rem; }
.hero-title { font-size:clamp(2.5rem,5vw,3.8rem); font-weight:800; line-height:1.1; margin-bottom:1rem; background:linear-gradient(135deg,#e2e8f0 0%,#a78bfa 40%,#60a5fa 70%,#34d399 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-sub { color:#64748b; font-size:1.05rem; max-width:480px; margin:0 auto 2rem; line-height:1.6; }
.stats-row { display:flex; justify-content:center; gap:3rem; margin-bottom:.5rem; }
.stat-item { text-align:center; }
.stat-num { font-size:1.5rem; font-weight:700; color:#e2e8f0; }
.stat-lbl { font-size:.72rem; color:#475569; text-transform:uppercase; letter-spacing:.1em; }
.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,.08),transparent); margin:.5rem 0 2rem; }
.xlate-panel { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.08); border-radius:24px; overflow:hidden; box-shadow:0 24px 80px rgba(0,0,0,.6),inset 0 0 0 1px rgba(255,255,255,.04); position:relative; z-index:1; }
.panel-inner { padding:1.8rem; }
.panel-hdr { display:flex; align-items:center; justify-content:space-between; margin-bottom:.8rem; }
.panel-lbl { font-size:.72rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:#cbd5e1; }
.char-cc { font-size:.72rem; color:#334155; }
.char-warn { color:#f59e0b !important; }
.char-danger { color:#ef4444 !important; }
div[data-baseweb="select"] > div { background:rgba(255,255,255,.04) !important; border:1px solid rgba(255,255,255,.1) !important; border-radius:10px !important; color:#e2e8f0 !important; font-size:.9rem !important; transition:border-color .2s; }
div[data-baseweb="select"] > div:hover { border-color:rgba(124,58,237,.6) !important; background:rgba(124,58,237,.06) !important; }
div[data-baseweb="popover"] { background:#0f0f23 !important; border:1px solid rgba(255,255,255,.1) !important; border-radius:12px !important; }
li[role="option"] { color:#cbd5e1 !important; font-size:.9rem !important; }
li[role="option"]:hover { background:rgba(124,58,237,.15) !important; }
li[role="option"][aria-selected="true"] { background:rgba(124,58,237,.25) !important; color:#a78bfa !important; }
.stTextArea > div > div > textarea { background:rgba(255,255,255,.03) !important; border:1px solid rgba(255,255,255,.07) !important; border-radius:14px !important;  font-size:1.05rem !important; line-height:1.7 !important; font-family:'Inter',sans-serif !important; padding:1rem !important; transition:border-color .2s !important; }color:#ffffff !important;color:#ffffff !important;
font-weight:600 !important;
.stTextArea > div > div > textarea:focus { border-color:rgba(124,58,237,.5) !important; box-shadow:0 0 0 3px rgba(124,58,237,.12) !important; }
.stTextArea > div > div > textarea::placeholder { color:#94a3b8 !important; }
.stTextArea > div { border:none !important; background:transparent !important; }
.result-box { background:rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.07); border-radius:14px; padding:1rem; min-height:180px; color:#cbd5e1; font-size:1.05rem; line-height:1.7; white-space:pre-wrap; word-break:break-word; }
.result-ph { background:rgba(255,255,255,.02); border:1px solid rgba(255,255,255,.05); border-radius:14px; padding:1rem; min-height:180px; color:#1e293b; font-size:1.05rem; font-style:italic; }
.detected-badge { display:inline-flex; align-items:center; gap:.4rem; background:rgba(52,211,153,.1); border:1px solid rgba(52,211,153,.3); color:#34d399; font-size:.72rem; font-weight:600; padding:.3rem .8rem; border-radius:50px; margin-bottom:.8rem; }
.stButton > button { background:transparent !important; border:1px solid rgba(255,255,255,.1) !important; border-radius:8px !important; color:#64748b !important; font-size:.8rem !important; padding:.4rem .8rem !important; transition:all .2s !important; font-family:'Inter',sans-serif !important; }
.stTextArea > div > div > textarea::placeholder { 
    color:#94a3b8 !important; 
}
.cta-btn > div > button { background:linear-gradient(135deg,#7c3aed 0%,#3b82f6 100%) !important; border:none !important; border-radius:16px !important; color:#ffffff !important;
font-weight:500 !important; font-size:1.1rem !important; font-weight:700 !important; padding:1rem 3rem !important; box-shadow:0 8px 32px rgba(124,58,237,.45) !important; transition:all .25s !important; }
.cta-btn > div > button:hover { transform:translateY(-3px) !important; box-shadow:0 16px 48px rgba(124,58,237,.6) !important; }
.swap-btn > div > button { background:rgba(124,58,237,.1) !important; border:1px solid rgba(124,58,237,.3) !important; border-radius:50% !important; color:#a78bfa !important; width:44px !important; height:44px !important; padding:0 !important; font-size:1.1rem !important; transition:all .25s !important; }
.swap-btn > div > button:hover { background:rgba(124,58,237,.25) !important; transform:rotate(180deg) !important; }
div[data-testid="metric-container"] { background:rgba(255,255,255,.03) !important; border:1px solid rgba(255,255,255,.06) !important; border-radius:14px !important; padding:1.2rem !important; text-align:center !important; }
div[data-testid="metric-container"] label { color:#475569 !important; font-size:.72rem !important; text-transform:uppercase !important; letter-spacing:.1em !important; }
div[data-testid="stMetricValue"] { color:#e2e8f0 !important; font-size:1.6rem !important; font-weight:700 !important; }
details { background:rgba(255,255,255,.02) !important; border:1px solid rgba(255,255,255,.06) !important; border-radius:14px !important; }
summary { color:#64748b !important; font-size:.85rem !important; padding:1rem !important; }
.footer-w { text-align:center; padding:2.5rem 0 1.5rem; color:#1e293b; font-size:.82rem; position:relative; z-index:1; }
.footer-w strong { color:#334155; }
div[data-testid="stSpinner"] div { border-top-color:#a78bfa !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def get_translator(): return Translator()

@st.cache_data(show_spinner=False)
def build_opts():
    opts = {"Auto Detect": "auto"}
    for code, name in LANGUAGES.items(): opts[name.title()] = code
    return dict(sorted(opts.items(), key=lambda x: (x[0] != "Auto Detect", x[0])))

lang_opts  = build_opts()
src_names  = list(lang_opts.keys())
tgt_names  = [n for n in src_names if n != "Auto Detect"]
LANG_COUNT = len(tgt_names)

for k, v in {"translated":"","detected":"","src_idx":0,"tgt_idx":tgt_names.index("Spanish") if "Spanish" in tgt_names else 0,"last_inp":""}.items():
    if k not in st.session_state: st.session_state[k] = v

st.markdown(f"""
<div class="hero-wrap">
  <div class="hero-badge">Powered by Google Translate API</div>
  <h1 class="hero-title">LinguaFlow</h1>
  <p class="hero-sub">Break every language barrier instantly.<br>Translate across {LANG_COUNT}+ languages with AI precision.</p>
  <div class="stats-row">
    <div class="stat-item"><div class="stat-num">{LANG_COUNT}+</div><div class="stat-lbl">Languages</div></div>
    <div class="stat-item"><div class="stat-num">5K</div><div class="stat-lbl">Char Limit</div></div>
    <div class="stat-item"><div class="stat-num">Free</div><div class="stat-lbl">Forever</div></div>
  </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

c_from, c_swap, c_to = st.columns([6,1,6])
with c_from:
    sel_src = st.selectbox("From", src_names, index=st.session_state.src_idx, key="sel_src", label_visibility="collapsed")
with c_swap:
    st.markdown('<div class="swap-btn">', unsafe_allow_html=True)
    if st.button("⇄", key="swapbtn", help="Swap languages"):
        if sel_src != "Auto Detect":
            old_tgt = tgt_names[st.session_state.tgt_idx]
            st.session_state.src_idx = src_names.index(old_tgt)
            if sel_src in tgt_names: st.session_state.tgt_idx = tgt_names.index(sel_src)
            if st.session_state.translated: st.session_state.last_inp = st.session_state.translated
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with c_to:
    sel_tgt = st.selectbox("To", tgt_names, index=st.session_state.tgt_idx, key="sel_tgt", label_visibility="collapsed")

st.session_state.src_idx = src_names.index(sel_src)
st.session_state.tgt_idx = tgt_names.index(sel_tgt)

st.markdown("<br>", unsafe_allow_html=True)

left_col, right_col = st.columns(2, gap="medium")

with left_col:
    inp_cc = len(st.session_state.last_inp)
    cc_cls = "char-danger" if inp_cc > 4800 else ("char-warn" if inp_cc > 4000 else "char-cc")
    st.markdown(f'<div class="xlate-panel"><div class="panel-inner"><div class="panel-hdr"><span class="panel-lbl">Source Text</span><span class="{cc_cls}">{inp_cc} / 5000</span></div>', unsafe_allow_html=True)
    inp = st.text_area("src", value=st.session_state.last_inp, placeholder="Type or paste your text here...", height=220, max_chars=5000, key="src_ta", label_visibility="collapsed")
    st.session_state.last_inp = inp
    if inp:
        if st.button("Clear source", key="clr_src"): st.session_state.last_inp=""; st.session_state.translated=""; st.session_state.detected=""; st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="xlate-panel"><div class="panel-inner"><div class="panel-hdr"><span class="panel-lbl">Translation</span></div>', unsafe_allow_html=True)
    if st.session_state.translated:
        if st.session_state.detected and sel_src == "Auto Detect":
            st.markdown(f'<div class="detected-badge">Detected: {html_module.escape(st.session_state.detected)}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-box">{html_module.escape(st.session_state.translated)}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        with bc1: st.code(st.session_state.translated, language=None)
        with bc2:
            if st.button("Clear result", key="clr_tgt"): st.session_state.translated=""; st.session_state.detected=""; st.rerun()
    else:
        st.markdown(f'<div class="result-ph">Translation of your text will appear here...</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
_, btn_col, _ = st.columns([3,2,3])
with btn_col:
    st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
    clicked = st.button("Translate Now", key="translate_btn", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

if clicked:
    if not inp or not inp.strip():
        st.warning("Please enter some text before translating.")
    else:
        sc = lang_opts[sel_src]; tc = lang_opts[sel_tgt]
        if sc != "auto" and sc == tc:
            st.info("Source and target language are the same.")
        else:
            with st.spinner("Translating..."):
                try:
                    t = get_translator()
                    res = t.translate(inp, src=sc, dest=tc)
                    st.session_state.translated = res.text
                    if sc == "auto":
                        try:
                            d = t.detect(inp)
                            st.session_state.detected = LANGUAGES.get(d.lang, d.lang).title()
                        except: st.session_state.detected = ""
                    time.sleep(0.2)
                    st.success(f"Translation complete: {sel_src} to {sel_tgt}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Translation failed: {e}")
                    st.session_state.translated = ""

if st.session_state.translated:
    st.markdown("<br>", unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    iw = len(inp.split()) if inp else 0
    ow = len(st.session_state.translated.split())
    oc = len(st.session_state.translated)
    rt = round(oc / max(len(inp),1), 2) if inp else 0
    with m1: st.metric("Input Words",  iw)
    with m2: st.metric("Output Words", ow)
    with m3: st.metric("Characters",   oc)
    with m4: st.metric("Length Ratio", f"{rt}x")

st.markdown("<br>", unsafe_allow_html=True)
with st.expander(f"Browse all {LANG_COUNT}+ Supported Languages"):
    sl = sorted(LANGUAGES.values())
    cols = st.columns(5); ch = len(sl)//5+1
    for i,col in enumerate(cols):
        with col:
            for lang in sl[i*ch:(i+1)*ch]: st.markdown(f"- {lang.title()}")

st.markdown('<div class="footer-w">Built with love | <strong>LinguaFlow v2.0</strong> | Powered by <strong>Streamlit</strong> + <strong>Google Translate</strong></div>', unsafe_allow_html=True)
