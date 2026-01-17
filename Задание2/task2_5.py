import time
import os
from functools import wraps


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        print(f"Функция '{func.__name__}' выполнилась за {execution_time:.6f} секунд")
        return result
    return wrapper


@timing_decorator
def sum_numbers(a, b):
    result = a + b
    print(f"Сумма чисел {a} и {b} равна: {result}")
    return result


@timing_decorator
def process_file(input_file='input.txt', output_file='output.txt'):
    """
    修改这里：获取当前文件所在的目录，然后拼接文件路径
    """
    # 获取当前.py文件所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建完整的文件路径
    input_path = os.path.join(current_dir, input_file)
    output_path = os.path.join(current_dir, output_file)
    
    try:
        # 使用完整路径读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            numbers = f.read().strip().split()
        
        if len(numbers) < 2:
            print(f"Ошибка: в файле {input_path} должно быть хотя бы два числа")
            return
        
        a = float(numbers[0])
        b = float(numbers[1])
        result = a + b
        
        # 使用完整路径写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Сумма чисел {a} и {b} равна: {result}")
        
        print(f"Результат записан в файл {output_path}")
        return result
    
    except FileNotFoundError:
        print(f"Ошибка: файл {input_path} не найден")
    except ValueError:
        print(f"Ошибка: в файле {input_path} содержатся некорректные данные")


def create_test_files():
    """
    创建测试文件在当前目录
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, 'input.txt')
    output_path = os.path.join(current_dir, 'output.txt')
    
    # 创建input.txt，如果它不存在
    if not os.path.exists(input_path):
        with open(input_path, 'w', encoding='utf-8') as f:
            f.write("10.5 20.3")
        print(f"Создан файл: {input_path}")
    
    # 创建空的output.txt
    open(output_path, 'w', encoding='utf-8').close()


def main():
    create_test_files()
    
    print("Тест первой функции (сумма чисел):")
    print("-" * 40)
    sum_numbers(10, 20)
    print()
    
    print("Тест второй функции (обработка файлов):")
    print("-" * 40)
    process_file()
    
    # 显示output.txt的内容
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, 'output.txt')
    
    print()
    print("Содержимое файла output.txt:")
    print("-" * 40)
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content if content else "Файл пуст")
    except FileNotFoundError:
        print(f"Файл {output_path} не найден")


if __name__ == "__main__":
    main()