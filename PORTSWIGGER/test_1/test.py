# app_vuln.py — demo SSRF (vulnerable)
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/fetch')
def fetch():
    url = request.args.get('url', '')
    if not url:
        return 'Provide ?url=', 400
    # VULNERABLE: trực tiếp fetch URL từ input user
    r = requests.get(url, timeout=5)
    return Response(r.content, status=r.status_code, headers={'Content-Type': r.headers.get('Content-Type','text/plain')})

if __name__ == '__main__':
    app.run(port=5000)
