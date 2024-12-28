from typing import Optional,Annotated, AsyncGenerator
from fastapi import Depends, FastAPI, HTTPException, Query, Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import func
from datetime import datetime
import httpx
from contextlib import asynccontextmanager
import json

sql_file_name = "database.db"
sqlite_url = f"sqlite:///{sql_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep =  Depends(get_session)

# Define the lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup logic
    create_db_and_tables()
    yield  # Pause here for app's lifecycle
    # Shutdown logic (e.g., cleanup resources if needed)

# Create the FastAPI app with the lifespan
app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#suivi du tuto suivant pour l'ecriture du code: https://fastapi.tiangolo.com/tutorial/sql-databases/#run-the-code 

class Logement(SQLModel, table=True):
    __tablename__ = "logement"
    __table_args__ = {"extend_existing": True}
    id_logement: Optional[int] = Field(default=None, primary_key=True)
    adresse: str
    numero_telephone: str
    adresse_ip: str

class Piece(SQLModel, table=True):
    __tablename__ = "piece"
    __table_args__ = {"extend_existing": True}
    id_piece: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    position_x: int
    position_y: int
    position_z: int
    logement_id: int = Field(foreign_key="logement.id_logement")

class TypeCapteurActionneur(SQLModel, table=True):
    __tablename__ = "typecapteuractionneur"
    __table_args__ = {"extend_existing": True}
    id_type: Optional[int] = Field(default=None, primary_key=True)
    nom_type: str
    unite_mesure: str
    precision_min: int
    precision_max: int

class CapteurActionneur(SQLModel, table=True):
    __tablename__ = "capteuractionneur"
    __table_args__ = {"extend_existing": True}
    id_capAct: Optional[int] = Field(default=None, primary_key=True)
    reference_commerciale: str
    id_piece: int = Field(foreign_key="piece.id_piece")
    port_communication: int
    id_type: int = Field(foreign_key="typecapteuractionneur.id_type")

class Mesure(SQLModel, table=True):
    __tablename__ = "mesure"
    __table_args__ = {"extend_existing": True}
    id_mesure: Optional[int] = Field(default=None, primary_key=True)
    valeur: int
    date_mesure: datetime = Field(default_factory=datetime.utcnow)
    id_capAct: int = Field(foreign_key="capteuractionneur.id_capAct")

class Facture(SQLModel, table=True):
    __tablename__ = "facture"
    __table_args__ = {"extend_existing": True}
    id_facture: Optional[int] = Field(default=None, primary_key=True)
    type_facture: str
    date_facture: str
    montant: int
    valeur_consommation: float
    unite_consommation: str
    id_logement: int = Field(foreign_key="logement.id_logement")








# LOGEMENT
@app.post("/logement/")
def create_logement(
    adresse: str = Form(...),
    numero_telephone: str = Form(...),
    adresse_ip: str = Form(...),
    session: SessionDep = Depends(get_session)
) -> Logement:
    logement = Logement(
        adresse=adresse,
        numero_telephone=numero_telephone,
        adresse_ip=adresse_ip
    )
    session.add(logement)
    session.commit()
    session.refresh(logement)
    return logement


@app.get("/logement/")
def read_logements(
    session: SessionDep = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Logement]:
    logements = session.exec(select(Logement).offset(offset).limit(limit)).all()
    return logements

