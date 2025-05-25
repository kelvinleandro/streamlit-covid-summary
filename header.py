import streamlit as st


def render_header():
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            "# Covid-19 Summary",
        )

    with col2:
        country = st.selectbox(
            label="Select a country",
            options=["all", "brazil", "usa"],
            format_func=lambda x: x.capitalize(),
            key="country_select",
        )

    return country
