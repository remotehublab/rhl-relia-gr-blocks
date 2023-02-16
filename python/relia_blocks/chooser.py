from relia_blocks.api import downloader, VariableBlock

class ChooserWidget(VariableBlock):
    def __init__(self, identifier, options, labels, data_type):
        self.options = options
        self.labels = labels
        self.options_by_label = dict(zip(self.labels, self.options))
        self.labels_by_option = dict(zip(self.options, self.labels))
        self.state = False
        self._checkbox_callback = None
        self.data_type = data_type
        super().__init__(identifier=identifier, callback=self.on_new_data)

    def change(self, value):
        if value in self.options_by_label:
            self.state = self.options_by_label[value]
        else:
            self.state = value

    def get_data(self) -> dict:
        return {
            'params': {
                'options': self.options,
                'labels': self.labels,
                'state': self.state,
            }
        }

    def on_change(self, callback):
        self._checkbox_callback = callback

    def on_new_data(self, data_item):

        try:
            new_state = self.data_type(data_item['value'])
        except Exception as err:
            print("Error converting item", data_item['value'], "into", self.data_type)
            return
        self.state = new_state
        new_state_value = self.labels_by_option.get(self.state)
        if self._checkbox_callback is not None and new_state_value is not None:
            self._checkbox_callback(new_state)
