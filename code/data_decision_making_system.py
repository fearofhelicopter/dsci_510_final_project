import math
import pprint
import numpy as np
import pandas as pd
from data_analysis_and_visualizations import main_data_analysis


def search_make_name(make_id):
    make_2021 = pd.read_csv("../data/all_make_tabel_2021.csv")
    make_2022 = pd.read_csv("../data/all_make_tabel_2022.csv")
    make_2021 = make_2021[make_2021["make_id"] == make_id]
    if make_2021.empty:
        make_2022 = make_2022[make_2022["make_id"] == make_id]
        return make_2022["make_name"].values[0]
    else:
        return make_2021["make_name"].values[0]


def search_model_name(model_id):
    model_2021 = pd.read_csv("../data/all_models_tabel_2021.csv")
    model_2022 = pd.read_csv("../data/all_models_tabel_2022.csv")
    model_2021 = model_2021[model_2021["model_id"] == model_id]
    if model_2021.empty:
        model_2022 = model_2022[model_2022["model_id"] == model_id]
        make = search_make_name(model_2022["make_id"].values[0])
        return model_2022["model_name"].values[0], make
    else:
        make = search_make_name(model_2021["make_id"].values[0])
        return model_2021["model_name"].values[0], make


def search_model_id(model_name):
    model_2021 = pd.read_csv("../data/all_models_tabel_2021.csv")
    model_2022 = pd.read_csv("../data/all_models_tabel_2022.csv")
    model_2021 = model_2021[model_2021["model_name"] == model_name]

    if model_2021.empty:
        model_2022 = model_2022[model_2022["model_name"] == model_name]
        if model_2022.empty:
            return False
        else:
            return model_2022["model_id"].values[0]
    else:
        return model_2021["model_id"].values[0]


def calculate_scale(records, scale=10):
    scale_list = []
    max_n = max([x[1] for x in records])
    for record in records:
        record_id, value = record
        if value == 0:
            scale_list.append([record_id, 0])
        else:
            scale_list.append([record_id, 1 + value * (scale - 1) / max_n])
    return scale_list


def decision_making(merged_price):
    # we want the change of increase price is minimized and the change of increase invoice is maximized
    weights = [0.6, 0.3, 0.1]
    price = merged_price["increase_rate_%"].values
    invoice = merged_price["increase_invoice_rate%"].values

    price = [-1 * x for x in price]
    price = [(x[0], x[1] + abs(min(price)) + 1) for x in enumerate(price)]
    price = calculate_scale(records=price)

    for i in range(len(invoice)):
        if np.isnan(invoice[i]):
            invoice[i] = 0
    for i in range(len(invoice)):
        if np.isinf(invoice[i]):
            invoice[i] = np.NINF
    for i in range(len(invoice)):
        if np.isinf(invoice[i]):
            invoice[i] = max(invoice)

    invoice = [(x[0], x[1] + abs(min(invoice)) + 1) for x in enumerate(invoice)]
    invoice = calculate_scale(records=invoice)

    score = []
    for i in range(len(invoice)):
        each_score = price[i][1] * weights[0] + invoice[i][1] * weights[1]
        score.append(each_score)

    merged_price["score"] = score
    return merged_price


def play_board():
    data = main_data_analysis()
    data = decision_making(data)
    contin = True
    while contin:
        print("Choice Your Options: ")
        print("1. Enter a Model (system will give you advise)")
        print("2. Enter a Price Range (system will give you advise)")
        print("Other numbers to quit")
        option = int(input("Option: "))
        if option == 1:
            model_name = input("Enter a Model: ").upper()
            model = search_model_id(model_name)
            if model:
                new_data = data[data["model_id"] == model]
                try:
                    price = float(new_data["price_2022"].values[0])
                    start = price - 2000
                    end = price + 2000
                    new_data1 = data[(data["price_2022"] >= start) & (data["price_2022"] <= end)]
                    new_data1.sort_values(by='score', ascending=False)
                    if not new_data1.empty:
                        if new_data1["model_id"].values[0] != model:
                            model = new_data1["model_id"].values[0]
                            model, make = search_model_name(model_id=model)
                            print("The better model for similar price to buy is", model, make)
                            print()
                        else:
                            print(model_name, "is a good choice.")
                            print()
                    else:
                        print("No Search Found. Try Again.")
                        print()
                except:
                    print("Invalid Model Name. Try Again.")
                    print()
            else:
                print("Invalid Model Name. Try Again.")
                print()

        elif option == 2:
            start = int(input("Start Price: "))
            end = int(input("End Price: "))
            while start >= end:
                start = int(input("Start Price: "))
                end = int(input("End Price: "))
            new_data = data[(data["price_2022"] >= start) & (data["price_2022"] <= end)]
            new_data.sort_values(by='score', ascending=False)
            if not new_data.empty:
                model = new_data["model_id"].values[0]
                model, make = search_model_name(model_id=model)
                print("The best model to buy in this range is", model, make)
                print()
            else:
                print("No Search Found. Try Again.")
                print()
        else:
            contin = False


if __name__ == "__main__":
    play_board()
