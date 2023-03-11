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

kafka_cancer = api.model('Push data', {
    'lat': fields.Float(required=True),
    'lon': fields.Float(required=True),
    'nom': fields.String(required=True),
    'prenom': fields.String(required=True),
    'dateNaiss': fields.String(required=True),
    'ville': fields.String(required=True),
    'thickness': fields.Float(required=True),
    'size': fields.Float(required=True),
    'shape': fields.Float(required=True),
    'madh': fields.Float(required=True),
    'epsize': fields.Float(required=True),
    'bnuc': fields.Float(required=True),
    'bchrom': fields.Float(required=True),
    'nNuc': fields.Float(required=True),
    'mit': fields.Float(required=True),
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