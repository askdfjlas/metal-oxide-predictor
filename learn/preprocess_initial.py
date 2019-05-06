# File for preprocessing as described in slide 13
import time_plots

k = 1
INDIUM_INDEX = 11


def write_csv(file, row):  # Function for writing a row to a CSV file
    for i in range(len(row)):
        # Semicolons so a previous parsing function may be used
        file.write(str(row[i]) + ('\n' if i == len(row) - 1 else ';'))


# Round things depending on their magnitude
def discretize(arr):
    for i in range(len(arr) - 1):
        if arr[i] > 400:
            arr[i] = round(arr[i]/100)*100
        elif arr[i] > 100:
            arr[i] = round(arr[i]/50)*50
        elif arr[i] > 20:
            arr[i] = round(arr[i]/10)*10
        elif arr[i] > 5:
            arr[i] = round(arr[i]/2)*2
        else:
            arr[i] = round(arr[i]/0.5)*0.5


def main(input_f, output_f):  # Main function
    rows = time_plots.retrieve_rows(input_f)  # Retrieve 2D array
    file = open(output_f, "w")
    for i in range(24, len(rows) - k):  # Skip first 24 and last k hours
        row = rows[i]
        # Format: current row excluding date/time, indium concentrations 12 and 24 hours ago
        # Class label: indium concentration k hours in advance
        arr = row[2:] + [rows[i - 12][INDIUM_INDEX]] + \
            [rows[i - 24][INDIUM_INDEX]] + [rows[i + k][INDIUM_INDEX]]
        arr.pop(2)  # This column (hydrocarbon) has many many missing values
        if -200 not in arr:  # If no missing values
            discretize(arr)
            write_csv(file, arr)

    file.close()


if __name__ == "__main__":
    main("../data/AirQualityUCI/AirQualityUCI.csv", "../data/preliminary.csv")
