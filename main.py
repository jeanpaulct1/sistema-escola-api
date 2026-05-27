from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from typing import Optional
from pydantic import BaseModel
from routes import materiais # Importa a nossa nova pasta de rotas
from database import supabase # <--- É esta linha que apaga a luz amarela!
from routes import materiais, turmas  # <--- Adicione o turmas aqui


app = FastAPI(title="API do Portal Escolar")

# 1. Configuração de CORS (Essencial para o React conseguir acessar a API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite acesso de qualquer site (Ideal para testes)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(materiais.router)
app.include_router(turmas.router)  # <--- Não esqueça de incluir o roteador de turmas!

# 3. Modelo de Dados do Login
class LoginRequest(BaseModel):
    email: str
    senha: str 

# 4. Rota principal de Login
@app.post("/api/login")
def login(dados: LoginRequest):
    try:
        # A. Valida o e-mail e senha no sistema seguro do Supabase
        resposta_auth = supabase.auth.sign_in_with_password({
            "email": dados.email,
            "password": dados.senha
        })
        
        user_id = resposta_auth.user.id
        
        # B. Busca quem é esse usuário na tabela 'profiles' para saber se é professor ou aluno
        resposta_perfil = supabase.table("profiles").select("*").eq("id", user_id).execute()
        
        # Se encontrou o perfil, guarda os dados. Se não, cria um dicionário vazio
        perfil = resposta_perfil.data[0] if resposta_perfil.data else {}
        
        # C. Devolve os dados formatados exatamente como o seu React precisa ler
        return {
            "access_token": resposta_auth.session.access_token,
            "usuario": {
                "id": user_id,
                "email": dados.email,
                "nome": perfil.get("nome", "Usuário"),
                "papel": perfil.get("papel", "aluno") # Agora o React vai receber a palavra 'professor'
            }
        }
        
    except Exception as e:
        # Se a senha estiver errada, devolve erro 401
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")