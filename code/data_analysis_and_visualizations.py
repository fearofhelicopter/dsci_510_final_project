import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import logging
import seaborn as sns

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


def load_data():
    data_path = "../data"
    # data_file = "/all_models_tabel_2021.csv"
    # model_data_2021 = pd.read_csv(data_path + data_file)
    data_file_trim1 = "/models_trims_tabel_2021.csv"
    data_file_trim2 = "/models_trims_tabel_2022.csv"
    trims_data_2021 = pd.read_csv(data_path + data_file_trim1)
    trims_data_2022 = pd.read_csv(data_path + data_file_trim2)
    return trims_data_2021, trims_data_2022


def main_data_analysis():
    trims_data_2021, trims_data_2022 = load_data()
    # data processing
    trims_data_2021 = trims_data_2021.rename(columns={'price': 'price_2021', 'invoice': 'invoice_2021'}).drop(
        columns=["Unnamed: 0"])
    trims_data_2022 = trims_data_2022.rename(columns={'price': 'price_2022', 'invoice': 'invoice_2022'}).drop(
        columns=["Unnamed: 0"])
    trims_data_2021_mean = trims_data_2021.groupby(['model_id']).mean()
    trims_data_2022_mean = trims_data_2022.groupby(['model_id']).mean()

    # merge data
    merged_price = pd.merge(trims_data_2021_mean, trims_data_2022_mean, how="inner", on=["model_id"])
    merged_price.reset_index(inplace=True)

    # calculate the percentage of change of prices and invoices
    price_2021 = merged_price["price_2021"].values
    price_2022 = merged_price["price_2022"].values
    invoice_2021 = merged_price["invoice_2021"].values
    invoice_2022 = merged_price["invoice_2022"].values

    increase_rate, invoice_rate, sell_statue = [], [], []
    for i in range(len(price_2021)):
        invoice = (invoice_2022[i] / invoice_2021[i] - 1) * 100
        price = (price_2022[i] / price_2021[i] - 1) * 100
        increase_rate.append(price)
        invoice_rate.append(invoice)
        if np.isnan(invoice):
            sell_statue.append(None)
        elif invoice > price:
            sell_statue.append(1)
        else:
            sell_statue.append(0)

    merged_price["increase_rate_%"] = increase_rate
    merged_price["increase_invoice_rate%"] = invoice_rate
    merged_price["sell_status"] = sell_statue
    return merged_price


