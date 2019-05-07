import json
import dtree_build
import sys
import csv


def node_label(node, attributes=None):
    if node.results != None:
        return str(node.results)
    split_col = str(node.col)
    if attributes is not None:
        split_col = attributes[node.col]
    split_val = str(node.value)
    if type(node.value) == int or type(node.value) == float:
        split_val = ">=" + str(node.value)
    return split_col + ': ' + split_val + '?'


def get_child(node, attributes=None):
    if node == None:
        return None
    curr_node = {}
    curr_node["name"] = node_label(node, attributes)
    children = []
    tb_child = get_child(node.tb, attributes)
    if tb_child:
        children.append(tb_child)
    fb_child = get_child(node.fb, attributes)
    if fb_child:
        children.append(fb_child)

    if len(children) > 0:
        curr_node["children"] = children
    return curr_node


def dtree_to_jsontree(tree, attributes=None):
    root = {}
    root["name"] = node_label(tree, attributes)
    children = []
    tb_child = get_child(tree.tb, attributes)
    if tb_child:
        children.append(tb_child)
    fb_child = get_child(tree.fb, attributes)
    if fb_child:
        children.append(fb_child)

    root["children"] = children
    return root


def main(col_names=None):
    # parse command-line arguments to read the name of the input csv file
    if len(sys.argv) < 2:  # input file name should be specified
        print("Please specify input csv file name")
        return

    csv_file_name = sys.argv[1]

    data = []
    with open(csv_file_name) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            data.append(list(row))
    tree = dtree_build.buildtree(data, min_gain =0.01, min_samples = 30)

    max_tree_depth = dtree_build.max_depth(tree)
    print("max number of questions=" + str(max_tree_depth))

    json_tree = dtree_to_jsontree(tree, col_names)
    print(json_tree)

    # create json data for d3.js interactive visualization
    with open(csv_file_name + ".json", "w") as write_file:
        json.dump(json_tree, write_file)


if __name__ == "__main__":
    col_names = [
        'Age',
        'Work class',
        'Education',
        'Marital status',
        'Occupation',
        'Relationship',
        'Race',
        'Sex',
        'Native-country',
        'Income']
    main(col_names)