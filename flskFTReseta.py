import sys
import ftd2xx as ftd
import json
from flask import Flask
import reseter as rstr

app = Flask(__name__)


def convert_dic(data):
    if isinstance(data, bytes):  return data.decode('ascii')
    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    return data

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/device-info")    
def device_Info():
   
    try:
        d = ftd.open(0)    # Open first FTDI device
        di = d.getDeviceInfo() 
        #di = convert_dic(di)

        dij = json.dumps(   {
                            'description':  di['description'].decode('utf-8'),
                            'serial':       di['serial'].decode('utf-8')       
                            }
        
                        )
        print(dij)
    except:
        d.close()    
        return 404
    d.close();
    return dij

@app.route("/init-reseter")
def init_reseter ():
    rstr.init_reseter()


@app.route("/reset-device", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        print("Reseting Image")
    
# specifying host as 0.0.0.0 causes server to be run on machine local IP rather than localhost
if __name__ == "__main__":
    app.run( host = '0.0.0.0')

