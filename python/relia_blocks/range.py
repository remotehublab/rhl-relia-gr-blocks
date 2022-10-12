from PyQt5 import QtCore

class RangeWidget:
    def __init__(self, identifier, ranges, slot, label, style, rangeType=float, orientation=QtCore.Qt.Horizontal):
        # slot is a callback to change things.
        # so calling self.slot(self.rangeType(value))
        # will trigger the value change.

        # so we have to add a callback to the register_block
        # to say "hey, add", and push some dummy data from time
        # to time.
        pass