# Code to build tree from csv
import time_plots
import dtree_build
import dtree_draw

labels = ["CO", "tin oxide", "benzene", "titania", "NOx", "tungsten oxide",
          "NO2", "tungsten oxide2", "indium oxide", "temperature", "relative humidity", "absolute humidity",
          "ic 12 hours prior", "ic 24 hours prior"]


def main(input_f, output_img):
    rows = time_plots.retrieve_rows(input_f)
    tree = dtree_build.buildtree(rows, scoref=dtree_build.variance, min_gain=1, min_samples=100)
    dtree_draw.drawtree(tree, labels, output_img)


if __name__ == "__main__":
    main("../data/preliminary.csv", "../data/initial.jpg")
