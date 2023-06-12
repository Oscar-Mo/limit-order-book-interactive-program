import uuid
import time


class Record:

    def __init__(self, price, quantity, recordTime):
        self.price = price
        self.quantity = quantity
        self.time = time.localtime()
        self.id = str(uuid.uuid4())

    def toValues(self):
        return self.price, self.quantity, time.strftime("%H:%M:%S", self.time)

    def getPrice(self):
        return self.price
