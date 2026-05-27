from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import supabase # <--- É esta linha que apaga a luz amarela!

# Importamos a conexão do arquivo que acabamos de criar!
from database import supabase 

# Criamos o roteador específico para materiais
router = APIRouter(
    prefix="/api/materiais",
    tags=["Materiais"]
)

# O nosso Contrato (DTO)
class MaterialCreate(BaseModel):
    titulo: str
    descricao: str
    turma_id: str
    url_drive: Optional[str] = None
    url_youtube: Optional[str] = None

# A rota GET com filtro opcional
@router.get("")
def listar_materiais(turma_id: Optional[int] = None):
    # Se o React pedir uma turma específica, a gente filtra (.eq)
    if turma_id:
        resposta = supabase.table("materiais").select("*").eq("turma_id", turma_id).execute()
    # Se não pedir (ex: tela do professor), a gente traz tudo
    else:
        resposta = supabase.table("materiais").select("*").execute()
        
    return resposta.data

# A rota POST
@router.post("/")
def criar_material(material: MaterialCreate):
    dados_banco = {
        "titulo": material.titulo,
        "descricao": material.descricao,
        "turma_id": material.turma_id,
        "url_drive": material.url_drive,
        "url_youtube": material.url_youtube
    }
    
    resposta = supabase.table("materiais").insert(dados_banco).execute()
    
    return {
        "mensagem": "Material criado com sucesso!", 
        "dados": resposta.data
    }

    # A rota DELETE (Repare que ela espera o ID na própria URL)
@router.delete("/{material_id}")
def deletar_material(material_id: int):
    # Vai no Supabase, procura o ID exato e deleta a linha
    resposta = supabase.table("materiais").delete().eq("id", material_id).execute()
    
    return {"mensagem": f"Material {material_id} apagado com sucesso!"}