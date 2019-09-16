from .__init__ import *
from .hostManager import *
from jsonschema import validate
from bson.json_util import dumps
import pymongo
import requests
import os
import paramiko
import bcrypt

genID_schema = {
    "type" : "object",
    "properties" : {
        "genID" : {"type" : "array"},
    },
    "required": ["genID"]
}

descr_schema = {
    "type" : "object",
    "properties" : {
        "description" : {"type" : "string"},
    },
    "required": ["description"]
}

@method_decorator([login_required], name='dispatch')
class LandAddExperiment(View):
    def get(self, request):
        return render(request, 'repoIndex/addExperiment.html')

@method_decorator([login_required], name='dispatch')
class LandQueryExperimentType(View):
    def get(self, request):
        exp_types = db.experiment_types.find({},{"_id":0}).sort("Name",pymongo.ASCENDING)
        print('exp_types is:',exp_types)
        return render(request, 'repoIndex/queryExperimentType.html',{'exp_types': exp_types})

@method_decorator([login_required], name='dispatch')
class LandQueryExperiment(View):
    def get(self, request):
        return render(request, 'repoIndex/queryExperiment.html')

@method_decorator([login_required], name='dispatch')
class LandNewExperimentType(View):
    def get(self, request):
        return render(request, 'repoIndex/newExperimentType.html')

@method_decorator([login_required], name='dispatch')
class LandValidateGenID(View):
    def get(self, request):
        return render(request, 'repoIndex/validateGenID.html')

def validateJSONschema(json_file,schema):
    try:
        data = json.loads(json_file)
        validate(instance=data, schema=schema)
        print("JSON valid")
        return (data)
    except Exception as e:
        err_msg = "Error in validating JSON schema: " + str(e)
        # print(err_msg)
        return (err_msg)

def wrapvalidateJSONschema(json_file,schema,request):
    try:
        schema_valid = validateJSONschema(json_file,schema)
        if schema_valid != "OK":
            print(schema_valid)
            return RedirectIfWrong(request,'repoIndex/errorUploading.html',{'error_string': str(schema_valid)})
        return "OK"
    except Exception as e:
        err_msg = "Error in JSON schema validation function"
        print(err_msg)
        return RedirectIfWrong(request,'repoIndex/errorUploading.html',{'error_string': str(err_msg)})

def validateGenID(genID_list):
    try:
        print("Entered GenID validation")
        # print("genid list is:", genID_list)
        genIDs = json.dumps(genID_list)
        # print(genIDs)
        req_list=[]
        params = {'parameters': '[{"values": '+genIDs+', "id": 0}]', 'template_id': 10}
        # print(params)
        r = requests.post('https://las.ircc.it/mdam/api/runtemplate/', data=params, verify=False)
        resp = json.loads(r.text)

        for el in resp['body']:
            # print("genID:",el[0])
            req_list.append(el[0])
        # print("req_list is:", req_list)
        diff = set(genID_list).symmetric_difference(set(req_list))
        # diff = [x for x in set(genID_list) if x not in set(req_list)]
        print("diff is:", len(diff))
        if len(diff) == 0:
            return ("OK")
        else:
            return (diff)
    except Exception as e:
        print ('Error validateGenID', e)
        return ("X")

