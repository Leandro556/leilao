
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.models import get_all_editais
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/editais")
def listar_editais():
    editais = get_all_editais()
    return [{
        'id': row[0],
        'estado': row[1],
        'municipio': row[2],
        'descricao': row[3],
        'data': row[4],
        'url': row[5],
    } for row in editais]

def start_api():
    uvicorn.run("app.api.routes:app", host="0.0.0.0", port=8000, reload=False)
