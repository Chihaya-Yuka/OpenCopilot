from flask import Flask, request, Response
import requests

app = Flask(__name__)

TARGET_URL = "https://skibidi.24a.fun"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    url = f"{TARGET_URL}/{path}"
    headers = {key: value for key, value in request.headers if key != 'Host'}
    data = request.get_data()
    method = request.method
    resp = requests.request(method, url, headers=headers, data=data, cookies=request.cookies, allow_redirects=False)
    response = Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2333)
