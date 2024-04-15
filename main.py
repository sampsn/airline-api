"""
Have these endpoints:

GET / -> list[airline_name]
GET /:airline_name -> list[flight_num]
GET /:airline_name/:flight_num -> Flight

POST /:airline
PUT /:airline/:flight_num
DELETE /:airline/:flight_num

"""

import json

from fastapi import FastAPI

from models import Flight, Airline, FlightRequest


app = FastAPI()

with open("airlines.json", "r") as f:
    data: dict = json.load(f)

airlines: dict[Airline, list[Flight]] = {
    Airline(airline_name): [Flight(**flight) for flight in flights]
    for airline_name, flights in data.items()
}

# for key, value in data.items():
#     if isinstance(value, list):
#         airlines[key] = [Flight(**f) for f in value]


# print(airlines)


@app.get("/")
async def get_airlines() -> list[str]:
    return airlines.keys()


@app.get("/{airline_name}")
async def get_flight_nums(airline_name: Airline) -> list[str]:
    return [flight.flight_num for flight in airlines[airline_name]]


@app.get("/{airline_name}/{flight_number}")
async def get_flight(airline_name: Airline, flight_number: str) -> Flight | None:
    for flight in airlines[airline_name]:
        if flight.flight_num == flight_number:
            return flight


@app.post("/{airline}")
async def create_flight(airline: Airline, flight: Flight):
    airlines[airline].append(flight)


@app.put("/{airline}/{flight_number}")
async def update_flight(
    airline: Airline, flight_number: str, updated_flight_info: FlightRequest
) -> str:
    for flight in airlines[airline]:
        if flight.flight_num == flight_number:
            flight.capacity = updated_flight_info.capacity
            flight.estimated_flight_duration = (
                updated_flight_info.estimated_flight_duration
            )
    return "Flight updated successfully"


@app.delete("/{airline_name}/{flight_number}")
async def delete_flight(airline_name: Airline, flight_number: str) -> str:
    for flight in airlines[airline_name]:
        if flight.flight_num == flight_number:
            airlines[airline_name].remove(flight)
    return "Flight deleted successfully"
