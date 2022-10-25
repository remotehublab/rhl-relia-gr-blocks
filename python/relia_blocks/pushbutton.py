from relia_blocks.api import downloader, VariableBlock

class PushButtonWidget(VariableBlock):
    def __init__(self, identifier, choices):
        self.choices = choices
        self.state = 0
        self._pushbutton_callback = None
        super().__init__(identifier=identifier, callback=self.on_new_data)

    def pressed(self, callback):
        self.state = 1
        self._pushbutton_callback = callback

    def get_data(self) -> dict:
        return {
            'params': {
                'state': self.state,
                'choices': self.choices,
            }
        }

    def released(self, callback):
        self._pushbutton_callback = callback
        self.state = 0

    def on_new_data(self, data_item):
        #new_state = data_item['value']
        #self.state = new_state
        new_state_value = self.choices.get(self.state)
        if self._pushbutton_callback is not None and new_state_value is not None:
            self._pushbutton_callback(new_state_value)
