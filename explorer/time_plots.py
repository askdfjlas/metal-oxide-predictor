# Code to make graphs of all four metal oxide concentrations over time
import matplotlib.pyplot as plt

# Label names
labels = ["date", "time", "carbon monoxide", "tin oxide", "non-methane hydrocarbon", "benzene",
          "titanium dioxide", "NOx", "tungsten trioxide", "NO2", "tungsten oxide no2", "indium oxide",
          "temperature", "relative humidity", "absolute humidity"]

# Labels hashed to their index for convenience
label_dict = {}
for q in range(len(labels)):
    label_dict[labels[q]] = q


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
        rows.append(entry[:-2])

    return rows


# Plot concentrations over time
def time_plot(concentrations, label):
    plt.plot([i for i in range(len(concentrations))], [c for c in concentrations])
    plt.title(label + " concentration time plot")
    plt.show()


def main(input_f):
    rows = retrieve_rows(input_f)

    time_plot(list(map(lambda x: x[label_dict["tin oxide"]], rows))[0: 250], "Tin Oxide")
    time_plot(list(map(lambda x: x[label_dict["titanium dioxide"]], rows))[0: 250], "Titanium Dioxide")
    time_plot(list(map(lambda x: x[label_dict["tungsten trioxide"]], rows))[0: 250], "Tungsten Trioxide")
    time_plot(list(map(lambda x: x[label_dict["indium oxide"]], rows))[0: 250], "Indium Oxide")


if __name__ == "__main__":
    main("../data/AirQualityUCI/AirQualityUCI.csv")
