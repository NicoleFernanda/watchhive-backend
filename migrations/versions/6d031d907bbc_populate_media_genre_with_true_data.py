"""populate media_genre with true data

Revision ID: 6d031d907bbc
Revises: 69a4ea8a6305
Create Date: 2025-09-17 21:40:01.174102

"""
import csv
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d031d907bbc'
down_revision: Union[str, Sequence[str], None] = '69a4ea8a6305'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CSV_PATH = Path(__file__).parent.parent / "data" / "media_genre_tv.csv"


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    meta = sa.MetaData()
    
    # tabelas
    media_table = sa.Table(
        "media", meta,
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("id_themoviedb", sa.Integer),
        sa.Column("media_type", sa.String),
    )

    media_genre_table = sa.Table(
        "media_genre", meta,
        sa.Column("media_id", sa.Integer),
        sa.Column("genre_id", sa.Integer),
    )

    # carrega os ids de media e cria uma chave com os valores em comum que serão procurados no csv
    media_rows = conn.execute(sa.select(
        media_table.c.id, 
        media_table.c.id_themoviedb, 
        media_table.c.media_type
    )).fetchall()

    media_lookup = {
        (row.id_themoviedb, row.media_type.strip().lower()): row.id
        for row in media_rows
    }

     # processa o csv
    items_to_insert = []
    with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in reader:
            key = (int(row["id_themoviedb"]), row["media_type"].strip().lower())
            media_id = media_lookup.get(key)
            genre_id_str = row.get("id_genre") 
            if media_id and genre_id_str:
                items_to_insert.append({
                    "media_id": media_id,
                    "genre_id": int(genre_id_str)
                })
    
    if items_to_insert:
        conn.execute(media_genre_table.insert(), items_to_insert)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute("DELETE FROM media_genre")
