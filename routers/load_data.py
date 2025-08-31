import csv
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from datetime import datetime, date
from models.midia import Midia, Genre

load_data_router = APIRouter(prefix="/insert", tags=["midia", "genres", "load_data"])

@load_data_router.post("/load-from-csv")
def load_data_to_db(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(load_genres_from_csv, db)
    background_tasks.add_task(load_midias_from_csv, "api/movies_data.csv", db)
    background_tasks.add_task(load_midias_from_csv, "api/tv_series_data.csv", db)
    return {"message": "Carga iniciada em background"}


def load_genres_from_csv(db: Session):
    file_path = "api/genres_all.csv"  # caminho do CSV
    
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                genre_id = int(row["id"])
                name = row["name"]

                # verificar se já existe
                exists = db.query(Genre).filter(Genre.id == genre_id).first()
                if not exists:
                    new_genre = Genre(id=genre_id, ds_description=name)
                    db.add(new_genre)

            db.commit()

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo CSV não encontrado")

    return {"message": "Gêneros carregados com sucesso!"}


def load_midias_from_csv(file_path: str, db: Session):
    """Carrega filmes ou séries do CSV e salva no banco"""
    with open(file_path, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [f.strip().replace("\ufeff", "") for f in reader.fieldnames]

        for row in reader:
            print(row.keys())
            # Verifica se já existe a midia
            exists = db.query(Midia).filter(Midia.id == int(row["id"])).first()
            if exists:
                continue

            data_str = row.get("data_lancamento", "")

            if data_str:
                dt_launch_date = datetime.strptime(data_str, "%Y-%m-%d").date()
            else:
                dt_launch_date = None


            # Cria a Midia
            midia = Midia(
                id=int(row["id"]),
                id_imdb=row["id_imdb"],
                ds_title=row["titulo"],
                ds_original_name=row["titulo_original"],
                ds_description=row["descricao"] or None,
                dt_launch=dt_launch_date or None,
                ds_original_language=row["lingua_original"],
                ds_midia_type=row["tipo_midia"],
                ds_poster_url=row["poster_url"] or None,
                di_popularity=float(row["popularity"]) if row["popularity"] else None,
                di_vote_average=float(row["vote_average"]) if row["vote_average"] else None,
                di_vote_count=int(row["vote_count"]) if row["vote_count"] else None,
                fl_adult=row["adult"].lower() == "true" if row["adult"] else False
            )

            # Adiciona os gêneros
            genre_ids = [int(g) for g in row["generos"].split()]
            genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            midia.genres = genres

            db.add(midia)
        db.commit()
