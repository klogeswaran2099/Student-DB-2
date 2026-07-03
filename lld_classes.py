from abc import ABC, abstractmethod
from typing import List

class EnrollmentRepository(ABC):
    @abstractmethod
    def save_enrollment(self, student_id: int, course_code: str) -> bool:
        pass
        
    @abstractmethod
    def get_enrollments(self, student_id: int) -> List[str]:
        pass

class Student:
    def __init__(self, student_id: int, name: str, department: str):
        self.student_id = student_id
        self.name = name
        self.department = department

    def get_id(self) -> int:
        return self.student_id

class Enrollment:
    def __init__(self, student: Student, course_code: str, repo: EnrollmentRepository):
        self.student = student
        self.course_code = course_code
        self.repo = repo

    def process(self) -> bool:
        return self.repo.save_enrollment(self.student.get_id(), self.course_code)

class WaitlistedEnrollment(Enrollment):
    def __init__(self, student: Student, course_code: str, repo: EnrollmentRepository, position: int):
        super().__init__(student, course_code, repo)
        self.position = position

    def process(self) -> bool:
        return True
