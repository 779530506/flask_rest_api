import logging
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.services.nifi_service import deletePipeline,createPipelineInDepartement
from api.serializers import nifi_delete_pipeline,nifi_deploy_pipeline
from api.auth_middleware import token_required
log = logging.getLogger(__name__)

ns = api.namespace('nifi', description='Operations related to nifi')

@ns.route('/')
class NifiCollection(Resource):

    @api.response(500, 'Erreur pipeline  not created.')
    @api.response(201, 'template successfully created.')
    @api.expect(nifi_deploy_pipeline)
    @token_required
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        
        try:            
            createPipelineInDepartement(name_hospital,name_dep,name_pipeline)
            return "pipeline created successfull", 201
        except Exception as e:
            return str(e), 500
    
    @api.response(204, 'pipeline successfully deleted.')
    @api.response(500, 'Erreur pipeline  not deleted.')
    @api.expect(nifi_delete_pipeline)
    @token_required
    def delete(self):
        """
        Deletes blog post.
        """
        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        try:
            deletePipeline(name_hospital,name_dep,name_pipeline)
            return "pipeline deleted successfull", 204
        except Exception as e:
            return str(e), 500



