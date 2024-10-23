import re
from typing import Optional

from fastapi import Depends, HTTPException, Query

from src.models.repository import ElasticsearchRepository
from src.schema.response import (
    GetGoodsDetailResponse,
    GetGoodsListResponse,
    GetGoodsPageResponse,
)


async def get_goods_list_handler(
    category: str = Query(default=None, max_length=15),
    search_after: Optional[list[int]] = Query(default=None),
    es_repo: ElasticsearchRepository = Depends(ElasticsearchRepository),
) -> GetGoodsPageResponse:
    if not category:
        goods_list, next_search_after = await es_repo.get_product_list(
            search_after=search_after
        )
    else:
        match = re.match(r"(\D+)(\d+)", category)
        if not match:
            raise HTTPException(status_code=400, detail="Invalid query format.")

        category_type, category_id = match.groups()

        goods_list, next_search_after = await es_repo.get_product_list_by_category(
            category_type=category_type,
            category_id=category_id,
            search_after=search_after,
        )

    if goods_list is None:
        goods_list = []

    response = [
        GetGoodsListResponse(
            id=goods["id"],
            brand_name=goods["brand_name"],
            product_name=goods["product_name"],
            price=goods["price"],
            discounted_price=goods["discounted_price"],
        )
        for goods in goods_list
    ]

    return GetGoodsPageResponse(products=response, next_search_after=next_search_after)


async def get_goods_by_id_handler(
    goods_id: int, es_repo: ElasticsearchRepository = Depends(ElasticsearchRepository)
) -> GetGoodsDetailResponse:
    goods: dict | None = await es_repo.get_product_by_id(product_id=goods_id)

    if goods is None:
        raise HTTPException(status_code=404, detail="Goods Not Found")

    return GetGoodsDetailResponse(
        category=f"{goods['category_1']} > {goods['category_2']} > {goods['category_3']}",
        **goods,
    )


async def search_goods_handler(
    keyword: str,
    search_after: Optional[list[int]] = Query(default=None),
    es_repo: ElasticsearchRepository = Depends(ElasticsearchRepository),
) -> GetGoodsPageResponse:
    if not keyword:
        raise HTTPException(
            status_code=422, detail="Keyword is required and cannot be empty."
        )

    goods_list, next_search_after = await es_repo.search_products(
        keyword=keyword, search_after=search_after
    )

    response = [
        GetGoodsListResponse(
            id=goods["id"],
            brand_name=goods["brand_name"],
            product_name=goods["product_name"],
            price=goods["price"],
            discounted_price=goods["discounted_price"],
        )
        for goods in goods_list
    ]

    return GetGoodsPageResponse(products=response, next_search_after=next_search_after)
