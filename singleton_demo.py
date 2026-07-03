import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Naive lazy initialization (if cls._instance is None) fails under concurrency because 
        # two threads might pass the None check at the exact same time before either writes 
        # to the variable, creating two instances. 
        
        if cls._instance is None:           # First check without locking for performance
            with cls._lock:                 # Acquire thread lock
                if cls._instance is None:   # Second check guarantees only one thread creates it
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def get_connection(self):
        return "Connection active"
