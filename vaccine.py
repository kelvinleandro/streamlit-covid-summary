import streamlit as st
import altair as alt
import pandas as pd
from api import get_vaccine_coverage


def render_vaccine_panel(country: str):
    st.subheader("Vaccine coverage")

    data = get_vaccine_coverage(country)
    timeline = data.timeline if hasattr(data, "timeline") else data

    if not timeline:
        st.warning("No data available")
        return

    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(list(timeline.keys()), format="%m/%d/%y"),
            "Value": list(timeline.values()),
        }
    )

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("Date:T", title="Year", axis=alt.Axis(format="%Y")),
            y=alt.Y(
                "Value:Q",
                title="Coverage",
                axis=alt.Axis(format="~s", tickMinStep=1e9),
            ),
            tooltip=[
                alt.Tooltip("Date:T", title="Date"),
                alt.Tooltip("Value:Q", title="Coverage", format=","),
            ],
        )
        .properties(width="container", height=400)
    )

    st.altair_chart(chart, use_container_width=True)
