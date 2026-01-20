from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

from app_types.constants import DATABASE_URL

# Criar o diretório para o banco de dados se não existir
def ensure_database_exists():
    """Garante que o diretório do banco de dados existe"""
    if DATABASE_URL.startswith('sqlite:///'):
        # Extrair o caminho do arquivo do DATABASE_URL
        db_path = DATABASE_URL.replace('sqlite:///', '')
        
        # Remover ./ do início se existir
        if db_path.startswith('./'):
            db_path = db_path[2:]
        
        # Converter para caminho absoluto
        db_path = os.path.abspath(db_path)
        
        # Criar o diretório pai se não existir
        db_dir = os.path.dirname(db_path)
        if db_dir:
            Path(db_dir).mkdir(parents=True, exist_ok=True)
            print(f"📁 Diretório verificado: {db_dir}")
        
        print(f"📍 Banco de dados será criado em: {db_path}")
        
        # Verificar se já existe
        if os.path.exists(db_path):
            print(f"ℹ️  Banco de dados já existe")
        else:
            print(f"🆕 Novo banco de dados será criado")

# Garantir que o banco existe antes de criar o engine
ensure_database_exists()

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Importar get_password_hash DENTRO da função para evitar importação circular
    from auth import get_password_hash
    from models import Base, Pet, User
    from app_types import GenderEnum, SpeciesEnum, StatusEnum
    
    print("🗄️  Criando tabelas no banco de dados...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise
    
    db = SessionLocal()
    try:
        # Verificar se já existem dados
        existing_pets = db.query(Pet).count()
        existing_users = db.query(User).count()
        
        if existing_pets > 0 or existing_users > 0:
            print(f"ℹ️  Banco já possui dados: {existing_users} usuários, {existing_pets} pets")
            return
        
        print("📝 Criando dados iniciais...")
        
        # Criar usuários
        user1 = User(
            full_name="João Silva",
            email="joao@email.com",
            whatsapp="11999999999",
            city="São Paulo",
            password=get_password_hash("senha123")
        )
        
        user2 = User(
            full_name="Maria Santos",
            email="maria@email.com",
            whatsapp="21999999999",
            city="Rio de Janeiro",
            password=get_password_hash("senha123")
        )
        
        admin_user = User(
            full_name="Admin",
            email="yladacz@gmail.com",
            whatsapp="11999999999",
            city="São Paulo",
            password=get_password_hash("@Senha123")
        )
        
        db.add_all([user1, user2, admin_user])
        db.commit()
        print("✅ 3 usuários criados!")
        
        # Dados de pets
        dogs_data = [
            {"name": "Luna", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=400&h=300&fit=crop"},
            {"name": "Max", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop"},
            {"name": "Bella", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop"},
            {"name": "Thor", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"},
            {"name": "Lola", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"},
            {"name": "Zeus", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop"},
            {"name": "Maya", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop"},
            {"name": "Apollo", "gender": GenderEnum.MALE, "photo": "https://www.petelegante.com.br/media/dicas/ado%C3%A7%C3%A3o-de-cachorro-filhote.jpg"},
            {"name": "Nala", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&h=300&fit=crop"},
            {"name": "Rocky", "gender": GenderEnum.MALE, "photo": "https://static.wixstatic.com/media/e2e4ef_8681efaf6b4c4f05b2605a1162957150~mv2.jpg/v1/fill/w_516,h_432,al_c,q_80,usm_0.66_1.00_0.01,enc_avif,quality_auto/Simon_cachorro_PatinhasCarentes_05.jpg"},
            {"name": "Sofia", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&h=300&fit=crop"},
            {"name": "Bruno", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&h=300&fit=crop"},
            {"name": "Rex", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1601758228041-f3b2795255f1?w=400&h=300&fit=crop"},
            {"name": "Karen", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1605568427561-40dd23c2acea?w=400&h=300&fit=crop"},
            {"name": "Charlie", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1551717743-49959800b1f6?w=400&h=300&fit=crop"}
        ]
        
        cats_data = [
            {"name": "Mimi", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Simba", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Carminha", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"},
            {"name": "Felix", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop"},
            {"name": "BellaCat", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop"},
            {"name": "Garfield", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop"},
            {"name": "NalaCat", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Pink", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "MayaCat", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"},
            {"name": "Whiskers", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&h=300&fit=crop"},
            {"name": "Laly", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=400&h=300&fit=crop"},
            {"name": "Shadow", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=400&h=300&fit=crop"},
            {"name": "Brina", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&h=300&fit=crop"},
            {"name": "Tiger", "gender": GenderEnum.MALE, "photo": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=400&h=300&fit=crop"},
            {"name": "Mia", "gender": GenderEnum.FEMALE, "photo": "https://images.unsplash.com/photo-1596854407944-bf87f6fdd49e?w=400&h=300&fit=crop"}
        ]
        
        cities = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília", "Fortaleza", "Manaus", "Curitiba", "Recife", "Porto Alegre"]
        
        print("🐕 Criando cachorros...")
        for i, dog in enumerate(dogs_data):
            pet = Pet(
                name=dog["name"],
                species=SpeciesEnum.DOG,
                breed="Vira-lata",
                age=12 + (i * 6),
                gender=dog["gender"],
                city=cities[i % len(cities)],
                description=f"{dog['name']} é um{'a' if dog['gender'] == GenderEnum.FEMALE else ''} cachorro{'a' if dog['gender'] == GenderEnum.FEMALE else ''} muito carinhoso{'a' if dog['gender'] == GenderEnum.FEMALE else ''} e brincalhão{'a' if dog['gender'] == GenderEnum.FEMALE else ''}.",
                photos=[dog["photo"]],
                status=StatusEnum.AVAILABLE
            )
            db.add(pet)
        
        print("🐱 Criando gatos...")
        for i, cat in enumerate(cats_data):
            pet = Pet(
                name=cat["name"],
                species=SpeciesEnum.CAT,
                breed="Sem raça definida",
                age=8 + (i * 4),
                gender=cat["gender"],
                city=cities[i % len(cities)],
                description=f"{cat['name']} é um{'a' if cat['gender'] == GenderEnum.FEMALE else ''} gato{'a' if cat['gender'] == GenderEnum.FEMALE else ''} muito dócil e independente.",
                photos=[cat["photo"]],
                status=StatusEnum.AVAILABLE
            )
            db.add(pet)
        
        db.commit()
        print(f"✅ {len(dogs_data)} cachorros criados!")
        print(f"✅ {len(cats_data)} gatos criados!")
        print(f"📊 Total: {len(dogs_data) + len(cats_data)} pets no banco de dados")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()