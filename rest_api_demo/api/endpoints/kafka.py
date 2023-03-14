import logging
from flask import request,jsonify
from flask_restplus import Resource
from api.restplus import api
from api.auth_middleware import token_required
from kafka import KafkaConsumer, KafkaProducer
import json
import settings

from api.serializers import kafka_cancer
log = logging.getLogger(__name__)

ns = api.namespace('kafka', description='Operations related to kafka')

@ns.route('/')
class KafkaCollection(Resource):
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.response(500, 'Erreur data  not push.')
    @api.response(201, 'data successfully pushed.')
    @api.expect(kafka_cancer)
    # creation pipeline
    #@token_required
    def post(self):
        """
        Push to kafka.
        """
        TOPIC_NAME = "Cancer_Multilayer_PerceptronSource_sarr"

        producer = KafkaProducer(
            bootstrap_servers = settings.KAFKA_BROKER_PORT,
        )
        # breakpoint()

        req = request.get_json()
        json_payload = json.dumps(req)
        json_payload = str.encode(json_payload)
        # push data into INFERENCE TOPIC
        
        print(json_payload)
        producer.send(TOPIC_NAME, json_payload)
        producer.flush()
        print("Sent to consumer")
        return jsonify({
            "message": "You will receive an email in a short while with the plot", 
            "status": "Pass"})
    
    