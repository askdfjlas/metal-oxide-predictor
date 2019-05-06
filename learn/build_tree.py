# Code to build tree from csv
import dtree_build
import dtree_draw
import dtree_to_json
import json

labels = ["CO", "tin oxide", "benzene", "titania", "NOx", "tungsten oxide",
          "NO2", "tungsten oxide2", "indium oxide", "temperature", "relative humidity", "absolute humidity",
          "ic 12 hours prior", "ic 24 hours prior"]  # Attribute names


# Read .csv into rows
def retrieve_rows(input_f):
    data = open(input_f)
    rows = []

    for line in data:
        arr = line.rstrip().split(';')
        entry = []

        for element in arr:
            element = element.replace(',', '.')
            try:
                element = float(element)
            except ValueError:
                pass

            entry.append(element)
        rows.append(entry)

    return rows


def main(input_f, output_img, output_json):
    rows = retrieve_rows(input_f)  # Read rows from input file]
    tree = dtree_build.buildtree(rows, scoref=dtree_build.variance, min_gain=1, min_samples=30)  # Build the tree
    dtree_draw.drawtree(tree, labels, output_img)  # Draw .jpg of tree
    json_tree = dtree_to_json.dtree_to_jsontree(tree, labels)  # Convert tree to JSON for d3.js visualization

    # Dump json tree into a file
    json_file = open(output_json, "w")
    json.dump(json_tree, json_file)
    json_file.close()


if __name__ == "__main__":
    main("../data/training/preliminary.csv", "../data/output/initial.jpg", "../data/output/initial.json")
