from .__init__ import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import pymongo
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
                
                if encrypted_pw == decrypted_pw is not True:
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
                        'description': description
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

            return render(request, 'repoIndex/endHostRegister.html')
        except Exception as e:
            print ('Error HostRegister API', e)
            return redirect('/')

@method_decorator([login_required], name='dispatch')
class LandHostManager(View):
    def get(self, request):
        try:
            existing_hosts = db.hosts.find({},{"_id":0,"description":0}).sort("hostname",pymongo.ASCENDING)
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
                print("valid connection test is:",valid)
                if valid == "OK":
                    status = "UP"
                else:
                    status = "DOWN"
                address = username+"@"+hostname
                host_status["address"] = address
                host_status["path"] = path
                host_status["status"] = status
                conn_results.append(host_status.copy())
            print("conn_results is: ",conn_results)
        
        except Exception as e:
            print ('Error LandHostManager API', e)
            return redirect('/')
        return render(request, 'repoIndex/hostManager.html',{'conn_results': list(conn_results)})