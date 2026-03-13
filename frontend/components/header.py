"""
Header Component for DermaScan AI
"""
import streamlit as st


def render_header():
    """Render the professional medical header"""
    st.markdown("""
    <div class="medical-header">
        <div class="medical-header-content">
            <h1>🏥 DermaScan AI</h1>
            <p class="subtitle">Advanced AI-Powered Dermatology Analysis System</p>
            <div class="badges">
                <span class="badge">🧠 EfficientNet-B3</span>
                <span class="badge">📊 96% AUC-ROC</span>
                <span class="badge">🔬 13 Conditions</span>
                <span class="badge">🇮🇳 India Optimized</span>
                <span class="badge">⚡ Real-time Analysis</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
