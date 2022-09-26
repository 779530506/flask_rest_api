import logging

from flask import request
from flask_restplus import Resource,reqparse
from rest_api_demo.api.restplus import api
import pathlib
from rest_api_demo.api.services.nifi_service import deleteDep,createPipelineInDepartement
from flask_restplus import fields

log = logging.getLogger(__name__)

ns = api.namespace('nifi', description='Operations related to nifi')


nifi_delete_pipeline = api.model('Delete pipeline', {
    'name_hospital': fields.String(required=True),
    'name_dep': fields.String(required=True),
    'name_pipeline': fields.String(required=True),
})
nifi_deploy_pipeline = api.model('Deploy pipeline', {
    'name_hospital': fields.String(required=True),
    'name_dep': fields.String(required=True),
    'name_pipeline': fields.String(required=True)
})


@ns.route('/')
class NifiCollection(Resource):

    # @api.marshal_list_with(category)
    # def get(self):
    #     """
    #     Returns list of blog categories.
    #     """
    #     categories = Category.query.all()
    #     return categories

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
        #breakpoint()
        deleteDep(name_hospital,name_dep,name_pipeline)
        return None, 204


