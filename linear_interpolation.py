class LinearInterpolation:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def evaluate(self, time):
        return time * self.start - (1 - time) * self.end
