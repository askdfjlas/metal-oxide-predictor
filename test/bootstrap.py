import preprocess_initial
import build_tree
import random


def get_sets(rows):  # Generate training and test sets
    train_set = []  # Slowly append new entries to the training set
    test_set = list(rows)
    for i in range(len(rows)):
        rand = random.randint(0, len(rows) - 1)
        train_set.append(list(rows[rand]))
        test_set[rand] = None  # Temporarily mark picked entries as None

    count = 0  # Keep track of popping index
    for i in range(len(test_set)):
        if test_set[i - count] is None:
            test_set.pop(i - count)
            count += 1

    return train_set, test_set


def list_to_csv(data, output_f):  # Write list to csv file
    output = open(output_f, "w")
    for arr in data:
        preprocess_initial.write_csv(output, arr)
    output.close()


def main(input_csv, train_set_f, test_set_f):
    rows = build_tree.retrieve_rows(input_csv)
    train_set, test_set = get_sets(rows)

    list_to_csv(train_set, train_set_f)
    list_to_csv(test_set, test_set_f)


if __name__ == "__main__":
    main("../data/training/preliminary.csv", "../data/training/train_set.csv", "../data/testing/test_set.csv")
