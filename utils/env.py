import os

def is_docker():
    '''
    Check if the code is running in a docker container
    May get a smarter check in the future. For now just relying on this 
    variable only being set by Compose'''
    try:
        ret = os.getenv("USING_DOCKER", False)
        if ret:
            return True # Easy way to convert str to bool
    except Exception:
        return False
