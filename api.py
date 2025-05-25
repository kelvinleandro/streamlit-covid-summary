import streamlit as st
import asyncio
import httpx
from typing import Union, List
from models import (
    CovidAll,
    CountriesCovidAll,
    CovidHistoricalTimeline,
    CovidHistoricalCountry,
    CovidVaccineCountryCoverage,
    TimeLine,
)

BASE_URL = "https://disease.sh/v3/covid-19"


async def get_covid_all_global() -> CovidAll:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/all")
        response.raise_for_status()
        return CovidAll(**response.json())


async def get_covid_all_by_country(country: str) -> CovidAll:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/countries/{country}", params={"strict": True}
        )
        response.raise_for_status()
        return CovidAll(**response.json())


async def get_covid_all_async(country: str = "all") -> CovidAll:
    normalized = country.strip().lower()
    return (
        await get_covid_all_global()
        if normalized == "all"
        else await get_covid_all_by_country(normalized)
    )


@st.cache_data
def get_covid_all(country: str = "all") -> CovidAll:
    return asyncio.run(get_covid_all_async(country))


async def get_covid_all_countries_async(
    sort_by: str = "cases",
) -> List[CountriesCovidAll]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/countries", params={"sort": sort_by})
        response.raise_for_status()
        return [CountriesCovidAll(**item) for item in response.json()]


def get_covid_all_countries(sort_by: str = "cases") -> List[CountriesCovidAll]:
    return asyncio.run(get_covid_all_countries_async(sort_by))


async def get_covid_historical_async(
    country: str = "all",
) -> Union[CovidHistoricalTimeline, CovidHistoricalCountry]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/historical/{country}", params={"lastdays": "all"}
        )
        response.raise_for_status()
        data = response.json()

        if "timeline" in data:
            return CovidHistoricalCountry(**data)
        else:
            return CovidHistoricalTimeline(**data)


@st.cache_data
def get_covid_historical(
    country: str = "all",
) -> Union[CovidHistoricalTimeline, CovidHistoricalCountry]:
    return asyncio.run(get_covid_historical_async(country))


async def get_vaccine_coverage_all() -> TimeLine:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/vaccine/coverage",
            params={"lastdays": "all", "fullData": False},
        )
        response.raise_for_status()
        return response.json()


async def get_vaccine_coverage_by_country(country: str) -> CovidVaccineCountryCoverage:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/vaccine/coverage/countries/{country}",
            params={"lastdays": "all", "fullData": False},
        )
        response.raise_for_status()
        return CovidVaccineCountryCoverage(**response.json())


async def get_vaccine_coverage_async(
    country: str = "all",
) -> Union[TimeLine, CovidVaccineCountryCoverage]:
    normalized = country.strip().lower()
    return (
        await get_vaccine_coverage_all()
        if normalized == "all"
        else await get_vaccine_coverage_by_country(normalized)
    )


@st.cache_data
def get_vaccine_coverage(
    country: str = "all",
) -> Union[TimeLine, CovidVaccineCountryCoverage]:
    return asyncio.run(get_vaccine_coverage_async(country))
