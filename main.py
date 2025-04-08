from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

# Crea las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoModa API",
    description="Backend del sistema de gestión de inventario de EcoModa",
    version="1.0.0",
)

# Middleware CORS (permite conexión con el frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplazar con dominio del frontend en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener la sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ========== RUTAS PRODUCTOS ==========

@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, stock: int = 0, db: Session = Depends(get_db)):
    # Crear producto
    db_producto = crud.crear_producto(db, producto)
    
    # Crear inventario con el stock proporcionado
    crud.crear_inventario(db, schemas.InventarioCreate(producto_id=db_producto.id, cantidad=stock))
    
    return db_producto

@app.get("/productos/", response_model=list[schemas.Producto])
def listar_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_productos(db, skip, limit)

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.obtener_producto(db, producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.eliminar_producto(db, producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


# ========== RUTAS INVENTARIO ==========

@app.post("/inventario/", response_model=schemas.Inventario)
def crear_inventario(inventario: schemas.InventarioCreate, db: Session = Depends(get_db)):
    return crud.crear_inventario(db, inventario)

@app.get("/inventario/", response_model=list[schemas.Inventario])
def listar_inventario(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_inventario(db, skip, limit)

@app.get("/inventario/{producto_id}", response_model=schemas.Inventario)
def obtener_stock(producto_id: int, db: Session = Depends(get_db)):
    db_stock = crud.obtener_stock_producto(db, producto_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return db_stock

@app.put("/inventario/{producto_id}", response_model=schemas.Inventario)
def actualizar_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    db_stock = crud.actualizar_stock(db, producto_id, cantidad)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return db_stock
