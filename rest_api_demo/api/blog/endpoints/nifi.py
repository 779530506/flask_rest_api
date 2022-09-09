import logging

from flask import request
from flask_restplus import Resource
from rest_api_demo.api.blog.business import create_category, delete_category, update_category
from rest_api_demo.api.blog.serializers import category, category_with_posts
from rest_api_demo.api.restplus import api
import pathlib
from rest_api_demo.api.blog.endpoints.services.nifi_service import check_current_user,deploy_template

log = logging.getLogger(__name__)

ns = api.namespace('nifi', description='Operations related to nifi')


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
    def post(self):
        """
        Creates a new blog category.
        """
        data = request.json
        template_dir ="~/template"
        # start up position
        origin_x = 661
        origin_y = -45

        # Make sure current user login is okay
        check_current_user()

        for template_file in pathlib.Path(template_dir).iterdir():
            if template_file.is_file():
                deploy_template(template_file, origin_x, origin_y)

        return None, 201


