"""
Sidebar Component for DermaScan AI
"""
import streamlit as st


def render_sidebar(state_cities):
    """
    Render the sidebar with location selection and information
    
    Args:
        state_cities: Dictionary of states and their cities
        
    Returns:
        tuple: (selected_state, selected_city)
    """
    with st.sidebar:
        st.markdown("### 📍 Location")
        selected_state = st.selectbox(
            "State", 
            list(state_cities.keys()), 
            index=list(state_cities.keys()).index("Delhi")
        )
        cities = state_cities.get(selected_state, ["Other"])
        selected_city = st.selectbox("City", cities, index=0)

        st.markdown("---")
        st.markdown("### 🔬 About DermaScan AI")
        st.markdown("""
        <div class="pro-card" style="font-size:0.85rem;">
            <p style="margin-bottom:0.8rem;">
                Advanced AI-powered dermatology analysis system using deep learning 
                to detect and classify skin conditions.
            </p>
            <p style="margin-bottom:0.5rem;"><strong>🧠 Technology</strong></p>
            <p style="margin-bottom:0.8rem;color:#cbd5e1;">
                • EfficientNet-B3 Architecture<br>
                • 96% AUC-ROC Accuracy<br>
                • Real-time Analysis
            </p>
            <p style="margin-bottom:0.5rem;"><strong>🔬 Detects 13 Conditions</strong></p>
            <p style="margin-bottom:0.8rem;color:#cbd5e1;">
                • 3 Cancer Types<br>
                • 4 Benign Conditions<br>
                • 6 Skin Diseases
            </p>
            <p style="margin-bottom:0.5rem;"><strong>📊 Training Data</strong></p>
            <p style="color:#cbd5e1;">
                • HAM10000 Dataset<br>
                • DermNet Collection<br>
                • 10,000+ Images
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🚨 Emergency Contacts")
        st.markdown("""
        <div class="emergency-card">
            <h4>🇮🇳 India Helplines</h4>
            <p>🚨 Emergency: <b>112</b></p>
            <p>🚑 Ambulance: <b>108</b></p>
            <p>🏥 Health: <b>104</b></p>
            <p>🎗️ Cancer: <b>1800-11-6006</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⚕️ Medical Disclaimer")
        st.markdown("""
        <div style="font-size:0.75rem;color:#94a3b8;line-height:1.5;padding:0.5rem;">
            This AI tool is for educational and screening purposes only. 
            It is NOT a substitute for professional medical diagnosis. 
            Always consult a qualified dermatologist for proper evaluation.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(
            "<p style='text-align:center;color:#94a3b8;font-size:0.75rem;font-weight:600;'>"
            "🏥 DermaScan AI v1.0<br>Medical Grade Analysis</p>",
            unsafe_allow_html=True,
        )
    
    return selected_state, selected_city
