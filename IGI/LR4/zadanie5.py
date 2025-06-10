from matrix import StatisticalAnalyzer

class Task5:
    my = 1
    def __init__(self):
        self.statistical_analyzer = StatisticalAnalyzer(100, 100)

    def run(self):
        while True:
            print(
                'Choose one of the options:\n'
                '0) Back\n'
                '1) Generate new random matrix\n'
                '2) Get statistical data\n'
            )
            option = proverka(0,2)
            match option:
                case 0:
                    return
                case 1:
                    print('Enter the number of rows of the matrix:')
                    n = proverka(1,100)
                    print('Enter the number of columns of the matrix:')
                    m = proverka(1,100)
                    print('Enter a minimum possible random value of matrix:')
                    min_value = proverka(int(-1e5), int(1e5))
                    print('Enter a maximum possible random value of matrix:')
                    max_value = proverka(min_value, int(1e5))

                    self.statistical_analyzer = StatisticalAnalyzer(
                        n, m, min_value, max_value
                    )
                case 2:
                    Task5.my = 2
                    self.statistical_analyzer.display_statistics()

def proverka(n,x):
    while(True):
        try:
            value = int(input())
            if(n <= value <=x):
                return value
        except ValueError:
            print('Try again!')  