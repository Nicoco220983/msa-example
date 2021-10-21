import os

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

import sqlalchemy as sa

import pydantic

HERE = os.path.abspath(os.path.dirname(__file__))

subapp = FastAPI()

def register_msa_subapp(app):
    app.mount("/msa/example", subapp)

def register_msa_db_models(Base, _Session):
    global Session, Data
    Session = _Session

    class Data(Base):
        __tablename__ = "msa_example_datas"

        id = sa.Column(sa.String(80), primary_key=True)
        value = sa.Column(sa.Integer, nullable=False)

        def export(self):
            return {
                "id": self.id,
                "value": self.value
            }

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

STATIC_DIR = os.path.join(HERE, "static")
subapp.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@subapp.get("/")
def root_endp():
    return FileResponse(os.path.join(HERE, "static/index.html"))


class GetDataRes(pydantic.BaseModel):
    id: str
    value: int

@subapp.get("/{id}", response_model=GetDataRes)
def get_endp(id: str, db: sa.orm.Session = Depends(get_db)):
    data = db.query(Data).filter_by(id=id).first()
    if data is None:
        data = Data(id=id, value=0)
    return data.export()

class PostDataReq(pydantic.BaseModel):
    value: int

@subapp.post("/{id}", response_model=GetDataRes)
def post_endp(id: str, item: PostDataReq, db: sa.orm.Session = Depends(get_db)):
    data = db.query(Data).filter_by(id=id).with_for_update().first()
    if data is None:
        data = Data(id=id, value=0)
    data.value = item.value
    db.add(data)
    db.commit()
    db.refresh(data)
    return data.export()