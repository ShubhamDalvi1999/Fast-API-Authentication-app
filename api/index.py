from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "message": "API is working!",
            "path": self.path,
            "note": "This is a test handler to verify Vercel serverless functions"
        }
        
        self.wfile.write(json.dumps(response).encode()) 