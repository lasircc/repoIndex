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

@method_decorator([login_required], name='dispatch')
class LandHostManager(View):
    def get(self, request):
        return render(request, 'repoIndex/hostManager.html')

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
        ssh = paramiko.SSHClient()
        # transport = paramiko.Transport((hostname, 22))
        # sftp = paramiko.SFTPClient.from_transport(transport)
        # ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        # ssh.load_system_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        host_exist = socket.gethostbyname(hostname)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username = username, password = password)
        # command="ls -lha"
        # stdin , stdout, stderr = ssh.exec_command(command)
        # print(stdout.read())
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

        # read[i]=t_read[360:375]
        # raw_speed[i]=t_read[360:364]
        # address[i]=t_read[221:233]
        # print('Receieved data on cable %s from %s via IP: %s at %s \n'%(Cable[i],WMI_Port[i],address[i],read[i]))
        # stdin, stdout, stderr = ssh.exec_command('sudo ifconfig %s down'%(target_eth[i]))
        # print ('Disabling %s : \n\n'%(WMI_Port[i]))
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
            # print("request is: ",request.POST)

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

            valid = testConnection(hostname,host_username,host_password,host_path)
            print("valid is:", valid)

            if valid == "OK":

                # key = getattr(settings, "SECRET_KEY", None)
                # print("key is ", key)

                key = b'n_jrI9S9ivI9iYQDEfVPqfntsxFyfSBp8375JFvIsxM='

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

                # hashed_password = bcrypt.hashpw(host_password.encode('utf-8'), bcrypt.gensalt())
                # print("hashed_password is:", hashed_password)
                # pw_hash_test = bcrypt.checkpw(host_password.encode('utf-8'), hashed_password)
                # print("Pwd hash check =" , pw_hash_test)
                
                # if pw_hash_test is not True:
                #     error_string = "An error occurred during password hashing"
                #     print(error_string)
                #     return render(request, 'repoIndex/errorRegisterHost.html',{'error_string': error_string})

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
                # for doc in inserted_host:
                #     print("inserted_host is:", doc)
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
