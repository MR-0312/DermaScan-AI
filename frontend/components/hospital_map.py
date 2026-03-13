"""
Hospital Map Component for DermaScan AI
"""
import streamlit as st


def render_hospital_map(result, selected_city, selected_state):
    """
    Render the hospital finder with embedded Google Maps
    
    Args:
        result: Dictionary containing prediction results
        selected_city: Selected city name
        selected_state: Selected state name
    """
    hosp_type = result.get("hospital_type", "Dermatologist")
    location = result.get("hospital_location", f"{selected_city}, {selected_state}")

    st.markdown(
        f'<div class="pro-card">'
        f"<h3>🏥 Find {hosp_type}</h3>"
        f"<p>📍 Searching in: <strong>{location}</strong></p>"
        f"</div>",
        unsafe_allow_html=True,
    )

    search_query = result.get("hospital_search_query", "dermatologist near me")
    full_query = f"{search_query} in {selected_city}, {selected_state}, India"
    maps_url = "https://www.google.com/maps/search/" + full_query.replace(" ", "+")
    
    # Embed Google Maps
    maps_embed_url = f"https://www.google.com/maps/embed/v1/search?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q={full_query.replace(' ', '+')}"
    
    st.markdown(
        f'<div class="map-container">'
        f'<iframe width="100%" height="450" style="border:0;" '
        f'src="{maps_embed_url}" allowfullscreen loading="lazy"></iframe>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.link_button(
        f"🗺️ Open in Google Maps - {hosp_type}",
        maps_url,
        width="stretch",
    )

    st.markdown("")

    emergency = result.get("emergency_numbers", {})
    if emergency:
        emer_html = '<div class="emergency-card"><h4>🚨 Emergency Contacts</h4>'
        for label, num in emergency.items():
            emer_html += f"<p>📞 {label}: <b>{num}</b></p>"
        emer_html += "</div>"
        st.markdown(emer_html, unsafe_allow_html=True)
