from fastapi import FastAPI
from sqlalchemy.orm import Session
from models import Product, Inventory  # Asegúrate de tener estos modelos correctamente definidos
from database import SessionLocal, engine
from sqlalchemy import create_engine

app = FastAPI()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para obtener los productos con su stock
@app.get("/productos/")
async def obtener_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    productos = db.query(Product).offset(skip).limit(limit).all()
    productos_con_stock = []
    for producto in productos:
        # Suponiendo que 'Inventory' es el modelo para el inventario
        stock = db.query(Inventory).filter(Inventory.producto_id == producto.id).first()
        stock = stock.cantidad if stock else 0  # Si no hay stock, asumir que es 0
        producto_dict = producto.__dict__
        producto_dict["stock"] = stock  # Añadir el stock
        productos_con_stock.append(producto_dict)
    return productos_con_stock
