from flask import Flask, request, jsonify
from flask_restx import Api, Resource, Namespace, reqparse
from werkzeug.datastructures import FileStorage
import uuid
import csv
import sys
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from io import StringIO
from handlers import logger as logging
from settings import APP_PORT
from db import save_task, get_task_result


app = Flask(__name__)
api = Api(app, 
          version="1.0", 
          title="Distance Calculator API",
          description="API for calcualte distance between coords and reverse geocoding.",
          prefix="/api",
          doc='/swagger')
ns = Namespace("v1", description="API version 1")

geolocator = Nominatim(user_agent="geocode_app_useragent")

upload_parser = reqparse.RequestParser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "csv"

@ns.route("/calculateDistances")
class CalculateDistances(Resource):
    @ns.expect(upload_parser)
    def post(self):
        if "file" not in request.files:
            logging.error("No file part in the request")
            return {"error": "No file part in the request"}, 400

        file = request.files["file"]
        if file.filename == "":
            logging.error("No file selected for uploading")
            return {"error": "No file selected for uploading"}, 400

        if not file or not allowed_file(file.filename):
            logging.error("Allowed file types are csv")
            return {"error": "Allowed file types are csv"}, 400

        stream = StringIO(file.read().decode("UTF-8"))
        task_id = str(uuid.uuid4())
        points = []

        csv_reader = csv.reader(stream, delimiter=",")
        next(csv_reader)

        for row in csv_reader:
            if len(row) != 3:
                continue
            try:
                points.append({
                    "name": row[0],
                    "latitude": float(row[1]),
                    "longitude": float(row[2])
                })
            except ValueError as e:
                logging.error(f"Error processing row {row}: {e}")
                continue

        if not points:
            logging.error("Invalid CSV format or no valid points found")
            return {"error": "Invalid CSV format or no valid points found"}, 400

        task = {"task_id": task_id, "status": "running", "points": points, "links": []}

        try:
            for i, point_a in enumerate(points):
                location = geolocator.reverse(f"{point_a['latitude']}, {point_a['longitude']}", exactly_one=True)
                point_a["address"] = location.raw.get("display_name", "Unknown address")
                for j, point_b in enumerate(points[i+1:], start=i+1):
                    distance = geodesic(
                        (point_a["latitude"], point_a["longitude"]),
                        (point_b["latitude"], point_b["longitude"])
                    ).meters
                    task["links"].append({
                        "name": f"{point_a['name']}{point_b['name']}",
                        "distance": round(distance, 2)
                    })
            save_task(task)
            task['status'] = "done"
            logging.info(f"Task {task_id} successfully processed")
        except Exception as e:
            logging.error(f"Failed to save task {task_id}: {e}")
            return {"error": "Failed to save task"}, 500

        return {"task_id": task_id, "status": task['status']}, 202


@ns.route("/getResult/<string:task_id>")
class GetResult(Resource):
    @ns.doc(params={"task_id": "Task UID"})
    def get(self, task_id):
        logging.info(f"Retrieving result for task ID: {task_id}")
        task = get_task_result(task_id)
        if task:
            logging.info(f"Task {task_id} found, returning result.")
            return task, 200
        else:
            logging.warning(f"Task {task_id} not found.")
            return {"error": "Task not found"}, 404


api.add_namespace(ns)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=APP_PORT)
