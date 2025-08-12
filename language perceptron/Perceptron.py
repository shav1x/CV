import math
import random


class Perceptron:

    perceptrons_working = [] # <-- static list of created perceptrons (num of languages possible)

    def __init__(self, learning_rate, epochs, alphabet, language):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.alphabet = alphabet
        self.dimensions = len(self.alphabet)
        self.weighted_sum = 0
        self.language = language
        self.bias = random.random()
        self.weights = [random.random() for i in range(self.dimensions)]
        self.freq = [0 for _ in range(self.dimensions)]
        Perceptron.perceptrons_working.append(self)

    @staticmethod
    def predict():
        perceptron_predicted = sorted(Perceptron.perceptrons_working, key=lambda x: x.weighted_sum, reverse=True)[0]
        return perceptron_predicted

    def update_weight_and_bias(self):
        nWeights = [0 for i in range(self.dimensions)]
        coeff = self.learning_rate
        for i in range(self.dimensions):
            nWeights[i] = self.weights[i] + coeff * self.freq[i]
        self.weights = nWeights
        self.bias += coeff

    def calculate_weighted_sum(self):
        self.weighted_sum = 0
        for i in range(self.dimensions):
            self.weighted_sum += self.freq[i] * self.weights[i]
        self.weighted_sum += self.bias

    def train(self, dataset_row):
        self.set_freq(dataset_row)
        self.normalize()
        self.calculate_weighted_sum()

    def set_freq(self, dataset_row):
        self.freq = [0 for _ in range(self.dimensions)]
        for char in dataset_row:
            if char in self.alphabet:
                self.freq[self.alphabet.index(char)] += 1

    def normalize(self):
        magnitude = math.sqrt(sum(x ** 2 for x in self.freq))
        if magnitude == 0: raise ValueError("You must enter some text, not numbers")
        for i in range(len(self.freq)):
            self.freq[i] /= magnitude
