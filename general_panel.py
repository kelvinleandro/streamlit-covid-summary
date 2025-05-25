import streamlit as st
from models import CovidAll


def render_general_panel(data: CovidAll):
    format_millions = lambda x: f"{x / 1_000_000:.2f}M"

    cols = st.columns(4)

    with cols[0]:
        st.metric(label="Cases", value=format_millions(data.cases))

    with cols[1]:
        st.metric(label="Deaths", value=format_millions(data.deaths))

    with cols[2]:
        st.metric(label="Recovered", value=format_millions(data.recovered))

    with cols[3]:
        st.metric(label="Active", value=format_millions(data.active))