def generate_result(merged_price):
    result_path = '../result/'
    merged_price.to_csv(result_path + "merged_price_invoice.csv")
    merged_price_cheap_cars = merged_price[merged_price["price_2021"] < 40000]
    merged_price_cheap_cars.to_csv(result_path + "merged_price_invoice_cheap_cars.csv")
    merged_price_median_cars = merged_price[
        (merged_price["price_2021"] >= 40000) & (merged_price["price_2021"] < 80000)]
    merged_price_median_cars.to_csv(result_path + "merged_price_invoice_median_cars.csv")
    merged_price_luxury_cars = merged_price[(merged_price["price_2021"] >= 80000)]
    merged_price_luxury_cars.to_csv(result_path + "merged_price_invoice_luxury_cars.csv")

    # show Car Prices change from 2021 to 2022
    title = 'Car Prices change from 2021 to 2022'
    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(8)
    plt.plot(merged_price["model_id"], merged_price["price_2021"], color="black", label="price 2021")
    plt.plot(merged_price["model_id"], merged_price["price_2022"], color="red", label="price 2022")
    plt.xlabel('model_id')
    plt.ylabel('price')
    plt.title('Car Prices change from 2021 to 2022')
    plt.legend()
    plt.savefig(result_path + title + '.pdf')

    # show prices change from 2021 to 2022 of three classes
    title = "prices change from 2021 to 2022 of three classes"
    fig = plt.figure()
    fig.set_figwidth(21)
    fig.set_figheight(8)
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)
    ax1.plot(merged_price_cheap_cars["model_id"], merged_price_cheap_cars["price_2021"], label='cheap car price 2021')
    ax1.plot(merged_price_cheap_cars["model_id"], merged_price_cheap_cars["price_2022"], label='cheap car price 2022')
    ax2.plot(merged_price_median_cars["model_id"], merged_price_median_cars["price_2021"],
             label='median car price 2021')
    ax2.plot(merged_price_median_cars["model_id"], merged_price_median_cars["price_2022"],
             label='median car price 2022')
    ax3.plot(merged_price_luxury_cars["model_id"], merged_price_luxury_cars["price_2021"],
             label='luxury car price 2021')
    ax3.plot(merged_price_luxury_cars["model_id"], merged_price_luxury_cars["price_2022"],
             label='luxury car price 2022')
    ax1.set_xlabel('model')
    ax1.set_ylabel('Price')
    ax1.set_title('Cheap Car Prices Change')
    ax1.legend()
    ax2.set_xlabel('model')
    ax2.set_ylabel('Price')
    ax2.set_title('Median Car Prices Change')
    ax2.legend()
    ax3.set_xlabel('model')
    ax3.set_ylabel('Price')
    ax3.set_title('Luxury Car Prices Change')
    ax3.legend()
    plt.savefig(result_path + title + '.pdf')

    # Increase Rate(%) of three classes
    title = "Increase Rate(%) of three classes"
    fig = plt.figure()
    fig.set_figwidth(21)
    fig.set_figheight(8)
    ax1 = fig.add_subplot(1, 3, 1)
    ax2 = fig.add_subplot(1, 3, 2)
    ax3 = fig.add_subplot(1, 3, 3)

    ax1.plot(merged_price_cheap_cars["model_id"], merged_price_cheap_cars["increase_rate_%"],
             label='cheap car increate_rate')

    ax2.plot(merged_price_median_cars["model_id"], merged_price_median_cars["increase_rate_%"],
             label='median car increate_rate')

    ax3.plot(merged_price_luxury_cars["model_id"], merged_price_luxury_cars["increase_rate_%"],
             label='luxury car increate_rate')

    ax1.set_xlabel('model')
    ax1.set_ylabel('increate_rate')
    ax1.set_title('Cheap Car Increate Rate')
    ax1.legend()
    ax2.set_xlabel('model')
    ax2.set_ylabel('increate_rate')
    ax2.set_title('Median Car Increate Rate')
    ax2.legend()
    ax3.set_xlabel('model')
    ax3.set_ylabel('increate_rate')
    ax3.set_title('Luxury Car Increate Rate')
    ax3.legend()
    plt.savefig(result_path + title + '.pdf')

    # Car Prices Increase Rate from 2021 to 2022
    title = "Car Prices Increase Rate from 2021 to 2022"
    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(8)
    plt.plot(merged_price["model_id"], merged_price["increase_rate_%"], label="increate_rate")
    plt.xlabel('model_id')
    plt.ylabel("Increase Rate(%)")
    plt.title('Car Prices Increase Rate from 2021 to 2022')
    plt.legend()
    plt.savefig(result_path + title + '.pdf')

    # Car Invoice Increase Rate from 2021 to 2022
    title = "Car Invoice Increase Rate from 2021 to 2022"
    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(8)
    plt.plot(merged_price["model_id"], merged_price["increase_invoice_rate%"], label="increate_rate")
    plt.xlabel('model_id')
    plt.ylabel("Invoice Increase Rate(%)")
    plt.title('Car Invoices Increase Rate from 2021 to 2022')
    plt.legend()
    plt.savefig(result_path + title + '.pdf')

    # Compare invoice change and price change
    title = "Compare invoice change and price change"
    data_sell = merged_price["sell_status"].values
    number_1 = 0
    number_0 = 0
    other = 0
    for i in range(len(data_sell)):
        if np.isnan(data_sell[i]):
            other += 1
        elif int(data_sell[i]) == 1:
            number_1 += 1
        elif int(data_sell[i]) == 0:
            number_0 += 1
    cate = [number_1, number_0, other]
    labels = ['Relatively Cheap', 'Relatively Expensive', 'Not found']
    colors = sns.color_palette('pastel')[0:5]
    plt.pie(cate, labels=labels, colors=colors, autopct='%.0f%%')
    plt.savefig(result_path + title + '.pdf')


if __name__ == "__main__":
    data = main_data_analysis()
    generate_result(data)
    logging.info("result saved")
