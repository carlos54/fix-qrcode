import json
from flask import Flask, redirect, render_template, jsonify, request, abort
from jsonschema import validate, ValidationError  # type: ignore

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'The super simple redirect QRCODE server is running'


@app.route('/<id>', methods=["GET"])
def search_url(id:str):

    with open("data.json", "r") as file: 
        data_array = json.load(file)

    data = {}
    for key in data_array:
         data[key.get("key")] = key.get("value")
    
    url =  data.get(id, None)
    if url is None:
        return render_template('404.html')
    else:
        return  redirect(url)


@app.route("/data", methods=["GET"])
def get_datafile():
    with open("data.json", "r") as file: 
        data_array = json.load(file)

    return jsonify(data_array)


@app.route("/data", methods=["POST"])
def update_datafile():
    json_bytes = request.files.get("data")
    with open("validator.schema", "r") as f:
        schema = json.loads(f.read())

    if not json_bytes :
        abort(404, "Missing data payload  - data : application/json file")
      
    try:
        data_array = json.loads(json_bytes.read())
        validate(instance=data_array, schema=schema)
        with open("data.json", "w", encoding="utf-8") as f :
            json.dump(data_array, f, indent=3)

    except ValidationError as err :
        abort(403, f"respondents json data/json not valide : {err}")
       
    except BaseException as err:
        abort(403,f"error occur : {err}")

    else :
       return jsonify({'success':True})



if __name__ == '__main__':
    app.run()
    #app.run(host='127.0.0.1',  port = 5000, debug=True)
    