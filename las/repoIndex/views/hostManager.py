from .__init__ import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from django.http import JsonResponse
import pymongo
from pymongo.collection import ReturnDocument
import requests
import os
import paramiko
import socket
import bcrypt
import base64

key = b'n_jrI9S9ivI9iYQDEfVPqfntsxFyfSBp8375JFvIsxM='

def get_key(password):
    try:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(password)
        print("done")
        return base64.urlsafe_b64encode(digest.finalize())
    except Exception as e:
        print(e)
        return (e)     

def testConnection(hostname,username,password,path):
    #connectivity test
    try:
        print("entered testConnection")
        ssh = paramiko.SSHClient()
        host_exist = socket.gethostbyname(hostname)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            f = Fernet(key)
            decrypted_pw = f.decrypt(password)
            password=decrypted_pw.decode()
        except:
            pass

        print("testconnection username=",username)
        ssh.connect(hostname, username = username, password = password)
        command = "stat " + path #or stat
        print("command is:",command)
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout =stdout.read()
        stderr=stderr.read()
        print("stdout = ",len(stdout))
        print("stderr = ",len(stderr))
        if len(stderr) > 0:
            print("Failed to open path " + path + " on " + hostname)
            return ("P")
        ssh.close()    
        return ("OK")
    except paramiko.ssh_exception.NoValidConnectionsError as error:
        # print("Failed to connect to host '%s' with error: %s" % (hostname, error))
        error_msg = "Failed to connect to host " + hostname + " with error " + str(error)
        print(error_msg)
        ssh.close()
        return (error_msg)
    except paramiko.AuthenticationException as authexp:
        error_msg = "Authentication failed for user " + username + "@" + hostname + " with provided password.\n Please verify your credentials"
        print(error_msg)
        ssh.close()
        return (error_msg)
    except paramiko.SSHException as sshException:
        print("Could not establish SSH connection: ", sshException)
        error_msg = "Could not establish SSH connection"
        print(sshException)
        ssh.close()
        return (error_msg)
    except socket.timeout as e:
        print("Connection timed out")
        error_msg = "Connection timed out"
        print(e)
        ssh.close()
        return (error_msg)
    except socket.error as e:
        print("socket Error")
        error_msg = "Failed to resolve hostname " + hostname +" \n"+str(e)
        ssh.close()
        return (error_msg)
    except Exception as e:
        error_msg = "Error occurred during connection test: " + str(e)
        print(error_msg)
        ssh.close()
        return (error_msg)

