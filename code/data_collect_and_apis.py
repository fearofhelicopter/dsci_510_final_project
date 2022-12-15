import os
import time
import pandas as pd
import requests
import pandas
import pprint
import logging
from multiprocessing.pool import Pool
import csv
from configs import (
    CAR_API_TOKEN,
    CAR_API_SECRET,
    CAR_API_BASIC_URL,
    CAR_API_LOGIN,
    CAR_API_YEARS,
    CAR_API_MAKES,
    CAR_API_TRIMS,
    CAR_API_MODELS,
    CAR_MD_HEADER,
    CAR_MD_MAINTENANCE,
    CAR_MD_BASIC_URL,
    CAR_MD_MAINTENANCE_LIST,
    CAR_MD_UPCOMING_REPAIR
)
from csv import writer

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)



def car_api_login():
    try:
        token_value = {"api_token": CAR_API_TOKEN, "api_secret": CAR_API_SECRET}
        headers = {"Authorization": f"Bearer {token_value}"}
        response = requests.request("POST", CAR_API_BASIC_URL + CAR_API_LOGIN, headers=headers, json=token_value)
        if response.status_code == 200:
            logging.info("login success.")
            return response.text
        else:
            logging.info("login fail.")
            return False
    except:
        logging.info("login fail.")
        return False


def car_api_all_makes(year):
    param = {"year": year}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.request("GET", CAR_API_BASIC_URL + CAR_API_MAKES, params=param, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        make_id = []
        make_name = []
        for elem in data:
            make_id.append(elem["id"])
            make_name.append(elem['name'])
        dic = {"make_id": make_id, "make_name": make_name}
        logging.info("fetch car makes data success.")
        return dic
    else:
        logging.info("fetch data failed.")


def car_api_all_models(make_id, year):
    param = {"page": 1, "year": year, "make_id": make_id}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.request("GET", CAR_API_BASIC_URL + CAR_API_MODELS, params=param, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        make_id = []
        model_name = []
        model_id = []
        for elem in data:
            model_id.append(elem["id"])
            make_id.append(elem["make_id"])
            model_name.append(elem['name'].upper())
        logging.info("fetch car models data success.")
        return model_id, make_id, model_name
    else:
        logging.info("fetch data failed.")


def car_api_trims(year, model_id):
    param = {"year": year, "verbose": "yes", "make_model_id": model_id}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.request("GET", CAR_API_BASIC_URL + CAR_API_TRIMS, params=param, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        trim_id, model_id, invoice, price = [], [], [], []
        for each in data:
            trim_id.append(each["id"])
            model_id.append(each["make_model_id"])
            invoice.append(each["invoice"])
            price.append(each["msrp"])
        logging.info("fetch car trims data success.")
        return trim_id, model_id, invoice, price
    else:
        logging.info("fetch data failed.")


def car_md_maintenance(year, make, model):
    # seach model id
    data_model = pd.read_csv("../data/all_models_tabel_2021.csv")
    data_each_model = data_model[data_model["model_name"] == model.upper()]
    model_id = data_each_model["model_id"]
    param = {"year": "2015", "make": "CHEVROLET", "model": "EQUINOX", "mileage": 51000}
    response = requests.request("GET", CAR_MD_BASIC_URL + CAR_MD_MAINTENANCE, params=param, headers=CAR_MD_HEADER)
    if response.status_code == 200:
        pprint.pprint(response.json())
        cost = 0
        for each in response.json()["data"]:
            cost += each["repair"]["total_cost"]
        logging.info("fetch car models maintenance data success.")
        l1 = [year, model_id, cost]
        with open("../data/service_cost.csv", "a") as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(l1)
            f_object.close()
        logging.info("write new maintenance searching record success.")
    else:
        logging.info("fetch data failed.")


def start_fetch_the_data(year):
    data = pd.DataFrame(car_api_all_makes(year))
    # first get all makes in 2021, and save
    try:
        data.to_csv(f"../data/all_make_tabel_{year}.csv")
    except:
        logging.info("file exists.")
    make_id_fetch = data["make_id"].values
    model_id, make_id, model_name = [], [], []

        # get all models of makes in 202x, and save
    for id in make_id_fetch:
        model, make, model_n = car_api_all_models(id, year)
        model_id += model
        make_id += make
        model_name += model_n
        time.sleep(0.1)
    dic = {"model_id": model_id, "model_name": model_name, "make_id": make_id}
    data_models = pd.DataFrame(dic)
    try:
        data_models.to_csv(f"../data/all_models_tabel_{year}.csv")
        logging.info("file generated.")
    except:
        logging.info("file exists.")

        # get all trims by the model id in 202x, and then save
    models = data_models["model_id"].values
    trim_id, model_id, invoice, price, = [], [], [], []
    for id in models:
        l1, l2, l3, l4 = car_api_trims(year, id)
        trim_id += l1
        model_id += l2
        invoice += l3
        price += l4
        time.sleep(0.1)
    dic = {"trim_id": trim_id, "model_id": model_id, "invoice": invoice, "price": price}
    data_trims = pd.DataFrame(dic)

    try:
        data_trims.to_csv(f"../data/models_trims_tabel_{year}.csv")
        logging.info("file generated.")
    except:
        logging.info("file exists.")


def add_to_csv(filename, objects):
    # Open our existing CSV file in append mode
    with open(filename, 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = csv.writer(f_object)
        writer_object.writerow(objects)
        f_object.close()


def main():
    # create a service_cost
    with open('../data/service_cost.csv', 'w') as csvfile:
        fieldnames = ['year', 'model_id', 'maintenance_cost']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # generate data
    logging.info("start data fetching....")
    global TOKEN
    TOKEN = car_api_login()
    if TOKEN:
        start_fetch_the_data(2021)
        start_fetch_the_data(2022)
    logging.info("data fetching done....")


if __name__ == '__main__':
    TOKEN = car_api_login()
    if car_api_login():
        model, make, model_n = car_api_all_models(1, 2022)
    pass
