class Stock:
    """
    A class used to represent a Stock in the stock market.

    Attributes:
    name : str
        The name of the Stock
    price : float
        The Stock's price per share
    dividend : float
        The Stock's dividend payout per share
    split : int
        The Stock's split per share
    updated_dividend : Boolean
        Whether or not there has been a change in the Stock's dividend
    updated_split : Boolean
        Whether or not there has been a change in the Stock's split

    Methods:
    update_price(price: float)
        Updates the price of the Stock per share
    update_dividend(dividend: float, user: User)
        Updates the Stock's dividend payout per share
    update_split(split: int, user: User)
        Updates the Stock's split per share
    """
    def __init__(self, name, price, dividend, split):
        """
        Initialize a Stock.

        Parameters:
        name : str
        The name of the Stock
        price : float
            The Stock's price per share
        dividend : float
            The Stock's dividend payout per share
        split : int
            The Stock's split per share
        updated_dividend : Boolean
            Whether or not there has been a change in the Stock's dividend (default: False)
        updated_split : Boolean
            Whether or not there has been a change in the Stock's split (default: False)
        """
        self.name = name
        self.price = price
        self.dividend = dividend
        self.split = split
        self.updated_dividend = False
        self.updated_split = False

    def update_price(self, price):
        """
        Update the Stock's price per share.

        Parameters:
        price : float
            The Stock's price per share to be updated
        """
        self.price = price

    def update_dividend(self, dividend, user):
        """
        Update the Stock's dividend payout per share.

        Parameters:
        dividend : float
            The Stock's price per share to be updated
        user : User
            A User who may or may not own shares of the Stock
        """
        self.dividend = dividend
        self.updated_dividend = True
        if self in user.shares:
            user.update_dividend_income(self)

    def update_split(self, split, user):
        """
        Update the Stock's dividend payout per share.

        Parameters:
        split : float
            The Stock's split per share to be updated
        user : User
            A User who may or may not own shares of the Stock
        """
        self.price *= self.split/split
        self.updated_split = True
        if self in user.shares:
            user.shares[self] *= split/self.split
            user.shares[self] = int(user.shares[self])
        self.split = split


