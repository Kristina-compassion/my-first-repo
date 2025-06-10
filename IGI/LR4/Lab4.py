from zadanie1 import Task1
from zadanie2 import Task2
from zadanie3 import task3
from main4zadanie import Task4
from zadanie5 import Task5

def to_face():
    while True:
        try:
            value = int(input())
            if 0 <= value <= 5:
                return value
        except ValueError:
            print('Try again!')                

while True:
        print(
                'Choose one of the options:\n'
                '0) Exit\n'
                '1) Go to task 1\n'
                '2) Go to task 2\n'
                '3) Go to task 3\n'
                '4) Go to task 4\n'
                '5) Go to task 5'
            )
        option = to_face()
        match option:
            case 0:
                break
            case 1:
                task = Task1()
                task.run()
            case 2:
                task = Task2()
                task.run()
            case 3:
                task3()
            case 4:
                task = Task4()
                task.run()
            case 5:
                task = Task5()
                task.run()