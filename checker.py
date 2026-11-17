import pandas as pd

ranges = pd.read_csv("data/reference_ranges.csv")
people = pd.read_excel("samples/Blood_reports_data_base.xlsx")
people["Gender"] = people["Gender"].str.strip().str.title()
people["Name"] = people["Name"].str.strip()


def check_value(test_name, value, gender):
    row = ranges[ranges["test_name"] == test_name].iloc[0]
    if gender.lower() == "male":
        low, high = row["low_male"], row["high_male"]
    else:
        low, high = row["low_female"], row["high_female"]

    if value < low:
        flag = "LOW"
    elif value > high:
        flag = "HIGH"
    else:
        flag = "NORMAL"
    return flag, low, high


if __name__ == "__main__":
    person = people.iloc[2]
    print("Checking:", person["Name"], "-", person["Gender"])
    for test in ranges["test_name"]:
        value = person[test]
        flag, low, high = check_value(test, value, person["Gender"])
        print(f"{test}: {value}  ->  {flag}  (normal {low} to {high})")