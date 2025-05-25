import streamlit as st
import asyncio
from api import get_covid_all
from header import render_header
from general_panel import render_general_panel
from timeseries import render_timeseries_panel

st.set_page_config(layout="wide")

country = render_header()

data = asyncio.run(get_covid_all(country))
render_general_panel(data)

c1, c2, c3 = st.columns(3)
with c1:
    render_timeseries_panel(country)