@method_decorator([login_required], name='dispatch')
class HostRegister(View):
    def post(self, request):
        try:
            print("entered HostRegister")

            print("hostname = ",request.POST['hostname'])
            print("host_username = ",request.POST['host_username'])
            # print("host_password = ",request.POST['host_password'])
            print("host_path = ",request.POST['host_path'])
            print("description = ",request.POST['description'])

            hostname = request.POST['hostname']
            host_username = request.POST['host_username']
            host_password = request.POST['host_password']
            host_path = request.POST['host_path']
            description = request.POST['description']

            existing_service = db.hosts.find_one({'hostname' : hostname, 'host_username' : host_username, 'host_path' : host_path},{"_id":0})

            if existing_service:
                print("exist host_name", existing_service['hostname'])
                print("exist host_username", existing_service['host_username'])
                print("exist host_path", existing_service['host_path'])
                error_string = "Sorry but this service is already registered\n\n Address: " + existing_service['host_username'] + "@" + existing_service['hostname'] + "\n Path: " + existing_service['host_path']
                print(error_string)
                return render(request, 'repoIndex/errorRegisterHost.html',{'error_string': error_string})
            

            valid = testConnection(hostname,host_username,host_password,host_path)
            print("valid is:", valid)

            if valid == "OK":

                message = host_password.encode()
                print("K:",key)
                f = Fernet(key)
                print("F:",f)
                encrypted_pw = f.encrypt(message)
                decrypted_pw = f.decrypt(encrypted_pw)
                print("ENC",encrypted_pw)
                
                if message == decrypted_pw is not True:
                    error_string = "An error occurred during password encryption"
                    print(error_string)
                    return render(request, 'repoIndex/errorRegisterHost.html',{'error_string': error_string})

                new_host = db.hosts.update_one(
                    { 'hostname': hostname },
                    {"$setOnInsert":{
                        'hostname': hostname,
                        'host_username': host_username,
                        'host_password': encrypted_pw,
                        'host_path': host_path,
                        'description': description,
                        'enabled': True
                        }
                    },
                    upsert = True
                    )
                print("new_host is:", new_host.upserted_id)
                # inserted_host = db.hosts.find().sort([("_id", -1)]).limit(1) 
                inserted_host = db.hosts.find_one({'hostname' : hostname})
                print("inserted_host is:", inserted_host)
                return render(request, 'repoIndex/endRegisterHost.html',{'new_host': inserted_host})
            elif valid == "P":
                error_string = "Failed to open path " + host_path + " on " + hostname + ": \n it may not exist or user " + host_username + " does not have permission to access"
                print(error_string)
                return render(request, 'repoIndex/errorRegisterHost.html',{'error_string': error_string})
            else:
                error_string = "An error occurred during connection test"
                print(error_string)
                return render(request, 'repoIndex/errorRegisterHost.html',{'error_string': error_string, 'valid': valid})

        except Exception as e:
            print ('Error HostRegister API', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class LandHostEdit(View):
    def post(self, request):
        try:
            print("entered LandHostEdit")
            print("hostname = ",request.POST['host_edit_address'])
            print("host_username = ",request.POST['host_edit_path'])
            print("host_toggle = ",request.POST['host_edit_toggle'])
            host_edit = {}
            host_edit['address'] = request.POST['host_edit_address']
            host_edit['path'] = request.POST['host_edit_path']
            host_edit['toggle'] = request.POST['host_edit_toggle']
            # if description needed query the db here and pass it to the next view
            print("host_edit is:", host_edit)
            return render(request, 'repoIndex/hostEdit.html', {'host_edit': host_edit})

        except Exception as e:
            print ('Error LandHostEdit', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class HostEdit(View):
    def post(self, request):
        try:
            print("entered HostEdit")
            # if 'host_change_path' in request.POST:
            #     print("request is: ",request.POST)
            #     print("host = ",request.POST['host_change_address'])
            #     print("host_path = ",request.POST['host_change_path'])
            #     print("host_orig_path = ",request.POST['host_change_orig_path'])

            #     address = request.POST['host_change_address']
            #     host_new_path = request.POST['host_change_path']
            #     host_orig_path = request.POST['host_change_orig_path']
            #     username = address.split('@')[0]
            #     hostname = address.split('@')[1]

            #     print("username is: ",username)
            #     print("hostname is: ",hostname)

            #     target_host = db.hosts.find_one_and_update(
            #             {'hostname' : hostname, 'host_username' : username, 'host_path' : host_orig_path},
            #             {"$set":{
            #                 'host_path': host_new_path,
            #                 }
            #             },
            #             return_document = ReturnDocument.AFTER
            #             )
                        
            #     modified_host_id = target_host['_id']
            #     print("modified target_host is:", modified_host_id)

            #     modified_host = db.hosts.find_one({"_id" : modified_host_id })
            #     print("modified_host is:", modified_host)
            #     return render(request, 'repoIndex/endRegisterHost.html',{'modified_host': modified_host})


            if 'host_change_password' in request.POST:
                print("host change password = ",request.POST['host_change_address'])
                # print("host_new_password = ",request.POST['host_change_password'])

                address = request.POST['host_change_address']
                host_new_password = request.POST['host_change_password']
                username = address.split('@')[0]
                hostname = address.split('@')[1]

                print("username is: ",username)
                print("hostname is: ",hostname)

                message = host_new_password.encode()
                print("K:",key)
                f = Fernet(key)
                print("F:",f)
                encrypted_pw = f.encrypt(message)
                # decrypted_pw = f.decrypt(encrypted_pw)
                print("ENC",encrypted_pw)

                target_host = db.hosts.find_one_and_update(
                        {'hostname' : hostname, 'host_username' : username},
                        {"$set":{
                            'host_password': encrypted_pw,
                            }
                        },
                        return_document = ReturnDocument.AFTER
                    )

                modified_host_id = target_host['_id']
                print("modified target_host is:", modified_host_id)

                modified_host = db.hosts.find_one({"_id" : modified_host_id })
                print("modified_host is:", modified_host)
                return render(request, 'repoIndex/endRegisterHost.html',{'modified_host': modified_host})

            if 'host_disable' in request.POST:
                print("host disable = ",request.POST['host_disable'])

                address = request.POST['host_disable']
                username = address.split('@')[0]
                hostname = address.split('@')[1]

                target_host = db.hosts.find_one_and_update(
                        {'hostname' : hostname, 'host_username' : username},
                        {"$set":{
                            'enabled': False,
                            }
                        },
                        return_document = ReturnDocument.AFTER
                    )
                
                disabled_host_id = target_host['_id']
                print("disabled target_host is:", disabled_host_id)

                disabled_host = db.hosts.find_one({"_id" : disabled_host_id })
                print("disabled_host is:", disabled_host)
                return render(request, 'repoIndex/endRegisterHost.html',{'disabled_host': disabled_host})

            if 'host_enable' in request.POST:
                print("host enable = ",request.POST['host_enable'])

                address = request.POST['host_enable']
                username = address.split('@')[0]
                hostname = address.split('@')[1]

                target_host = db.hosts.find_one_and_update(
                        {'hostname' : hostname, 'host_username' : username},
                        {"$set":{
                            'enabled': True,
                            }
                        },
                        return_document = ReturnDocument.AFTER
                    )
                
                enabled_host_id = target_host['_id']
                print("enabled target_host is:", enabled_host_id)

                enabled_host = db.hosts.find_one({"_id" : enabled_host_id })
                print("enabled_host is:", enabled_host)
                return render(request, 'repoIndex/endRegisterHost.html',{'enabled_host': enabled_host})

        except Exception as e:
            print ('Error HostEdit', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class LandHostManager(View):
    def get(self, request):
        try:
            print("entered LandHostManager")
            existing_disabled_hosts = db.hosts.find({"enabled": False},{"_id":0,"description":0}).sort("hostname",pymongo.ASCENDING)
            # conn_results = {}
            disabled_hosts = []
            for doc in existing_disabled_hosts:
                host_status = {}
                print("existing_disabled_hosts is:", doc)
                hostname = doc['hostname']
                username = doc['host_username']
                password = doc['host_password']
                path = doc['host_path']
                print("hostname=",hostname)
                print("username=",username)
                print("password=",password)
                print("path=",path)
                # valid = testConnection(hostname,username,password,path)
                # print("valid connection test is:",valid)

                # if valid == "OK":
                #     status = "UP"
                # elif valid == "P":
                #     status = "PATH"
                # else:
                #     status = "DOWN"

                address = username+"@"+hostname
                host_status["address"] = address
                host_status["path"] = path
                host_status["status"] = status
                disabled_hosts.append(host_status.copy())

            print("disabled_hosts is: ",disabled_hosts)
            return render(request, 'repoIndex/hostManager.html', {'disabled_hosts': disabled_hosts})
        
        except Exception as e:
            print ('Error LandHostManager API', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class ExistingHostsTest(View):
    def post(self, request):
        try:
            print("entered ExistingHostsTest")
            existing_hosts = db.hosts.find({"enabled": True},{"_id":0,"description":0}).sort("hostname",pymongo.ASCENDING)
            # conn_results = {}
            conn_results = []
            for doc in existing_hosts:
                host_status = {}
                print("existing_hosts is:", doc)
                hostname = doc['hostname']
                username = doc['host_username']
                password = doc['host_password']
                path = doc['host_path']
                print("hostname=",hostname)
                print("username=",username)
                print("password=",password)
                print("path=",path)
                valid = testConnection(hostname,username,password,path)
                # valid="OK"
                print("valid connection test is:",valid)

                if valid == "OK":
                    status = "UP"
                elif valid == "P":
                    status = "PATH"
                else:
                    status = "DOWN"

                address = username+"@"+hostname
                host_status["address"] = address
                host_status["path"] = path
                host_status["status"] = status
                conn_results.append(host_status.copy())

            print("conn_results is: ",conn_results)
            return JsonResponse(conn_results, safe=False)
            # return conn_results
        
        except Exception as e:
            print ('Error ExistingHostsTest API', e)
            return redirect('/')

class AutocompleteHostsAddExperiment(View):
    def get(self, request):
        try:
            print("REQUEST IS:", request.GET)
            if request.GET.get("q"):
                print("received query")
                param = str(request.GET.get("q"))
                print ("param is:", param)
                known_hosts = db.hosts.find({ "hostname": {'$regex' : ".*"+param+".*", '$options': "ix"}, "enabled": True },{"_id":0}).sort("hostname",pymongo.ASCENDING)
                # doc = db[dbcollection].find({fieldFilter:{"$regex":regex, "$options": 'ix'}, 'access_w': {'$exists': True, '$in': user['heritage']['w']} }).limit(10)
                print('known_hosts is:', known_hosts)
                return JsonResponse(to_json(known_hosts), safe=False)
        except Exception as e:
            print ('Error AutocompleteHostsAddExperiment API', e)
            return redirect('/')