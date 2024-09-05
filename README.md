
# Distance Calculator API

### Introduction
This Distance Calculator API is a Flask-based RESTful service designed to calculate distances between multiple geographic locations using latitude and longitude values. The service provides endpoints for uploading location data via CSV files and retrieving calculated distances and human-readable addresses for each point.

###Requirements
- Docker
- Docker-compose

### Installation and Setup
Before running the service, ensure you have Docker and Docker-compose installed on your system. Clone the repository and configure the service using the provided `.env_dev` file for development environments.

### Clone the Repository
```bash
git clone git@github.com:Egorich42/coordinate_calculator.git
cd coordinate_calculator
```

###Environment Configuration


Fill .env_dev with your values or leave the defaults.

### Running the Service
To build and run the service on your local machine, execute:
```
docker-compose --env-file .env_dev build
docker-compose --env-file .env_dev up
```
Alternatively, you can build and run the service with a single command:
```
docker-compose --env-file .env_dev up --build
```

### API Endpoints
Access the Swagger UI to interact with the API at:
```
http://localhost:8080/swagger
```

#### Calculate Distances

`POST /api/v1/calculateDistances`

Uploads a CSV file containing point locations and calculates distances between them. The CSV file should have the following structure:

    Point (Name)
    Latitude
    Longitude

EXAMPLE FILE exists in current repo - `test_points.csv`

Example with cURL:
```
curl -F 'file=@path_to_your_file/test_points.csv' http://localhost:8080/api/v1/calculateDistances
```


#### Get Task Result

`GET /api/v1/getResult/<task_id>`

Retrieves the result of a previously submitted task.

Example with cURL:
```
curl http://localhost:8080/api/v1/getResult/1a581688-bb78-489b-8ca7-2ee62cc80836
```

### Running Tests

To run tests, use the following command:

```
docker-compose --env-file .env_dev build
docker-compose --env-file .env_dev run tests
```

### Shutting Down the Service
```
docker-compose --env-file .env_dev down
```
Or, if you want to remove local volumes:
```
docker-compose --env-file .env_dev down --volumes --remove-orphans --rmi local
```