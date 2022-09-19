from bdb import Breakpoint
from ensurepip import version
import requests
import json
import sys
import pathlib
import xml.etree.ElementTree as ET
import argparse
import os
from jinja2 import Template
import logging
# Get command args
# parser = argparse.ArgumentParser(description='Deploy templates to secured nifi cluster')
# parser.add_argument('--hostname', metavar='hostname', dest="hostname", type=str, required=True,
#                     help="nifi cluster hostname")
# parser.add_argument('--port', metavar='port', type=str, dest="port", required=True, help="nifi cluster ports")
# parser.add_argument('--template-dir', metavar='template dir', type=str, dest="template_dir", required=True,
#                     default="./template", help="the dir that contains nifi templates (default to ./template)")
# parser.add_argument('--cert-file', metavar='path to cert file', type=str, dest="cert_file", required=False,
#                     default="./certs/nifi.cer", help="the path to the cert file (default to ./certs/nifi.cer)")
# parser.add_argument('--username', metavar='username', type=str, dest="username", required=False,
#                     help="username to login to nifi cluster")
# parser.add_argument('--password', metavar='password', type=str, dest="password", required=True,
#                     help="password to login to nifi cluster")
# parser.add_argument('--delete-after-create', metavar='delete after create', type=str, dest="remove_after_create",
#                     required=False, default=True, help="Delete template after it has been instantiated")

#args = parser.parse_args()

log = logging.getLogger(__name__)
hostname = "51.77.212.74"
port = "8443"
template_dir = "/home/abdoulayesarr/template"
remove_after_create = "/me"
username = "admin"
password = "admin1234Thies"

cert_file = False

host_url = "https://" + hostname + ":" + port + "/nifi-api"

print("Host ip is {0} port is {1} and the host URL is {2}".format(hostname, port, host_url) )


def get_root_resource_id():
    # URL to get root process group information
    resource_url = host_url + "/flow/process-groups/226f892a-0183-1000-5a21-5986e4e6dd64"

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
def upload_template(template_file_name):
    upload_url = host_url + "/process-groups/" + get_root_resource_id() + "/templates/upload"
    print (upload_url)
    file_string = open(template_dir+ "/" + template_file_name, 'r').read()

    # using jinjia template

    #template = Template(file_string)
    # rendered= template.render(password=os.environ['es_password'])
    # multipart_form_data = {
    #   'template': rendered,
    # }

    multipart_form_data = {
      'template': file_string,
    }
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.post(upload_url, files=multipart_form_data, headers= auth_header, verify=cert_file, proxies={'https': ''})
    print (response)


# create an instance using the template id
def instantiate_template(dep_id,template_file_name, originX, originY):
    #create_instance_url = host_url + "/process-groups/" + get_root_resource_id() + "/template-instance"
    create_instance_url = host_url + "/process-groups/" + dep_id + "/template-instance"
    payload = {"templateId": get_template_id(template_file_name), "originX": originX, "originY": originY}
    originX = originX + 600
    originY = originY - 50
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.post(create_instance_url, json=payload, headers= auth_header, verify=cert_file, proxies={'https': ''})
    handle_error(create_instance_url, response)


# get list of templates that used for searching template id
def get_templates():
    get_template_instance_url = host_url + "/flow/templates"
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    response = requests.get(get_template_instance_url,  headers= auth_header, verify=cert_file, proxies={'https': ''})
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
        if get_template_name(template_dir + "/" + template_file_name) == template["template"]["name"]:
            print ("Creating instance of " + template["template"]["name"] + " ...")
    template_id = template["template"]["id"]
    return template_id


# removes a template from nifi cluster by its id.
def remove_template(template_id):
    
    if template_id != "":
        delete_template_url = host_url + "/templates/" + template_id
        auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
        response = requests.delete(delete_template_url, headers= auth_header, verify=cert_file, proxies={'https': ''})
        handle_error(delete_template_url, response)
    else:
        raise SystemError("Can not remove template without a template id")


# check current user session if any
def check_current_user():
    current_user_url = host_url + "/flow/current-user"
    auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
    print(current_user_url)
    res = requests.get(current_user_url, headers=auth_header, verify=cert_file, proxies={'https': ''})
    handle_error(current_user_url, res)


# get authentication token(JWT token) using username and password
def get_auth_token() -> str:
    auth_token_url = host_url + "/access/token"
    res = requests.post(auth_token_url, data={'username': username, 'password': password}, verify=cert_file, proxies={'https': ''})
    handle_error(auth_token_url, res)
    return res.text


# Check and raise exception for a given
def handle_error(endpoint, res):
    if not res.status_code == 200 and not res.status_code == 201:
        raise SystemError("Expect {0} call return either 200 or 401 but got status code {1} with response {2}".format(endpoint, res.status_code, res.text))


# deploys a template to nifi for a specified location
def deploy_template(dep_id,template_file, origin_x, origin_y):
    remove_template(get_template_id(template_file.name))
    upload_template(template_file.name)
    instantiate_template(dep_id,template_file.name, origin_x, origin_y)
    if remove_after_create == "true":
        remove_template(get_template_id(template_file.name))

def getHopitalByName(hospital_name):
    # URL to get root process group information
    resource_url = host_url + "/flow/process-groups/226f892a-0183-1000-5a21-5986e4e6dd64"

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
    resource_url = host_url + "/flow/process-groups/"+id_hospital

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
    resource_url = host_url + "/flow/process-groups/"+id_departement

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
        resource_url = host_url + "/process-groups/"+id_processor_group+"?clientId="+client_id+"&version="+str(version)
        auth_header = {'Authorization': 'Bearer ' + get_auth_token()}
        response = requests.delete(resource_url, headers=auth_header, verify=False, proxies={'https': ''})
        handle_error(resource_url, response)
        json = response.json()

        return json
    except Exception as e:
        raise Exception('impossible de suprimer un pipeline: %s'% str(e))

def createPipelineInDepartement(name_hopital,name_dep):
    template_dir ="/home/abdoulayesarr/template"
    # start up position
    origin_x = 661
    origin_y = -45

    # Make sure current user login is okay
    check_current_user()
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
    for template_file in pathlib.Path(template_dir).iterdir():
        if template_file.is_file():
            deploy_template(id_departement,template_file, origin_x, origin_y)

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
