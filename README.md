# Deep learning on SUSY dataset using Kafka and TensorFlow
The main aim of this project is to create a containerized data pipeline to stream the data from the SUSY dataset, train a deep learning model and testing the performance of the deep learning model. The SUSY dataset is simulated particle accelerator data, thus we used Kafka to stream the data and consume the data using TensorFlow. Further, build a deep learning model and train it using the consumed data. The trained model is saved to MongoDB and used Pyspark and Pandas to test the saved model on the test data. The entire data pipeline is containerized using Docker##### Check the project report for how to run the project.
## To Run
1) Download the SUSY dataset from UCI machine learning repository. <br>
2) Build the image for writekafka using the docker file in the file named
“writekafka. <br>
3) Build the docker image for readtrainkafka using the docker file in the file
named “readtrainkafka”. <br>
4) Use the docker compose file docker_compose_kafka.yml to create and launch
the containers for kafka and zookeeper. Use the command “docker exec. <br>
broker kafka-topics --bootstrap-server broker:9092 --create --topic trainData”
to create the topic trainData. <br>
5) Pull the docker image for MongoDB 6.0 and build the image. <br>
6) Use “docker exec -it MongoDB_Container_Name” bash” command to get to
the containershell. Run “mongosh” inside the container to get into MongoDB.
Create a database called “bigdata” and a collection called "MLModels”. And
exit the container. <br>
7) Use the command “docker run -it --volume "Dataset Location in Local
Machine":/writekafka --network="host" writekafka” to launch the writekafka
container. <br>
8) Use the command “docker run -it --network="host" readtrainkafka” to run the
readtrainkafka container. <br>
9) Use the commands in MongoDB step to view the saved model. <br>
10) Pull the image for pyspark jupyter notebook from docker hub. <br>
11) Use the command “docker run -it -p 8888:8888 --volume "Test Data Location
in Local Machine":/readTest --name pyspark jupyter/pyspark-notebook” to
launch the pyspark notebook and access the jupyter notebook in the local
machine browser. <br>
12) Use the command “docker inspect -f
'{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' MongoDB
container name” to get the IP address of the MongoDB container. <br>
13) Run the notebook, but change the timestamp or model ID that needed to be
chosen and view the results. And use the IP address acquired in the previous
step to connect to MongoDB client. <br>
### Datapipeline
<img src="figures/flowdiagram.jpg" width="500" height="600">>
