# app.py
from flask import Flask, request, redirect, Response
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)

# Trust the edge proxy for proto/host so request.scheme & request.host are correct
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=0)

CANONICAL_HOST = "www.rivue.ai"

@app.before_request
def canonicalize():
    # Determine scheme/host as seen by the client (honor X-Forwarded-* from DO/Cloudflare)
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.headers.get("X-Forwarded-Host", request.host.split(":")[0])

    # Build a safe path+query suffix
    path = request.path
    qs = request.query_string.decode("utf-8")
    suffix = f"{path}?{qs}" if qs else path

    # 1) Force HTTPS
    if scheme != "https":
        return redirect(f"https://{host}{suffix}", code=308)  # 308 preserves method/body

    # 2) Force canonical host (apex → www)
    if host != CANONICAL_HOST:
        return redirect(f"https://{CANONICAL_HOST}{suffix}", code=308)

# Optional: add HSTS to all responses (after TLS works)
@app.after_request
def add_security_headers(resp: Response):
    # 6 months HSTS; preload if/when you’re confident
    resp.headers.setdefault("Strict-Transport-Security", "max-age=15552000; includeSubDomains")
    return resp

@app.route("/")
def home():
    return "Hello from the canonical host!"
