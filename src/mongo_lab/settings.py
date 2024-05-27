from typing import Final, TypedDict


class MongoCredentials(TypedDict):
    host: str
    port: int


MONGO_HOST: Final[str] = "localhost"
MONGO_PORT: Final[int] = 27017
DATABASE: Final[str] = "store_network"

mongo_credentials: MongoCredentials = {
    "host": MONGO_HOST,
    "port": MONGO_PORT
}

MONGO_CONNECT_STR: Final[str] = 'mongodb://{host}:{port}/'.format(**mongo_credentials)


# Таблицы параметров для расчета цен
CATEGORY_DISCOUNTS = {
    'эконом': {
        'base_customer': 0.05,
        'base_corporate': 0.02,
        'bulk_customer': 0.06,
        'bulk_corporate': 0.03
    },
    'стандарт': {
        'base_customer': 0.07,
        'base_corporate': 0.04,
        'bulk_customer': 0.07,
        'bulk_corporate': 0.05
    },
    'премиум': {
        'base_customer': 0.10,
        'base_corporate': 0.05,
        'bulk_customer': 0.11,
        'bulk_corporate': 0.06
    }
}

BULK_DISCOUNTS = {
    10: 0.02,
    100: 0.03,
    1000: 0.05
}

LOYALTY_DISCOUNTS = {
    'базовый': 0.05,
    'серебро': 0.10,
    'золото': 0.15
}