@method_decorator([login_required], name='dispatch')
class AddExperiment(View):
    def post(self, request):
        try:
            print("entered AddExperiment")
            # print("request is: ",request.POST)
            print("request genID file is: ",request.FILES['exp_genID-file'])
            print("request descr file is: ",request.FILES['exp_descr-file'])

            hostname = request.POST['hostname']
            exp_name = request.POST['exp_name']
            exp_type = request.POST['exp_type']
            pipeline = request.POST['pipeline']

            wb_genID = request.FILES['exp_genID-file'].read()
            # print(wb_genID)
            # data_genID = json.loads(wb_genID)
            # print(data_genID)
            data_genID = validateJSONschema(wb_genID,genID_schema)
            print("schema_valid of genID file = OK")
            if "Error" in data_genID:
                print(data_genID)
                return render(request,'repoIndex/errorUploading.html',{'error_string': data_genID})
            
            wb_descr = request.FILES['exp_descr-file'].read()
            # print(wb_descr)
            # data_descr = json.loads(wb_descr)
            # print(data_descr)
            data_descr = validateJSONschema(wb_descr,descr_schema)
            print("schema_valid of description file = OK")
            if "Error" in data_descr:
                print(data_descr)
                return render(request,'repoIndex/errorUploading.html',{'error_string': data_descr})

            valid = validateGenID(data_genID['genID'])
            print("valid is:", valid)

            if valid == "OK":
                new_exp = db.experiments.update_one(
                    { 'exp_name': exp_name },
                    {"$setOnInsert":{
                        'exp_name': exp_name,
                        'genID': data_genID['genID'],
                        'exp_type': exp_type,
                        'pipeline': pipeline,
                        'description': data_descr['description']
                        }
                    },
                    upsert = True
                    )
                
                exp_objID = new_exp.upserted_id
                print("new_exp is:", exp_objID)

                # key = getattr(settings, "SECRET_KEY", None)
                # print("key is ", key)

                doc = db.hosts.find_one({'hostname' : hostname}, {'description' :0, '_id': 0})
                print("doc is: ",doc)
                username = doc['host_username']
                password = doc['host_password']
                path = doc['host_path']
                # print("inserted_host is:", inserted_host['host_path'])

                # TODO put Fernet encr and decr in separate fcts
                key = b'n_jrI9S9ivI9iYQDEfVPqfntsxFyfSBp8375JFvIsxM='
                print("K:",key)
                f = Fernet(key)
                print("F:",f)
                encrypted_pw = password
                decrypted_pw = f.decrypt(encrypted_pw)
                print("ENC",encrypted_pw)

                # print(username['host_username'])
                # print(password['host_password'])
                # print(path['host_path'])

                conn_test = testConnection(hostname,username,decrypted_pw,path)
                print("conn_test is: ", conn_test)
                if conn_test != "OK":
                    print(conn_test)
                    return render(request, 'repoIndex/errorUploading.html',{'error_string': conn_test})


                # TODO put in a fct------------------
                ssh = paramiko.SSHClient() 
                host_exist = socket.gethostbyname(hostname)
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, username=username, password=decrypted_pw)
                command="cd " + path + "; mkdir " + str(exp_objID) #add put file
                # touch filename.json; echo str_file_content >> filename.json
                print("executing ",command)
                stdin , stdout, stderr = ssh.exec_command(command)
                print(stdout.read())
                # sftp = ssh.open_sftp()
                # sftp.put(localpath, path)
                # sftp.close()
                ssh.close()
                # --------------------------
            

                exp_path = username+"@"+hostname+path+"/"+str(exp_objID)
                print("exp_path is:", exp_path)

                db.experiments.update({'_id': exp_objID}, {"$set": {'path': exp_path}})

                return render(request, 'repoIndex/endExperiment.html',{'new_exp': new_exp})
            elif valid == "X":
                error_string = "An error occurred in genID validation stage"
                # return render(request, 'repoIndex/errorUploading.html',{'exp_types': exp_types})
                print(error_string)
            else:
                error_string = "Sorry but the following GenIDs are not in the LAS database: \n"
                print(error_string)
                return render(request, 'repoIndex/errorUploading.html',{'error_string': error_string, 'valid': valid})

        except Exception as e:
            print ('Error AddExperiment', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class QueryExperimentType(View):
    def get(self, request):
        try:
            print("entered QueryExperimentType")
            return render(request, 'repoIndex/queryExperimentType.html')
        except Exception as e:
            print ('Error QueryExperimentType', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class NewExperimentType(View):
    def post(self, request):
        try:
            print("entered NewExperimentType")

            print("exp_type_name = ",request.POST['exp_type_name'])
            print("exp_type_description = ",request.POST['exp_type_description'])

            exp_type_name = request.POST['exp_type_name']
            exp_type_description = request.POST['exp_type_description']

            existing_types = db.experiment_types.find_one({'Name' : exp_type_name},{"_id":0})

            if existing_types:
                existing_name = existing_types['Name']
                existing_desc = existing_types['Description']
                print("exist name", existing_name)
                print("exist desc", existing_desc)
                error_string = "Sorry but type \""+exp_type_name+"\" already exists. \n Name: "+existing_name+"\n Description: "+existing_desc
                print(error_string)
                return render(request, 'repoIndex/errorNewExperimentType.html',{'error_string': error_string})
            
            new_exp_type = db.experiment_types.update_one(
                    { 'Name': exp_type_name },
                    {"$setOnInsert":{
                        'Name': exp_type_name,
                        'Description': exp_type_description,
                        }
                    },
                    upsert = True
                    )
                
            inserted_type = db.experiment_types.find_one({'Name' : exp_type_name})
            print("inserted_type is:", inserted_type)

            return render(request, 'repoIndex/endNewExperimentType.html',{'inserted_type': inserted_type}) #TODO fix this

        except Exception as e:
            print ('Error NewExperimentType', e)
            return redirect('/')


@method_decorator([login_required], name='dispatch')
class QueryExperiment(View):
    def post(self, request):
        try:
            print("entered QueryExperiment")
            # print("request is: ",request.POST)

            print("exp_name = ",request.POST['exp_name'])
            print("genID = ",request.POST['genID'])
            print("exp_type = ",request.POST['exp_type'])
            print("pipeline = ",request.POST['pipeline'])
            print("path = ",request.POST['path'])
            print("description = ",request.POST['description'])

            exp_name = request.POST['exp_name']
            exp_genID = request.POST['genID']
            exp_type = request.POST['exp_type']
            pipeline = request.POST['pipeline']
            exp_path = request.POST['path']
            description = request.POST['description']

            if exp_genID != "":
                genID = exp_genID.split("\r\n")
                print("genId is:",genID)
                print("len genid:", len(genID))
            else:
                genID = ""

            query = {}
            if exp_name != "":
                # query['exp_name'] = { '$eq': exp_name }
                query['exp_name'] = { '$regex' : ".*"+exp_name+".*" }
            if genID != "":
                query['genID'] = { '$in': genID }
            if exp_type != "":
                # query['exp_type'] = { '$eq': exp_type }
                query['exp_type'] = { '$regex' : ".*"+exp_type+".*" }
            if exp_path != "":
                query['path'] = { '$regex' : ".*"+exp_path+".*" }
            if pipeline != "":
                # query['pipeline'] = { '$eq': pipeline }
                query['pipeline'] = { '$regex' : ".*"+pipeline+".*" }
            if description != "":
                query['description'] = { '$regex' : ".*"+description+".*" }

            #add filters by user

            print("query is:", query)
            results = list(db.experiments.find(query,{"_id":0}).sort("exp_name",pymongo.ASCENDING))
            for doc in results:
                print(doc)

            # exp_types=db.experiment_types.find({},{"_id":0}).sort("Name",pymongo.ASCENDING)
            # print('exp_types is:',exp_types)
            # return render(request, 'repoIndex/queryExperimentType.html',{'exp_types': exp_types})

            return render(request, 'repoIndex/endQueryExperiment.html',{'results': results})
        except Exception as e:
            print ('Error QueryExperiment', e)
            return redirect('/')

