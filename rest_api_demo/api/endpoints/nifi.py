import logging
from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.services.nifi_service import deleteDep,createPipelineInDepartement
from api.serializers import nifi_delete_pipeline,nifi_deploy_pipeline

log = logging.getLogger(__name__)

ns = api.namespace('nifi', description='Operations related to nifi')

@ns.route('/')
class NifiCollection(Resource):

    @api.response(201, 'template successfully created.')
    @api.expect(nifi_deploy_pipeline)
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        createPipelineInDepartement(name_hospital,name_dep,name_pipeline)

        return None, 201
    
    @api.response(204, 'pipeline successfully deleted.')
    @api.expect(nifi_delete_pipeline)
    def delete(self):
        """
        Deletes blog post.
        """
        data = request.json
        name_hospital= data['name_hospital']
        name_dep = data['name_dep']
        name_pipeline = data['name_pipeline']
        deleteDep(name_hospital,name_dep,name_pipeline)
        return None, 204


