from bdb import Breakpoint
from ensurepip import version
from symbol import parameters
import requests
import json
import sys
import pathlib
import xml.etree.ElementTree as ET
import argparse
import os
from jinja2 import Template
import logging
from rest_api_demo import settings

        

log = logging.getLogger(__name__)




def get_root_resource_id():
    # URL to get root process group information
    resource_url = settings.HOST_URL + "/flow/process-groups/c2fc4b9b-3395-1c76-bea7-6d27e5170942"

    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.get(resource_url, headers=auth_header, verify=False, proxies={'https': ''})

    if not response.status_code == 200:
        print(response)
        print(response.content)
    json = response.json()
    resource_id = json["processGroupFlow"]["id"]
    print(resource_id)
    return resource_id


# print out the name of the template
def get_template_name(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return root[2].text


# upload the template from local to remote nifi cluster
def upload_template(template_file_name,params):
    upload_url = settings.HOST_URL + "/process-groups/" + get_root_resource_id() + "/templates/upload"
    print (upload_url)
    file_string = open(settings.TEMPLATE_DIR+ "" + template_file_name, 'r').read().replace('TEMPLATE_PIPELINE',params["name_pipeline"])
    file_string=file_string.replace('KAFKA_TOPIC_NAME',params["KAFKA_TOPIC_NAME"])
    file_string=file_string.replace('ELASTIC_URL_PORT', settings.ELASTIC_URL_PORT)
    file_string=file_string.replace('ELASTIC_PASSWORD', settings.ELASTIC_PASSWORD)
    file_string=file_string.replace('ELASTIC_USERNAME', settings.ELASTIC_USERNAME)
    file_string=file_string.replace('JSON_RECORD_READER', settings.JSON_RECORD_READER)
    file_string=file_string.replace('JSON_RECORD_WRITER', settings.JSON_RECORD_WRITER)
    file_string=file_string.replace('KAFKA_BROKER_PORT', settings.KAFKA_BROKER_PORT)
    file_string=file_string.replace('KAFKA_Group_ID_NAME', params["KAFKA_Group_ID_NAME"])
    file_string=file_string.replace('ELASTIC_INDEX_NAME',params["ELASTIC_INDEX_NAME"])
    file_string=file_string.replace('DLQ_KAFKA_TOPIC', settings.DLQ_KAFKA_TOPIC)
    
  

    multipart_form_data = {
      'template': file_string,
    }
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.post(upload_url, files=multipart_form_data, headers= auth_header, verify=settings.CERT_FILE, proxies={'https': ''})
    print (response)


# create an instance using the template id
def instantiate_template(dep_id,template_file_name, originX, originY):
    #create_instance_url = settings.HOST_URL + "/process-groups/" + get_root_resource_id() + "/template-instance"
    create_instance_url = settings.HOST_URL + "/process-groups/" + dep_id + "/template-instance"
    payload = {"templateId": get_template_id(template_file_name), "originX": originX, "originY": originY}
    originX = originX + 600
    originY = originY - 50
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.post(create_instance_url, json=payload, headers= auth_header, verify=settings.CERT_FILE, proxies={'https': ''})
    handle_error(create_instance_url, response)


# get list of templates that used for searching template id
def get_templates():
    get_template_instance_url = settings.HOST_URL + "/flow/templates"
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.get(get_template_instance_url,  headers= auth_header, verify=settings.CERT_FILE, proxies={'https': ''})
    handle_error(get_template_instance_url, response)
    json = response.json()
    templates = json["templates"]
    return templates


# get the id of the template that matches the name of the saved template
def get_template_id(template_file_name):
    templates = get_templates()
    template_id = ""
    for template in templates:
        print(template)
        
        print(template_file_name)
        if get_template_name(settings.TEMPLATE_DIR + "/" + template_file_name) == template["template"]["name"]:
            print ("Creating instance of " + template["template"]["name"] + " ...")
    template_id = template["template"]["id"]
    return template_id


# removes a template from nifi cluster by its id.
def remove_template(template_id):
    
    if template_id != "":
        delete_template_url = settings.HOST_URL + "/templates/" + template_id
        auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
        response = requests.delete(delete_template_url, headers= auth_header, verify=settings.CERT_FILE, proxies={'https': ''})
        handle_error(delete_template_url, response)
    else:
        raise SystemError("Can not remove template without a template id")


# check current user session if any
def check_current_user():
    current_user_url = settings.HOST_URL + "/flow/current-user"
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    print(current_user_url)
    res = requests.get(current_user_url, headers=auth_header, verify=settings.CERT_FILE, proxies={'https': ''})
    handle_error(current_user_url, res)


# get authentication token(JWT token) using settings.USERNAME_NIFI and password
def get_auth_token() -> str:
    auth_token_url = settings.HOST_URL + "/access/token"
    res = requests.post(auth_token_url, data={'username': settings.USERNAME_NIFI, 'password': settings.PASSWORD_NIFI}, verify=settings.CERT_FILE, proxies={'https': ''})
    handle_error(auth_token_url, res)
    return res.text


# Check and raise exception for a given
def handle_error(endpoint, res):
    if not res.status_code == 200 and not res.status_code == 201:
        raise SystemError("Expect {0} call return either 200 or 401 but got status code {1} with response {2}".format(endpoint, res.status_code, res.text))


# deploys a template to nifi for a specified location
def deploy_template(dep_id,template_file, params ):
    # start up position
    origin_x = 661
    origin_y = -45
    remove_template(get_template_id(template_file.name))
    upload_template(template_file.name,params)
    instantiate_template(dep_id,template_file.name, origin_x, origin_y)
    if settings.REMOVE_AFTER_CREATE == "true":
        remove_template(get_template_id(template_file.name))

def getHopitalByName(hospital_name):
    # URL to get root process group information
    resource_url = settings.HOST_URL + "/flow/process-groups/c2fc4b9b-3395-1c76-bea7-6d27e5170942"

    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.get(resource_url, headers=auth_header, verify=False, proxies={'https': ''})


    json = response.json()
    id_pg=[pg["component"]["id"] for pg in json["processGroupFlow"]["flow"]["processGroups"] if pg["component"]["name"]==hospital_name]
    
    if len(id_pg)>0:
        return id_pg[0]
    else:
        return ""
def getDepHopitalByName(id_hospital,name_deparetement):
    # URL to get root process group information
    resource_url = settings.HOST_URL + "/flow/process-groups/"+id_hospital

    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.get(resource_url, headers=auth_header, verify=False, proxies={'https': ''})


    json = response.json()
    id_pg=[pg["component"]["id"] for pg in json["processGroupFlow"]["flow"]["processGroups"] if pg["component"]["name"]==name_deparetement]
    
    if len(id_pg)>0:
        return id_pg[0]
    else:
        return ""

def getPipelineDepByName(id_departement,name_pipeline):
    # URL to get root process group information
    resource_url = settings.HOST_URL + "/flow/process-groups/"+id_departement

    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.get(resource_url, headers=auth_header, verify=False, proxies={'https': ''})


    json = response.json()
    info_pg=[{"id":pg["component"]["id"],"revision":pg["revision"]} for pg in json["processGroupFlow"]["flow"]["processGroups"] if pg["component"]["name"]==name_pipeline]
    
    if len(info_pg)>0:
        return info_pg[0]
    else:
        return ""

def deleteDep(name_hopital,name_dep,name_pipeline):
    
    try:
        id_hopital = getHopitalByName(name_hopital)
    except Exception as e :
        log.error('Error de recupération hopital: %s'%str(e))
        raise Exception('Error de recupération hopital: %s'%str(e))

    try: 
        id_departement= getDepHopitalByName(id_hopital,name_dep)
    except Exception as e :
        log.error('Error de recupération departement: %s'%str(e))
        raise Exception('Error de recupération departement: %s'%str(e))
    try: 
        info_processor= getPipelineDepByName(id_departement,name_pipeline)
        client_id = info_processor["revision"]["clientId"]
        id_processor_group = info_processor["id"]
        version = info_processor["revision"]["version"]
    except Exception as e :
        log.error('Error de recupération pipeline: %s'%str(e))
        raise Exception('Error de recupération pipeline: %s'%str(e))
    
    
    try:
        resource_url = settings.HOST_URL + "/process-groups/"+id_processor_group+"?clientId="+client_id+"&version="+str(version)
        auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
        response = requests.delete(resource_url, headers=auth_header, verify=False, proxies={'https': ''})
        handle_error(resource_url, response)
        json = response.json()

        return json
    except Exception as e:
        raise Exception('impossible de suprimer un pipeline: %s'% str(e))

def createPipelineInDepartement(name_hopital,name_dep,name_pipeline):
   
    KAFKA_Group_ID_NAME = '_'.join(["elastic",name_hopital,name_dep,name_pipeline])
    KAFKA_TOPIC_NAME    = '_'.join([name_hopital,name_dep,name_pipeline])
    ELASTIC_INDEX_NAME = '_'.join([name_hopital,name_dep,name_pipeline])
    params = {
        'KAFKA_Group_ID_NAME' : KAFKA_Group_ID_NAME,
        'KAFKA_TOPIC_NAME': KAFKA_TOPIC_NAME,
        'name_pipeline': name_pipeline,
        'ELASTIC_INDEX_NAME': ELASTIC_INDEX_NAME 
        }
    # Make sure current user login is okay
    check_current_user()
    try:
        id_hopital = getHopitalByName(name_hopital)
    except Exception as e :
        log.error('Error de recupération hopital: %s'%str(e))
        return 'Error de recupération hopital: %s'% str(e)
    try: 
        id_departement= getDepHopitalByName(id_hopital,name_dep)
    except Exception as e :
        log.error('Error de recupération departement: %s'%str(e))
        raise Exception('Error de recupération departement: %s'%str(e))
    for template_file in pathlib.Path(settings.TEMPLATE_DIR).iterdir():
        if template_file.is_file():
            deploy_template(id_departement,template_file,params )

# # main function starts here
# def main():

#     # start up position
#     origin_x = 661
#     origin_y = -45

#     # Make sure current user login is okay
#     check_current_user()

#     for template_file in pathlib.Path(template_dir).iterdir():
#         if template_file.is_file():
#             deploy_template(template_file, origin_x, origin_y)


# if __name__ == "__main__":
#     main()
