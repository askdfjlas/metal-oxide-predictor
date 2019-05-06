from math import log

class decisionnode:
    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb  # True branch
        self.fb = fb  # False branch


# Divides a set on a specific column. Can handle numeric
# or nominal values
def divideset(rows, column, value):
    # Make a function that tells
    # if the split is on numeric value (>=/<)
    # or on nominal value (==/!=)
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] > value
    else:
        split_function = lambda row: row[column] == value

    # Divide the rows into two sets and return them
    set1 = [row for row in rows if split_function(row)]  # Missing values go into both branches
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


# Create counts of class labels for a given set
# (the last column of each row is the class attribute)
def uniquecounts(rows):
    results = {}
    for row in rows:
        # The result is the last column
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results


# Probability that a randomly placed item will
# be in the wrong category
# Using the closed form here:
# https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp


# Entropy is the sum of p(x)log(p(x)) across all
# the different possible classes
def entropy(rows):
    results = uniquecounts(rows)
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log(p, 2)
    return ent


def variance(rows):
    if len(rows) == 0: return 0
    data = [float(row[len(row) - 1]) for row in rows]
    mean = sum(data) / len(data)
    variance = sum([(d - mean) ** 2 for d in data]) / len(data)
    return variance


def prediction(leaf_labels):
    total = 0
    result = {}
    for label, count in leaf_labels.items():
        total += count
        result[label] = count

    for label, val in result.items():
        result[label] = str(int(result[label]/total * 100))+"%"

    return result


def classify(observation, tree):
    if tree.results != None:
        return prediction(tree.results)
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v > tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        return classify(observation, branch)


# Classify an observation with missing data
def mdclassify(observation, tree):
    if tree.results != None:
        return prediction(tree.results)
    else:
        v = observation[tree.col]
        if v == None:
            tr, fr = mdclassify(observation, tree.tb), mdclassify(observation, tree.fb)
            tcount = sum(tr.values())
            fcount = sum(fr.values())
            tw = float(tcount) / (tcount + fcount)
            fw = float(fcount) / (tcount + fcount)
            result = {}
            for k, v in tr.items(): result[k] = v * tw
            for k, v in fr.items(): result[k] = v * fw
            return result
        else:
            if isinstance(v, int) or isinstance(v, float):
                if v >= tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            else:
                if v == tree.value:
                    branch = tree.tb
                else:
                    branch = tree.fb
            return mdclassify(observation, branch)


def buildtree(rows, scoref=entropy,
              min_gain=0, min_samples=0):
    if len(rows) == 0:
        return decisionnode()
    current_score = scoref(rows)

    # Set up accumulator variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        # Generate the list of different values in
        # this column
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        # Now try dividing the rows up for each value
        # in this column
        for value in column_values.keys():
            (set1, set2) = divideset(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            if gain > best_gain and len(set1) > min_samples and len(set2) > min_samples and gain > min_gain:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    # Create the sub branches
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0], scoref, min_gain, min_samples)
        falseBranch = buildtree(best_sets[1], scoref, min_gain, min_samples)
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))


def max_depth(tree):
    if tree.results != None:
        return 0
    else:
        # Compute the depth of each subtree
        tDepth = max_depth(tree.tb)
        fDepth = max_depth(tree.fb)

        # Use the larger one
        if (tDepth > fDepth):
            return tDepth + 1
        else:
            return fDepth + 1


def printtree(tree, current_branch, attributes=None,  indent='', leaff=prediction):
    # Is this a leaf node?
    if tree.results != None:
        print(indent + current_branch + str(leaff(tree.results)))
    else:
        # Print the split question
        split_col = str(tree.col)
        if attributes is not None:
            split_col = attributes[tree.col]
        split_val = str(tree.value)
        if type(tree.value) == int or type(tree.value) == float:
            split_val = ">=" + str(tree.value)
        print(indent + current_branch + split_col + ': ' + split_val + '? ')

        # Print the branches
        indent = indent + '  '
        printtree(tree.tb, 'T->', attributes, indent)
        printtree(tree.fb, 'F->', attributes, indent)
