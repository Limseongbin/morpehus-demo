import json
import requests
import urllib3
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
## Global Static Variables
HOST = morpheus["morpheus"]["applianceHost"]
INTERNAL_HOST = morpheus["customOptions"]["internalHost"]
TOKEN = morpheus["morpheus"]["apiAccessToken"]
AWS_KEY = morpheus["customOptions"]["awsKey"]
AWS_SECRET = morpheus["customOptions"]["awsSecret"]
AWS_VPC = morpheus["customOptions"]["awsVpc"]
AWS_REGION = morpheus["customOptions"]["awsRegion"]
INTERNAL_URL = "https://%s" % (INTERNAL_HOST)
CLOUD_INIT_PASSWORD = "Password123?"
WINDOWS_PASSWORD = "Password123?"
 
## Variables
AMI_UBUNTU = morpheus["customOptions"]["amiubuntu"]
AMI_CENTOS = morpheus["customOptions"]["amicentos"]
 
## Request headers
HTTP_HEADERS = {"Content-Type":"application/json","Accept":"application/json","Authorization": "BEARER " + (TOKEN)}
HTTP_UPLOAD_HEADERS = {"Authorization": "BEARER " + (TOKEN)}
 
 
 
## Functions
def create_virtual_image(name, ostype, amiid):
    url = "https://%s/api/virtual-images" % (HOST)
    jbody = {
      "virtualImage": {
        "name": name,
        "osType": ostype,
        "minRamGB": 1,
        "isCloudInit": "on",
        "installAgent": "on",
        "externalId": amiid,
        "virtioSupported": "off",
        "vmToolsInstalled": "off",
        "isForceCustomization": "off",
        "trialVersion": "off",
        "isSysprep": "off",
        "isAutoJoinDomain": "off",
        "visibility": "private",
        "imageType": "ami"
      }
    }
  
    body = json.dumps(jbody)
 
    response = requests.post(url, headers=HTTP_HEADERS, data=body, verify=False)
    if not response.ok:
        print("Error creating virtual image: Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Request error occured")
    data = response.json()
    print("Virtual Image %s added" % (name))
 
 
 
def get_vi_id_by_name(vi_name):
    url = "https://%s/api/virtual-images" % (HOST)
 
    response = requests.get(url, headers=HTTP_HEADERS, verify=False)
    if not response.ok:
        raise Exception("Error getting virtual image '%s': Response code %s: %s" % (vi_name, response.status_code, response.text))
 
    data = response.json()
 
    for vi in data["virtualImages"]:
        if vi["name"] == vi_name:
            return vi["id"]
 
    raise Exception("Searched %s virtual images. Virtual image '%s' not found..." % (len(data["credentials"]), vi_name))
 
 
 
def create_node_type(name, shortname, version, viid):
    url = "https://%s/api/library/container-types" % (HOST)
    jbody = {
      "containerType": {
        "name": name,
        "shortName": shortname,
        "containerVersion": version,
        "provisionTypeCode": "amazon",
        "virtualImageId": viid,
        "statTypeCode": "amazon",
        "logTypeCode": "amazon",
        "serverType": "vm",
        "config": {
        }
      },
      "instanceType": {
        "backupType": "amazonSnapshot",
        "viewSet": "amazonCustom"
      }
    }
  
    body = json.dumps(jbody)
 
    response = requests.post(url, headers=HTTP_HEADERS, data=body, verify=False)
    if not response.ok:
        print("Error creating node type: Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Request error occured")
    data = response.json()
    print("Node Type %s added" % (name))
 
 
 
def get_node_type_id_name(ct_name):
    url = "https://%s/api/library/container-types" % (HOST)
 
    response = requests.get(url, headers=HTTP_HEADERS, verify=False)
    if not response.ok:
        raise Exception("Error getting node type '%s': Response code %s: %s" % (ct_name, response.status_code, response.text))
 
    data = response.json()
 
    for ct in data["containerTypes"]:
        if ct["name"] == ct_name:
            return ct["id"]
 
    raise Exception("Searched %s container types. Container type '%s' not found..." % (len(data["credentials"]), ct_name))
 
 
 
def create_instance_type(name, code):
    url = "https://%s/api/library" % (HOST)
    jbody = {
      "instanceType": {
        "name": name,
        "code": code,
        "category": "os",
        "visibility": "private"
      }
    }
  
    body = json.dumps(jbody)
 
    response = requests.post(url, headers=HTTP_HEADERS, data=body, verify=False)
    if not response.ok:
        print("Error creating instance type: Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Request error occured")
    data = response.json()
    print("Instance Type %s added" % (name))
 
 
 
