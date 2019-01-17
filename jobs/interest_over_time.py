import pandas as pd


class Interest:

    def __init__(self):
        self.computer_label= None
        self.interest = None
        self.date = None

    def __dict__(self):
        dic = {
            "computer_label": self.computer_label,
            "interest": self.interest,
            "date": self.date.isoformat()
        }
        return dic
