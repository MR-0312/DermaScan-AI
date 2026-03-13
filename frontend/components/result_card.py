"""
Result Card Components for DermaScan AI
"""
import streamlit as st

TIER_ICONS = {
    "CANCER": "🔴",
    "PRE-CANCER": "🟡",
    "BENIGN": "🟢",
    "DISEASE": "🔵",
}


def render_severity_banner(result):
    """Render the severity banner"""
    severity = result.get("severity", "LOW").lower()
    tagline = result.get("tagline", "Analysis Complete")
    action = result.get("action", "Consult a doctor")
    
    severity_emoji = {
        "critical": "🚨",
        "high": "⚠️",
        "medium": "⚡",
        "low": "✅"
    }.get(severity, "ℹ️")

    st.markdown(
        f'<div class="severity-banner banner-{severity}">'
        f"<h2>{severity_emoji} {tagline}</h2>"
        f"<h3>📋 {action}</h3>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_metrics(result):
    """Render the key metrics cards"""
    c1, c2, c3 = st.columns(3)
    
    conf = result["confidence"]
    conf_color = "#10b981" if conf > 0.7 else "#f59e0b" if conf > 0.4 else "#ef4444"
    conf_emoji = "🎯" if conf > 0.7 else "⚡" if conf > 0.4 else "⚠️"
    
    tier = result.get("tier", "UNKNOWN")
    tier_icon = TIER_ICONS.get(tier, "⚪")
    tier_color = {
        "CANCER": "#ef4444",
        "PRE-CANCER": "#f59e0b",
        "BENIGN": "#10b981",
        "DISEASE": "#3b82f6",
    }.get(tier, "#94a3b8")

    with c1:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Confidence Score</div>'
            f'<div class="value" style="color:{conf_color};">{conf_emoji} {conf:.1%}</div>'
            f'<div class="sublabel">{result.get("confidence_level", "")}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Classification</div>'
            f'<div class="value" style="color:{tier_color};">{tier_icon} {tier}</div>'
            f'<div class="sublabel">{result.get("severity", "")} Severity</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f'<div class="metric-card">'
            f'<div class="label">Diagnosis</div>'
            f'<div class="value" style="font-size:1.3rem;color:#3b82f6;">🔬 {result["predicted_class"]}</div>'
            f'<div class="sublabel">AI Prediction</div>'
            f"</div>",
            unsafe_allow_html=True,
        )
