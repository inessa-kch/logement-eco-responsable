from typing import Optional,Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import func
from datetime import datetime
import httpx

sql_file_name = "database.db"
sqlite_url = f"sqlite:///{sql_file_name}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

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
def create_logement(logement: Logement, session: SessionDep) -> Logement:
    session.add(logement)
    session.commit()
    session.refresh(logement)
    return logement

@app.get("/logement/")
def read_logements(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Logement]:
    logements = session.exec(select(Logement).offset(offset).limit(limit)).all()
    return logements

@app.get("/logement/{logement_id}")
def read_logement(logement_id: int, session: SessionDep) -> Logement:
    logement = session.get(Logement, logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    return logement

@app.delete("/logement/{logement_id}")
def delete_logement(logement_id: int, session: SessionDep):
    logement = session.get(Logement, logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    session.delete(logement)
    session.commit()
    return {"ok": True}

# PIECE
@app.post("/piece/")
def create_piece(piece: Piece, session: SessionDep) -> Piece:
    session.add(piece)
    session.commit()
    session.refresh(piece)
    return piece

@app.get("/piece/")
def read_pieces(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Piece]:
    pieces = session.exec(select(Piece).offset(offset).limit(limit)).all()
    return pieces

@app.get("/piece/{piece_id}")
def read_piece(piece_id: int, session: SessionDep) -> Piece:
    piece = session.get(Piece, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    return piece

@app.delete("/piece/{piece_id}")
def delete_piece(piece_id: int, session: SessionDep):
    piece = session.get(Piece, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    session.delete(piece)
    session.commit()
    return {"ok": True}

@app.get("/piece/{piece_id}/logement")
def read_piece_logement(piece_id: int, session: SessionDep):
    piece = session.get(Piece, piece_id)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    logement = session.get(Logement, piece.logement_id)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    return logement


# TYPE CAPTEUR ACTIONNEUR
@app.post("/typecapteuractionneur/")
def create_typecapteuractionneur(typecapteuractionneur: TypeCapteurActionneur, session: SessionDep) -> TypeCapteurActionneur:
    session.add(typecapteuractionneur)
    session.commit()
    session.refresh(typecapteuractionneur)
    return typecapteuractionneur

@app.get("/typecapteuractionneur/")
def read_typecapteuractionneurs(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[TypeCapteurActionneur]:
    typecapteuractionneurs = session.exec(select(TypeCapteurActionneur).offset(offset).limit(limit)).all()
    return typecapteuractionneurs

@app.get("/typecapteuractionneur/{typecapteuractionneur_id}")
def read_typecapteuractionneur(typecapteuractionneur_id: int, session: SessionDep) -> TypeCapteurActionneur:
    typecapteuractionneur = session.get(TypeCapteurActionneur, typecapteuractionneur_id)
    if not typecapteuractionneur:
        raise HTTPException(status_code=404, detail="TypeCapteurActionneur not found")
    return typecapteuractionneur

@app.delete("/typecapteuractionneur/{typecapteuractionneur_id}")
def delete_typecapteuractionneur(typecapteuractionneur_id: int, session: SessionDep):
    typecapteuractionneur = session.get(TypeCapteurActionneur, typecapteuractionneur_id)
    if not typecapteuractionneur:
        raise HTTPException(status_code=404, detail="TypeCapteurActionneur not found")
    session.delete(typecapteuractionneur)
    session.commit()
    return {"ok": True}


# CAPTEUR ACTIONNEUR
@app.post("/capteuractionneur/")
def create_capteuractionneur(capteuractionneur: CapteurActionneur, session: SessionDep) -> CapteurActionneur:
    session.add(capteuractionneur)
    session.commit()
    session.refresh(capteuractionneur)
    return capteuractionneur

@app.get("/capteuractionneur/")
def read_capteuractionneurs(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[CapteurActionneur]:
    capteuractionneurs = session.exec(select(CapteurActionneur).offset(offset).limit(limit)).all()
    return capteuractionneurs

@app.get("/capteuractionneur/{capteuractionneur_id}")
def read_capteuractionneur(capteuractionneur_id: int, session: SessionDep) -> CapteurActionneur:
    capteuractionneur = session.get(CapteurActionneur, capteuractionneur_id)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    return capteuractionneur

@app.delete("/capteuractionneur/{capteuractionneur_id}")
def delete_capteuractionneur(capteuractionneur_id: int, session: SessionDep):
    capteuractionneur = session.get(CapteurActionneur, capteuractionneur_id)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    session.delete(capteuractionneur)
    session.commit()
    return {"ok": True}

@app.get("/capteuractionneur/{capteuractionneur_id}/piece")
def read_capteuractionneur_piece(capteuractionneur_id: int, session: SessionDep):
    capteuractionneur = session.get(CapteurActionneur, capteuractionneur_id)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    piece = session.get(Piece, capteuractionneur.id_piece)
    if not piece:
        raise HTTPException(status_code=404, detail="Piece not found")
    return piece


# MESURE
@app.post("/mesure/")
def create_mesure(mesure: Mesure, session: SessionDep) -> Mesure:
    session.add(mesure)
    session.commit()
    session.refresh(mesure)
    return mesure

@app.get("/mesure/")
def read_mesures(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Mesure]:
    mesures = session.exec(select(Mesure).offset(offset).limit(limit)).all()
    return mesures

@app.get("/mesure/{mesure_id}")
def read_mesure(mesure_id: int, session: SessionDep) -> Mesure:
    mesure = session.get(Mesure, mesure_id)
    if not mesure:
        raise HTTPException(status_code=404, detail="Mesure not found")
    return mesure

@app.delete("/mesure/{mesure_id}")
def delete_mesure(mesure_id: int, session: SessionDep):
    mesure = session.get(Mesure, mesure_id)
    if not mesure:
        raise HTTPException(status_code=404, detail="Mesure not found")
    session.delete(mesure)
    session.commit()
    return {"ok": True}

@app.get("/mesure/{mesure_id}/capteuractionneur")
def read_mesure_capteuractionneur(mesure_id: int, session: SessionDep):
    mesure = session.get(Mesure, mesure_id)
    if not mesure:
        raise HTTPException(status_code=404, detail="Mesure not found")
    capteuractionneur = session.get(CapteurActionneur, mesure.id_capAct)
    if not capteuractionneur:
        raise HTTPException(status_code=404, detail="CapteurActionneur not found")
    return capteuractionneur


# FACTURE
@app.post("/facture/")
def create_facture(facture: Facture, session: SessionDep) -> Facture:
    session.add(facture)
    session.commit()
    session.refresh(facture)
    return facture

@app.get("/facture/")
def read_factures(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)]=100,
) -> list[Facture]:
    factures = session.exec(select(Facture).offset(offset).limit(limit)).all()
    return factures

@app.get("/facture/{facture_id}")
def read_facture(facture_id: int, session: SessionDep) -> Facture:
    facture = session.get(Facture, facture_id)
    if not facture:
        raise HTTPException(status_code=404, detail="Facture not found")
    return facture

@app.delete("/facture/{facture_id}")
def delete_facture(facture_id: int, session: SessionDep):
    facture = session.get(Facture, facture_id)
    if not facture:
        raise HTTPException(status_code=404, detail="Facture not found")
    session.delete(facture)
    session.commit()
    return {"ok": True}

@app.get("/facture/{facture_id}/logement")
def read_facture_logement(facture_id: int, session: SessionDep):
    facture = session.get(Facture, facture_id)
    if not facture:
        raise HTTPException(status_code=404, detail="Facture not found")
    logement = session.get(Logement, facture.id_logement)
    if not logement:
        raise HTTPException(status_code=404, detail="Logement not found")
    return logement





# WEBSITE

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, session: SessionDep, city: str = "Paris"):
    # Fetch pie chart data
    query = select(Facture.type_facture, func.sum(Facture.montant).label("total_amount")).group_by(Facture.type_facture)
    grouped_data = session.exec(query).all()
    chart_data = [["Type de facture", "Montant total"]] + [[item.type_facture, item.total_amount] for item in grouped_data]

    # Fetch weather data
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Paris",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()  # Génère une exception en cas d'erreur HTTP
            data = response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de requête: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    # Process weather data
    forecast = data.get("daily", {})
    if not forecast:
        raise HTTPException(status_code=404, detail="Prévisions météo introuvables.")

    weather_data = [
        {
            "date": forecast["time"][i],
            "temperature_max": forecast["temperature_2m_max"][i],
            "temperature_min": forecast["temperature_2m_min"][i],
        }
        for i in range(len(forecast["time"]))
    ]

    return templates.TemplateResponse("index.html", {"request": request, "chart_data": chart_data, "weather_data": weather_data})


@app.get("/consommation", response_class=HTMLResponse)
async def consommation(request: Request, session: SessionDep):
    # Fetch data for the chart
    query = select(Facture.type_facture, func.sum(Facture.montant).label("total_amount")).group_by(Facture.type_facture)
    grouped_data = session.exec(query).all()
    chart_data = [["Type de facture", "Montant total"]] + [[item.type_facture, item.total_amount] for item in grouped_data]
    return templates.TemplateResponse("consommation.html", {"request": request, "chart_data": chart_data})

@app.get("/etat", response_class=HTMLResponse)
async def etat(request: Request, session: SessionDep):
    capteurs = session.exec(select(CapteurActionneur)).all()
    return templates.TemplateResponse("etat.html", {"request": request, "capteurs": capteurs})

@app.get("/economies", response_class=HTMLResponse)
async def economies(request: Request, session: SessionDep):
    # Fetch data for the chart
    query = select(Facture.type_facture, func.sum(Facture.montant).label("total_amount")).group_by(Facture.type_facture)
    grouped_data = session.exec(query).all()
    chart_data = [["Type de facture", "Montant total"]] + [[item.type_facture, item.total_amount] for item in grouped_data]
    return templates.TemplateResponse("economies.html", {"request": request, "chart_data": chart_data})


@app.get("/configuration", response_class=HTMLResponse)
async def configuration(request: Request):
    return templates.TemplateResponse("configuration.html", {"request": request})




@app.get("/website", response_class=HTMLResponse)
async def get_website_data(request: Request, session: SessionDep, city: str = "Paris"):
    # Fetch pie chart data
    query = select(Facture.type_facture, func.sum(Facture.montant).label("total_amount")).group_by(Facture.type_facture)
    grouped_data = session.exec(query).all()
    chart_data = [["Type de facture", "Montant total"]] + [[item.type_facture, item.total_amount] for item in grouped_data]

    # Fetch weather data
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 48.8566,
        "longitude": 2.3522,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "Europe/Paris",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)
            response.raise_for_status()  # Génère une exception en cas d'erreur HTTP
            data = response.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Erreur de requête: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)

    # Process weather data
    forecast = data.get("daily", {})
    if not forecast:
        raise HTTPException(status_code=404, detail="Prévisions météo introuvables.")

    weather_data = [
        {
            "date": forecast["time"][i],
            "temperature_max": forecast["temperature_2m_max"][i],
            "temperature_min": forecast["temperature_2m_min"][i],
        }
        for i in range(len(forecast["time"]))
    ]

    return templates.TemplateResponse("website.html", {"request": request, "chart_data": chart_data, "weather_data": weather_data})









if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

