import streamlit as st
import altair as alt
import pandas as pd
from api import get_covid_all_countries


def render_comparison_panel():
    st.subheader("Countries Comparison")

    sort_by = st.selectbox(
        "Sort by",
        options=["cases", "deaths", "recovered"],
        index=0,
        format_func=str.capitalize,
    )

    data = get_covid_all_countries(sort_by)
    if not data or len(data) < 1:
        st.warning("No data available")
        return

    top_five = data[:5]
    df = pd.DataFrame([dict(row) for row in top_five])

    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(
                f"{sort_by}:Q",
                title=sort_by.capitalize(),
                axis=alt.Axis(format="~s"),
            ),
            y=alt.Y("country:N", sort="-x", title="Country"),
            tooltip=[
                alt.Tooltip("country:N", title="Country"),
                alt.Tooltip(f"{sort_by}:Q", title=sort_by.capitalize(), format=","),
            ],
        )
        .properties(width="container", height=400)
    )

    st.altair_chart(chart, use_container_width=True)
