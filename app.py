from flask import Flask
from flask import Response
from flask import redirect
from flask import request
from flask import jsonify
import json
import requests

from urllib.parse import unquote

app = Flask(__name__)
# default values
SERVER = 'https://binderhubeit.com'
PROVIDER_PREF = 'gh'

# returns error 500 with prompt of missing arguments 
def missing_arg(arg):
    return Response("Error! Missing arg from GET request: " + arg, 500)

@app.route('/')
def hello():
    print(request.args)
    return jsonify(request.args)

# handles building and redirecting
@app.route('/build', methods=['GET'])
def build():
    # if custom server passed use that server
    if 'server' in request.args:
        server = request.args.get('server')
    # else use default
    else:
        server = SERVER
    # if custom provider passed use that provider
    if 'provider' in request.args:
        provider = request.args.get('provider')
    else:
        provider = PROVIDER_PREF
    # cases if provider is github
    # if username not passed, return error 500
    if provider == 'gh' and 'username' not in request.args:
        return missing_arg('username')
    # else set username
    else:
        username = request.args.get('username')
    # if provider not passed, return error 500
    if provider == 'gh' and 'repo' not in request.args:
        return missing_arg('repo')
    # else set username
    else:
        repo = request.args.get('repo')

    # if filepath passed use filepath
    if 'filepath' in request.args:
        filepath = unquote(request.args.get('filepath'))
    else:
        filepath = None

    # set binderhub URL based on arguments set
    binderhub_url = server + '/build/' + provider +'/' + username + '/' + repo + '/master'
    # get streaming response
    response = requests.get(binderhub_url,stream=True)
    # traverse stream
    for line in response.iter_lines():
        # if valid line passed by stream
        if line:
            # retrieve status for update
            status = json.loads(line.decode('utf-8').replace('data:',''))
            try:
                # if phase in status identify state
                if 'phase' in status:
                    print(status)
                    # if ready build URL and redirect to notebook
                    if status['phase'] == 'ready':
                        # if filepath exists
                        if filepath:
                            # if notebook launch notebook app
                            if filepath.find('.ipynb') != -1:
                                nb_url = status['url']+'notebooks/'+filepath+'?token='+status['token']
                            # if directory launch tree directory mode
                            else:
                                nb_url = status['url']+'tree/'+filepath+'?token='+status['token']
                        # if no filepath just open root tree
                        else:    
                            nb_url = status['url']+'?token='+status['token']
                        return redirect(nb_url)
                    # if failed status return error message and status 500
                    elif status['phase'] == 'failed':
                        return Response(status["message"], 500)
                else:
                    return Response("Invalid structure, no `phase` key in response", 500)

            except Exception as e:
                return Response(str(e),500)
    

if __name__ == '__main__':
    app.run()