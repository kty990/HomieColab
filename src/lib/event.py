class Event:
    def __init__(self):
        self.handlers = set()
    
    def add_handler(self, handler):
        self.handlers.add(handler)
    
    def remove_handler(self, handler):
        self.handlers.remove(handler)
    
    def fire(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)


USER_REACTED = Event()