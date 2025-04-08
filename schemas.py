from pydantic import BaseModel

# ========== PRODUCTOS ==========

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str | None = None  # Si planeas usarlo

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        orm_mode = True

# ========== INVENTARIO ==========

class InventarioBase(BaseModel):
    producto_id: int
    cantidad: int

class InventarioCreate(InventarioBase):
    pass

class Inventario(InventarioBase):
    id: int

    class Config:
        orm_mode = True
