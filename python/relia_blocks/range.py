from PyQt5 import QtCore

from relia_blocks.api import downloader, VariableBlock

class RangeWidget(VariableBlock):
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

        super().__init__(identifier=identifier)

    def get_data(self) -> dict:
        return {
            'params': {
                'x_start': -16000,
                'x_step': 100,
                'vlen': 200
            }
        }

    def on_new_data(self, data_item):
        print(f"New data in {self.identifier}: {data_item}")
        # TODO: process data_item
        value = self.rangeType(data_item['value'])
        self.slot(value)
