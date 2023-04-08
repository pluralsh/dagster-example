import os.path

def in_kubernetes():
    return os.path.isfile("/var/run/secrets/kubernetes.io/serviceaccount/token")