"""
Care Advice Card Component for DermaScan AI
"""
import streamlit as st


def render_care_advice(result):
    """
    Render care advice and risk factors
    
    Args:
        result: Dictionary containing prediction results
    """
    care = result.get("care_advice", [])
    if care:
        st.markdown('<div class="pro-card"><h3>💊 Recommended Care Steps</h3>', unsafe_allow_html=True)
        for i, a in enumerate(care, 1):
            icon = "✓" if not a.startswith("  ") else "→"
            st.markdown(
                f'<div class="info-item">'
                f'<div class="info-item-icon">{icon}</div>'
                f'<div>{a}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    risks = result.get("risk_factors", [])
    if risks:
        st.markdown("")
        risk_html = '<div class="pro-card"><h3>⚠️ Risk Factors</h3>'
        risk_html += '<p style="margin-bottom:1rem;color:#cbd5e1;">Factors that may increase risk:</p>'
        for r in risks:
            risk_html += f'<div class="info-item"><div class="info-item-icon">⚡</div><div>{r}</div></div>'
        risk_html += "</div>"
        st.markdown(risk_html, unsafe_allow_html=True)
