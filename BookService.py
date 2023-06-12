from Record import Record
import time

class BookService:

    def __init__(self):
        self.bidOrders = []
        self.offerOrders = []
        self.time = time.localtime()
        self.history = []

    def getBidOrders(self):
        bidOrders = self.bidOrders
        return sorted(bidOrders,
                      key=lambda order: (-order.getPrice(), order.getTime()))

    def getOfferOrders(self):
        offerOrders = self.offerOrders
        return sorted(offerOrders,
                      key=lambda order: (order.getPrice(), order.getTime()))

    def addOrder(self, order):
        if (order.getPrice() == ""):
            self.setMarketOrder(order)
        else:
            order.setPrice(int(order.getPrice()))

        if (order.getOrderType() == "BUY"):
            self.bidOrders.append(order)
        elif (order.getOrderType() == "SELL"):
            self.offerOrders.append(order)
        else:
            print("ERROR -- Unrecognised order type")

    def removeOrder(self, order):
        if (order.getOrderType() == "BUY"):
            self.bidOrders.remove(order)
        elif (order.getOrderType() == "SELL"):
            self.offerOrders.remove(order)


    def transact(self, bid, ask):
        if (bid.getQuantity() > ask.getQuantity()):
            volume = ask.getQuantity()
            bid.setQuantity(bid.getQuantity() - ask.getQuantity())
            self.addToHistory(bid.getPrice(), volume, self.time)
            self.removeOrder(ask)
        elif (bid.getQuantity() < ask.getQuantity()):
            volume = bid.getQuantity()
            ask.setQuantity(ask.getQuantity() - bid.getQuantity())
            self.addToHistory(bid.getPrice(), volume, self.time)
            self.removeOrder(bid)
        elif (ask.getQuantity() == bid.getQuantity()):
            volume = ask.getQuantity()
            self.addToHistory(bid.getPrice(), volume, self.time)
            self.removeOrder(bid)
            self.removeOrder(ask)
        else:
            print("ERROR transacting")

    def addToHistory(self, price, volume, time):
        self.history.append(Record(price, volume, time))

    def fillOrders(self):
        for bid in self.getBidOrders():
            for ask in self.getOfferOrders():
                if bid.getPrice() == ask.getPrice():
                    self.transact(bid, ask)
                    self.fillOrders()
                    return

    def step(self):
        self.fillOrders()
        self.time = time.localtime()

    def getSpread(self):
        if len(self.getBidOrders()) == 0 or len(self.getOfferOrders()) == 0:
            return "NA"
        highestBid = self.getBidOrders()[0]
        lowestOffer = self.getOfferOrders()[0]
        return str(lowestOffer.getPrice() - highestBid.getPrice())

    def clearOrders(self):
        self.bidOrders.clear()
        self.offerOrders.clear()

    def getHistory(self):
        return self.history[::-1]

    def getLastPrice(self):
        if len(self.getHistory()) == 0:
            return "NA"
        return str(self.getHistory()[0].getPrice())

    def setMarketOrder(self, order):
        if (order.getOrderType() == "BUY"):
            order.setPrice(self.getOfferOrders()[0].getPrice())
        elif (order.getOrderType() == "SELL"):
            order.setPrice(self.getBidOrders()[0].getPrice())
        else:
            print("ERROR")




