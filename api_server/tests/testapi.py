# This file not used for pytest, 
# just for manual testing with docker
import requests 

# r = requests.get('http://localhost:5000/api/v1/place/8201/powers')
# r = requests.get('http://localhost:5000/api/v1/place/8201/lights')
# r = requests.get('http://localhost:5000/api/v1/place')

test_json = {
        'username': 'guest',
        'password': 'test_password'
}
rv = requests.get('http://localhost:5000/api/v1/login', json=test_json)