class User:
    """
    A class used to represent a User of the stock market.

    Attributes:
    shares : Dictionary
        A collection of the amount of Stock shares owned by a User
    dividend_income : float
        The User's total income from all Stock dividend payouts
    transactions : List
        The User's transactions for a date

    Methods:
    add_transaction(action: str, stock: Stock, shares: int, price: float)
        Records a transaction into the User's transaction history
    update_dividend_income(stock: Stock)
        Updates the User's dividend income
    print_statement(date: str)
        Prints the User's statement for the specified date
    """
    def __init__(self):
        """
        Initialize a stock market User.
        """
        self.shares = {}
        self.dividend_income = 0.0
        self.transactions=[]

    def add_transaction(self, action, stock, shares, price):
        """
        Records a transaction into the User's transaction history

        Parameters:
        action : str
            The action performed by a User; either BUY or SELL
        stock : Stock
            The Stock in which the action was performed with
        shares : int
            The amount of shares that the User bought or sold
        price : float
            The price per share that the User bought or sold for
        """
        if action == 'BUY':
            self.transactions.append(['BUY', stock.name, shares, price])
            if stock not in self.shares:
                self.shares[stock] = 0
            self.shares[stock] += shares
            if price != stock.price:
                new_price = (price * shares + stock.price * (self.shares[stock]-shares))/self.shares[stock]
                stock.update_price(new_price)
        else:
            profit = price * shares - shares*stock.price
            self.shares[stock] -= shares
            self.transactions.append(['SELL', stock.name, shares, price, profit])

    def update_dividend_income(self, stock):
        """
        Updates the User's dividend income

        Parameters:
        stock : Stock
            The Stock that issued a dividend payout
        """
        if stock in self.shares:
            self.dividend_income += stock.dividend * self.shares[stock]

    def print_statement(self, date):
        """
        Prints the User's statement for the specified date

        Parameters:
        date : str
            The date of the statement to be printed
        """
        # Reformat date string
        date = date.replace('/', '-')
        # User's Stocks information
        print('On {}, you have:'.format(date))
        for stock in self.shares:
            if self.shares[stock] != 0:
                print('    - {} shares of {} at ${:.2f} per share'.format(self.shares[stock], stock.name, stock.price))
        if self.dividend_income == 0:
            print('    - $0 of dividend income')
        else:
            print('    - ${:.2f} of dividend income'.format(self.dividend_income))

        # Transactions
        print('  Transactions:')
        for transaction in self.transactions:
            if transaction[0] == 'BUY':
                print('    - You bought {} shares of {} at a price of ${:.2f} per share'.format(transaction[2], transaction[1], transaction[3]))
            else:
                if transaction[4] >= 0:
                    print('    - You sold {} shares of {} at a price of ${:.2f} per share for a profit of ${:.2f}'.format(transaction[2], transaction[1], transaction[3], transaction[4]))
                else:
                    print('    - You sold {} shares of {} at a price of ${:.2f} per share for a loss of ${:.2f}'.format(transaction[2], transaction[1], transaction[3], transaction[4]))
        self.transactions = []
        for stock in self.shares:
            if stock.updated_dividend == True:
                print('    - {} paid out ${:.2f} dividend per share, and you have {} shares'.format(stock.name, stock.dividend, self.shares[stock]))
            stock.updated_dividend = False
            if stock.updated_split == True:
                print('    - {} split {} to 1, and you have {} shares'.format(stock.name, stock.split, self.shares[stock]))
            stock.updated_split = False


def update_stock_action(stock_action, stocks, user):
    """
    Update the Stock's attributes according to its actions

    Parameters:
    stock_action : Dictionary
        The action performed by the Stock
    stocks : List
        A list of the current stocks and their data so far
    user : User
        A User who may or may not own shares of the Stock

    Returns:
        stock : The updated Stock.
    """
    if stock_action['stock'] not in stocks:
        stocks[stock_action['stock']] = Stock(stock_action['stock'], 0.0, 0.0, 1)

    stock = stocks[stock_action['stock']]
    # If there is a change in the dividend, update it
    if stock_action['dividend'] != '':
        stock.update_dividend(float(stock_action['dividend']), user)
    # If there is a change in the split, update it
    if stock_action['split'] != '':
        stock.update_split(int(stock_action['split']), user)

    return stock

def update_user_action(user_action, stocks, user):
    """
    Update the User's attributes according to the provided data

    Parameters:
    user_action : Dictionary
        The action performed by the User
    stocks : List
        A list of the current stocks and their data so far
    user : User
        The User who performed the action
    """
    if user_action['ticker'] not in stocks:
        stocks[user_action['ticker']] = Stock(user_action['ticker'], user_action['price'], 0.0, 1)

    user_stock = stocks[user_action['ticker']]
    user.add_transaction(user_action['action'], user_stock, user_action['shares'], user_action['price'])

