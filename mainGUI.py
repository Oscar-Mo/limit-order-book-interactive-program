from tkinter import *
from tkinter.ttk import *
from BookService import BookService
from Order import Order



def updateUI():
    def updateListUI(listUI, data):
        listUI.delete(*listUI.get_children())
        for item in data:
            listUI.insert(parent="", index="end", values=item.toValues())

    def updateInformationUI():
        spreadValueLabel.configure(text="Spread: " + bookService.getSpread())
        priceValueLabel.configure(text="Last Price: " + bookService.getLastPrice())
        historyList.delete(*historyList.get_children())
        for record in bookService.getHistory():
            historyList.insert(parent="", index="end", values=record.toValues())

    updateListUI(bidList, bookService.getBidOrders())
    updateListUI(offerList, bookService.getOfferOrders())
    updateInformationUI()

def processOrder(orderType, quantity, price):
    order = Order(orderType, quantity, price)
    bookService.addOrder(order)
    updateUI()

def setUpTable(table, alignment):
    table['show'] = 'headings' # gets rid of empty first column
    table.column("price_column", width=100, anchor=alignment)
    table.column("quantity_column", width=100, anchor=alignment)
    table.column("time_column", width=100, anchor=alignment)
    table.heading("price_column", text="Price")
    table.heading("quantity_column", text="Quantity")
    table.heading("time_column", text="Time")

def step():
    bookService.step()
    updateUI()

def clearOrders():
    bookService.clearOrders()
    updateUI()


bookService = BookService()

root = Tk()
root.title("Limit Order Book")

# Big frames
interactiveFrame = Frame(root)
interactiveFrame.pack(side=LEFT, fill=BOTH)
informationFrame = Frame(root, width=100, height=100)
informationFrame.pack(side=LEFT, fill=BOTH)




# Book
bookLabelFrame = Frame(interactiveFrame)
bookLabelFrame.pack(side=TOP)
bidLabelFrame = Frame(bookLabelFrame)
bidLabelFrame.pack(side=LEFT)
bidLabel = Label(bidLabelFrame, text="BIDS")
bidLabel.pack()
offersLabelFrame = Frame(bookLabelFrame)
offersLabelFrame.pack(side=LEFT)
offerLabel = Label(offersLabelFrame, text="OFFERS")
offerLabel.pack()


bookFrame = Frame(interactiveFrame)
bookFrame.pack(fill=BOTH, expand=1)
bookScrollbar = Scrollbar(bookFrame, orient=VERTICAL)

bidList = Treeview(bookFrame, columns=("time_column", "quantity_column", "price_column"),
                   yscrollcommand=bookScrollbar.set)
setUpTable(bidList, alignment=E)

offerList = Treeview(bookFrame, columns=("price_column", "quantity_column", "time_column"),
                     yscrollcommand=bookScrollbar.set)
setUpTable(offerList, alignment=W)

bookScrollbar.configure(command=bidList.yview)
bidList.pack(side=LEFT, fill=BOTH, expand=1)
offerList.pack(side=LEFT, fill=BOTH, expand=1)
bookScrollbar.pack(side=RIGHT, fill=Y)


# Command interface
commandFrame = Frame(interactiveFrame)
commandFrame.pack(fill=X)
orderTypeFrame = Frame(commandFrame)
orderTypeFrame.pack()
orderType = StringVar(orderTypeFrame)
orderType.set("BUY")  # Default
typeOptionMenu = OptionMenu(orderTypeFrame, orderType, "BUY", "SELL")
typeOptionMenu.pack()

quantityFrame = Frame(commandFrame)
quantityFrame.pack()
quantityLabel = Label(quantityFrame, text="Quantity: ")
quantityLabel.pack(side=LEFT)
quantityText = Entry(quantityFrame)
quantityText.pack(side=LEFT)

priceFrame = Frame(commandFrame)
priceFrame.pack()
priceLabel = Label(priceFrame, text="Price: ")
priceLabel.pack(side=LEFT)
priceText = Entry(priceFrame)
priceText.pack(side=LEFT)

addOrderButton = Button(commandFrame, text="Add Order",
                        command=lambda: processOrder(
                            orderType=orderType.get(),
                            quantity=int(quantityText.get()),
                            price=priceText.get())
                        )
addOrderButton.pack(side=TOP)


stepButton = Button(commandFrame, text="Execute", command=step)
stepButton.pack(side=RIGHT)
clearOrdersButton = Button(commandFrame, text="Clear Orders", command=clearOrders)
clearOrdersButton.pack(side=LEFT)





## Information
historyLabel = Label(informationFrame, text="History")
historyLabel.pack()
historyScrollbar = Scrollbar(informationFrame, orient=VERTICAL)
historyList = Treeview(informationFrame,
                       columns=("price_column", "volume_column", "time_column"),
                       yscrollcommand=historyScrollbar.set)
historyList['show'] = 'headings' # gets rid of empty first column
historyList.column("price_column", width=100, anchor=N)
historyList.column("volume_column", width=100, anchor=N)
historyList.column("time_column", width=100, anchor=N)
historyList.heading("price_column", text="Price")
historyList.heading("volume_column", text="Volume")
historyList.heading("time_column", text="Time")
historyList.pack(side=TOP, fill=BOTH, expand=1)

spreadValueLabel = Label(informationFrame, text="Spread: " + bookService.getSpread())
spreadValueLabel.pack()
priceValueLabel = Label(informationFrame, text="Last Price: " + bookService.getLastPrice())
priceValueLabel.pack()





# root.geometry("600x400")
root.mainloop()
