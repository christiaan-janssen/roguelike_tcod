class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs

    def __repr__(self):
        return "An item"

    def __str__(self):
        return "An item"
