from zadanie4 import Triangle
import math

class Task4:
    def __init__(self):
        self.triangle = Triangle(6, 16, 'purple', 30)

    def run(self):
        while True:
            print(
                'Choose one of the options:\n'
                '0) Back\n'
                '1) Set parameters\n'
                '2) Get area\n'
                '3) Draw\n'
                )
            option = proverka()
            match option:
                case 0:
                    return
                case 1:
                    a, b, h = 0, 0, 0
                    while True:
                        print('Enter the length of the base:')
                        b = proverka()
                        print('Enter the angle:')
                        a = proverka()
                        print('Enter the height value')
                        h = proverka()
                        angleR = math.radians(a)
                        x = h / math.tan(angleR)
                        if(x>a):
                            print('Invalid arguments. Try again!')
                        else:
                            break
                    color = input('Input valid color (example: red): ')
                    self.triangle = Triangle(
                        h, b, color, a
                    )
                case 2:
                    print(self.triangle.area())
                case 3:
                    text = input('Input text for tag picture: ')
                    self.triangle.draw(text)

def proverka():
    while(True):
        try:
            value = float(input())
            return value
        except ValueError:
            print('Try again!')      