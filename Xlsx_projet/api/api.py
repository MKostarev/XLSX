from typing import List

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from django.contrib.auth import authenticate
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ninja import NinjaAPI
from .schemas import TokenOut, AuthIn, ProductWithCrossesOut, ArticleCrossOut, ArticleCrossIn, \
    ArticleUpdateSchema
from Xlsx_projet.settings import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET, JWT_ALGORITHM
from ninja.security import HttpBearer
from upload_files.models import Product, ProductGroup


api = NinjaAPI()


@api.post("/auth/token", response={200: TokenOut, 401: dict})
def login(request, payload: AuthIn):
    user = authenticate(username=payload.username, password=payload.password)
    if not user:
        return 401, {"error": "Invalid credentials"}

    # Генерируем JWT-токен
    access_token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        },
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return 200, {"access": access_token}



# Аутентификация через JWT
class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            request.user_id = payload["user_id"]
            return token
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

@api.get("/get_article_crosses", response=List[ProductWithCrossesOut], auth=JWTBearer())
def get_article_crosses(request):
    """Возвращает все товары с их кроссами"""
    products = Product.objects.all()
    return [
        {
            "product": product,
            "crosses": []
        }
        for product in products
    ]


@api.post(
    "/add_article_crosses",
    response={201: ArticleCrossOut, 400: dict, 401: dict, 409: dict},
    auth=JWTBearer()
)
def add_article_crosses(request, payload: ArticleCrossIn):
    """
    Добавляет новый артикул с кросс-ссылками
    Обязательные поля: brand, article, cross_brand, cross_article
    Остальные поля - опциональны
    """
    try:
        # Проверяем существование артикула
        if Product.objects.filter(article=payload.article).exists():
            return 409, {"detail": "Артикул уже существует"}

        # Получаем группу товаров
        product_group = None
        if payload.product_group_id:
            product_group = ProductGroup.objects.get(id=payload.product_group_id)
        else:
            product_group = ProductGroup.objects.get(name='Запчасти')

        # Создаем продукт
        product = Product.objects.create(
            brand=payload.brand,
            article=payload.article,
            cross_brand=payload.cross_brand,
            cross_article=payload.cross_article,
            trading_numbers=payload.trading_numbers,
            description=payload.description or "",
            additional_name=payload.additional_name or "",
            product_status=payload.product_status or "",
            specifications=payload.specifications or "",
            product_group=product_group
        )

        return 201, {
            "id": product.id,
            "brand": product.brand,
            "article": product.article,
            "cross_brand": product.cross_brand,
            "cross_article": product.cross_article
        }

    except ProductGroup.DoesNotExist:
        return 400, {"detail": "Указанная группа товаров не существует"}
    except Exception as e:
        return 400, {"detail": f"Ошибка при создании: {str(e)}"}


@api.post(
    "/update_article_crosses",
    response={200: ArticleCrossOut, 404: dict, 400: dict},
    auth=JWTBearer()
)
def update_article_crosses(request, payload: ArticleUpdateSchema):
    """Обновляет данные товара и кросс-ссылок"""
    try:
        # Ищем товар по артикулу
        product = get_object_or_404(Product, article=payload.article)

        # Обновляем поля
        if payload.brand:
            product.brand = payload.brand
        if payload.new_article:
            product.article = payload.new_article
        if payload.cross_brand:
            product.cross_brand = payload.cross_brand
        if payload.cross_article:
            product.cross_article = payload.cross_article
        if payload.trading_numbers is not None:
            product.trading_numbers = payload.trading_numbers
        if payload.description is not None:
            product.description = payload.description
        if payload.additional_name is not None:
            product.additional_name = payload.additional_name
        if payload.product_status is not None:
            product.product_status = payload.product_status
        if payload.specifications is not None:
            product.specifications = payload.specifications
        if payload.product_group_id:
            product.product_group = get_object_or_404(ProductGroup, id=payload.product_group_id)

        product.save()

        return 200, {
            "id": product.id,
            "brand": product.brand,
            "article": product.article,
            "cross_brand": product.cross_brand,
            "cross_article": product.cross_article
        }

    except Exception as e:
        return 400, {"detail": str(e)}

#Тест API
@api.get("/test")
def hello(request):
    return {"message": "Hello World!"}



