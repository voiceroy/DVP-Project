import polars as pl
import getdata
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pl.read_csv("owid-covid-data.csv")


def get_input() -> dict:
    plot_details = {}

    # Select the country
    countries = sorted(set(df.get_column("location")))
    for i, country in enumerate(countries, start=1):
        print(f"{i}.{country}")
    choice = 0
    choice = int(input("Enter the country no: "))
    plot_details["country"] = countries[choice - 1]

    # Select data to plot
    availdata = [
        "total_cases",
        "new_cases",
        "total_deaths",
        "new_deaths",
    ]
    print("Avaliable Data:")
    for i, avail in enumerate(availdata, start=1):
        print(f"{i}. {' '.join(avail.split('_')).title()}")
    choice = int(input("Enter choice: "))
    plot_details["column"] = availdata[choice - 1]

    # Select scale for the y-axis
    scales = ["log", "linear"]
    for i, scale in enumerate(scales, start=1):
        print(f"{i}. {scale.upper()}")
    choice = int(input("Scale for y-axis: "))
    plot_details["scale"] = scales[choice - 1]

    # Save the plot?
    plot_details["save"] = False
    choice = input("Do you want to save the plot(y/n): ")
    if choice.strip().lower() == "y":
        plot_details["save"] = True

    return plot_details


def process_input(plot_details: dict) -> dict:
    filtered = df.filter(pl.col("location") == plot_details["country"])
    plot_details["y_axis"] = filtered.get_column(plot_details["column"])
    plot_details["x_axis"] = filtered.get_column("date").str.to_datetime("%Y-%m-%d")

    return plot_details


def plot_data(plot_details: dict):
    title = f"{plot_details['country'].title()}: {' '.join(plot_details['column'].split('_')).title()} {plot_details['scale'].upper()} Scale"

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))

    plt.plot_date(
        plot_details["x_axis"],
        plot_details["y_axis"],
        label=" ".join(plot_details["column"].split("_")).title(),
    )
    plt.title(title)

    plt.yscale(plot_details["scale"])
    plt.xlabel("Date")
    plt.ylabel(" ".join(plot_details["column"].split("_")).title())

    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.gcf().autofmt_xdate()

    if plot_details["save"] is True:
        plt.savefig(
            fname=title + ".png",
            format="png",
            bbox_inches="tight",
        )

    plt.show()


if __name__ == "__main__":
    if not getdata.refresh():
        print("Could not retrieve data, exiting")
        exit(-1)

    plt.rcParams["figure.figsize"] = (16, 9)
    plot_details = get_input()
    plot_details = process_input(plot_details)
    plot_data(plot_details)
