from sqlalchemy.orm import Session
import models, schemas


# ========== PRODUCTOS ==========

def crear_producto(db: Session, producto: schemas.ProductoCreate, stock: int):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    
    # Crear el inventario para el producto con el stock
    db_inventario = models.Inventario(producto_id=db_producto.id, cantidad=stock)
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    
    return db_producto

def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def obtener_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def eliminar_producto(db: Session, producto_id: int):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto


# ========== INVENTARIO ==========

def crear_inventario(db: Session, inventario: schemas.InventarioCreate):
    db_inventario = models.Inventario(**inventario.dict())
    db.add(db_inventario)
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

def obtener_inventario(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventario).offset(skip).limit(limit).all()

def obtener_stock_producto(db: Session, producto_id: int):
    return db.query(models.Inventario).filter(models.Inventario.producto_id == producto_id).first()

def actualizar_stock(db: Session, producto_id: int, nueva_cantidad: int):
    stock = db.query(models.Inventario).filter(models.Inventario.producto_id == producto_id).first()
    if stock:
        stock.cantidad = nueva_cantidad
        db.commit()
        db.refresh(stock)
    return stock
