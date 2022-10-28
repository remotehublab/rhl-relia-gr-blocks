from relia_blocks.api import downloader, VariableBlock

class PushButtonWidget(VariableBlock):
    def __init__(self, identifier, choices, label):
        self.label = label
        self.state = False
        self._push_button_pressed_callback = None
        self._push_button_released_callback = None
        super().__init__(identifier=identifier, callback=self.on_new_data)

    def pressed(self, callback):
        self._push_button_pressed_callback = callback

    def get_data(self) -> dict:
        return {
            'params': {
                'state': self.state,
                'label': self.label,
            }
        }

    def released(self, callback):
        self._push_button_released_callback = callback

    def on_new_data(self, data_item):
        print("new data on push button:", data_item)
        new_state = data_item['value']
        self.state = new_state

        if new_state == True:
            if self._push_button_pressed_callback is not None:
                self._push_button_pressed_callback()
        elif new_state == False:
            if self._push_button_released_callback is not None:
                self._push_button_released_callback()

