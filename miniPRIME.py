import random

class Position(dict):
    """This class creates a financial position in which trades are stored and information regarding the development of the position can be showed
        in a user friendly way.

    The position is at start an empty dictionary where the instrument, portfolio, price, acquirer, counterparty, quantity, marketplace and time of the transaction can be stored.
    The position can be grouped by portfolio kind, acquirer, conterparty or marketplace to give an easy overlook to the user. Only selected information
    from the transaction is presented together with current market price of the instrument, the profit/loss from the transaction and the total profit/loss
    for the positions.

    The position class consists of:

          :param acquirer: the acquirer of the transaction
          :param counterparty:the counterparty of the transaction
          :param instrument: the instrument that has been traded
          :param marketplace: the market where the instrument was traded
          :param portfolio: the kind of portfolio the trade belongs to
          :param price: the price of the instrument at transaction
          :param quantity: the quantity of the traded instrument
          :param time: the time of the trade
          :type acquirer: strings
          :type counterparty: stringv
          :type instrument: instrument object
          :type marketplace: string
          :type portfolio: string
          :type price: float
          :type quantity: integer
          :type time: string.

    The instrument has the following methods:

          :method convert_data: converts a Position from dictionary with keys to a structure where each line is one trade and structured by:
                                Name, Issuer, Market Price, Trading price, Profit/Loss, Profit/Loss (%), Currency, Quantity, Day of transaction
                                where Profit/Loss are calculated refering to current market price and the transaction price
          :method group_by: creates subpositions based one of the following categories:
                            portfolio, marketplace, acquirer, counterparty.
                            The method prints out a user friendly structure where some information are presented in order to give the user an onverlook.
          :method profit: returns the profit of one transaction based on its current market price, transaction price and quantity
          :method profit_percent: returns the profit in percent of one transaction based on its current market price, transaction price and quantity
          :method total_profit: returns the profit of all transactions based on their current market price, transaction price and quantity
          :method total_profit_percent:  returns the profit in percent of all transactions based on their current market price, transaction price and quantity

      :Example:

      A empty position named gonna_get_rich is created:
        gonna_get_rich=Position()

      The two Instrument ABB and Volvo are traded and the information is then stored in gonna_get_rich:
        ABB.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=10, marketplace="OMX", time=stime, position=gonna_get_rich)
        Volvo.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=3, marketplace="OMX", time=stime, position=gonna_get_rich)

      Information about the position and its porfit/loss can be showed by (however since price have not been updated the result is not that interesting):
        gonna_get_rich.group_by()

      If first the prices are updated and then the group_by method is used, one sees a more interesting result:
        ABB.price_update()
        Volvo.price_update()
        gonna_get_rich.group_by()

      If one wish not to group by kind of portfolio, one can provide the group_by method with the category argument:
        gonna_get_rich.group_by(category="counterparty")

    """

    def __init__(self):
        keyDict = {"instrument","portfolio","price","acquirer", "counterparty", "quantity", "marketplace", "time"}
        for key in keyDict:
            self[key]=[]

    def __str__(self):
        "Prints out the information about the portfolio in correlation to current market price"

        data=self.convert_data()
        sheet=""
        col_width = max(len(word) for row in data for word in row) # padding
        for row in data:
            sheet=sheet+"".join(word.center(col_width) for word in row)+"\n"
        return sheet

    def convert_data(self):
        "Extracts parts of the data, and makes some calculations, in the position from dictionary with keys, such as quantity, to one line structrue"
        "in order to select certain information to present to the user in a user friendly way"

        data=[["Name:", "Issuer:","Market Price:", "Trading price:", "Profit/Loss:" ,"Profit/Loss (%):","Currency:", "Quantity:", "Day of transaction:"]]
        for i in range(len(self["instrument"])):
            mp=self["instrument"][i].getprice()
            tp=self["price"][i]
            q=self["quantity"][i]
            data.append([self["instrument"][i].getname(), self["instrument"][i].getissuer(), str(mp), str(tp), str(self.profit(mp,tp,q)),
                            str(self.profit_percent(mp,tp)), self["instrument"][i].getcurrency(), str(q), self["time"][i]])
        return data

    def group_by(self, category="portfolio"):
        "Groups the position in subpositions on instrument together with the selected category, by default the kind of portfolio, and presents this to"
        "the user as printouts. To make it user friendly the printout starts with Positions: followed by the keys which the subpositions where created by."
        "Then selected information from trade are presented together with its current market price and the profit/loss."
        "The printout ends with a total view over the total profit from all trades."
        "The categories which can be grouped by are portfolio, marketplace, acquirer and counterparty."

        assert category=="portfolio" or category=="marketplace" or category=="acquirer" or category=="counterparty"
        diffcat=set(self[category])
        print("Positions:")
        for key in sorted(diffcat):
            print("\n"+key+": \n")
            d=Position()
            for i in range(len(self[category])):
                if self[category][i]==key:
                    for orgkey in self.keys():
                        d[orgkey].append(self[orgkey][i])
            print(d)
        print("Total profit: "+str(self.total_profit()))
        print("Total profit (%): "+str(self.total_profit_percent())+"\n\n")

    def profit(self,market_price, trade_price, quantity):
        "Returns the current profit of one trasaction"

        return round((market_price-trade_price)*quantity,2)

    def profit_percent(self, market_price, trade_price):
        "Returns the current profit in percent of one transaction"

        return round(100*(market_price-trade_price)/trade_price,2)

    def total_profit(self):
        "Returns the total current profit of all transactions in the current position"

        market_price=[self["instrument"][i].getprice() for i in range(len(self["instrument"]))]
        return round(sum([self.profit(mp,tp,q) for mp, tp, q in zip(market_price, self["price"], self["quantity"])]),2)

    def total_profit_percent(self):
        "Returns the total current profit in percent of all transactions in the current position"

        market_price=[self["instrument"][i].getprice() for i in range(len(self["instrument"]))]
        return round(100*self.total_profit()/sum([tp*q for tp, q in zip(self["price"], self["quantity"])]),2)


