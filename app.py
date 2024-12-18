from flask import Flask, render_template, request, jsonify
import requests
import os
import json

app = Flask(__name__)

IP = {}
IP['RGB_LIGHT_STRIP_1']="10.1.1.21"
IP['RGB_LIGHT_STRIP_2']="10.1.1.22"
IP['RGB_LIGHT_STRIP_3']="10.1.1.23"
IP['RGB_LIGHT_STRIP_4']="10.1.1.24"

IP['ACTUATOR_1']="10.1.1.40"
IP['ACTUATOR_2']="10.1.1.41"

REQUEST_CONFIG={}
REQUEST_CONFIG['CONNECT_TIMEOUT']=0.5
REQUEST_CONFIG['READ_TIMEOUT']=10

LED_STATUS_FILE = 'led_status.json'

# Estado inicial de los LEDs
INITIAL_LED_STATUS = {
    "level1": {
        "Lobby": False,
        "Retail 1": False,
        "Retail 2": False,
        "Retail 3": False,
        "Historic House": False,
        "Site": False
    },
    "level2": {
        "Office 2": False,
        "Lobby": False,
        "Office 1": False,
        "Parking": False
    },
    "level3": {
        "Parking": False
    },
    "level4": {
        "407": False,
        "406": False,
        "405": False,
        "404": False,
        "403": False,
        "402": False,
        "401": False,
        "412": False,
        "411": False,
        "410": False,
        "409": False,
        "408": False,
        "Amenities" : False
    },
    "level5": {
        "507": False,
        "506": False,
        "505": False,
        "504": False,
        "503": False,
        "502": False,
        "501": False,
        "516": False,
        "515": False,
        "514": False,
        "513": False,
        "512": False,
        "511": False,
        "510": False,
        "509": False,
        "508": False
    },
    "level6": {
        "607": False,
        "606": False,
        "605": False,
        "604": False,
        "603": False,
        "602": False,
        "601": False,
        "616": False,
        "615": False,
        "614": False,
        "613": False,
        "612": False,
        "611": False,
        "610": False,
        "609": False,
        "608": False
    },
    "level7": {
        "707": False,
        "706": False,
        "705": False,
        "704": False,
        "703": False,
        "702": False,
        "701": False,
        "716": False,
        "715": False,
        "714": False,
        "713": False,
        "712": False,
        "711": False,
        "710": False,
        "709": False,
        "708": False
    },
    "level8": {
        "807": False,
        "806": False,
        "805": False,
        "804": False,
        "803": False,
        "802": False,
        "801": False,
        "816": False,
        "815": False,
        "814": False,
        "813": False,
        "812": False,
        "811": False,
        "810": False,
        "809": False,
        "808": False
    },
    "level9": {
        "PH1": False,
        "PH2": False,
        "Common": False
    }
}


def reset_led_status():
    # Cargar el estado actual de los LEDs
    status = load_led_status()

    # Establecer todos los LEDs en False
    for level in status:
        for led in status[level]:
            status[level][led] = False

    # Guardar los cambios en el archivo
    save_led_status(status)
    print("Todos los estados de los LEDs se han puesto en False.")

def create_led_status_file():
    if not os.path.isfile(LED_STATUS_FILE):
        with open(LED_STATUS_FILE, 'w') as file:
            json.dump(INITIAL_LED_STATUS, file, indent=4)
        print(f"Archivo {LED_STATUS_FILE} creado con estado inicial.")

# Cargar el estado de los LEDs desde el archivo
def load_led_status():
    create_led_status_file()  # Asegurarse de que el archivo exista
    with open(LED_STATUS_FILE, 'r') as file:
        return json.load(file)

# Guardar el estado de los LEDs en el archivo
def save_led_status(status):
    with open(LED_STATUS_FILE, 'w') as file:
        json.dump(status, file, indent=4)
        
