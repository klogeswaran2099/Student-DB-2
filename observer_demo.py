from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, student_id: int, new_marks: float):
        pass

class EmailNotifier(Observer):
    def update(self, student_id: int, new_marks: float):
        pass 

class AuditLogNotifier(Observer):
    def update(self, student_id: int, new_marks: float):
        pass 

class MarksUpdateNotifier:
    def __init__(self):
        self._observers = []

    def register(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def deregister(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def update_marks(self, student_id: int, new_marks: float):
        for observer in self._observers:
            observer.update(student_id, new_marks)
