import numpy

class MatrixAnalyzer:
    def __init__(self, n, m, min_value, max_value):
        self.n = n
        self.m = m
        self.min_value = min_value
        self.max_value = max_value
        self.matrix = self._generate_matrix()

    def _generate_matrix(self):
        return numpy.random.randint(
            self.min_value, self.max_value + 1, size=(self.n, self.m)
        )

    def get_flat_matrix(self):
        return self.matrix.flatten()


class StatisticalAnalyzer(MatrixAnalyzer):
    def __init__(self, n, m, min_value=-100, max_value=100):
        super().__init__(n, m, min_value, max_value)
        self.flat_matrix = self.get_flat_matrix()

    def mean(self):
        return numpy.mean(self.flat_matrix)

    def median(self):
        return numpy.median(self.flat_matrix)

    def variance(self):
        return numpy.var(self.flat_matrix)

    def std_deviation(self):
        return numpy.std(self.flat_matrix)
    
    def min_value_info(self):
        min_val = numpy.min(self.matrix)
        indices = numpy.argwhere(self.matrix == min_val)
        count = len(indices)
        return min_val, count, indices

    def std_deviation_my(self):
        mean_val = numpy.mean(self.flat_matrix)
        squared_diffs = [(x - mean_val) ** 2 for x in self.flat_matrix]
        variance_manual = sum(squared_diffs) / len(self.flat_matrix)
        std_manual = round(variance_manual ** 0.5, 2)

        return std_manual
    

    def display_statistics(self):
        print("Statistical parameters:")
        print("The average value: {:.2f}".format(self.mean()))
        print("The median: {:.2f}".format(self.median()))
        print("Variance: {:.2f}".format(self.variance()))
        print("Standard deviation: {:.2f}".format(self.std_deviation()))
        std1 = self.std_deviation_my()
        print(f"Standard deviation (my): {std1}")
        min_val, count, indices = self.min_value_info()
        print(f"Minimum value in matrix: {min_val}")
        print(f"Count of minimum value: {count}")
        print(f"Indices of minimum value:")
        for index in indices:
            print(tuple(int(i) for i in index))