@app.route('/toggle-actuator')
def toggle_actuator():
    
    level=request.args.get('level', type=str)
    name_button=request.args.get('name_button', type=str)

    relay = request.args.get('relay', type=int)
    controller = request.args.get('controller', type=int)
    
    status = load_led_status()

    # Cambiar el estado del LED
    current_state = status[level][name_button]

    if current_state == False:

        turn = 1

    else:

        turn = 0

    status[level][name_button] = not current_state
    save_led_status(status)
    
    if controller == 1:
        try:

            requests.get("http://"+IP['ACTUATOR_1'], params={'device':relay,'turn':turn,}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: ACTUATOR_1 {IP['ACTUATOR_1']}")

    elif controller == 2:
        try:

            requests.get("http://"+IP['ACTUATOR_2'], params={'device':relay,'turn':turn,}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: ACTUATOR_2 {IP['ACTUATOR_2']}")
                
    response = {'menssage': 'Recibido'}

    return jsonify(response)
	
@app.route('/set-range-leds')
def set_range_leds():
    
    level=request.args.get('level', type=str)
    name_button=request.args.get('name_button', type=str)

    led_position_min = request.args.get('led_position_min', type=int)
    led_position_max = request.args.get('led_position_max', type=int)
    strip_number = request.args.get('strip_number', type=int)
    device_number = request.args.get('device_number', type=int)

    status = load_led_status()

    # Cambiar el estado del LED
    current_state = status[level][name_button]

    if current_state == False:

        red_brightness = 255
        green_brightness = 155
        blue_brightness = 40

    else:

        red_brightness = 0
        green_brightness = 0
        blue_brightness = 0

    status[level][name_button] = not current_state
    save_led_status(status)
    
    if device_number == 1:
        try:

            requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min,'led_position_max':led_position_max,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_1 {IP['RGB_LIGHT_STRIP_1']}")

    elif device_number==2:

        try:

            requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min,'led_position_max':led_position_max,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_2 {IP['RGB_LIGHT_STRIP_2']}")
    
    elif device_number==3:

        try:

            requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min,'led_position_max':led_position_max,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_3 {IP['RGB_LIGHT_STRIP_3']}")
            
    response = {'menssage': 'Recibido'}

    return jsonify(response)

@app.route('/set-dual-range-leds')
def set_dual_range_leds():
    
    level=request.args.get('level', type=str)
    name_button=request.args.get('name_button', type=str)

        # Primer rango
    led_position_min1 = request.args.get('led_position_min1', type=int)
    led_position_max1 = request.args.get('led_position_max1', type=int)
    
    # Segundo rango
    led_position_min2 = request.args.get('led_position_min2', type=int)
    led_position_max2 = request.args.get('led_position_max2', type=int)

    strip_number = request.args.get('strip_number', type=int)
    device_number = request.args.get('device_number', type=int)

    status = load_led_status()

    # Cambiar el estado del LED
    current_state = status[level][name_button]

    if current_state == False:

        red_brightness = 255
        green_brightness = 155
        blue_brightness = 40

    else:

        red_brightness = 0
        green_brightness = 0
        blue_brightness = 0

    status[level][name_button] = not current_state
    save_led_status(status)
    
    if device_number == 1:

        try:

            requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min1,'led_position_max':led_position_max1,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
            requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min2,'led_position_max':led_position_max2,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_1 {IP['RGB_LIGHT_STRIP_1']}")

    elif device_number==2:

        try:

            requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min1,'led_position_max':led_position_max1,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
            requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min2,'led_position_max':led_position_max2,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_2 {IP['RGB_LIGHT_STRIP_2']}")
    
    elif device_number==3:

        try:

            requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min1,'led_position_max':led_position_max1,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
            requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params={'red_brightness':red_brightness,'green_brightness':green_brightness,'blue_brightness':blue_brightness,'led_position_min':led_position_min2,'led_position_max':led_position_max2,'strip_number':strip_number}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        except:

            print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_3 {IP['RGB_LIGHT_STRIP_3']}")
            
    response = {'menssage': 'Recibido'}

    return jsonify(response)

@app.route('/on-all-strips')
def on_all_strips():
    
    try:

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 1
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 2
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 3
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 4
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
        
    except:
        
        print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_1 {IP['RGB_LIGHT_STRIP_1']}")

    try:

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 1
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 2
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 3
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 4
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
        
    except:
        
        print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_2 {IP['RGB_LIGHT_STRIP_2']}")

    try:

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 1
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 2
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 3
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))

        params = {
            'red_brightness': 255,
            'green_brightness': 155,
            'blue_brightness': 40,
            'led_position_min1': 0,
            'led_position_max1': 300,
            'strip_number': 4
        }
        
        requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params=params, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
        
    except:
        
        print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_3 {IP['RGB_LIGHT_STRIP_3']}")
        
    response = {'menssage': 'Se han apagado todos'}
    
    return jsonify(response)

@app.route('/off-all-strips')
def off_all_strips():
    
	turn = request.args.get('turn', type=str)
    
	try:
		requests.get("http://"+IP['RGB_LIGHT_STRIP_1'], params={'strips':turn}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
		
	except:
		print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_1 {IP['RGB_LIGHT_STRIP_1']}")

	try:
		requests.get("http://"+IP['RGB_LIGHT_STRIP_2'], params={'strips':turn}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
		
	except:
		print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_2 {IP['RGB_LIGHT_STRIP_2']}]")
  
	try:
		requests.get("http://"+IP['RGB_LIGHT_STRIP_3'], params={'strips':turn}, timeout=(REQUEST_CONFIG['CONNECT_TIMEOUT'], REQUEST_CONFIG['READ_TIMEOUT']))
		
	except:
		print(f"No se encuentra el dispositivo: RGB_LIGHT_STRIP_3 {IP['RGB_LIGHT_STRIP_3']}]")
  
	response = {'menssage': 'Se han apagado todos'}
	
	return jsonify(response)

@app.route("/",methods=['GET','POST'])
def index():

	return render_template("index.html")
	 	    
if __name__ == "__main__":
    
	create_led_status_file()
	app.run(port=80,host='0.0.0.0',debug=True)
