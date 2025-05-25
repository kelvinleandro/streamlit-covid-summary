import streamlit as st
import altair as alt
import pandas as pd
from api import get_covid_historical


def render_timeseries_panel(country: str):
    st.subheader("Timeseries analysis")
    timeseries_feature = st.selectbox(
        "Select timeseries feature",
        options=["cases", "deaths", "recovered"],
    )

    data = get_covid_historical(country)
    timeline = data.timeline if hasattr(data, "timeline") else data
    series = getattr(timeline, timeseries_feature, {})

    if not series:
        st.warning("No data available")
        return

    df = pd.DataFrame(
        {
            "Date": pd.to_datetime(list(series.keys()), format="%m/%d/%y"),
            "Value": list(series.values()),
        }
    )

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("Date:T", title="Date", axis=alt.Axis(format="%Y")),
            y=alt.Y(
                "Value:Q",
                title=f"{timeseries_feature.capitalize()}",
                axis=alt.Axis(format="~s"),
            ),
            tooltip=[
                alt.Tooltip("Date:T", title="Date"),
                alt.Tooltip("Value:Q", title="Value", format=","),
            ],
        )
        .properties(width="container", height=400)
    )

    st.altair_chart(chart, use_container_width=True)
