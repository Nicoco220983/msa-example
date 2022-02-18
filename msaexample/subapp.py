import os

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select

import pydantic

HERE = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(HERE, "static")

# database

Base = declarative_base()

class MyTable(Base):
    __tablename__ = "msa_example_datas"

    id = sa.Column(sa.String(80), primary_key=True)
    value = sa.Column(sa.Integer, nullable=False)

async def install_msa_db(app):
    async for db in app.get_db():
        conn = await db.connection()
        await conn.run_sync(Base.metadata.create_all)

# subapp

async def register_msa_subapp(app):

    subapp = FastAPI()
    app.mount("/msa/example", subapp)

    subapp.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @subapp.get("/")
    def root_endp():
        return FileResponse(os.path.join(HERE, "static/index.html"))

    class DataModel(pydantic.BaseModel):
        id: str
        value: int

    @subapp.get("/{id}", response_model=DataModel)
    async def get_endp(id: str, db = Depends(app.get_db)):
        rows = await db.execute(select(MyTable).filter_by(id=id))
        data = rows.scalars().first()
        if data is None:
            data = MyTable(id=id, value=0)
        return _export_data(data)
    
    def _export_data(data):
        return {
            "id": data.id,
            "value": data.value
        }

    class PostDataReq(pydantic.BaseModel):
        value: int

    @subapp.post("/{id}", response_model=DataModel)
    async def post_endp(id: str, item: PostDataReq, db = Depends(app.get_db)):
        rows = await db.execute(select(MyTable).filter_by(id=id).with_for_update())
        data = rows.scalars().first()
        if data is None:
            data = MyTable(id=id, value=0)
        data.value = item.value
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return _export_data(data)