"""
=================================================================
DERMASCAN-AI — Professional Medical UI
Production Grade Healthcare Interface
=================================================================
"""

import json
import streamlit as st
import requests
from PIL import Image
from pathlib import Path

# Import components
from components.header import render_header
from components.sidebar import render_sidebar
from components.result_card import render_severity_banner, render_metrics, TIER_ICONS
from components.confidence_chart import render_confidence_chart
from components.care_advice_card import render_care_advice
from components.hospital_map import render_hospital_map

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="DermaScan AI | Advanced Dermatology Analysis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"

# ═══════════════════════════════════════════════════════════
# LOAD EXTERNAL DATA & STYLES
# ═══════════════════════════════════════════════════════════
config_dir = Path(__file__).parent.parent / "configs"

with open(config_dir / "india_cities.json", "r", encoding="utf-8") as f:
    STATE_CITIES = json.load(f)

# Load CSS
css_file = Path(__file__).parent / "assets" / "style.css"
with open(css_file, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Remove tooltips with JavaScript
st.markdown("""
<script>
// Remove all title attributes that cause tooltips
document.addEventListener('DOMContentLoaded', function() {
    function removeTooltips() {
        const elements = document.querySelectorAll('[title]');
        elements.forEach(el => {
            if (el.getAttribute('title') === 'keyboard_double') {
                el.removeAttribute('title');
            }
        });
    }
    
    // Run immediately
    removeTooltips();
    
    // Run periodically to catch dynamically added elements
    setInterval(removeTooltips, 500);
    
    // Also run on mutations
    const observer = new MutationObserver(removeTooltips);
    observer.observe(document.body, { 
        childList: true, 
        subtree: true,
        attributes: true,
        attributeFilter: ['title']
    });
});
</script>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
selected_state, selected_city = render_sidebar(STATE_CITIES)

# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════
render_header()

# ═══════════════════════════════════════════════════════════
# UPLOAD SECTION
# ═══════════════════════════════════════════════════════════
uploaded_file = st.file_uploader(
    "Upload a skin image for analysis",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file:
    img_col, action_col = st.columns([1, 2])

    with img_col:
        image = Image.open(uploaded_file)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, caption="📸 Uploaded Image", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with action_col:
        st.markdown(f"**📍 Location:** {selected_city}, {selected_state}")
        st.markdown("")

        analyze = st.button("🔬 Analyze Image", width="stretch")

        if analyze:
            with st.spinner("🔄 Analyzing your image with AI..."):
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type,
                        )
                    }
                    params = {"city": selected_city, "state": selected_state}

                    resp = requests.post(
                        f"{API_URL}/predict",
                        files=files,
                        params=params,
                        timeout=60,
                    )

                    if resp.status_code == 200:
                        st.session_state["result"] = resp.json()
                        st.success("✅ Analysis complete!")
                        st.rerun()
                    else:
                        st.error(f"❌ Server error: {resp.text}")

                except requests.exceptions.ConnectionError:
                    st.error(
                        "⚠️ Cannot connect to API server. "
                        "Open another terminal and run: `python -m api.app`"
                    )

        st.markdown("""
        <div class="pro-card">
            <h3>💡 Tips for Best Results</h3>
            <p>
                ✓ Use a clear, well-lit close-up photo<br>
                ✓ Center the affected area in the frame<br>
                ✓ Keep camera 10-15 cm from the skin<br>
                ✓ Avoid shadows and reflections<br>
                ✓ Use natural lighting when possible
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# RESULTS SECTION
# ═══════════════════════════════════════════════════════════
if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("---")

    # Severity Banner
    render_severity_banner(result)

    # Key Metrics
    render_metrics(result)

    # Cancer Warning
    cancer_warning = result.get("cancer_warning", "")
    if cancer_warning:
        st.markdown(
            f'<div class="warning-box">'
            f'<div class="warning-box-icon">⚠️</div>'
            f"<div><strong>MEDICAL ALERT:</strong> {cancer_warning}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Diagnosis", "📊 Confidence Analysis", "💊 Care Advice", "🏥 Find Hospitals"]
    )

    # Tab 1: Diagnosis
    with tab1:
        st.markdown(
            f'<div class="pro-card">'
            f'<h3>🔬 {result["predicted_class"]}</h3>'
            f'<p>{result.get("description", "")}</p>'
            f'<p style="margin-top:1rem;padding:0.8rem;background:#334155;border-radius:8px;">'
            f'<strong>⏰ {result.get("urgency_message", "")}</strong></p>'
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="pro-card">'
            f"<h3>🎯 AI Confidence Assessment</h3>"
            f'<p>{result.get("confidence_message", "")}</p>'
            f"</div>",
            unsafe_allow_html=True,
        )

        diff = result.get("differential_diagnosis", [])
        if len(diff) > 1:
            diff_html = '<div class="pro-card"><h3>🔍 Differential Diagnosis</h3>'
            diff_html += '<p style="margin-bottom:1rem;color:#cbd5e1;">Other possible conditions to consider:</p>'
            for d in diff:
                d_icon = TIER_ICONS.get(d.get("tier", ""), "⚪")
                d_prob = d.get("probability", 0)
                diff_html += (
                    f'<div class="info-item">'
                    f'<div class="info-item-icon">{d_icon}</div>'
                    f'<div><strong>{d["class_name"]}</strong> — Probability: {d_prob:.1%}</div>'
                    f"</div>"
                )
            diff_html += "</div>"
            st.markdown(diff_html, unsafe_allow_html=True)

    # Tab 2: Confidence Chart
    with tab2:
        render_confidence_chart(result)

    # Tab 3: Care Advice
    with tab3:
        render_care_advice(result)

    # Tab 4: Hospitals
    with tab4:
        render_hospital_map(result, selected_city, selected_state)

    # Disclaimer
    disclaimer = result.get(
        "disclaimer",
        "This is an AI tool for educational purposes only. "
        "Not a substitute for professional medical diagnosis.",
    )
    st.markdown(
        f'<div class="disclaimer-box">'
        f"<strong>⚕️ MEDICAL DISCLAIMER:</strong> {disclaimer}"
        f"</div>",
        unsafe_allow_html=True,
    )

    inf_t = result.get("inference_time", 0)
    st.markdown(
        f'<p style="text-align:center;color:#94a3b8;font-size:0.85rem;margin-top:1.5rem;">'
        f'⚡ Analysis completed in {inf_t:.2f}s | 🧠 EfficientNet-B3 | 🏥 DermaScan AI v1.0'
        f'</p>',
        unsafe_allow_html=True
    )

elif not uploaded_file:
    st.markdown(
        '<div class="upload-placeholder">'
        '<div class="icon">📸</div>'
        "<h3>Upload a Skin Image to Begin Analysis</h3>"
        "<p>Our advanced AI system will analyze the image, identify potential conditions, "
        "provide personalized care recommendations, and help you locate nearby medical facilities.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

# ═══════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#94a3b8;font-size:0.8rem;line-height:1.8;'>"
    "🏥 <strong>DermaScan AI</strong> | 🧠 EfficientNet-B3 Architecture | 📊 HAM10000 + DermNet Dataset<br>"
    "🔬 13 Skin Conditions | 🎯 96% AUC-ROC Accuracy | ⚡ Real-time Analysis<br>"
    "🛠️ Built with PyTorch • FastAPI • Streamlit<br>"
    "<em>For educational and research purposes only. Not a substitute for professional medical advice.</em>"
    "</p>",
    unsafe_allow_html=True,
)
