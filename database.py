from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Nombre del archivo de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./eco_moda.db"

# Conexión para SQLite (check_same_thread es necesario para evitar errores en SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()
