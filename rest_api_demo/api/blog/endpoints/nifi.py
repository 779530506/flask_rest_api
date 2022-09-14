import logging

from flask import request
from flask_restplus import Resource,reqparse
from rest_api_demo.api.blog.business import create_category, delete_category, update_category
from rest_api_demo.api.blog.serializers import category, category_with_posts
from rest_api_demo.api.restplus import api
import pathlib
from rest_api_demo.api.blog.endpoints.services.nifi_service import deleteDep,check_current_user,deploy_template
from flask_restplus import fields

log = logging.getLogger(__name__)

ns = api.namespace('nifi', description='Operations related to nifi')


nifi_delete_pipeline = api.model('Delete pipeline', {
    'name_hospital': fields.String(required=True),
    'name_dep': fields.String(required=True),
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
    @api.expect(category)
    def post(self,name):
        """
        Creates a new blog category.
        """
        data = request.json
        template_dir ="/home/abdoulayesarr/template"
        # start up position
        origin_x = 661
        origin_y = -45

        # Make sure current user login is okay
        check_current_user()

        for template_file in pathlib.Path(template_dir).iterdir():
            if template_file.is_file():
                deploy_template(template_file, origin_x, origin_y)

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
        #breakpoint()
        deleteDep(name_hospital,name_dep)
        return None, 204


