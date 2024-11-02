from datetime import datetime

from fastapi import Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.schema.response import GetCheckoutResponse, OrderInfo, ShippingInfo
from src.service.auth import get_session_data
from src.service.cart import CartService
from src.service.order import OrderService
from src.service.session import SessionService
from src.service.user import UserService


async def get_checkout_handler(
    session_id: str = Cookie(None),
    session_service: SessionService = Depends(SessionService),
    user_service: UserService = Depends(UserService),
    cart_service: CartService = Depends(CartService),
) -> GetCheckoutResponse:
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing Session ID")

    session_data = await get_session_data(
        session_id=session_id, session_service=session_service
    )

    if "user_id" not in session_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = session_data["user_id"]

    user = await user_service.get_user_info(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    # 주문자 정보
    order_info = OrderInfo(
        user_id=user.id,
        name=user.buyer.name,
        email=user.email,
        phone_number=user.buyer.phone_number,
    )
    # 배송지 정보
    shipping_info = ShippingInfo(
        recipient_name=user.buyer.name,
        contact_number=user.buyer.phone_number,
        delivery_address=user.buyer.address,
    )
    # 주문 상품 목록
    cart_items = await cart_service.get_cart(user_id=user_id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    # 총 상품 금액
    total_price = sum(
        (item.discounted_price if item.discounted_price else item.price) * item.quantity
        for item in cart_items
    )
    # 주문 번호 생성
    now = datetime.now()
    date_str = now.strftime("%y%m%d%H%M")  # YYMMDDHHMM 형식
    order_no = f"Y{date_str}{user_id}"

    return GetCheckoutResponse(
        order_no=order_no,
        order_info=order_info,
        shipping_info=shipping_info,
        items=cart_items,
        total_price=total_price,
    )


async def create_order_handler(
    session_id: str = Cookie(None),
    session_service: SessionService = Depends(SessionService),
    cart_service: CartService = Depends(CartService),
    order_service: OrderService = Depends(OrderService),
):
    if not session_id:
        raise HTTPException(status_code=400, detail="Missing Session ID")

    session_data = await get_session_data(
        session_id=session_id, session_service=session_service
    )

    if "user_id" not in session_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = session_data["user_id"]
    cart_items = await cart_service.get_cart(user_id=user_id)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    created_order = await order_service.create_order(user_id=user_id, items=cart_items)
    await order_service.created_order_items(order_id=created_order.id, items=cart_items)
    await order_service.change_to_sold(items=cart_items)
    await cart_service.clear_cart(user_id=user_id)

    return JSONResponse(content={"message": "Your order has been completed"})
