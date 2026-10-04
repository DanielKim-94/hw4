from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation: list[dict[str, str]] = Field(default_factory=list)
    current_page: str | None = None
    product_id: str | None = None

class CustomerContext(BaseModel):
    user_id: int | None = None
    name: str | None = None
    email: str | None = None
    current_page: str | None = None
    product_id: str | None = None
    current_product: dict | None = None

class ProductReference(BaseModel):
    product_id: str
    name: str
    price: float
    image_url: str | None = None
    garment_type: str = ""
    description: str = ""

class ChatResponse(BaseModel):
    message: str
    suggested_products: list[ProductReference] = Field(default_factory=list)

class ProductInfo(BaseModel):
    status: str = Field(description="found or unknown_product")
    product_id: str | None = None
    name: str | None = None
    description: str | None = None
    garment_type: str | None = None
    price: float | None = None
    colors: list[str] = Field(default_factory=list)
    image_file_path: str | None = None

class StockLine(BaseModel):
    size: str
    quantity: int

class StockLookup(BaseModel):
    status: str = Field(description="in_stock, out_of_stock, unavailable_size, or unknown_product")
    product_id: str | None = None
    product_name: str | None = None
    requested_size: str | None = None
    stock: list[StockLine] = Field(default_factory=list)
    quantity: int | None = None

class AlternativeProduct(BaseModel):
    product_id: str
    name: str
    price: float
    image_url: str
    reason: str

class AlternativesResult(BaseModel):
    status: str = Field(description="found or unknown_product")
    source_product: str
    alternatives: list[AlternativeProduct] = Field(default_factory=list)