def get_instance_type_id_name(it_name):
    url = "https://%s/api/library" % (HOST)
 
    response = requests.get(url, headers=HTTP_HEADERS, verify=False)
    if not response.ok:
        raise Exception("Error getting instance type '%s': Response code %s: %s" % (it_name, response.status_code, response.text))
 
    data = response.json()
 
    for it in data["instanceTypes"]:
        if it["name"] == it_name:
            return it["id"]
 
    raise Exception("Searched %s instances. Instance type '%s' not found..." % (len(data["instances"]), it_name))
 
 
 
def add_instance_logo(instance_id, name):
    url = "https://%s/api/library/instance-types/%s/update-logo" % (HOST, instance_id)
    files = {'logo': open(name, "rb")}
 
    response = requests.put(url, headers=HTTP_UPLOAD_HEADERS, files=files, verify=False)
 
    if not response.ok:
        print("Error adding logo: Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Request error occured")
 
    print("Logo %s added" % (name))
 
 
 
def create_layout(name, instance_id, container_id, workflow_id):
    url = "https://%s/api/library/%s/layouts" % (HOST, instance_id)
    jbody = {
      "instanceTypeLayout": {
        "name": name,
        "instanceVersion": "Latest",
        "creatable": True,
        "provisionTypeCode": "amazon",
        "memoryRequirement": "1024",
        "taskSetId": workflow_id,
        "optionTypes": [
    
        ],
        "containerTypes": [
          container_id
        ],
        "specTemplates": [
    
        ],
        "permissions": {
        }
      }
    }
  
    body = json.dumps(jbody)
 
    response = requests.post(url, headers=HTTP_HEADERS, data=body, verify=False)
    if not response.ok:
        print("Error creating layout: Response code %s: %s" % (response.status_code, response.text))
        raise Exception("Request error occured")
    data = response.json()
    print("Layout %s added" % (name))
 
 
 
 
 
 
 
## Main
## Create Virtual Images
create_virtual_image("AWS CentOS 7", "35", AMI_CENTOS)
create_virtual_image("AWS Ubuntu 20.04", "16", AMI_UBUNTU)
ubuntuvi = get_vi_id_by_name("AWS Ubuntu 20.04")
 
## Create Custom Ubuntu Instance
create_node_type("Custom Ubuntu 20.04 node","custUb2004node","20.04",ubuntuvi)
ubuntu_node_id = get_node_type_id_name("Custom Ubuntu 20.04 node")
create_instance_type("Custom Ubuntu", "customUbuntu")
instance_type_id = get_instance_type_id_name("Custom Ubuntu")
add_instance_logo(instance_type_id, "/ubuntu_logo.jpg")
create_layout("Custom Ubuntu Layout", instance_type_id, ubuntu_node_id, "")
 
## Module 3 - Create DBVAR Instance
create_instance_type("DBVAR", "dbVar")
instance_type_id = get_instance_type_id_name("DBVAR")
create_layout("DBVAR Layout", instance_type_id, ubuntu_node_id, "")
 
## Module 3 - Create APPVAR Instance
create_instance_type("APPVAR", "appVar")
instance_type_id = get_instance_type_id_name("APPVAR")
create_layout("APPVAR Layout", instance_type_id, ubuntu_node_id, "")
 
 
 
## JSON Server
create_file_template("option_lists/app.json", "provision", "App JSON", "app.json", "/opt/jsonserver", "root", "appjson", "App")
app_json_template_id = get_file_template_id_name("App JSON")
 
task_id1 = add_library_task("App JSON", "appJSON", app_json_template_id)
task_id2 = add_task("JSON Server Install", "jsonServerInstall", "1", "script", "on", "repository", repo_id, "/option_lists/json_server_install.sh", "resource")
 
workflow_id = add_workflow("JSON Server Install", task_id1, task_id2, "provision")
 
create_node_type("JSON server node","jsonServernode","Latest",ubuntuvi)
ubuntu_node_id = get_node_type_id_name("JSON server node")
create_instance_type("JSON Server", "jsonServer")
instance_type_id = get_instance_type_id_name("JSON Server")
add_instance_logo(instance_type_id, "/JSONImage.png")
 
create_layout("JSON Server Layout", instance_type_id, ubuntu_node_id, workflow_id)
CLOSE
