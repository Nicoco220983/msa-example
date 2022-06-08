import os

from fastapi import FastAPI
from starlette.responses import HTMLResponse

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

import msaexample


MSA_MODULES = [
    msaexample
]


HERE = os.path.abspath(os.path.dirname(__file__))
DATABASE_URL = os.getenv("MSA_DATABASE_URL", "sqlite+aiosqlite:///./test.db")


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    global engine
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async def get_db() -> AsyncSession:
        async with async_session() as session:
            yield session
    app.get_db = get_db
    for pkg in MSA_MODULES:
        if hasattr(pkg, "msa_register_subapp"):
            await pkg.msa_register_subapp(app)
        if hasattr(pkg, "msa_install_db"):
            await pkg.msa_install_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    await engine.dispose()


@app.get("/", response_class=HTMLResponse)
async def msapage():
    page = await msaexample.msa_get_as_page()
    return f"""<html>
<head>
    <title>photoparty</title>
    <style>
        html, body {{
            width: 100%;
            height: 100%;
            padding: 0;
            margin: 0;
        }}
    </style>
    {page.get('head', '')}
</head>
<body>
    {page.get('body', '')}
</body>
</html>"""
