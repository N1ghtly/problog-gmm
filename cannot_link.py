class CannotLinkConstraint:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def contains(self, evid):
        return self.a == evid or self.b == evid

    def get_other(self, evid):
        return self.b if self.a == evid else self.a

    def __str__(self):
        return "Cannot link between " + str(self.a) + " and " + str(self.b)

