from typing import Optional

from pydantic import BaseModel, Field


class GetGoodsResponse(BaseModel):
    id: int
    brand_name: str
    product_name: str
    price: int
    discounted_price: int


class GetGoodsDetailResponse(BaseModel):
    id: int
    category: str
    brand_name: str
    product_name: str
    price: int
    discounted_price: int
    capacity: Optional[str] = None
    key_specification: Optional[str] = None
    expiration_date: Optional[str] = None
    how_to_use: Optional[str] = None
    ingredient: Optional[str] = None
    caution: Optional[str] = None
    contact_number: str


class GetProductResponse(BaseModel):
    id: int
    product_name: str
    price: int
    discounted_price: int


class GetProductDetailResponse(BaseModel):
    id: int
    category: str
    product_name: str
    price: int
    discounted_price: int
    capacity: Optional[str] = None
    key_specification: Optional[str] = None
    expiration_date: Optional[str] = None
    how_to_use: Optional[str] = None
    ingredient: Optional[str] = None
    caution: Optional[str] = None
    inventory_quantity: int
    use_status: bool


class GetRegisterInfoResponse(BaseModel):
    user_type: str
    email: str
    name: str


class GetSellerInfoResponse(BaseModel):
    email: str
    registration_number: str
    brand_name: str
    contact_number: Optional[str] = None


class GetBuyerInfoResponse(BaseModel):
    email: str
    name: str
    phone_number: str
    address: str


class CartResponse(BaseModel):
    product_id: int
    product_name: str
    price: int
    discounted_price: int
    quantity: int


class ShippingInfo(BaseModel):
    recipient_name: str = Field(description="받는 분")
    contact_number: str = Field(description="연락처")
    delivery_address: str = Field(description="배송 주소")
    delivery_message: str = Field(None, description="배송 메시지")


class GetCheckoutResponse(BaseModel):
    user_id: int = Field(description="주문자 ID")
    shipping_info: ShippingInfo
    items: list[CartResponse]
    total_price: int = Field(description="총 상품 금액")
