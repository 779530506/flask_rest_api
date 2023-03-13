from opensearchpy import OpenSearch
import requests
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
class OpenSearchClass:




  def __init__(self):
    self.url="http://51.77.212.74:9200"
    self.username="admin"
    self.password="admin"
    self.auth=(self.username,self.password)
  def create_hospital_log_index_template (self,  pipeline_name,username):
    response={}
    pipeline_name = "log_hospital_index_of_"+username+"_"+pipeline_name
    payload={
      "index_patterns": [pipeline_name+"*"],
      "template": {
        "settings": {
          "number_of_shards": 2,
          "number_of_replicas": 1,
          "plugins.index_state_management.rollover_alias": pipeline_name
        },
        "mappings": {
          "properties": {
              "agent_timestamp": {
                "type": "date",
                "format": "strict_date_time||strict_date_optional_time||epoch_millis||strict_date_optional_time_nanos"
              },
              "location":{
                "type":"geo_point"
                } 
            }
          }
      }
    }
    response_get=requests.get(
      url="{}/_index_template/{}".format(self.url, pipeline_name) , auth=self.auth, verify=False
    )
    #Index Template does not exist
    if response_get.status_code==404:
      response_put=requests.put(
        url="{}/_index_template/{}".format(self.url, pipeline_name) ,json=payload,
        auth=self.auth, verify=False)
      if response_put.status_code in (200, 201):
        logger.info("The index template has been successfully created "+pipeline_name)
        response["message"] ="The index template has been successfully created "+pipeline_name
        response["code"] =1
      else:
        logger.error("Error while creating index with code" + str(response_put.status_code) + "and message error " + str(response_put.content))
        response["message"] ="The index template has not been correctly create "
        response["code"] =0

    elif response_get.status_code == 200:
      logger.info("The index template already exist " + pipeline_name)
      response["message"] ="The index template already exist "  + pipeline_name
      response["code"] =2
    else:
    
      logger.error("Error while creating index template  with code" + str(response_get.status_code) + "and message error " + str(response_get.content))
      response["message"] ="The index template has not been correctly create " + pipeline_name
      response["code"] =0
    return response
  # def createIndexTemplate(pipelinename):#pipelinename
  #     client = getClient()
  #     response = client.indices.put_template(pipelinename, {
  #     "template": pipelinename+"*",
  #     "order": 0,
  #     "settings": {
  #         "number_of_shards": 1
  #     },
  #     "mappings": {
  #       "properties": {
  #         "timestamp": {
  #           "type": "date",
  #           "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
  #         }
  #       }
  #      }
  #     })
  #     if response.get('acknowledged'):
  #         return True
  #     else:
  #         return False
      
  # def createIndex(pipeline_name):
  #     client = getClient()
  #     index_alias = pipeline_name
  #     index_name = pipeline_name+'-0001'
  #     index_body = {
  #       'settings': {
  #         'index': {
  #           'number_of_shards': 3
  #         },
            
  #       }
  #     }
  #     all_index = client.indices.get_alias().keys()
  #     if index_name  in all_index:
  #         client.indices.delete(index_name)
  #     response = client.indices.create(index_name, body=index_body)
  #     if response.get('acknowledged'):
  #         # on créé l'aliase
  #         client.indices.put_alias(index_name, index_alias)
  #         return True
          
  #     else:
  #         return False
  
  def create_hospital_log_alias (self,  pipeline_name,username):
    response = {}
    pipeline_name = "log_hospital_index_of_"+username+"_"+pipeline_name
    payload = {"aliases": {pipeline_name: {"is_write_index": True}}}
    response_get=requests.get(
            url="{}/{}".format(self.url, pipeline_name) , auth=self.auth, verify=False
    )
    #Alias does not exist
    if response_get.status_code==404:

      response_put=requests.put(url="{}/{}".format(self.url, pipeline_name+"_000001") ,json=payload,auth=self.auth, verify=False)

      if response_put.status_code in (200, 201):
        logger.info("The alias  has been successfully created "+pipeline_name)
        response["message"] ="The alias  has been successfully created "+pipeline_name
        response["code"] =1
      else:

        logger.error("Error while creating index with code" + str(response_put.status_code) + "and message error " + str(response_put.content))
        response["message"] ="The alias  not created "+pipeline_name
        response["code"] =0
            

    elif response_get.status_code == 200:
      logger.info("The alias  already exist " + pipeline_name)
      response["message"] ="The alias  already exist  "+pipeline_name
      response["code"] =2
    else:
      logger.error("Error creating index with code" + str(response_get.status_code) + "and message error " + str(response_get.content))
      response["message"] ="The index has not been correctly create "+pipeline_name
      response["code"] =0

    return response

  def create_storage_Opensearch(self,pipeline_name,username):
    self.create_hospital_log_index_template(pipeline_name,username)
    response = self.create_hospital_log_alias(pipeline_name,username)

    return response

  def create_tenant (self,  username):
    response ={}
    payload = {"description": "A tenant for the user".format(username)}

    #check  if the tenant exist
    url="{}/_opendistro/_security/api/tenants/{}".format(self.url, "tenant_for_"+username)
    response_get=requests.get(url=url , auth=self.auth, verify=False)
    #Alias does not exist
    if response_get.status_code==404:
      response_put=requests.put(
        url=url ,json=payload,
        auth=self.auth, verify=False)

      if response_put.status_code in (200, 201):
        logger.info("The tenant  has been successfully created " + username)
        response["message"] ="The tenant  has been successfully created " + username
        response["code"] =1
      else:
        logger.error("Error1 while creating tenant with code" + str(response_put.status_code) + "and message error " + str(response_put.content))
        response["message"] ="The tenant has not been correctly create " + username
        response["code"] =0
    elif response_get.status_code == 200:
      logger.info("The tenant  already exist " + username)
      response["message"] ="The tenant  already exist " + username
      response["code"] =2
    else:
      logger.error("Error creating tenant with code" + str(response_get.status_code) + "and message error " + str(response_get.content))
      response["message"] ="The tenant has not been correctly create " + username
      response["code"] =0
    
    return response

  def create_role (self,  username):
    response = {}
    payload ={
      "cluster_permissions": [],

      "index_permissions": [
        {
        "index_patterns": ["log_hospital_index_for_"+username+"_*"],
        "dls": "",
        "fls": [],
        "masked_fields": [],
        "allowed_actions": [ "read"]
        }
      ],
      "tenant_permissions": [
        {"tenant_patterns": ["tenant_for_"+username],
        "allowed_actions": ["kibana_all_read", "kibana_all_write"]
        }
      ]
      }

    #check  if the tenant exist
    url="{}/_opendistro/_security/api/roles/{}".format(self.url, "role_for_"+username)
    response_get=requests.get(url=url , auth=self.auth, verify=False)
    #Alias does not exist
    if response_get.status_code==404:
      response_put=requests.put(
            url=url ,json=payload,
            auth=self.auth, verify=False)
      if response_put.status_code in (200, 201):
        logger.info("The role  has been successfully created " + username)
        response["message"] ="The role  has been successfully created" + username
        response["code"] =1
      else:
        logger.error("Error1 while creating role with code" + str(response_put.status_code) + "and message error " + str(response_put.content))
        response["message"] ="The role has not been correctly create" + username
        response["code"] =0
    elif response_get.status_code == 200:
      logger.info("The role  already exist " + username)
      response["message"] ="The role  already exist" + username
      response["code"] =2
    else:
      logger.error("Error creating tenant with code" + str(response_get.status_code) + "and message error " + str(response_get.content))
      response["message"] ="The role  has not been correctly create"  
      response["code"] =0
    
    return response

  def create_user (self,  username, password):

    response ={}
    payload = {
      "password":password,
      "opendistro_security_roles": ["role_for_"+username, "dlq"],
      "attributes": {"username": username }
    }

    #check  if the tenant exist
    url="{}/_opendistro/_security/api/internalusers/{}".format(self.url, username)
    response_get=requests.get(url=url , auth=self.auth, verify=False)
    #Alias does not exist
    if response_get.status_code==404:
      response_put=requests.put(
        url=url ,json=payload,
        auth=self.auth, verify=False)

      if response_put.status_code in (200, 201):
        logger.info("The user  has been successfully created " + username)
        response["message"] ="The user  has been successfully created"  + username 
        response["code"] =1
      else:
        logger.error("Error while creating user  with code" + str(response_put.status_code) + "and message error " + str(response_put.content))
        response["message"] ="The user has not been correctly create "  + username 
        response["code"] =0

    elif response_get.status_code == 200:
      logger.info("The user  already exist " + username)
      response["message"] ="The user  already exist "  + username 
      response["code"] =2
    else:
      logger.error("Error creating user with code" + str(response_get.status_code) + "and message error " + str(response_get.content))
      response["message"] ="The tenant has not been correctly create "  + username 
      response["code"] =0

  def createUserwithRoleAndTenant(self,  username, password):
    if self.create_tenant(username)["code"] ==1:
      if self.create_role(username) ["code"] ==1:
        res = self.create_user(username,password) 
        return res
    else:
      return False

  def deleteUser (self,  username):
    response = {}
    url="{}/_opendistro/_security/api/internalusers/{}".format(self.url, username)
    response_delete=requests.delete(url=url , auth=self.auth, verify=False)
    if response_delete.status_code == 200:
      response["message"] =username+ " supprimé dans le serveur"  
      response["code"] =1
      return response
    if response_delete.status_code == 404:
      response["message"] =username+ " n'existe pas dans le serveur"  
      response["code"] =2
      return response
    else:
      return   False
    
