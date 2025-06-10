def decor(func):
    def wrapper():
        print("Начало программы")
        func()
        print("Конец программы")
    return wrapper    

def generator():
    while True:
        try:
            num = int(input("Введите целое число (0, чтобы закончить): "))
            if num == 0:
                break
            yield num
        except ValueError:
            print("Ошибка во вводе значения")

@decor
def task2():
    max_number = None
    for num in generator():
        if max_number is None or num > max_number:
            max_number = num

    if max_number is not None:
        print(f"Наибольшее число: {max_number}")
    else:
        print("Не ввели число")        