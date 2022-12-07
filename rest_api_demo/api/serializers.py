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
    'name_pipeline': fields.String(required=True),
    'username': fields.String(required=True)
})

user_register = api.model('User register ', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
})
user_show = api.model('User register ', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
})
user_login = api.model('User register ', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'email': fields.String(required=True),
})

username = api.model('User register ', {
    'username': fields.String(required=True),
})