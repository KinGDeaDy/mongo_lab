from bson.objectid import ObjectId

from mongo_lab.services.database import MongoDB

if __name__ == '__main__':
    mongo = MongoDB()
    # Пример использования
    store_id: ObjectId = mongo.add_store("Магазин 1")
    rack_id: ObjectId = mongo.add_rack(store_id, "Стойка 1")
    product_id: ObjectId = mongo.add_product(rack_id, {
        'name': 'Товар 1',
        'base_price': 100.0,
        'bulk_price': 90.0,
        'duty': 10.0,
        'category': 'эконом',
        'properties': {'цвет': 'красный', 'вес': '1кг'}
    })
    product_info = mongo.get_product_info(product_id, 'золото')
    print(product_info)

