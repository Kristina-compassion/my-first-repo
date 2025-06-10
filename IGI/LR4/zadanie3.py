import matplotlib.pyplot as plt
import numpy as np
import math

class ris:
    def __init__(self,e):
        self.e = e
        self.Sx = []
        self.Yx = []
    def  otrisovka(self):
        self.func()
        x = np.arange(-0.99, 1.0, 0.01)
        plt.plot(x, self.Yx, label='1 / (1 - x)', color='orange')
        plt.plot(x, self.Sx, label=f'Ряд Тейлора', linestyle='--', color='purple') 
        plt.title('Сравнение функции и её разложения')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.savefig(r"C:\Users\LENOVO\353502_Klepatskiy_10\IGI\LR4\graph.png")
        print("График сохранён как graph.png")
        plt.show() 

    def func(self):
        x = -0.99
        while(-1<x<1):
            max_iter=500
            sum_series = 0 
            term = 1  
            natur = 1/(1-x)      
            n = 0           
            while(abs(term) >= self.e and n < max_iter):
                sum_series += term 
                n += 1
                term *= x  
            self.Sx.append(sum_series)
            self.Yx.append(natur)   
            x+=0.01   


def task3():
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
    seque = []   
    median = 0
    while(abs(term) >= eps and n < max_iter):
        sum_series += term 
        seque.append(term)
        n += 1
        term *= x
    if(n%2!=0):
        median = seque[(n//2)]
    else:
        l = seque[((n//2)-1)]
        r = seque[(n//2)]
        median = (l+r)/2   
    i = 0       
    d = 1/(n-1)
    mid = sum_series / n     
    sum_d=0   
    while(i<len(seque)):
        sum_d += ((seque[i]-mid)*(seque[i]-mid)) 
        i+=1
    d*=sum_d 
    sko = math.sqrt(d)  
    math_value = 1 / (1 - x)     
    Fx = sum_series
    terms = n
    math_Fx = math_value
    my = ris(eps)
    my.otrisovka()
    print(f"Значение СКО: {sko}")
    print(f"Значение дисперсии: {d}")
    print(f"Среднее значение последовательности: {mid}")
    print(f"Значение медианы последовательности: {median}")
    print(f"Значение функции F(x) через ряд: {Fx}")
    print(f"Число просуммированных членов ряда: {terms}")
    print(f"Точное значение функции Math F(x): {math_Fx}")          