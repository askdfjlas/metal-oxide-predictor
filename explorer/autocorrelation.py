import time_plots
import matplotlib.pyplot as plt

TOTAL_LAGS = 200


# Get (undivided) covariance
def get_covariance(rows, mean, index, k):
    cov = 0

    for i in range(len(rows) - k):
        cov += (rows[i][index] - mean)*(rows[i + k][index] - mean)

    return cov


# Get (undivided) variance and mean
def get_mean_variance(rows, index):
    mean = 0
    variance = 0
    for row in rows:
        mean += row[index]

    mean /= len(rows)
    for row in rows:
        variance += pow(row[index] - mean, 2)

    return mean, variance


def main(input_f):
    rows = time_plots.retrieve_rows(input_f)
    mean, variance = get_mean_variance(rows, time_plots.label_dict["indium oxide"])

    autocorrelations = []
    for i in range(TOTAL_LAGS):
        autocorrelations.append(get_covariance(rows, mean, time_plots.label_dict["indium oxide"], i)/variance)

    plt.plot(list(range(TOTAL_LAGS)), [v for v in autocorrelations])
    plt.title("Autocorrelation plot for Indium Oxide Concentration, k up to 8.3 days")
    plt.show()


if __name__ == "__main__":
    main("../data/AirQualityUCI/AirQualityUCI.csv")
