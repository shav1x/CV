from Perceptron import Perceptron
from Dataset import Dataset


def main():
    training_file = "data/lang.train.csv"
    testing_file = "data/lang.test.csv"
    training_dataset = Dataset.load_from_csv(training_file)
    testing_dataset = Dataset.load_from_csv(testing_file)

    english_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    polish_alphabet = ['A', 'Ą', 'B', 'C', 'Ć', 'D', 'E', 'Ę', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Ł',
                       'M', 'N', 'Ń', 'O', 'Ó', 'P', 'Q', 'R', 'S', 'Ś', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ź', 'Ż']
    spanish_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ',
                        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    german_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                       'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü', 'ß']

    learning_rate = 0.1
    epochs = 20
    perceptrons = [Perceptron(learning_rate, epochs, english_alphabet, "English"),
                   Perceptron(learning_rate, epochs, polish_alphabet, "Polish"),
                   Perceptron(learning_rate, epochs, spanish_alphabet, "Spanish"),
                   Perceptron(learning_rate, epochs, german_alphabet, "German")]

    # Training
    print(f"Epochs: {epochs} | Learning rate: {learning_rate}")
    print(f"\nTraining for {len(perceptrons)} languages...")
    for i in range(epochs):
        row_counter = -1
        for row in training_dataset.texts:
            row_counter += 1
            for j in range(len(perceptrons)):
                if perceptrons[j].language == training_dataset.labels[row_counter]:
                    perceptrons[j].train(row)
            language = Perceptron.predict().language
            if not language == training_dataset.labels[row_counter]:
                for p in perceptrons:
                    if not p.language == language:
                        p.update_weight_and_bias()
    print("Training is completed.\n")

    # Choice
    choice = input("Enter '1' to proceed to testing the file, or '2' to provide the text to define the language: ")
    match choice:
        case '1':
            # Testing
            print(f"Testing the file {testing_file}...")
            correct = 0
            summ = len(testing_dataset.texts)
            counter = -1
            for row in testing_dataset.texts:
                counter += 1
                for perceptron in perceptrons:
                    perceptron.set_freq(row)
                    perceptron.normalize()
                    perceptron.calculate_weighted_sum()
                language_defined = Perceptron.predict().language
                if language_defined == testing_dataset.labels[counter]:
                    correct += 1
            print(f"Accuracy: {(correct / summ) * 100}%")
        case '2':
            text = input("Enter the text to define the language: ").strip().upper()
            for perceptron in perceptrons:
                perceptron.set_freq(text)
                perceptron.normalize()
                perceptron.calculate_weighted_sum()
            language_defined = Perceptron.predict().language
            print(f"Language defined: {language_defined}")
        case _:
            raise ValueError("Invalid choice, exiting...")


if __name__ == "__main__":
    main()
