def task1():
    while(True):
        try:
            x = float(input("Введите |x| < 1: "))
            if abs(x) >= 1:
                print("Разложение не сходится, |x| ≥ 1")
                raise
            eps = 1e-6 
            eps = float(input("Введите точность: "))
            break
        except:
            print("неправильный ввод")
    max_iter=500
    sum_series = 0 
    term = 1        
    n = 0           
    while(abs(term) >= eps and n < max_iter):
        sum_series += term 
        n += 1
        term *= x
    math_value = 1 / (1 - x)     
    Fx = sum_series
    terms = n
    math_Fx = math_value
    print(f"Значение функции F(x) через ряд: {Fx}")
    print(f"Число просуммированных членов ряда: {terms}")
    print(f"Точное значение функции Math F(x): {math_Fx}")