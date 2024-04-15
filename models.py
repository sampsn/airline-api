from pydantic import BaseModel as bm
from enum import Enum


class Airline(Enum):
    DELTA = "Delta"
    SOUTHWEST = "Southwest"
    ALASKA = "Alaska"


class Flight(bm):
    flight_num: str
    capacity: int
    estimated_flight_duration: int


class FlightRequest(bm):
    capacity: int
    estimated_flight_duration: int
