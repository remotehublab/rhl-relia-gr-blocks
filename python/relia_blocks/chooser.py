from relia_blocks.api import downloader, VariableBlock

class CheckBoxWidget(VariableBlock):
    def __init__(self, identifier, options, labels):
        self.options = options
        self.labels = labels
        self.state = False
        self._checkbox_callback = None
        super().__init__(identifier=identifier, callback=self.on_new_data)

    def change(self, value):
        self.state = self.choices_inv[value]

    def get_data(self) -> dict:
        return {
            'params': {
                'options': self.options,
                'labels': self.labels,
            }
        }

    def on_change(self, callback):
        self._checkbox_callback = callback

    def on_new_data(self, data_item):
        new_state = data_item['value']
        self.state = new_state
        new_state_value = self.choices.get(self.state)
        if self._checkbox_callback is not None and new_state_value is not None:
            self._checkbox_callback(new_state_value)
