import csv


class Dataset:

    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    @property
    def get_texts(self):
        return self.texts

    @property
    def get_labels(self):
        return self.labels

    @staticmethod
    def load_from_csv(file_path):
        text_list = []
        label_list = []

        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:

                label = row[0].strip()
                text = row[1].strip().upper()

                label_list.append(label)
                text_list.append(text)

        return Dataset(text_list, label_list)
