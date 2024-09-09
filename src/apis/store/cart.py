from fastapi import Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.models.repository import CartRepository, ElasticsearchRepository
from src.schema.request import AddToCartRequest
from src.schema.response import CartResponse
from src.service.auth import get_session_data
from src.service.session import SessionService


async def add_to_cart_handler(
    request: AddToCartRequest,
    cart_repo: CartRepository = Depends(CartRepository),
    session_id: str = Cookie(None),
    session_service: SessionService = Depends(),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing Session ID")

    session_data = await get_session_data(
        session_id=session_id, session_service=session_service
    )

    if "user_id" not in session_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    await cart_repo.add_product(
        user_id=session_data["user_id"],
        product_id=request.product_id,
        quantity=request.quantity,
    )

    await session_service.extend_session(session_id=session_id)

    response = JSONResponse(content={"message": "Goods added to cart successfully"})
    return response


async def get_cart_handler(
    cart_repo: CartRepository = Depends(CartRepository),
    es_repo: ElasticsearchRepository = Depends(ElasticsearchRepository),
    session_id: str = Cookie(None),
    session_service: SessionService = Depends(),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing Session ID")

    session_data = await get_session_data(
        session_id=session_id, session_service=session_service
    )

    if "user_id" not in session_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    cart_data = await cart_repo.get_cart(user_id=session_data["user_id"])

    cart_response = []
    for product_id, quantity in cart_data.items():
        product_info = await es_repo.get_product_by_id(product_id=product_id)
        cart_response.append(
            CartResponse(product_id=product_id, quantity=quantity, **product_info)
        )

    return cart_response


async def delete_from_cart_handler(
    product_id: int,
    cart_repo: CartRepository = Depends(CartRepository),
    session_id: str = Cookie(None),
    session_service: SessionService = Depends(),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing Session ID")

    session_data = await get_session_data(
        session_id=session_id, session_service=session_service
    )

    if "user_id" not in session_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    await cart_repo.delete_from_cart(
        user_id=session_data["user_id"], product_id=product_id
    )


async def clear_cart_handler(
    cart_repo: CartRepository = Depends(CartRepository),
    session_id: str = Cookie(None),
    session_service: SessionService = Depends(),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing Session ID")

    session_data = await get_session_data(
        session_id=session_id, session_service=session_service
    )

    if "user_id" not in session_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    await cart_repo.clear_cart(user_id=session_data["user_id"])