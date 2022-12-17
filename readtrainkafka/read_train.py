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
import pymongo

st = time.process_time()

features = 18


def consume_kafka_data(data):
    message = tf.io.decode_csv(data.message, [[0.0] for i in range(features)])
    key = tf.strings.to_number(data.key)
    return (message, key)

batch_size = 64
buffer_size = 64

train_data = tfio.IODataset.from_kafka('trainData', partition=0, offset=0)
train_data = train_data.shuffle(buffer_size= buffer_size)
train_data = train_data.map(consume_kafka_data)
train_data = train_data.batch(batch_size)

et1 = time.process_time()
load_data = et1 - st


opt = "adam"
Loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)
evalutions = ['accuracy']
epochs = 1



model = tf.keras.Sequential([
  tf.keras.layers.Input(shape=(features,)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dropout(0.4),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.4),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

print(model.summary())


model.compile(optimizer= opt, loss= Loss, metrics=evalutions)


model.fit(train_data, epochs=epochs)

et2 = time.process_time()
train_time = et2 - et1


def save_model_to_db(model, client, db, dbconnection, model_name):
  model_json = model.to_json()
  myclient = pymongo.MongoClient(client)
  mydb = myclient[db]
  mycon = mydb[dbconnection]
  info = mycon.insert_one({model_name: model_json, 'name': model_name, 'created_time':time.time()})
  print('Model saved with ID: ',info.inserted_id)
  details = {
  'inserted_id':info.inserted_id,
  'model_name':model_name,
  'created_time':time.time()
  }
  return details


details = save_model_to_db(model = model, client ='mongodb://localhost:27017/', db = 'bigData', dbconnection = 'MLModels', model_name = 'modelKafka')
print(details)

et3 = time.process_time()
save_db_time = et3 - et2

print("Time to consume from Kafka: ", load_data)
print("Time to train the model: ", train_time)
print("Time to save the model to MongoDB: ", save_db_time)