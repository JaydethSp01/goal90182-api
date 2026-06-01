from pydantic import BaseModel
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    categoria_id: int
    proveedor_id: int
