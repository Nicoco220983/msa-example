import os

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select

import pydantic as pyd

HERE = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(HERE, "static")


# msa

async def msa_register_subapp(app):
    MsaExample().msa_register_subapp(app)

async def msa_install_db(app):
    async for db in app.get_db():
        conn = await db.connection()
        await conn.run_sync(Base.metadata.create_all)

async def msa_get_as_page():
    return {
        "head": '<script type="module" src="/msa/example/static/msa-example.mjs"></script>',
        "body": """<div  style="display: flex; flex-direction:column; width:100%; height:100%; padding:1em; margin:0; align-items:center;">
            <h1>msaexample</h1>
            <msa-example></msa-example>
        </div>""",
    }


# database

Base = declarative_base()

class MyTable(Base):
    __tablename__ = "msa_example_datas"

    id = sa.Column(sa.String(80), primary_key=True)
    value = sa.Column(sa.Integer, nullable=False)


# subapp
    

class DataModel(pyd.BaseModel):
    id: str
    value: int


class MsaExample():


    def msa_register_subapp(self, app):

        subapp = FastAPI()
        app.mount("/msa/example", subapp)

        subapp.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

        @subapp.get("/")
        def root_endp():
            return FileResponse(os.path.join(HERE, "static/index.html"))

        @subapp.get("/{id}", response_model=DataModel)
        async def get_endp(id: str, db = Depends(app.get_db)):
            data = await self.get_data(db, id)
            return self.export_data(data)

        class PostDataReq(pyd.BaseModel):
            value: int

        @subapp.post("/{id}", response_model=DataModel)
        async def post_endp(id: str, item: PostDataReq, db = Depends(app.get_db)):
            data = await self.upsert_data(db, id, item.value)
            return self.export_data(data)


    async def get_data(self, db, id):
        rows = await db.execute(select(MyTable).filter_by(id=id))
        data = rows.scalars().first()
        if data is None:
            data = MyTable(id=id, value=0)
        return data


    async def upsert_data(self, db, id, value):
            rows = await db.execute(select(MyTable).filter_by(id=id).with_for_update())
            data = rows.scalars().first()
            if data is None:
                data = MyTable(id=id, value=0)
            data.value = value
            db.add(data)
            await db.commit()
            await db.refresh(data)
            return data

    
    def export_data(self, data):
        return DataModel(
            id=data.id,
            value=data.value,
        )