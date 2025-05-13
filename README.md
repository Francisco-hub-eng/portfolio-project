# API Portfolio Project
This project demonstrates API coding best practices using Python and FastAPI.

This project was built from examples from the book 
 [Hands-On APIs For API and Data Science](https://handsonapibook.com/).


LEARNING:
API

# SportsWorldCentral (SWC) Fantasy Football API Documentation

Thanks for using the SportsWorldCentral API. This is your one-stop shop for accessing data from our fantasy football website, www.sportsworldcentral.com.

## Table of Contents
- [Public API](#public-api)
- [Getting Started](#getting-started)
    - [Analytics](#analytics)
    - [Player](#player)
    - [Scoring](#scoring)
    - [Membership](#membership)
- [Terms of Service](#terms-of-service)
- [Example Code](#example-code)
- [Software Development Kit (SDK)](#software-development-kit-sdk)

## Public API
Our API is hosted at [https://miniature-garbanzo-75x6q4rgvqpfxj7q-8000.app.github.dev/]([https://miniature-garbanzo-75x6q4rgvqpfxj7q-8000.app.github.dev/])

Ypu can access the interactive documentation at [[https://miniature-garbanzo-75x6q4rgvqpfxj7q-8000.app.github.dev/]/docs]([https://miniature-garbanzo-75x6q4rgvqpfxj7q-8000.app.github.dev/]/docs).

You can view the OpenAPI Specification (OAS) file at [[https://miniature-garbanzo-75x6q4rgvqpfxj7q-8000.app.github.dev/]/openapi.json]([https://miniature-garbanzo-75x6q4rgvqpfxj7q-8000.app.github.dev/]/openapi.json)

We'll deploying our application soon. Check back for the public API address.

## Getting Started

Since all of the data is public, the SWC API doesn't require any authentication.
All of the following data is available using GET endpoints that return JSON data.

## Analytics

Get information about the health of the API and counts of leagues, teams, and players

## Player
You can get a list of all NFL players, or search for an individual player by player_id

### Scoring
You can get a list of NFL player performances, including the fantasy points they scored using SWC league scoring

## Membership
Get information about all the SWC fantasy football leagues and the teams in them.

## Terms of Service

By using the API, you agree to the following terms of service:

-**Usage Limits**: You are allowed up to 2000 requests per day. Exceeding this limit may result in your API key being suspended.
-**No Warranty**: We don't provide any warranty of the API or its operation.

## Example code

Here is some Python example ode for accessing the health check endpoint:

````
import httpx

HEALTH_CHECK_ENDPOINT = "/"

with httpx.Client(base_url=self.swc_base_url) as client:
    response = client.get(self.HEALTH_CHECK_ENDPOINT)
    print(response.json())
````

## Software Development Kit (SDK)
*Coming Soon*

Check back for the Python SDK for our API


## Hand-ons book followedy by Francisco Urra

## Tools
- SQLite : create the fantacy sport database
- SQLAlchemy: use SQL queries and access data from database from python and store data in python structures
- Python : code to read the database
- Pytest : test the code written in Python
- Pydantic : to create schemas, validation library
- FastAPI : web framework to build the API
- HTTPX : HTTP client for Python
- Uvicorn : web server to run the API
- FastAPI documentation: Swagger UI (docs), Redoc (redoc)