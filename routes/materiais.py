from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from database import supabase # <--- É esta linha que apaga a luz amarela!
import time # Adicione isso lá no topo do arquivo junto com os outros imports
import re # Biblioteca padrão do Python para extrair textos

def formatar_link_drive(url: str):
    if not url:
        return None
        
    # Procura o ID do arquivo no meio do link original
    match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
    
    if match:
        id_arquivo = match.group(1)
        # Retorna o link de download direto
        return f"https://drive.google.com/uc?export=download&id={id_arquivo}"
    
    return url # Se não for link do drive, devolve como chegou

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
    try:
        # Tenta buscar os dados normalmente
        if turma_id:
            resposta = supabase.table("materiais").select("*").eq("turma_id", turma_id).execute()
        else:
            resposta = supabase.table("materiais").select("*").execute()
        return resposta.data
        
    except Exception as e:
        # Se a conexão do Supabase cair (Server disconnected), ele cai aqui
        print("Conexão piscou! Tentando novamente...")
        time.sleep(0.5) # Espera meio segundo
        
        # Tenta exatamente a mesma coisa de novo com um túnel novo
        if turma_id:
            resposta = supabase.table("materiais").select("*").eq("turma_id", turma_id).execute()
        else:
            resposta = supabase.table("materiais").select("*").execute()
        return resposta.data
    
# A rota POST
@router.post("")
def criar_material(material: MaterialCreate):

    link_drive_pronto = formatar_link_drive(material.url_drive)

    dados_banco = {
        "titulo": material.titulo,
        "descricao": material.descricao,
        "turma_id": material.turma_id,
        "url_drive": link_drive_pronto,
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