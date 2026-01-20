from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

from app_types.constants import DATABASE_URL

def ensure_database_exists():
    if DATABASE_URL.startswith('sqlite:///'):
        db_path = DATABASE_URL.replace('sqlite:///', '')
        if db_path.startswith('./'):
            db_path = db_path[2:]
        db_path = os.path.abspath(db_path)
        db_dir = os.path.dirname(db_path)
        if db_dir:
            Path(db_dir).mkdir(parents=True, exist_ok=True)

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
    from auth import get_password_hash
    from models import Base, Pet, User
    from app_types import GenderEnum, SpeciesEnum, StatusEnum

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing_pets = db.query(Pet).count()
        existing_users = db.query(User).count()

        if existing_pets > 0 or existing_users > 0:
            return

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if admin_email and admin_password:
            admin_user = User(
                full_name=os.getenv("ADMIN_NAME", "Admin"),
                email=admin_email,
                whatsapp=os.getenv("ADMIN_WHATSAPP", ""),
                city=os.getenv("ADMIN_CITY", "São Paulo"),
                password=get_password_hash(admin_password)
            )
            db.add(admin_user)
            db.commit()

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

        for i, dog in enumerate(dogs_data):
            is_female = dog["gender"] == GenderEnum.FEMALE
            description = f"{dog['name']} é {'uma cadela' if is_female else 'um cachorro'} muito {'carinhosa' if is_female else 'carinhoso'} e {'brincalhona' if is_female else 'brincalhão'}."

            pet = Pet(
                name=dog["name"],
                species=SpeciesEnum.DOG,
                breed="Vira-lata",
                age=12 + (i * 6),
                gender=dog["gender"],
                city=cities[i % len(cities)],
                description=description,
                photos=[dog["photo"]],
                status=StatusEnum.AVAILABLE
            )
            db.add(pet)

        for i, cat in enumerate(cats_data):
            is_female = cat["gender"] == GenderEnum.FEMALE
            description = f"{cat['name']} é {'uma gata' if is_female else 'um gato'} muito dócil e independente."

            pet = Pet(
                name=cat["name"],
                species=SpeciesEnum.CAT,
                breed="Sem raça definida",
                age=8 + (i * 4),
                gender=cat["gender"],
                city=cities[i % len(cities)],
                description=description,
                photos=[cat["photo"]],
                status=StatusEnum.AVAILABLE
            )
            db.add(pet)

        db.commit()

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()