class Instrument(object):
    """This class creates a financial instrument which can be traded.

    The instrument has a name, issurer, currency and price.
    The instrument can be traded in different portfolios and quantities, at different markets and times with different acquirers and counterparties.
    The trade is "stored" in a specific position and the price can not be set after iniziation but the price can be updated as a real market.
    The instrument class requires

          :param currency: currency of the instrument
          :param issuer: issuer of the instrument
          :param name: name of the instrument
          :param price: price of the instrument
          :type currency: string
          :type issuer: string
          :type name: string
          :type price: float.

    The instrument has the following methods:

          :method getcurrency: returns the currency of the instrument
          :method getissuer: returns the issuer of the instrument
          :method getname: returns the name of the instrument
          :method getprice: returns the price of the instrument
          :method price_update: returns a updated price based on normal distribution with mean 0 and variance 0.1
          :method trade: saves the trading information in the given position.
                        Requires param: portfolio, acquirer, counterparty, quantity, marketplace, time, position


      :Example:

      Two different instruments are created:
        ABB=Instrument(name="ABB", currency="SEK", issuer="Asea Brown Boveri", price=75)
        Volvo=Instrument(name="Volvo", currency="SEK", issuer="Volvo AB", price=105)

      The two instruments are traded for position myPosition:
        ABB.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=10, marketplace="OMX", time=stime, position=myPositions)
        Volvo.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=3, marketplace="OMX", time=stime, position=myPositions)

      Price_update() can be used to update current market prices:
        ABB.price_update()
        Volvo.price_update()

    """
    def __init__(self, name, currency, issuer, price):
        "Check if all inputs except price are strings and that they are non-empty and that price is a nuber larget than zero"

        assert isinstance(name, str) and isinstance(currency, str) and isinstance(issuer, str), "All input must be strings"
        assert name!="" and currency!="" and issuer!="", "No empty strings allowed"
        assert isinstance(price, (int,float)) and price>0, "Price has to be a number larger than 0"
        self.name=name
        self.currency=currency
        self.issuer=issuer
        self.price=price

    def __str__(self):
        "Prints out the information in the instrument consisting of name, currency, issuer and price"

        return "Instrument name: "+self.name+"\nInstrument currency: "+self.currency+ "\nInstrument issuer: "+ self.issuer+"\nCurrent price: "+str(self.price)

    def getname(self):
        "Returns the name of the instrument"

        return self.name

    def getcurrency(self):
        "Returns the currency of the instrument"

        return self.currency

    def getissuer(self):
        "Returns the issuer of the instrument"

        return self.issuer

    def getprice(self):
        "Returns the price of the instrument"

        return self.price

    def price_update(self):
        "Returns an updated market price of the instrument. The stochastic element is selected to be normal distributionwith mean 0 and variance 0.1"

        self.price=round(self.price*(1+random.normalvariate(0,0.1)),2)

    def trading(self, portfolio, acquirer, counterparty, quantity, marketplace, time, position ):
        "Checks that all indata are strings, except quantity which checks that is an integer, and that they are non-empty."
        "Checks that position is a Position object created by the Position class"
        "Creates a trading and stores the information in the given position"

        assert isinstance(portfolio, str) and isinstance(acquirer, str) and isinstance(counterparty, str) and isinstance(marketplace, str) and isinstance(time, str), "Portfolio,  acquirer, counterparty, marketplace and time must be a string"
        assert isinstance(quantity, int), "Quantity must be an integer"
        assert portfolio!="" and acquirer!="" and counterparty!="" and marketplace!="" and time!="", "No empty strings allowed"
        assert position!=Position, "Position has to be an object created by the Position class"
        position["instrument"].append(self)
        position["portfolio"].append(portfolio)
        position["price"].append(self.price)
        position["acquirer"].append(acquirer)
        position["counterparty"].append(counterparty)
        position["quantity"].append(quantity)
        position["marketplace"].append(marketplace)
        position["time"].append(time)