def stock_market(actions, stock_actions):
    """
    A transaction statement generator for an existing trader on Forma AI's stock trading system.

    Parameters:
    actions : List
        The timestamped actions that the stock trader performed, it can be BUY or SELL type, and they can
        buy or sell a few different stocks. However, you should assume that the number of ticker is not limited to
        3 types as in the example below, but potentially infinite, so the ticker should not be hardcoded anywhere.
    stock_actions : List
        the timestamped actions that the stock performed regardless of who the trader is. It includes
        stock splits, and dividend payouts. Even though these actions are not performed by our trader, it still affects
        our trader's portfolios, so it should be recorded in the statement that we prepare.
    """
    # Reformat actions dict
    for action in actions:
        action['date'] = action['date'].split(' ')[0]
        action['price'] = float(action['price'])
        action['shares'] = int(action['shares'])

    i, j = 0, 0
    user = User()
    stocks = {}
    stock = None

    # Parse through actions and stock actions, printing the statements in order of date
    while (i < len(actions) and j < len(stock_actions)):
        # Only print a statement if it affects the user
        print_statement = False
        if actions[i]['date'] == stock_actions[j]['date']:
            date = actions[i]['date']
            # Update stock actions
            stock = update_stock_action(stock_actions[j], stocks, user)
            # Update user actions
            update_user_action(actions[i], stocks, user)
            print_statement = True
            i += 1
            j += 1

        elif actions[i]['date'] < stock_actions[j]['date']:
            date = actions[i]['date']
            update_user_action(actions[i], stocks, user)
            print_statement = True
            i += 1

        elif actions[i]['date'] > stock_actions[j]['date']:
            date = stock_actions[j]['date']
            stock = update_stock_action(stock_actions[j], stocks, user)
            if stock in user.shares:
                print_statement = True
            j += 1

        # Check if the next stock actions also occured on the same date
        while j < len(stock_actions) and stock_actions[j]['date'] == date:
            stock = update_stock_action(stock_actions[j], stocks, user)
            if stock in user.shares:
                print_statement = True
            j += 1

        # Check if the next user actions also occured on the same date
        while i < len(actions) and actions[i]['date'] == date:
            update_user_action(actions[i], stocks, user)
            i += 1

        if print_statement:
            user.print_statement(date)

    # Continue to record user actions, if there are any left
    while i < len(actions):
        date = actions[i]['date']
        print_statement = True
        while i < len(actions) and actions[i]['date'] == date:
            update_user_action(actions[i], stocks, user)
            i += 1

        user.print_statement(date)

    # Continue to record stock actions, if there are any left
    while j < len(stock_actions):
        date = stock_actions[j]['date']
        while j < len(stock_actions) and actions[i]['date'] == date:
            stock = update_stock_action(stock_actions[j], stocks, user)
            if stock in user.shares:
                print_statement = True
            j += 1

        if print_statement:
            user.print_statement(date)

if __name__ == "__main__":
    actions = [{'date': '1992/07/14 11:12:30', 'action': 'BUY', 'price': '12.3', 'ticker': 'AAPL', 'shares': '500'}, {'date': '1992/09/13 11:15:20', 'action': 'SELL', 'price': '15.3', 'ticker': 'AAPL', 'shares': '100'}, {'date': '1992/10/14 15:14:20', 'action': 'BUY', 'price': '20', 'ticker': 'MSFT', 'shares': '300'}, {'date': '1992/10/17 16:14:30', 'action': 'SELL', 'price': '20.2', 'ticker': 'MSFT', 'shares': '200'}, {'date': '1992/10/19 15:14:20', 'action': 'BUY', 'price': '21', 'ticker': 'MSFT', 'shares': '500'}, {'date': '1992/10/23 16:14:30', 'action': 'SELL', 'price': '18.2', 'ticker': 'MSFT', 'shares': '600'}, {'date': '1992/10/25 10:15:20', 'action': 'SELL', 'price': '20.3', 'ticker': 'AAPL', 'shares': '300'}, {'date': '1992/10/25 16:12:10', 'action': 'BUY', 'price': '18.3', 'ticker': 'MSFT', 'shares': '500'}]
    stock_actions = [{'date': '1992/08/14', 'dividend': '0.10', 'split': '', 'stock': 'AAPL'}, {'date': '1992/09/01', 'dividend': '', 'split': '3', 'stock': 'AAPL'}, {'date': '1992/10/15', 'dividend': '0.20', 'split': '', 'stock': 'MSFT'},{'date': '1992/10/16', 'dividend': '0.20', 'split': '', 'stock': 'ABC'}]

    stock_market(actions, stock_actions)
