import uuid
import time

class Order:

    def __init__(self, orderType, quantity, price):
        self.orderType = orderType
        self.quantity = quantity
        self.price = price
        self.time = time.localtime()
        self.id = str(uuid.uuid4())

    def getOrderType(self):
        return self.orderType

    def setTime(self, time):
        self.time = time

    def toValues(self):
        if self.orderType == "BUY":
            return time.strftime("%H:%M:%S", self.time), self.quantity, self.price
        if self.orderType == "SELL":
            return self.price, self.quantity, time.strftime("%H:%M:%S", self.time)

    def setQuantity(self, quantity):
        self.quantity = quantity

    def getPrice(self):
        return self.price

    def getTime(self):
        return self.time

    def getQuantity(self):
        return self.quantity

    def setPrice(self, price):
        self.price = price

