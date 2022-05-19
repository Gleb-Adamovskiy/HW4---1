from abc import ABC, abstractmethod
import re

class Storage(ABC):
    items = {}
    capacity = int

    @abstractmethod
    def add(self):
        "add`(<название>, <количество>)  - увеличивает запас items"

    @abstractmethod
    def remove(self):
        "remove`(<название>, <количество>) - уменьшает запас items"

    @abstractmethod
    def get_free_space(self):
        "вернуть количество свободных мест"

    @abstractmethod
    def get_items(self):
        "возвращает сожержание склада в словаре {товар: количество}"

    @abstractmethod
    def get_unique_items_count(self):
        "возвращает количество уникальных товаров"


class Store(Storage):
    # В нем хранится любое количество любых товаров
    def __init__(self):
        self._items = {}
        self._capacity = 100

    @property
    def items(self):
        return self._items

    @property
    def capacity(self):
        return self._capacity

    def sum_items(self):
        # вычисляет количество товара на складе
        return sum(self.items.values())

    def add(self, title: str, quantity: int):
        if self.capacity >= (self.sum_items() + quantity):
            # проверяем не превысим ли вместимость склада
            self.items[title] = self.items.get(title, 0) + quantity
            # если все нормально - добавляем товары на склад
            return self.items
        else:
            print("На складе недостаточно места, попробуйте уменьшить количество товара")
            return exit()

    def remove(self, title: str, quantity: int):
        if self.items[title] < quantity:
            print("не хватает на складе, попробуйте заказать меньше")
            return exit()
        else:
            self.items[title] = self.items.get(title, 0) - quantity
            if self.items[title] == 0:
                self.items.pop(title)
            return self.items

    def get_free_space(self):
        return self.capacity - self.sum_items()

    def get_items(self):
        return self.items

    def print_items(self):
        for k, v in self.items.items():
            print(v, ':', k)

    def get_unique_items_count(self):
        return len(self.items)


class Shop(Storage):
    # В нем хранится не больше 5 разных товаров
    def __init__(self):
        self._items = {}
        self._capacity = 20

    @property
    def items(self):
        return self._items

    @property
    def capacity(self):
        return self._capacity

    def sum_items(self):
        # вычисляет количество товара на складе магазина
        return sum(self.items.values())

    def add(self, title: str, quantity: int):
        if self.get_unique_items_count() < 5:
            # проверка не превышен ли предел на уникальные товары
            if self.capacity >= (self.sum_items() + quantity):
                # проверяем не превысим ли вместимость склада
                self.items[title] = self.items.get(title, 0) + quantity
                # если все нормально - добавляем товары на склад
                return self.items
            else:
                print("На складе магазина недостаточно места, попробуйте уменьшить количество товара")
                return exit()
        else:
            print("На складе уже есть 5 уникальных товаров")
            return exit()

    def remove(self, title: str, quantity: int):
        if title not in self.get_items():
            print("выбранного товара нет на этом складе")
            return exit()
        if self.items[title] < quantity:
            print("не хватает на складе, попробуйте заказать меньше")
            return exit()
        else:
            self.items[title] = self.items.get(title, 0) - quantity
            if self.items[title] == 0:
                self.items.pop(title)
            return self.items

    def get_free_space(self):
        return self.capacity - self.sum_items()

    def get_items(self):
        return self.items

    def print_items(self):
        for k, v in self.items.items():
            print(v, ':', k)

    def get_unique_items_count(self):
        return len(self.items)


class Request():
    _from = ""
    _to = ""
    _amount = int
    _product = ""

    def __init__(self, stroka, store, shop):
        # передаем текст запроса пользователя
        self.stroka = stroka

        def finder():
            # функция поиска числового значения в запросе
            return ''.join(re.findall("\d", self.stroka.lower()))

        def splitter():
            # функция для разбивки строки в словарь
            return self.stroka.split()

        # определяем индексы складов и продукта
        otkuda_index = splitter().index('из') + 1
        kuda_index = splitter().index('в') + 1
        what_index = splitter().index(finder()) + 1

        # задаем названия складов, количества и названия продуктов в поля экземпляра класса
        self._from = splitter()[otkuda_index]
        self._to = splitter()[kuda_index]
        self._product = splitter()[what_index]
        self._amount = int(finder())

        if "ск" in self._from:
            self._store = store
            self._shop = shop
        else:
            self._store = shop
            self._shop = store

    @property
    def from_(self):
        return self._from

    @property
    def to(self):
        return self._to

    @property
    def product(self):
        return self._product

    @property
    def amount(self):
        return self._amount

    @property
    def store(self):
        return self._store

    @property
    def shop(self):
        return self._shop


if __name__ == '__main__':
    store = Store()
    shop = Shop()
    # заполняем склад для проверки
    store.add(title='печеньки', quantity=90)
    shop.add(title='собачки', quantity=10)
    shop.add(title='коробки', quantity=5)
    # запрашиваем пользователя о перевозке
    user_request = Request(input("че куда везем? "), store, shop)
    # пытаемя забрать продукт со склада
    user_request.store.remove(user_request.product, user_request.amount)

    print(f"Курьер забирает {user_request.amount} {user_request.product} из "
          f"{user_request.from_}")

    print(f"Курьер везет {user_request.amount} {user_request.product} из "
          f"{user_request.from_} в {user_request.to}")
    # пытаемя поместить продукт на склад
    user_request.shop.add(user_request.product, user_request.amount)

    print(f"Курьер доставил {user_request.amount} {user_request.product} из "
          f"{user_request.from_} в {user_request.to}")
    # выводим список продуктов на складах
    print(f"В {user_request.from_} хранится:")
    user_request.store.print_items()
    print(f"В {user_request.to} хранится:")
    user_request.shop.print_items()
