class Person:
    """Базовый класс для человека."""
    
    def __init__(self, name, age):
        """
        Инициализация человека.
        
        Аргументы:
        name (str): ФИО человека
        age (int): Возраст человека
        """
        self.name = name
        self.age = age
    
    def display_info(self):
        """Вывод информации о человеке."""
        return f"ФИО: {self.name}, Возраст: {self.age}"


class Student(Person):
    """Класс Студент."""
    
    def __init__(self, name, age, group_number, average_score):
        """
        Инициализация студента.
        
        Аргументы:
        name (str): ФИО студента
        age (int): Возраст студента
        group_number (str): Номер группы
        average_score (float): Средний балл
        """
        super().__init__(name, age)
        self.group_number = group_number
        self.average_score = average_score
    
    def display_info(self):
        """Вывод информации о студенте."""
        base_info = super().display_info()
        return f"{base_info}, Группа: {self.group_number}, Средний балл: {self.average_score}"
    
    def calculate_scholarship(self):
        """Вычисление размера стипендии."""
        if self.average_score == 5:
            return 6000  # рублей
        elif self.average_score < 5:
            return 4000  # рублей
        else:
            return 0  # рублей
    
    def compare_scholarship(self, other_student):
        """
        Сравнение размера стипендии с другим студентом.
        
        Аргументы:
        other_student (Student): Другой студент для сравнения
        
        Возвращает:
        str: Результат сравнения
        """
        scholarship1 = self.calculate_scholarship()
        scholarship2 = other_student.calculate_scholarship()
        
        if scholarship1 > scholarship2:
            return f"Стипендия студента {self.name} больше стипендии студента {other_student.name}"
        elif scholarship1 < scholarship2:
            return f"Стипендия студента {self.name} меньше стипендии студента {other_student.name}"
        else:
            return f"Стипендии студентов {self.name} и {other_student.name} равны"


class Aspirant(Person):
    """Класс Аспирант."""
    
    def __init__(self, name, age, group_number, average_score, research_topic):
        """
        Инициализация аспиранта.
        
        Аргументы:
        name (str): ФИО аспиранта
        age (int): Возраст аспиранта
        group_number (str): Номер группы
        average_score (float): Средний балл
        research_topic (str): Тема научной работы
        """
        super().__init__(name, age)
        self.group_number = group_number
        self.average_score = average_score
        self.research_topic = research_topic
    
    def display_info(self):
        """Вывод информации об аспиранте."""
        base_info = super().display_info()
        return f"{base_info}, Группа: {self.group_number}, Средний балл: {self.average_score}, Научная работа: {self.research_topic}"
    
    def calculate_scholarship(self):
        """Вычисление размера стипендии."""
        if self.average_score == 5:
            return 8000  # рублей
        elif self.average_score < 5:
            return 6000  # рублей
        else:
            return 0  # рублей
    
    def compare_scholarship(self, other_aspirant):
        """
        Сравнение размера стипендии с другим аспирантом.
        
        Аргументы:
        other_aspirant (Aspirant): Другой аспирант для сравнения
        
        Возвращает:
        str: Результат сравнения
        """
        scholarship1 = self.calculate_scholarship()
        scholarship2 = other_aspirant.calculate_scholarship()
        
        if scholarship1 > scholarship2:
            return f"Стипендия аспиранта {self.name} больше стипендии аспиранта {other_aspirant.name}"
        elif scholarship1 < scholarship2:
            return f"Стипендия аспиранта {self.name} меньше стипендии аспиранта {other_aspirant.name}"
        else:
            return f"Стипендии аспирантов {self.name} и {other_aspirant.name} равны"


def main():
    """Основная функция для демонстрации работы классов."""
    
    # Создание объектов студентов
    student1 = Student("Иванов Иван Иванович", 20, "Группа 101", 4.8)
    student2 = Student("Петров Петр Петрович", 21, "Группа 102", 5.0)
    
    # Создание объектов аспирантов
    aspirant1 = Aspirant("Сидоров Алексей Сергеевич", 25, "Аспирантура 201", 4.9, "Исследование алгоритмов машинного обучения")
    aspirant2 = Aspirant("Кузнецова Мария Дмитриевна", 26, "Аспирантура 202", 5.0, "Разработка квантовых вычислений")
    
    # Вывод информации
    people = [student1, student2, aspirant1, aspirant2]
    
    for person in people:
        print(f"{person.__class__.__name__}:")
        print(f"  {person.display_info()}")
        scholarship = person.calculate_scholarship()
        print(f"  Стипендия: {scholarship} руб.")
        print()
    
    # Сравнение стипендий
    print("Сравнение стипендий студентов:")
    print(student1.compare_scholarship(student2))
    print()
    
    print("Сравнение стипендий аспирантов:")
    print(aspirant1.compare_scholarship(aspirant2))


if __name__ == "__main__":
    main()