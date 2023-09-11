class Category:
  
  def __init__(self, category):
    self.category = category
    self.ledger = list()
    self.balance = 0.0

  def deposit(self, amount, description=""):
    self.ledger.append({"amount":amount, "description": description})
    self.balance += amount

  def withdraw(self, amount, description=""):
    if self.check_funds(amount):
      self.ledger.append({"amount":amount * -1, "description":description})
      self.balance -= amount
      return True
    return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, other):
    if self.withdraw(amount, "Transfer to {}".format(other.category)):
      other.deposit(amount, "Transfer from {}".format(self.category))
      return True
    return False

  def check_funds(self, amount):
    if self.balance >= amount:
      return True
    return False

  def __repr__(self):
    description_category = ""
    description_category += self.category.center(30, "*") + "\n"
    for i in self.ledger:
      description_category += i["description"].ljust(23)[:23] + "{:>7.2f}".format(i["amount"])[:7] + "\n"

    description_category += "Total: {:.2f}".format(self.balance)
        
    return description_category
    
def create_spend_chart(categories):
    spent_amounts = []

    for category in categories:
        spent = 0
        for item in category.ledger:
            if item["amount"] < 0:
                spent += abs(item["amount"])
        spent_amounts.append(round(spent, 2))

    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.category, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")