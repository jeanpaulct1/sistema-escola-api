from fastapi import APIRouter
from database import supabase

router = APIRouter(
    prefix="/api/turmas",
    tags=["Turmas"]
)

@router.get("")
def listar_turmas():
    # Busca todas as turmas ordenadas pelo campo 'ordem'
    resposta = supabase.table("turmas").select("*").order("ordem").execute()
    return resposta.data