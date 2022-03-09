import ssl
import OpenSSL
import time
import subprocess
DEFAULT_HOSTNAME = 'google.com'

def get_fecha_expiracion(host=DEFAULT_HOSTNAME,port=443):
    print(host)
    fecha_expiracion_epoch=0
    try:
        certificate = ssl.get_server_certificate((host,port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, certificate)
        fecha_expiracion_cert = x509.get_notAfter().decode("utf-8") #YYYYMMDDhhmmssZ
        YEAR = int(fecha_expiracion_cert[:4])
        MONTH = int(fecha_expiracion_cert[4:6])
        DAY = int(fecha_expiracion_cert[6:8])
        Hour = int(fecha_expiracion_cert[8:10])
        Minute = int(fecha_expiracion_cert[10:12])
        Seconds = int(fecha_expiracion_cert[12:14])
        fecha_expiracion_epoch = time.mktime((YEAR, MONTH, DAY, Hour, Minute, Seconds, 0, 0, 0))

    except:
        try:
            print("Failed Normal-check start Legacy-check")
            cmd = "openssl s_client -showcerts -servername {h} -connect {h}:{p}".format(h=host,p=port)
            cmd += " </dev/null | openssl x509 -noout -enddate | awk -F '=' '/notAfter/ {print $2}'"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
            output, errors = p.communicate()
            t=time.strptime(output.decode('utf-8').strip(),"%b %d %H:%M:%S %Y %Z")
            fecha_expiracion_epoch = time.mktime(t)
        except:
            print("Failed Legacy-check, setting date to invalid date")
            fecha_expiracion_epoch = time.mktime(time.localtime(0))
    return fecha_expiracion_epoch
                            
def check_fecha_exp(time_exp_cert,days_alerts,time_now=int(time.time())):
    diff_time = time_exp_cert - time_now
    if diff_time <= ( days_alerts['CRITICAL'] * 86400 ):
        return 'CRITICAL'
    elif diff_time <= ( days_alerts['WARNING'] * 86400 ):
        return 'WARNING'
    elif diff_time <= ( days_alerts['NOTIFICATION'] * 86400 ):
        return 'NOTIFICATION'
    else:
        return 'OK'

from fastapi import FastAPI, Response, status
from pydantic import BaseModel

class Connection(BaseModel):
    host: str
    port: int = 443
    n_days: int = 60
    w_days: int = 30
    c_days: int = 7

app = FastAPI()

@app.post("/", status_code=200)
async def root(cnx: Connection, response: Response ):
    """
    this endpoint recived five(5) parameters only one is requiered the other are optional, parameters:
    - host: str # Requiered
    - port: int = 443 #Optional default:443
    - n_days: int = 60 #Optional default: 60 (days)
    - w_days: int = 30 #Optional default: 30 (days)
    - c_days: int = 7 #Optional default: 7 (days)
    
    examples:
    * curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com"}'
    * curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com", "port": 443}'
    * curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com", "port": 443, "n_days": 45}'
    * curl -X 'POST' 'http://127.0.0.1/' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"host": "yahoo.com", "n_days": 45, "w_days": 20, "c_days": 10}'
    """
    days_alerts = {"NOTIFICATION":cnx.n_days,"WARNING":cnx.w_days,"CRITICAL":cnx.c_days}
    print("host:",cnx.host)
    print("days_alerts_settings:",days_alerts)
    fecha = get_fecha_expiracion(host=cnx.host,port=cnx.port)
    estado = check_fecha_exp(time_exp_cert=fecha,days_alerts=days_alerts)
    if estado == 'CRITICAL':
        response.status_code = 599 #Critical_Alert
    if estado == 'WARNING':
        response.status_code = 499 #Warning_Alert
    if estado == 'NOTIFICATION':
        response.status_code = 299 #Notificacion_Alert
    return {"Estatus de Expiracion": estado, "Host":cnx.host,"Port":cnx.port,"Fecha Expiracion":time.asctime(time.localtime(fecha))}
