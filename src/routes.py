import multiprocessing
import os
import asyncio
from temporalio import workflow
from main import runner
import logging
with workflow.unsafe.imports_passed_through():
    from flask import Flask, Blueprint, jsonify, request

# Obtain a module-specific logger
logger = logging.getLogger(__name__)
main = Blueprint('main', __name__)

@main.route('/sentiment', methods=['GET'])
def sentiment():
    item = request.args.get('item')
    logger.info("Running analysis on new item: %s" % item)
    result, verdict = asyncio.run( runner(item) )
    response = {
        'item': item,
        'result': result,
        'verdict': verdict
    }
    return jsonify(response)

@main.route('/')
def home():
    return 'Hello, Temporal!'

class CFWorker(multiprocessing.Process):
    def __init__(self, port=None):
        super().__init__()
        self.port = port or int(os.getenv('PORT', 5000))

    def run(self):
        app = Flask(__name__)
        app.register_blueprint(main)
        app.run(host='0.0.0.0', port=self.port)