from ninja import Schema
from typing import List, Optional, Dict
from datetime import datetime

# Схемы для запроса/ответа
class AuthIn(Schema):
    username: str
    password: str

class TokenOut(Schema):
    access: str
    refresh: str = None  # опционально



# Схема для создания/обновления товара
class ProductIn(Schema):
    brand: str
    article: str
    trading_numbers: Optional[str] = None
    description: Optional[str] = None
    additional_name: Optional[str] = None
    product_status: Optional[str] = None
    specifications: Optional[str] = None


# Схема для вывода товара
class ProductOut(Schema):
    id: int
    brand: str
    article: str
    cross_brand: str | None = None
    cross_article: str | None = None

    class Config:
        from_attributes = True  # Для совместимости с Pydantic v2

class CrossReferenceOut(Schema):
    id: int
    cross_brand: str
    cross_article: str


# Схема для товара с кроссами (адаптируем вашу)
class ProductWithCrossesOut(Schema):
    product: ProductOut
    crosses: list[dict] = []

    @staticmethod
    def resolve_crosses(obj):
        if obj.cross_brand and obj.cross_article:
            return [{
                "cross_brand": obj.cross_brand,
                "cross_article": obj.cross_article
            }]
        return []

# Схема для входных данных
class ArticleCrossIn(Schema):
    brand: str
    article: str
    cross_brand: str
    cross_article: str
    trading_numbers: Optional[str] = None
    description: Optional[str] = None
    additional_name: Optional[str] = None
    product_status: Optional[str] = None
    specifications: Optional[str] = None
    product_group_id: Optional[int] = None

# Схема ответа
class ArticleCrossOut(Schema):
    id: int
    brand: str
    article: str
    cross_brand: str
    cross_article: str

class ArticleUpdateSchema(Schema):
    article: str
    brand: Optional[str] = None
    new_article: Optional[str] = None
    cross_brand: Optional[str] = None
    cross_article: Optional[str] = None
    trading_numbers: Optional[str] = None
    description: Optional[str] = None
    additional_name: Optional[str] = None
    product_status: Optional[str] = None
    specifications: Optional[str] = None
    product_group_id: Optional[int] = None



