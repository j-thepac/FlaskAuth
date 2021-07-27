# FLASK AUTHENTICATION
This is a simple project to demo authentication . 

## Requirement
* Valid user should be to open http://127.0.0.1:5000/protected

#### Usecase 1 : Access Using Browser
* User opens  http://127.0.0.1:5000/login from browser 
* Gives valid credentials and he will be redirected to /protected

#### Usecase 2 : Access directly from REST call
* User can directly open  http://127.0.0.1:5000/protected by GET Rest call  
	1. If he either gives valid Authorization header
	2. Either if he has valid token

## Pre-Req
* pip install -r requirements
* Set PASSWORD and SECRET_KEY in bashrc(linux) and bash_profile(mac) to any value
* Make sure u use same PASSWORD while loggin in

## Sample Rest Request

### python
*import requests
r=requests.get("http://127.0.0.1:5000/protected",headers={'Authorization': 'email:password'})*


