from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
from create_stack_dash import run_using_ui, stop_tests_using_ui
from waitress import serve

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=["POST"])
def parse_request():
    button_pressed = request.form.get('button')
    print('Request Type: {0}'.format(button_pressed))

    if button_pressed == 'generate_load':
        data = json.loads(request.form.get('form'))
        print('Data sent from UI: {0}'.format(data))
        returned_url = run_using_ui(data)
        prefix = data['prefix']
        if returned_url:
            return make_response(jsonify(url=returned_url, stack_name=prefix), 201)
        else:
            return make_response("Error", 500)
    elif button_pressed == 'stop_individual_test':
        prefix = request.form.get('stack')
        stop_tests_using_ui(prefix=prefix)
        return make_response(jsonify("Test {0} terminated".format(prefix)), 201)


CORS(app)
serve(app, host='0.0.0.0', port=5000)
