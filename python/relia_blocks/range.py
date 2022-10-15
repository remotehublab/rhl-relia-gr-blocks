from PyQt5 import QtCore

from relia_blocks.api import downloader

class RangeWidget:
    def __init__(self, identifier, ranges, slot, label, style, rangeType=float, orientation=QtCore.Qt.Horizontal):
        # slot is a callback to change things.
        # so calling self.slot(self.rangeType(value))
        # will trigger the value change.

        # so we have to add a callback to the register_block
        # to say "hey, add", and push some dummy data from time
        # to time.
        self.rangeType = rangeType
        self.slot = slot
        self.ranges = ranges
        self.label = label
        self.style = style
        self.orientation = orientation

        downloader.register_block(identifier, self, callback=self.on_new_data)


    def on_new_data(self, data_item):
        # TODO: process data_item
        value = self.rangeType(data_item)
        self.slot(value)
