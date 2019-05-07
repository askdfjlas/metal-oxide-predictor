import build_tree
import dtree_build
import matplotlib.pyplot as plt

NUM_POINTS = 100


def get_mean(node):  # Compute the mean at a node of the regression tree
    mean = 0
    for k in node:
        mean += float(node[k][:-1])/100*k  # Decimal percentage times value

    return int(mean)


def main(training_f, testing_f):
    rows = build_tree.retrieve_rows(training_f)  # Training rows
    test_rows = build_tree.retrieve_rows(testing_f)  # Testing rows
    tree = dtree_build.buildtree(rows, dtree_build.variance, min_gain=1, min_samples=30)  # Build tree with training set

    actual = []
    predicted = []
    for i in range(NUM_POINTS):
        row = test_rows[i]
        val = row.pop(-1)  # Exclude the class label, this was originally in there for convenience
        node = dtree_build.classify(row, tree)
        actual.append(val)
        predicted.append(get_mean(node))

    plt.plot(list(range(NUM_POINTS)), actual)
    plt.plot(list(range(NUM_POINTS)), predicted)
    axes = plt.gca()
    axes.set_ylim([0, 2400])
    plt.show()


if __name__ == "__main__":
    main("../data/training/train_set_48.csv", "../data/testing/test_set_48.csv")
