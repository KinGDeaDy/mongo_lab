def calculate_price(
        base_price: float,
        duty: float,
        category_discount: float,
        bulk_discount: float,
        loyalty_discount: float
) -> float:
    """
    вычисляет цену с учетом всех скидок и наценок.
    """
    price_with_duty = base_price + duty
    discounted_price = price_with_duty * (1 - category_discount) * (1 - bulk_discount) * (1 - loyalty_discount)
    return discounted_price
