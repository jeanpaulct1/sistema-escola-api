import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as senhas do arquivo .env
load_dotenv()

# Aqui pedimos a "etiqueta", e o Python vai ler o conteúdo lá no arquivo .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Cria a conexão única
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)