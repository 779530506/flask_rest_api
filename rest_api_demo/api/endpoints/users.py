import logging
from flask import request,jsonify,make_response,current_app
from flask_restplus import Resource 
from api.restplus import api
from api.services.nifi_service import deletePipeline,createPipelineInDepartement
from api.services.user_repositorie import UsersRepositorie
from api.services.opensearch_service import OpenSearchClass
from werkzeug.security import generate_password_hash,check_password_hash
from api.serializers import user_register,user_show,user_login,username
import jwt
import datetime
log = logging.getLogger(__name__)

ns = api.namespace('users', description='Operations related to user')

@ns.route('/')
class UsersCollection(Resource):
    #@ns.route('/register',methods=['POST'])
    @api.response(201, 'user successfully created.')
    @api.expect(user_register)
    def post(self): 
        response={}
        data = request.get_json() 
        hashed_password = generate_password_hash(data['password'], method='sha256')
        
        openSearchClass = OpenSearchClass()
        res = openSearchClass.createUserwithRoleAndTenant(username= data["username"],password =data["password"])
        if not res:
            response["message"] =  "user not created "
            response["code"] =  400
            
        UsersRepositorie.createUser(email=data["email"],password=hashed_password,username=data["username"])        
        response["message"] =  "user created successfull"
        response["code"] =  201
        return {"response" : response }

    @api.marshal_with(user_show, envelope='resource')
    def get(self, **kwargs):
        return UsersRepositorie.getAllUsers()     
    @api.expect(username)
    def delete(self):
        data = request.json
        username = data['username']
        openSearchClass = OpenSearchClass()
        return openSearchClass.deleteUser(username)


@ns.route('/token')
class Token(Resource): 
    @api.expect(user_login)       
    def post(self):
        auth = request.get_json()
        username = auth['username']
        password = auth['password']
        if not auth or not username or not password: 
            return make_response('could not verify', 401, {'Authentication': 'login required"'})   
        user = UsersRepositorie.getUser(username=username)  
        if check_password_hash(user['password'], password):
            token = jwt.encode({'id' : user['id'],'username' : user['username'],
             'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=5)},
             current_app.config["SECRET_KEY"], "HS256")
        
            return jsonify({'token' : token})
        
        return make_response('User login incorrecte',  401, {'Authentication': '"login required"'})

   