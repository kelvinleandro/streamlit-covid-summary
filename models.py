from pydantic import BaseModel
from typing import Dict, Optional


class CovidAll(BaseModel):
    cases: int
    deaths: int
    recovered: int
    active: int


class CountriesCovidAll(CovidAll):
    country: str


TimeLine = Dict[str, int]


class CovidHistoricalTimeline(BaseModel):
    cases: TimeLine
    deaths: TimeLine
    recovered: TimeLine


class CovidHistoricalCountry(BaseModel):
    country: str
    timeline: CovidHistoricalTimeline


class CovidVaccineCountryCoverage(BaseModel):
    country: str
    timeline: TimeLine
