""" FastAPI program - chapter 5"""

api_description = """
This API provides read-only access to info from the SportsWorldCentral (SWC) Fantasy Football API.
The endpoints are grouped into the following categories:

## Analytics
Get information about the health of the API and counts of leagues, teams, and players.

## Player
You can get a list of NFL players, or search for an individual player by player_id

## Scoring
You can get a list of NFL player performances, including the fantasy points they scored using SWC league scoring.

## Membership
Get information about all the SWC fantasy football leagues and the teams in them.
"""


from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

import crud, schemas
from database import SessionLocal

## FastAPI constructor with additional details added for OpenAPI Specification
app = FastAPI(
    description=api_description,
    title="Sports World Central (SWC) Fantasy Football API",
    version="0.1")

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",
         summary="Check to see if the SWC fantasy football API is running",
         response_description= "API is running",
         operation_id= "v0",
         tags=["analytics"])
async def root():
    return {"message": "API health check successful"}

@app.get("/v0/players/", response_model=list[schemas.Player],
         summary = "Get all the SWC players that meet all the parameters you sent with the request",
         response_description= "all SWC players from query",
         operation_id="v0_get_players",
         tags=["player"])
def read_players(skip : int = Query(0, description = "The number of items to skip at the beginning of API call."),
                 limit: int = Query(100, description= "The number of records to return after the skupped records."),
                 minimum_last_changed_date: date = Query(None, description= "The minimum date of change that you want to return records. Exclude any records changed before this."),
                 first_name: str = Query(None, description= "The first name of the players to return"),
                 last_name:str = Query(None, description= "The last name of the players to return"),
                 db: Session = Depends(get_db)
):
    players = crud.get_players(db, skip=skip, limit = limit,
                               min_last_changed_date=minimum_last_changed_date,
                               first_name=first_name,
                               last_name=last_name)
    return players

@app.get("/v0/players/{player_id}", 
         response_model=schemas.Player,
         summary = "Get one player using the Player ID, which is internal to SWC",
         response_description="One NFL player",
         operation_id="v0_get_players_by_player_id",
         tags=["player"])
def read_player(player_id : int,
                db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id = player_id)
    if player is None:
        raise HTTPException(status_code=404, detail = "Player not found")
    return player

@app.get("/v0/performances/",
         response_model=list[schemas.Performance],
         summary = "Get all the weekly performances that meet the parameters you sent with your request",
         response_description= "Weekly performances",
         operation_id= "v0_get_performances",
         tags=["scoring"])
def read_performances(skip: int = Query(0, description = "The number of items to skip at the beginning of API call."),
                      limit: int = Query(100, description= "The number of records to return after the skupped records."),
                      minimum_last_changed_date : date = Query(None, description= "The minimum date of change that you want to return records. Exclude any records changed before this."),
                      db: Session = Depends(get_db)):
    performances = crud.get_performances(db,
                                         skip=skip,
                                         limit = limit,
                                         min_last_changed_date=minimum_last_changed_date)
    return performances

@app.get("/v0/leagues/{league_id}", response_model=schemas.League,
         summary = "Get one league by league id",
         response_description= "find league by league id",
         operation_id="v0_get_leagues_by_league_id",
         tags=["membership"])
def read_league(league_id: int, 
                db: Session = Depends(get_db)):
    league = crud.get_league(db, league_id = league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="League not found")
    return league

@app.get("/v0/leagues/", response_model=list[schemas.League],
         summary = "Get all the SWC fantasy football leagues that match the parameters you send",
         response_description= "all leagues by query",
         operation_id= "v0_get_leagues",
         tags=["membership"])
def read_leagues(skip: int = Query(0, description = "The number of items to skip at the beginning of API call."),
                 limit: int = Query(100, description= "The number of records to return after the skupped records."),
                 minimum_last_changed_date : date = Query(None, description= "The minimum date of change that you want to return records. Exclude any records changed before this."),
                 league_name: str = Query(None, description="League name as string"),
                 db: Session = Depends(get_db)):
    leagues = crud.get_leagues(db,
                               skip=skip,
                               limit=limit,
                               min_last_changed_date=minimum_last_changed_date,
                               league_name=league_name)
    return leagues

@app.get("/v0/teams/", response_model=list[schemas.Team],
         summary = "Get all the SWC fantasy football teams that match the parameters you send",
         response_description= " all teams by query",
         operation_id = "v0_get_teams",
         tags=["membership"])
def read_teams(skip:int = Query(0, description = "The number of items to skip at the beginning of API call."),
               limit:int = Query(100, description= "The number of records to return after the skupped records."),
               minimum_last_changed_date: date = Query(None, description= "The minimum date of change that you want to return records. Exclude any records changed before this."),
               team_name: str = Query(None, description="team name as string"),
               league_id: int = Query(None, description="league as integer id number"),
               db: Session = Depends(get_db)):
    teams = crud.get_teams(db,
                           skip=skip,
                           limit=limit,
                           min_last_changed_date=minimum_last_changed_date,
                           team_name=team_name,
                           league_id=league_id)
    return teams

@app.get("/v0/counts/", response_model=schemas.Counts,
         summary="Get counts of the number of leagues, teams, and players in the SWC fantasy football",
         response_description= "counts of leagues, teams and players",
         operation_id = "v0_get_counts",
         tags=["analytics"])
def get_count(db:Session=Depends(get_db)):
    counts = schemas.Counts(
        league_count=crud.get_league_count(db),
        team_count = crud.get_team_count(db),
        player_count= crud.get_player_count(db)
    )
    return counts

