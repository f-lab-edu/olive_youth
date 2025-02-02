from fastapi import APIRouter, status

from src.apis.store import cart, goods, product
from src.schema import response

store_router = APIRouter(tags=["store"])

store_router.add_api_route(
    methods=["GET"],
    path="/goods",
    endpoint=goods.get_goods_list_handler,
    response_model=goods.GetGoodsPageResponse,
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["GET"],
    path="/goods/{goods_id}",
    endpoint=goods.get_goods_by_id_handler,
    response_model=goods.GetGoodsDetailResponse,
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["GET"],
    path="/search",
    endpoint=goods.search_goods_handler,
    response_model=goods.GetGoodsPageResponse,
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["POST"],
    path="/products",
    endpoint=product.create_product_handler,
    response_model=product.GetProductResponse,
    status_code=status.HTTP_201_CREATED,
)

store_router.add_api_route(
    methods=["GET"],
    path="/products/{product_id}",
    endpoint=product.get_product_by_id_handler,
    response_model=product.GetProductDetailResponse,
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["PATCH"],
    path="/products/{product_id}",
    endpoint=product.update_product_handler,
    response_model=product.GetProductResponse,
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["DELETE"],
    path="/products/{product_id}",
    endpoint=product.delete_product_handler,
    status_code=status.HTTP_204_NO_CONTENT,
)

store_router.add_api_route(
    methods=["POST"],
    path="/cart",
    endpoint=cart.add_to_cart_handler,
    status_code=status.HTTP_201_CREATED,
)

store_router.add_api_route(
    methods=["GET"],
    path="/cart",
    endpoint=cart.get_cart_handler,
    response_model=list[response.CartResponse],
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["DELETE"],
    path="/cart",
    endpoint=cart.clear_cart_handler,
    status_code=status.HTTP_204_NO_CONTENT,
)

store_router.add_api_route(
    methods=["DELETE"],
    path="/cart/{product_id}",
    endpoint=cart.delete_from_cart_handler,
    status_code=status.HTTP_204_NO_CONTENT,
)

store_router.add_api_route(
    methods=["PUT"],
    path="/cart/{product_id}",
    endpoint=cart.update_cart_quantity_handler,
    status_code=status.HTTP_200_OK,
)

store_router.add_api_route(
    methods=["DELETE"],
    path="/close-pit",
    endpoint=goods.close_pit_handler,
    status_code=status.HTTP_204_NO_CONTENT,
)
