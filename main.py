from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
from datetime import datetime

app = FastAPI()

# Static dosyaları servis et
try:
    app.mount("/static", StaticFiles(directory="public"), name="static")
except:
    pass

# Ana sayfa
@app.get("/", response_class=HTMLResponse)
async def get_root():
    return """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Solana Mint Tracker - solana-py-v2</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
                text-align: center;
            }
            h1 {
                color: #667eea;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .subtitle {
                color: #666;
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            .status {
                background: #f0f4ff;
                border: 2px solid #667eea;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
            .status-icon {
                font-size: 3em;
                margin-bottom: 10px;
            }
            .status-text {
                color: #667eea;
                font-weight: bold;
                font-size: 1.1em;
            }
            .info {
                background: #fff9e6;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                margin: 20px 0;
                text-align: left;
            }
            .info h3 {
                color: #d97706;
                margin-bottom: 10px;
            }
            .info ul {
                list-style-position: inside;
                color: #666;
            }
            .info li {
                margin: 5px 0;
            }
            .footer {
                margin-top: 30px;
                color: #999;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Solana-py-v2</h1>
            <p class="subtitle">Render Deployment Başarılı!</p>
            
            <div class="status">
                <div class="status-icon">✅</div>
                <div class="status-text">Web Siteniz Aktif ve Çalışıyor</div>
            </div>
            
            <div class="info">
                <h3>📋 Proje Bilgileri</h3>
                <ul>
                    <li><strong>Platform:</strong> Render.com</li>
                    <li><strong>URL:</strong> https://solana-py-v2.onrender.com/</li>
                    <li><strong>Backend:</strong> FastAPI (Python)</li>
                    <li><strong>Runtime:</strong> Python 3.9+</li>
                    <li><strong>GitHub:</strong> nano-id/solana-py-v2</li>
                </ul>
            </div>
            
            <div class="info">
                <h3>🔧 Sonraki Adımlar</h3>
                <ul>
                    <li>WebSockets ekleyerek gerçek zamanlı Solana takibi yapın</li>
                    <li>API endpoint'leri ekleyerek mint verilerini çekin</li>
                    <li>Veritabanı entegrasyonu yapın (PostgreSQL)</li>
                    <li>Web arayüzü ekleyerek kullanıcı dostu hale getirin</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Powered by FastAPI & Render.com</p>
                <p>Deploy: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            </div>
        </div>
    </body>
    </html>
    """

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "solana-py-v2",
        "timestamp": datetime.now().isoformat()
    }

# API endpoint örneği
@app.get("/api/status")
async def get_status():
    return {
        "service": "solana-py-v2",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/",
            "/health",
            "/api/status"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)