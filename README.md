# check_cert_ssl
check_cert_ssl is an API that help to check certificate-ssl from  any website, it has an endpoint that recived five(5) parameters only one is requiered and the other are optional, parameters: 
 - host: str # Requiered
 - port: int = 443 #Optional default:443
 - n_days: int = 60 #Optional default: 60 (days)
 - w_days: int = 30 #Optional default: 30 (days)
 - c_days: int = 7 #Optional default: 7 (days)
    
## Examples to usage:
 ```
curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com"}' 

curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com", "port": 443}' 

curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com", "port": 443, "n_days": 45}' 

curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com", "n_days": 45, "w_days": 20, "c_days": 10}'```
