from fastapi import Depends

from src.models.repository import (
    CartRepository,
    ElasticsearchRepository,
    ProductRepository,
)
from src.schema.response import CartResponse


class CartService:
    def __init__(
        self,
        cart_repo: CartRepository = Depends(CartRepository),
        es_repo: ElasticsearchRepository = Depends(ElasticsearchRepository),
        product_repo: ProductRepository = Depends(ProductRepository),
    ):
        self.cart_repo = cart_repo
        self.es_repo = es_repo
        self.product_repo = product_repo

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int) -> dict:
        # 1. MySQL에서 재고 확인
        stock = await self.product_repo.get_product_stock(product_id=product_id)

        if stock is None:
            return {
                "is_success": False,
                "status_code": 404,
                "message": "Product not found or unavailable",
            }
        if stock < quantity:
            return {
                "is_success": False,
                "status_code": 400,
                "message": "Insufficient stock",
            }

        # 2. 장바구니에 상품 추가 로직 호출
        await self.cart_repo.add_product(
            user_id=user_id, product_id=product_id, quantity=quantity
        )
        return {"is_success": True, "message": "Goods added to cart successfully"}

    async def get_cart(self, user_id: int) -> list[CartResponse]:
        cart_data = await self.cart_repo.get_cart(user_id=user_id)

        cart_response = []
        for product_id, quantity in cart_data.items():
            product_info = await self.es_repo.get_product_by_id(product_id=product_id)
            cart_response.append(
                CartResponse(product_id=product_id, quantity=quantity, **product_info)
            )

        return cart_response

    async def delete_from_cart(self, user_id: int, product_id: int):
        await self.cart_repo.delete_from_cart(user_id=user_id, product_id=product_id)

    async def clear_cart(self, user_id: int):
        await self.cart_repo.clear_cart(user_id=user_id)
