"""
Confidence Chart Component for DermaScan AI
"""
import streamlit as st
import plotly.graph_objects as go


def render_confidence_chart(result):
    """
    Render the confidence analysis chart
    
    Args:
        result: Dictionary containing prediction results
    """
    probs = result.get("all_probabilities", {})
    sorted_p = dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))
    names = list(sorted_p.keys())
    vals = list(sorted_p.values())

    cancer_set = {"Melanoma", "Basal Cell Carcinoma", "Actinic Keratoses"}
    benign_set = {
        "Melanocytic Nevi",
        "Benign Keratosis",
        "Dermatofibroma",
        "Vascular Lesions",
    }

    colors = []
    for n in names:
        if n == result["predicted_class"]:
            colors.append("#3b82f6")
        elif n in cancer_set:
            colors.append("#ef4444")
        elif n in benign_set:
            colors.append("#10b981")
        else:
            colors.append("#60a5fa")

    fig = go.Figure(
        go.Bar(
            x=vals,
            y=names,
            orientation="h",
            marker_color=colors,
            text=[f"{v:.1%}" for v in vals],
            textposition="outside",
            textfont=dict(color="#f1f5f9", size=12, family="Inter"),
        )
    )

    fig.update_layout(
        height=450,
        margin=dict(l=10, r=80, t=20, b=20),
        xaxis=dict(
            range=[0, min(1.0, max(vals) * 1.5)],
            tickfont=dict(color="#94a3b8", family="Inter"),
            gridcolor="#334155",
            title=None,
            showgrid=True,
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color="#f1f5f9", size=12, family="Inter"),
        ),
        plot_bgcolor="#1e293b",
        paper_bgcolor="#0f172a",
        font=dict(color="#f1f5f9", family="Inter"),
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown(
        '<div class="chart-legend">'
        '<span class="legend-item"><span style="color:#3b82f6;font-size:1.2rem;">●</span> Predicted</span>'
        '<span class="legend-item"><span style="color:#ef4444;font-size:1.2rem;">●</span> Cancer</span>'
        '<span class="legend-item"><span style="color:#10b981;font-size:1.2rem;">●</span> Benign</span>'
        '<span class="legend-item"><span style="color:#60a5fa;font-size:1.2rem;">●</span> Disease</span>'
        "</div>",
        unsafe_allow_html=True,
    )
