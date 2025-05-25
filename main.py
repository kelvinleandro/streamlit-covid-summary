import streamlit as st
from api import get_covid_all
from comparison_hbar import render_comparison_panel
from header import render_header
from general_panel import render_general_panel
from timeseries import render_timeseries_panel
from vaccine import render_vaccine_panel

st.set_page_config(layout="wide")

country = render_header()

data = get_covid_all(country)
render_general_panel(data)

c1, c2, c3 = st.columns(3)
with c1:
    render_timeseries_panel(country)

with c2:
    render_comparison_panel()

with c3:
    render_vaccine_panel(country)
