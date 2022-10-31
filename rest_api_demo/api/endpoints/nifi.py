import logging
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.services.nifi_service import deletePipeline,createPipelineInDepartement,run_pipeline,stop_pipeline
from api.serializers import nifi_delete_pipeline,nifi_deploy_pipeline
from api.auth_middleware import token_required
log = logging.getLogger(__name__)

ns = api.namespace('nifi', description='Operations related to nifi')

@ns.route('/')
class NifiCollection(Resource):
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    @api.response(500, 'Erreur pipeline  not created.')
    @api.response(201, 'template successfully created.')
    @api.expect(nifi_deploy_pipeline)
    #@token_required
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        response = {}
        try:            
            createPipelineInDepartement(name_hospital,name_dep,name_pipeline)
            response["message"] =  "pipeline created successfull"
            response["code"] =  201
            return {"response" : response }
        except Exception as e:
            response["message"] =  "Erreur pipeline not created "
            response["code"] =  500
            response["error"] =  str(e)
            return {"response" : response }
    
    @api.response(204, 'pipeline successfully deleted.')
    @api.response(500, 'Erreur pipeline  not deleted.')
    @api.expect(nifi_delete_pipeline)
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
    #@token_required
    def delete(self):
        """
        Deletes blog post.
        """
        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        response ={}
        try:
            deletePipeline(name_hospital,name_dep,name_pipeline)
            #return "pipeline deleted successfull", 204
            response["message"] =  "pipeline deleted successfull"
            response["code"] =  204
        except Exception as e:
            response["message"] =  "Erreur! pipeline not deleted, check if pipeline exist "
            response["code"] =  500
        return {"response" : response }


@ns.route('/pipeline_run')
class PipelineRun(Resource):
    @api.response(200, 'pipeline successfully run.')
    @api.response(500, 'Erreur pipeline  not running.')
    @api.expect(nifi_delete_pipeline)
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
  #  @token_required
    def post(self):

        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        response = {}
        try:
            run_pipeline(name_hospital,name_dep,name_pipeline)
            response["message"] =  "pipeline started successfull"
            response["code"] =  200
            return {"response" : response },200
        except Exception as e:
            response["message"] =  "Error, pipeline not started "
            response["code"] =  500
            return {"response" : response },500

@ns.route('/pipeline_stop')
class PipelineStop(Resource):
    @api.response(200, 'pipeline successfully stop.')
    @api.response(500, 'Erreur pipeline  not stop.')
    @api.expect(nifi_delete_pipeline)
    @api.doc(params={'Authorization': {'in': 'header', 'description': 'An authorization token'}})
   # @token_required
    def post(self):

        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        response ={}
        try:
            stop_pipeline(name_hospital,name_dep,name_pipeline)
            response["message"] =  "pipeline stopped successfull"
            response["code"] =  200
            return {"response" : response },200
        except Exception as e:
            response["message"] =  "Error, pipeline not stopped "
            response["code"] =  500
            return {"response" : response },500




