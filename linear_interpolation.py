class LinearInterpolation:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def evaluate(self, time):
        return time * self.end - (1 - time) * self.start
