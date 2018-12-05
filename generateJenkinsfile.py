import docker
import argparse
import string
import os

def parseContainer():
    parser = argparse.ArgumentParser(description='Generate a Jenksfile based on a running container. Provide a valid container name')

    parser.add_argument('string', metavar='c', type=str, nargs='+',
                        help='container name')

    args = parser.parse_args()
    print("* [DEBUG]: argument from commandline",args.string)
    return args.string 

# Reusuble function for initializing the docker client
def initClient():
    global client 
    client = docker.from_env()

# Lookup container name provided to cli. Container name must be valid.
def containerLookup():
    initClient() 
    print("* [DEBUG]:", client.containers.list())

    searchContainer = parseContainer()

    for container in client.containers.list():
        print("* [DEBUG]: List of container names.",container.name)
        if container.name in searchContainer:
            print("* [INFO]: Found container")
            return container.name
        else:
            print("* [INFO]: Container not found")
    

# Create a jenkinsfile based on container name provided to cli. Container name must be valid.
#TODO: Error handling
def createJenkinsFile( containerName ):
    cname = { 'var' : containerName }
    fileTemplate = string.Template("""
        pipeline {
        agent any

        stages {
            stage('Build') {
                steps {
                    echo 'Building for $var ...'
                }
            }
            stage('Test') {
                steps {
                    echo 'Testing for $var..'
                }
            }
            stage('Deploy to K8s') {
                steps {
                    echo 'Deploying for $var...'
                }
                sh(
                ./kubectl apply -f deployment.yaml
                , returnStatus: false, returnStdout: false)
            }
        }
    }
    """)

    cwdir = os.getcwd()
    fullpath = os.path.join(cwdir,"Jenkinsfile")
    print("* [INFO]: Writing out Jenkinsfile")
    f = open(fullpath,'w')
    f.write(fileTemplate.substitute(cname))
    f.close()
    print("* [INFO]: Done")
    return


def main():
    createJenkinsFile(containerLookup())


if __name__ == "__main__":
    main()