@app.get("/logement/{logement_id}")
def read_logement(logement_id: int, session: SessionDep = Depends(get_session)) -> Logement:
    logement = session.get(Logement, logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    return logement

@app.delete("/logement/{logement_id}")
def delete_logement(logement_id: int, session: SessionDep = Depends(get_session)):
    logement = session.get(Logement, logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    session.delete(logement)
    session.commit()
    return {"ok": True}

# PIECE
@app.post("/piece/")
def create_piece(
    logement_id: int = Form(...),
    nom: str = Form(...),
    position_x: float = Form(...),
    position_y: float = Form(...),
    position_z: float = Form(...),
    session: Session = Depends(get_session)
):
    # Fetch the logement using the selected ID
    logement = session.get(Logement, logement_id)
    
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")

    # Create a new piece and link it to the logement
    piece = Piece(
        logement_id=logement_id,
        nom=nom,
        position_x=position_x,
        position_y=position_y,
        position_z=position_z
    )

    session.add(piece)
    session.commit()
    session.refresh(piece)

    return {"message": "Pièce ajoutée avec succès", "piece": piece}





@app.get("/piece/")
def read_pieces(
    session: SessionDep = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Piece]:
    pieces = session.exec(select(Piece).offset(offset).limit(limit)).all()
    return pieces

@app.get("/piece/{piece_id}")
def read_piece(piece_id: int, session: SessionDep = Depends(get_session)) -> Piece:
    piece = session.get(Piece, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    return piece

@app.delete("/piece/{piece_id}")
def delete_piece(piece_id: int, session: SessionDep = Depends(get_session)):
    piece = session.get(Piece, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    session.delete(piece)
    session.commit()
    return {"ok": True}

@app.get("/logement/{logement_id}/piece/{piece_id}")
def read_piece_logement(logement_id: int, piece_id: int, session: Session = Depends(get_session)):
    logement = session.get(Logement, logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    
    piece = session.get(Piece, piece_id)
    if not piece or piece.logement_id != logement_id:
        raise HTTPException(status_code=404, detail="Piece not found in the specified Logement")
    
    return piece


# TYPE CAPTEUR ACTIONNEUR
@app.post("/typecapteuractionneur/")
def create_typecapteuractionneur(typecapteuractionneur: TypeCapteurActionneur, session: SessionDep = Depends(get_session)) -> TypeCapteurActionneur:
    session.add(typecapteuractionneur)
    session.commit()
    session.refresh(typecapteuractionneur)
    return typecapteuractionneur

@app.get("/typecapteuractionneur/")
def read_typecapteuractionneurs(
    session: SessionDep = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[TypeCapteurActionneur]:
    typecapteuractionneurs = session.exec(select(TypeCapteurActionneur).offset(offset).limit(limit)).all()
    return typecapteuractionneurs

@app.get("/typecapteuractionneur/{typecapteuractionneur_id}")
def read_typecapteuractionneur(typecapteuractionneur_id: int, session: SessionDep = Depends(get_session)) -> TypeCapteurActionneur:
    typecapteuractionneur = session.get(TypeCapteurActionneur, typecapteuractionneur_id)
    if not typecapteuractionneur:
        raise HTTPException(status_code=404, detail="TypeCapteurActionneur not found")
    return typecapteuractionneur

@app.delete("/typecapteuractionneur/{typecapteuractionneur_id}")
def delete_typecapteuractionneur(typecapteuractionneur_id: int, session: SessionDep = Depends(get_session)):
    typecapteuractionneur = session.get(TypeCapteurActionneur, typecapteuractionneur_id)
    if not typecapteuractionneur:
        raise HTTPException(status_code=404, detail="TypeCapteurActionneur not found")
    session.delete(typecapteuractionneur)
    session.commit()
    return {"ok": True}


# CAPTEUR ACTIONNEUR
@app.post("/capteuractionneur/")
def create_capteuractionneur(
    piece_id: int = Form(...),
    reference_commerciale: str = Form(...),
    port_communication: int = Form(...),
    type_id: int = Form(...),
    session: Session = Depends(get_session)
) -> CapteurActionneur:
    capteuractionneur = CapteurActionneur(
        id_piece=piece_id,
        reference_commerciale=reference_commerciale,
        port_communication=port_communication,
        id_type=type_id
    )
    session.add(capteuractionneur)
    session.commit()
    session.refresh(capteuractionneur)
    return capteuractionneur

@app.get("/capteuractionneur/")
def read_capteuractionneurs(
    session: SessionDep = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[CapteurActionneur]:
    capteuractionneurs = session.exec(select(CapteurActionneur).offset(offset).limit(limit)).all()
    return capteuractionneurs

@app.get("/capteuractionneur/{capteuractionneur_id}")
def read_capteuractionneur(capteuractionneur_id: int, session: SessionDep = Depends(get_session)) -> CapteurActionneur:
    capteuractionneur = session.get(CapteurActionneur, capteuractionneur_id)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    return capteuractionneur

@app.delete("/capteuractionneur/{capteuractionneur_id}")
def delete_capteuractionneur(capteuractionneur_id: int, session: SessionDep = Depends(get_session)):
    capteuractionneur = session.get(CapteurActionneur, capteuractionneur_id)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    session.delete(capteuractionneur)
    session.commit()
    return {"ok": True}

@app.get("/capteuractionneur/{capteuractionneur_id}/piece")
def read_capteuractionneur_piece(capteuractionneur_id: int, session: SessionDep = Depends(get_session)):
    capteuractionneur = session.get(CapteurActionneur, capteuractionneur_id)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    piece = session.get(Piece, capteuractionneur.id_piece)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    return piece


# MESURE
@app.post("/mesure/")
def create_mesure(mesure: Mesure, session: SessionDep = Depends(get_session)) -> Mesure:
    session.add(mesure)
    session.commit()
    session.refresh(mesure)
    return mesure

@app.get("/mesure/")
def read_mesures(
    session: SessionDep = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Mesure]:
    mesures = session.exec(select(Mesure).offset(offset).limit(limit)).all()
    return mesures

@app.get("/mesure/{mesure_id}")
def read_mesure(mesure_id: int, session: SessionDep = Depends(get_session)) -> Mesure:
    mesure = session.get(Mesure, mesure_id)
    if not mesure:
        raise HTTPException(status_code=404, detail="Mesure not found")
    return mesure

@app.delete("/mesure/{mesure_id}")
def delete_mesure(mesure_id: int, session: SessionDep = Depends(get_session)):
    mesure = session.get(Mesure, mesure_id)
    if not mesure:
        raise HTTPException(status_code=404, detail="Mesure not found")
    session.delete(mesure)
    session.commit()
    return {"ok": True}

@app.get("/mesure/{mesure_id}/capteuractionneur")
def read_mesure_capteuractionneur(mesure_id: int, session: SessionDep = Depends(get_session)):
    mesure = session.get(Mesure, mesure_id)
    if not mesure:
        raise HTTPException(status_code=404, detail="Mesure not found")
    capteuractionneur = session.get(CapteurActionneur, mesure.id_capAct)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    return capteuractionneur


# FACTURE
@app.post("/facture/")
def create_facture(
    id_logement: int = Form(...),
    type_facture: str = Form(...),
    date_facture: str = Form(...),
    montant: float = Form(...),
    valeur_consommation: float = Form(...),
    unite_consommation: str = Form(...),
    session: Session = Depends(get_session)
) -> Facture:
    print(f"Received logement_id: {id_logement}")
    facture = Facture(
        id_logement=id_logement,
        type_facture=type_facture,
        date_facture=date_facture,
        montant=montant,
        valeur_consommation=valeur_consommation,
        unite_consommation=unite_consommation
    )
    session.add(facture)
    session.commit()
    session.refresh(facture)
    return facture

@app.get("/facture/")
def read_factures(
    session: SessionDep = Depends(get_session),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Facture]:
    factures = session.exec(select(Facture).offset(offset).limit(limit)).all()
    return factures

@app.get("/facture/{facture_id}")
def read_facture(facture_id: int, session: SessionDep = Depends(get_session)) -> Facture:
    facture = session.get(Facture, facture_id)
    if not facture:
        raise HTTPException(status_code=404, detail="Facture not found")
    return facture

@app.delete("/facture/{facture_id}")
def delete_facture(facture_id: int, session: SessionDep = Depends(get_session)):
    facture = session.get(Facture, facture_id)
    if not facture:
        raise HTTPException(status_code=404, detail="Facture not found")
    session.delete(facture)
    session.commit()
    return {"ok": True}

@app.get("/facture/{facture_id}/logement")
def read_facture_logement(facture_id: int, session: SessionDep = Depends(get_session)):
    facture = session.get(Facture, facture_id)
    if not facture:
        raise HTTPException(status_code=404, detail="Facture not found")
    logement = session.get(Logement, facture.id_logement)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    return logement






@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, session: SessionDep = Depends(get_session), city: str = "Paris"):
    # Fetch pie chart data
    query = select(Facture.type_facture, func.sum(Facture.montant).label("total_amount")).group_by(Facture.type_facture)
    grouped_data = session.exec(query).all()
    chart_data = [["Type de facture", "Montant total"]] + [[item.type_facture, item.total_amount] for item in grouped_data]

    # Fetch weather data
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "daily": "temperature_2m_max,temperature_2m_min,weathercode",
        "timezone": "Europe/Paris",
    }

    gif_map = {
        "Clear sky": "clear_sky.gif",
        "Cloudy": "cloudy.gif",
        "Drizzly": "drizzly.gif",
        "Rain": "rain.gif",
        "Snowfall": "snowfall.gif",
        "Thunderstorm": "thunderstorm.gif"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de requête: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    # Process weather data
    forecast = data.get("daily", {})
    if not forecast:
        raise HTTPException(status_code=404, detail="Prévisions météo introuvables.")

    simplified_weather_code_map = {
        0: "Clear sky",
        1: "Clear sky",
        2: "Cloudy",
        3: "Cloudy",
        45: "Cloudy",
        48: "Cloudy",
        51: "Drizzly",
        53: "Drizzly",
        55: "Drizzly",
        56: "Drizzly",
        57: "Drizzly",
        61: "Rain",
        63: "Rain",
        65: "Rain",
        66: "Rain",
        67: "Rain",
        71: "Snowfall",
        73: "Snowfall",
        75: "Snowfall",
        77: "Snowfall",
        80: "Rain",
        81: "Rain",
        82: "Rain",
        85: "Snowfall",
        86: "Snowfall",
        95: "Thunderstorm",
        96: "Thunderstorm",
        99: "Thunderstorm",
    }

    weather_data = []
    for i in range(len(forecast["time"])):
        condition = simplified_weather_code_map.get(forecast["weathercode"][i])
        if not condition:
            raise HTTPException(status_code=500, detail=f"Unmapped weather code: {forecast['weathercode'][i]}")
        weather_data.append({
            "date": forecast["time"][i],
            "temperature_max": forecast["temperature_2m_max"][i],
            "temperature_min": forecast["temperature_2m_min"][i],
            "weather_condition": condition,
            "weather_gif": gif_map[condition]
        })

    return templates.TemplateResponse("index.html", {"request": request, "chart_data": chart_data, "weather_data": weather_data})






@app.get("/consommation", response_class=HTMLResponse)
async def get_consommation(
    request: Request,
    session: Session = Depends(get_session),
    logement_id: Optional[int] = None,
    json: bool = False
):
    logements = session.exec(select(Logement)).all()

    # Query to fetch line chart data for Internet, Electricite, and Eau
    query = select(
        Facture.date_facture, 
        Facture.valeur_consommation, 
        Facture.unite_consommation, 
        Facture.id_logement
    )
    
    # Filter by logement_id if provided
    if logement_id is not None:
        query = query.where(Facture.id_logement == logement_id)

    internet_data = session.exec(query.where(Facture.type_facture == 'Internet')).all()
    electricite_data = session.exec(query.where(Facture.type_facture == 'Electricite')).all()
    eau_data = session.exec(query.where(Facture.type_facture == 'Eau')).all()

    # Pie Chart Data - Aggregate by type and filter by logement_id
    pie_chart_query = select(
        Facture.type_facture,
        func.sum(Facture.montant).label("total_montant")
    ).where(Facture.id_logement == logement_id if logement_id else True)
    pie_chart_query = pie_chart_query.group_by(Facture.type_facture)

    pie_chart_data = session.exec(pie_chart_query).all()

    # Return JSON for AJAX requests
    if json:
        return JSONResponse({
            "internet_data": [list(row) for row in internet_data],
            "electricite_data": [list(row) for row in electricite_data],
            "eau_data": [list(row) for row in eau_data],
            "pie_chart_data": [list(row) for row in pie_chart_data]
        })

    # Default: Return HTML page with data
    return templates.TemplateResponse("consommation.html", {
        "request": request,
        "logements": logements,
        "internet_data": [list(row) for row in internet_data],
        "electricite_data": [list(row) for row in electricite_data],
        "eau_data": [list(row) for row in eau_data],
        "chart_data": [list(row) for row in pie_chart_data]
    })



@app.get("/etat", response_class=HTMLResponse)
async def etat(request: Request, session: SessionDep = Depends(get_session)):
    capteurs = session.exec(select(CapteurActionneur)).all()
    return templates.TemplateResponse("etat.html", {"request": request, "capteurs": capteurs})

@app.get("/economies", response_class=HTMLResponse)
async def economies(request: Request, session: SessionDep = Depends(get_session)):
    # Fetch data for the chart
    query = select(Facture.type_facture, func.sum(Facture.montant).label("total_amount")).group_by(Facture.type_facture)
    grouped_data = session.exec(query).all()
    chart_data = [["Type de facture", "Montant total"]] + [[item.type_facture, item.total_amount] for item in grouped_data]
    return templates.TemplateResponse("economies.html", {"request": request, "chart_data": chart_data})


@app.get("/configuration", response_class=HTMLResponse)
async def get_configuration(request: Request, session: SessionDep = Depends(get_session)):
    logements = session.exec(select(Logement)).all()
    types = session.exec(select(TypeCapteurActionneur)).all()
    return templates.TemplateResponse("configuration.html", {"request": request, "logements": logements, "types": types})

@app.get("/logement/{logement_id}/pieces")
def get_pieces_by_logement(logement_id: int, session: Session = Depends(get_session)):
    pieces = session.exec(select(Piece).where(Piece.logement_id == logement_id)).all()
    return pieces

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

