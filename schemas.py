# schemas.py

from pydantic import BaseModel
from typing import Optional


# ===== PRODUCTO =====
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True


# ===== INVENTARIO =====
class InventarioBase(BaseModel):
    producto_id: int
    cantidad: int

class InventarioCreate(InventarioBase):
    pass

class Inventario(InventarioBase):
    id: int

    class Config:
        orm_mode = True
