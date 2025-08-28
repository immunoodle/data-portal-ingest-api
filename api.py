from flask import Flask, jsonify, request
from dotenv import load_dotenv
from celery import Celery
from input_validation import post_validator
import os
import json

load_dotenv()
app = Flask(__name__)

app_worker = Celery('app_worker',
                    broker=os.environ.get(
                        "TASK_BROKER", 'redis://redis:6379/0'),
                    backend=os.environ.get(
                        "TASK_BACKEND", 'redis://redis:6379/0'))

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/validate_payload', methods=["POST"])
def validate():
    app.logger.info("Validating data ")
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    # Convert JSON payload to a Python dictionary
    data_dict = json.loads(json.dumps(data))

    if not post_validator(data_dict):
        return jsonify({'result': 'invalid'}), 200
    
    return jsonify({'result': 'valid'}), 200

@app.route('/ingest_data', methods=["POST"])
def ingest():
    app.logger.info("Ingesting data ")
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    
    # Convert JSON payload to a Python dictionary
    data_dict = json.loads(json.dumps(data))

    if not post_validator(data_dict):
        return jsonify({'error': 'Request is missing required fields'}), 422
    
    r = app_worker.send_task('tasks.ingest_template', kwargs=data_dict)
    # app.logger.info(r.backend)
    return r.id


@app.route('/ingest_task_status/<task_id>')
def get_status(task_id):
    status = app_worker.AsyncResult(task_id, app=app_worker)
    return str(status.state)




