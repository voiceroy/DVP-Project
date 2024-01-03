import polars as pl
import getdata


df = pl.read_csv("owid-covid-data.csv")


def get_input() -> dict:
    dct = {}

    countries = sorted(set(df.get_column("location")))
    for i, country in enumerate(countries, start=1):
        print(f"{i}.{country}")

    number = 0
    while True:
        number = int(input("Enter the country no: "))
        if number < 0 or number + 1 > len(countries):
            print("Enter a valid country number")
        else:
            break

    dct["country"] = countries[number - 1]

    availdata = [
        "total_cases",
        "new_cases",
        "total_deaths",
        "new_deaths",
        "new_tests",
        "total_tests",
    ]

    print("Avaliable Data:")
    for i, avail in enumerate(availdata, start=1):
        print(f"{i}. {avail}")

    datachoice = -1
    while True:
        datachoice = int(input("Enter choice: "))
        if datachoice < 0 or datachoice > len(availdata):
            print("Enter a valid choice")
        else:
            break

    dct["column"] = availdata[datachoice - 1]

    return dct


if __name__ == "__main__":
    if not getdata.refresh():
        print("Could not retrieve data, exiting")
        exit(-1)

    dct = get_input()
