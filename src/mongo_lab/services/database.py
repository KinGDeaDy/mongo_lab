from bson.objectid import ObjectId
from pymongo import MongoClient

from mongo_lab.settings import (BULK_DISCOUNTS, CATEGORY_DISCOUNTS, DATABASE,
                                LOYALTY_DISCOUNTS, MONGO_CONNECT_STR)
from mongo_lab.utils.calculations import calculate_price


class MongoDB:
    def __init__(self):
        self.__client: MongoClient = MongoClient(MONGO_CONNECT_STR)
        self._db = self.__client[DATABASE]
        # Коллекции
        self.stores_col = self._db['stores']
        self.racks_col = self._db['racks']
        self.products_col = self._db['products']

    def add_store(self, store_name: str) -> ObjectId:
        """
        добавляет магазин и возвращает его ID.
        """
        store_id = self.stores_col.insert_one(
            {'name': store_name, 'racks': []}
        ).inserted_id
        return store_id

    def add_rack(self, store_id: ObjectId, rack_name: str) -> ObjectId:
        """
        добавляет стойку в магазин и возвращает её ID.
        """
        rack_id = self.racks_col.insert_one(
            {'name': rack_name, 'products': []}
        ).inserted_id
        self.stores_col.update_one(
            {'_id': store_id},
            {'$push': {'racks': rack_id}}
        )
        return rack_id

    def add_product(
            self,
            rack_id: ObjectId,
            product_data: dict[str, str | float]
    ) -> ObjectId:
        """
        добавляет товар в стойку и возвращает его ID.
        """
        product_id = self.products_col.insert_one(product_data).inserted_id
        self.racks_col.update_one(
            {'_id': rack_id},
            {'$push': {'products': product_id}}
        )
        return product_id

    def get_product_info(
            self,
            product_id: ObjectId,
            loyalty_program: str
    ) -> dict[str, float | str]:
        """
        возвращает подробную информацию о товаре,
        включая рассчитанные цены для различных категорий и объемов.
        """
        product = self.products_col.find_one({'_id': product_id})
        if not product:
            return None
        base_price = product['base_price']
        bulk_price = product['bulk_price']
        duty = product['duty']
        category = product['category']
        category_discounts = CATEGORY_DISCOUNTS[category]

        prices = {}
        for quantity in [1, 10, 100, 1000]:
            bulk_discount = BULK_DISCOUNTS.get(quantity, 0)
            base_customer_price = calculate_price(
                base_price, duty, category_discounts['base_customer'],
                bulk_discount,
                LOYALTY_DISCOUNTS[loyalty_program]
            )
            base_corporate_price = calculate_price(
                base_price, duty, category_discounts['base_corporate'],
                bulk_discount, LOYALTY_DISCOUNTS[loyalty_program]
            )
            bulk_customer_price = calculate_price(
                bulk_price, duty, category_discounts['bulk_customer'],
                bulk_discount,
                LOYALTY_DISCOUNTS[loyalty_program]
            )
            bulk_corporate_price = calculate_price(
                bulk_price, duty, category_discounts['bulk_corporate'],
                bulk_discount, LOYALTY_DISCOUNTS[loyalty_program]
            )

            prices[quantity] = {
                'base_customer_price': base_customer_price,
                'base_corporate_price': base_corporate_price,
                'bulk_customer_price': bulk_customer_price,
                'bulk_corporate_price': bulk_corporate_price
            }

        return {
            'name': product['name'],
            'category': category,
            'properties': product['properties'],
            'prices': prices
        }
