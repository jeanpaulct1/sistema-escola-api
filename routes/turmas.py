from fastapi import APIRouter
from database import supabase
import time # Importando o relógio do Python


router = APIRouter(
    prefix="/api/turmas",
    tags=["Turmas"]
)

@router.get("")
def listar_turmas():
    try:
        resposta = supabase.table("turmas").select("*").order("ordem").execute()
        return resposta.data
    except Exception as e:
        print("Conexão piscou nas turmas! Tentando novamente...")
        time.sleep(0.5)
        resposta = supabase.table("turmas").select("*").order("ordem").execute()
        return resposta.data