FROM python:3.9

ADD read_train.py .

RUN pip install tensorflow pandas scikit-learn kafka-python tensorflow-io pymongo

CMD ["python", "./read_train.py"]