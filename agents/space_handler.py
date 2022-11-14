# python class for handling spaces in problem file

class SpaceHandler():
    def __init__(self):
        self.space = " "
        self.newline = "\n"
        self.tab = "\t"
        self.open_paren = "("
        self.close_paren = ")"
        self.colon = ":"
        self.dash = "-"
        self.underscore = "_"
        self.negate = "not"

    def space(self):
        return self.space

    def newline(self):
        return self.newline

    def tab(self):
        return self.tab

    def open_paren(self):
        return self.open_paren

    def close_paren(self):
        return self.close_paren

    def colon(self):
        return self.colon

    def dash(self):
        return self.dash

    def underscore(self):
        return self.underscore

    def negate(self):
        return self.negate
        