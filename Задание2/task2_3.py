import math


class Shape:
    """Базовый класс для всех геометрических фигур."""
    
    def area(self):
        """Вычисление площади фигуры."""
        raise NotImplementedError("Метод area должен быть реализован в дочернем классе")
    
    def perimeter(self):
        """Вычисление периметра фигуры."""
        raise NotImplementedError("Метод perimeter должен быть реализован в дочернем классе")
    
    def compare_area(self, other_shape):
        """
        Сравнение площади с другой фигурой.
        
        Аргументы:
        other_shape (Shape): Другая фигура для сравнения
        
        Возвращает:
        str: Результат сравнения
        """
        area1 = self.area()
        area2 = other_shape.area()
        
        if area1 > area2:
            return f"Площадь {self.__class__.__name__} больше площади {other_shape.__class__.__name__}"
        elif area1 < area2:
            return f"Площадь {self.__class__.__name__} меньше площади {other_shape.__class__.__name__}"
        else:
            return f"Площади {self.__class__.__name__} и {other_shape.__class__.__name__} равны"
    
    def compare_perimeter(self, other_shape):
        """
        Сравнение периметра с другой фигурой.
        
        Аргументы:
        other_shape (Shape): Другая фигура для сравнения
        
        Возвращает:
        str: Результат сравнения
        """
        per1 = self.perimeter()
        per2 = other_shape.perimeter()
        
        if per1 > per2:
            return f"Периметр {self.__class__.__name__} больше периметра {other_shape.__class__.__name__}"
        elif per1 < per2:
            return f"Периметр {self.__class__.__name__} меньше периметра {other_shape.__class__.__name__}"
        else:
            return f"Периметры {self.__class__.__name__} и {other_shape.__class__.__name__} равны"


class Square(Shape):
    """Класс Квадрат."""
    
    def __init__(self, side):
        """
        Инициализация квадрата.
        
        Аргументы:
        side (float): Длина стороны квадрата
        """
        self.side = side
    
    def area(self):
        """Вычисление площади квадрата."""
        return self.side ** 2
    
    def perimeter(self):
        """Вычисление периметра квадрата."""
        return 4 * self.side


class Rectangle(Shape):
    """Класс Прямоугольник."""
    
    def __init__(self, width, height):
        """
        Инициализация прямоугольника.
        
        Аргументы:
        width (float): Ширина прямоугольника
        height (float): Высота прямоугольника
        """
        self.width = width
        self.height = height
    
    def area(self):
        """Вычисление площади прямоугольника."""
        return self.width * self.height
    
    def perimeter(self):
        """Вычисление периметра прямоугольника."""
        return 2 * (self.width + self.height)


class Triangle(Shape):
    """Класс Треугольник (равносторонний)."""
    
    def __init__(self, side):
        """
        Инициализация равностороннего треугольника.
        
        Аргументы:
        side (float): Длина стороны треугольника
        """
        self.side = side
    
    def area(self):
        """Вычисление площади треугольника."""
        return (math.sqrt(3) / 4) * (self.side ** 2)
    
    def perimeter(self):
        """Вычисление периметра треугольника."""
        return 3 * self.side


class Circle(Shape):
    """Класс Круг."""
    
    def __init__(self, radius):
        """
        Инициализация круга.
        
        Аргументы:
        radius (float): Радиус круга
        """
        self.radius = radius
    
    def area(self):
        """Вычисление площади круга."""
        return math.pi * (self.radius ** 2)
    
    def perimeter(self):
        """Вычисление периметра (длины окружности) круга."""
        return 2 * math.pi * self.radius


def main():
    """Основная функция для демонстрации работы классов фигур."""
    
    # Создание объектов фигур
    square = Square(5)
    rectangle = Rectangle(4, 6)
    triangle = Triangle(3)
    circle = Circle(2.5)
    
    # Вывод информации о фигурах
    shapes = [square, rectangle, triangle, circle]
    
    for shape in shapes:
        print(f"{shape.__class__.__name__}:")
        print(f"  Площадь: {shape.area():.2f}")
        print(f"  Периметр: {shape.perimeter():.2f}")
        print()
    
    # Сравнение площадей и периметров
    print("Сравнение площадей:")
    print(square.compare_area(rectangle))
    print(triangle.compare_area(circle))
    print()
    
    print("Сравнение периметров:")
    print(rectangle.compare_perimeter(triangle))
    print(circle.compare_perimeter(square))


if __name__ == "__main__":
    main()