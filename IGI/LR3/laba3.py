from zadanie1 import task1
from zadanie2 import task2
from zadanie3 import task3
from zadanie4 import task4
from zadanie5 import task5

while(True):
    n=""
    n = input("Введите номер задания(1,2,3,4,5,q для выхода): ")
    if(n=="1"):
        task1()
    elif(n=="2"):
        task2()
    elif(n=="3"):
        task3()
    elif(n=="4"):
        task4()
    elif(n=="5"):
        task5()
    elif(n.lower()=="q"):
        break    
    else:
        print("Нет такого задания")                  