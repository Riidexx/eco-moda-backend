from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EcoModa API",
    description="Backend del sistema de gestión de inventario de EcoModa",
    version="1.0.0"
)

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========= PRODUCTOS ==========

@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, stock: int, db: Session = Depends(get_db)):
    db_producto = crud.crear_producto(db, producto)
    crud.crear_inventario(db, schemas.InventarioCreate(producto_id=db_producto.id, cantidad=stock))
    return db_producto

@app.get("/productos/", response_model=list[schemas.Producto])
def obtener_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.obtener_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.delete("/productos/{producto_id}", response_model=schemas.Producto)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.eliminar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# ========= INVENTARIO ==========

@app.get("/inventario/", response_model=list[schemas.Inventario])
def obtener_inventario(db: Session = Depends(get_db)):
    return crud.obtener_inventario(db)

@app.get("/inventario/{producto_id}", response_model=schemas.Inventario)
def obtener_stock_producto(producto_id: int, db: Session = Depends(get_db)):
    stock = crud.obtener_stock_producto(db, producto_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Producto no tiene inventario")
    return stock

@app.post("/reducir_stock/", response_model=schemas.Inventario)
def reducir_stock(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    stock = crud.obtener_stock_producto(db, producto_id)
    if not stock or stock.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    return crud.actualizar_stock(db, producto_id, stock.cantidad - cantidad)

@app.post("/comprar/", response_model=schemas.CompraConfirmacion)
def comprar_producto(producto_id: int, cantidad: int, db: Session = Depends(get_db)):
    stock = crud.obtener_stock_producto(db, producto_id)
    producto = crud.obtener_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not stock or stock.cantidad < cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")
    
    nuevo_stock = crud.actualizar_stock(db, producto_id, stock.cantidad - cantidad)
    
    return schemas.CompraConfirmacion(
        producto=producto,
        cantidad=cantidad,
        mensaje=f"Compra exitosa. Quedan {nuevo_stock.cantidad} unidades en inventario."
    )