if __name__ == "__main__":
    "Below is a small example how the Position and Instrument classes could be used in order to give a user the information one requires to keep up with the"
    "ever chaning financial markes."


    "Creates the Position myPosition and the Instruments ABB, Volvo and Volvocall"
    myPositions=Position()
    ABB=Instrument(name="ABB", currency="SEK", issuer="Asea Brown Boveri", price=75)
    Volvo=Instrument(name="Volvo", currency="SEK", issuer="Volvo AB", price=105)
    Volvocall=Instrument(name="Volvo call option", currency="SEK", issuer="Volvo AB", price=10)

    "First day of transactions, ABB and Volvo are traded in the Stock portfolio for 75 and 105 kr respectivly and Volvocall in Option portfolio for 10 kr"
    day=0
    stime=str(day)
    ABB.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=10, marketplace="OMX", time=stime, position=myPositions)
    Volvo.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=3, marketplace="OMX", time=stime, position=myPositions)
    Volvocall.trading(portfolio="Option Portfolio", acquirer='Option Desk', counterparty="SEB", quantity=50, marketplace="OMX", time=stime, position=myPositions)

    "Times fly by, but in a random way, and some days later, 1-5, the prices have been updated and ABB and Volvo are traded again."
    "After the trades the Position is presented and grouped by default; kind of  portfolio."
    timeleap=random.randint(1,5)
    day=day+timeleap
    stime=str(day)
    print("Day: "+stime+"\n")
    for _ in range(timeleap):
        ABB.price_update()
        Volvo.price_update()
        Volvocall.price_update()

    ABB.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="SEB", quantity=5, marketplace="NSDQ", time=stime, position=myPositions)
    Volvo.trading(portfolio="Stock Portfolio", acquirer='Equity Desk', counterparty="Deutsche Bank", quantity=3, marketplace="OMX", time=stime, position=myPositions)
    myPositions.group_by()

    "Times fly by again, but in a random way, and some days later, 1-5, the prices have been updated and the position is presented."
    timeleap=random.randint(1,5)
    day=day+timeleap
    stime=str(day)
    print("Day: "+stime+"\n")
    for _ in range(timeleap):
        ABB.price_update()
        Volvo.price_update()
        Volvocall.price_update()
    myPositions.group_by()

    "All good things comes to an end and after one more timejump the position is presented first with default grouping and then all possible categories."
    timeleap=random.randint(1,5)
    day=day+timeleap
    stime=str(day)
    print("Day: "+stime+"\n")
    for _ in range(timeleap):
        ABB.price_update()
        Volvo.price_update()
        Volvocall.price_update()
    myPositions.group_by()
    myPositions.group_by("portfolio")
    myPositions.group_by("counterparty")
    myPositions.group_by("marketplace")
    myPositions.group_by("acquirer")
