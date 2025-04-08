from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(String)
    precio = Column(Float)
    # Si hay relación con inventarios u otras tablas, agregarlas aquí
    inventory = relationship("Inventory", back_populates="producto")

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, index=True)
    cantidad = Column(Integer)

    producto = relationship("Product", back_populates="inventory")
