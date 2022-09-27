from api.restplus import api
from flask_restplus import fields




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