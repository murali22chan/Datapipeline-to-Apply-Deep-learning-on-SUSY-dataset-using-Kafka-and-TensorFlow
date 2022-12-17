FROM python:3.9

ADD write_to_kafka.py .

RUN pip install tensorflow pandas scikit-learn kafka-python tensorflow-io pyspark

CMD ["python", "./write_to_kafka.py"]