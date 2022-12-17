import numpy as np
import os
from datetime import datetime
import time
import threading
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError
from sklearn.model_selection import train_test_split
import pandas as pd
import tensorflow as tf
import tensorflow_io as tfio

st = time.process_time()

label_features = ['class', 'lepton_1_pT', 'lepton_1_eta','lepton_1_phi','lepton_2_pT','lepton_2_eta','lepton_2_phi','missing_energy_magnitude','missing_energy_phi','MET_rel','axial_MET','M_R','M_TR_2','R','MT2','S_R','M_Delta_R','dPhi_r_b','cos(theta_r1)']


df_itr = pd.read_csv("writekafka/SUSY.csv.gz", header = None, names = label_features,chunksize=100000)
df = next(df_itr)

train_data, test_data = train_test_split(df, test_size=0.1, shuffle=True)
print("Total Training Data: ",len(train_data))

x_train_data = train_data.drop(["class"], axis=1)
y_train_data = train_data["class"]


x_train = list(filter(None, x_train_data.to_csv(index=False).split("\n")[1:]))
y_train = list(filter(None, y_train_data.to_csv(index=False).split("\n")[1:]))



for i in range(len(x_train)):
    x_train[i] = x_train[i].rstrip()


for i in range(len(y_train)):
    y_train[i] = y_train[i].rstrip()

et1 = time.process_time()

load_data_time = et1 - st

def error_callback(exc):
    raise Exception('Error while sending data to kafka: {0}'.format(str(exc)))

def produce_to_kafka(topic_name, data):
    count=0
    producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])
    for message, key in data:
        producer.send(topic_name, key=key.encode('utf-8'), value=message.encode('utf-8')).add_errback(error_callback)
        count+=1
    producer.flush()
    print("Messages Written {0} into Topic: {1}".format(count, topic_name))

produce_to_kafka("trainData", zip(x_train, y_train))

et = time.process_time()

kafka_time = et - et1

print('Execution time for loading the data:', load_data_time, 'seconds')
print('Execution time for writing to kafka:', kafka_time, 'seconds')










