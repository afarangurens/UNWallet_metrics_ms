#  UNWallet Metrics Microservice
## Andrés Fernando Aranguren Silva
- --
## Analytics and Metrics Component

A FastAPI service microservice using a Mongodb database that handles the data analysis, data visualization and an optimization-based recommendation system for budgeting monthly expenses of an integrated system called UNWallet which is an expenses and income tracking app.

Main functions that this service manage:

- Statistical Anaylsis
- Suggestion based on historic data
- A recommendation budget plan given certain parameters like savings goal, monthly income, basic expenses, etc.


# Clone and App installation

1. First you'll need to clone this repository to your local machine using:

        git clone https://github.com/afarangurens/UNWallet_metrics_ms.git
        cd UNWallet_metrics_ms

# Deployment Instructions

1. This microservice consist in a tuple of a mongodb docker and a FastAPI docker, you will need to create the mongodb container first, for this pull the official mongo image from docker using:

        docker pull mongo

2. Then you'll need to run the mongo image using the following command:

        docker run -d -p 2717:27017 -v ~/UNWallet_metrics_db:/data/db --name unwallet_metrics_db mongo:latest

3. Now we're going to build the Dockerfile contained within the 'unwallet_metrics_ms' folder, for this you'll need to build the image using

        docker build -t unwallet_metrics_ms . 
 
4. We need to see the CONTAINER ID of our mongodb container, so we'll use the following command to see all the running containers:

        docker ps
        
5. Lastly you'll need to run the container image you just created through port 80:80 and linking it to the existing mongodb container using the container_id you just found:

        docker run --name unwallet_metrics_ms --link CONTAINER _ID:mongo -p 80:80 unwallet_metrics_ms


# Accesing the Service

1. The services can be found running on:

        http://localhost/docs

# Tests

- <a href="">Postman Collection</a></h5>

-- -
