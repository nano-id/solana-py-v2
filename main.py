from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json
import asyncio
from datetime import datetime
from typing import Set, Dict, List

app = FastAPI()

# Solana tracking variables
tracked_mints: Dict[str, Dict] = {}
websocket_clients: Set[WebSocket] = set()

# Static dosyaları servis et
try:
    app.mount("/static", StaticFiles(directory="public"), name="static")
except:
    pass

# Ana sayfa - MAVI TEMA
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
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #3b7fd9 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                max-width: 1200px;
                margin: 0 auto;
            }
            h1 {
                color: #1e3c72;
                font-size: 2.5em;
                margin-bottom: 20px;
                text-align: center;
            }
            .subtitle {
                color: #2a5298;
                font-size: 1.2em;
                text-align: center;
                margin-bottom: 30px;
            }
            .status {
                background: #e8f4f8;
                border: 2px solid #1e3c72;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
            }
            .status-icon {
                font-size: 3em;
                margin-bottom: 10px;
            }
            .tracker-area {
                background: #f8f9fa;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
            }
            .mint-item {
                background: white;
                border-left: 4px solid #2a5298;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .mint-address {
                font-family: 'Courier New', monospace;
                color: #1e3c72;
                font-weight: bold;
                word-break: break-all;
                font-size: 0.9em;
            }
            .btn-solana {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                cursor: pointer;
                margin: 10px;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn-solana:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .info {
                background: #e8f4f8;
                border-left: 4px solid #2a5298;
                padding: 15px;
                margin: 20px 0;
            }
            .info h3 {
                color: #1e3c72;
                margin-bottom: 10px;
            }
            .info ul {
                list-style-position: inside;
                color: #333;
            }
            .info li {
                margin: 5px 0;
            }
            .footer {
                margin-top: 30px;
                color: #666;
                font-size: 0.9em;
                text-align: center;
            }
            #mintList {
                max-height: 500px;
                overflow-y: auto;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .stat-card {
                background: white;
                border: 2px solid #2a5298;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                color: #1e3c72;
                font-weight: bold;
            }
            .stat-label {
                color: #666;
                margin-top: 5px;
            }
            .log-window {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 400px;
                max-height: 300px;
                background: rgba(0, 0, 0, 0.9);
                border: 2px solid #2a5298;
                border-radius: 10px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.5);
                overflow: hidden;
                z-index: 1000;
                display: flex;
                flex-direction: column;
            }
            .log-header {
                background: #1e3c72;
                color: white;
                padding: 10px 15px;
                font-weight: bold;
                cursor: move;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .log-close {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
                padding: 0;
                width: 25px;
                height: 25px;
            }
            .log-content {
                flex: 1;
                overflow-y: auto;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            .log-entry {
                color: #00ff00;
                margin-bottom: 5px;
                word-wrap: break-word;
            }
            .log-entry.error { color: #ff4444; }
            .log-entry.success { color: #44ff44; }
            .log-entry.warning { color: #ffaa00; }
            .log-entry.info { color: #00aaff; }
            .log-toggle {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #1e3c72;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 50px;
                cursor: pointer;
                font-size: 14px;
                z-index: 999;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .log-toggle:hover {
                background: #2a5298;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Solana-py-v2 - Mint Tracker</h1>
            <p class="subtitle">Solana Blockchain'de Yeni Mint'leri Takip Edin</p>
            
            <div class="status">
                <div class="status-icon">🔵</div>
                <div style="color: #1e3c72; font-weight: bold; font-size: 1.1em;">
                    Sistem Aktif - Gerçek Zamanlı Solana Takibi
                </div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="totalMints">0</div>
                    <div class="stat-label">Toplam Mint</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="freshMints">0</div>
                    <div class="stat-label">Yeni Mint</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="status">Offline</div>
                    <div class="stat-label">Bağlantı Durumu</div>
                </div>
            </div>
            
            <div class="tracker-area">
                <h3 style="color: #1e3c72; margin-bottom: 15px;">📊 Mint Listesi</h3>
                <div id="mintList">
                    <p style="color: #666; text-align: center; padding: 20px;">
                        Mint'ler burada görünecek...
                    </p>
                </div>
            </div>
            
            <div class="info">
                <h3>🔧 Proje Bilgileri</h3>
                <ul>
                    <li><strong>Platform:</strong> Render.com</li>
                    <li><strong>Backend:</strong> FastAPI (Python)</li>
                    <li><strong>Blockchain:</strong> Solana Mainnet</li>
                    <li><strong>Özellik:</strong> WebSocket gerçek zamanlı takip</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Powered by FastAPI & Render.com | Solana-py-v2</p>
                <p>Deploy: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            </div>
        </div>
        
        <!-- Log Toggle Button -->
        <button class="log-toggle" onclick="toggleLogWindow()">📋 Log Görüntüle</button>
        
        <!-- Log Window -->
        <div class="log-window" id="logWindow" style="display: none;">
            <div class="log-header">
                <span>📊 Canlı Log Akışı</span>
                <button class="log-close" onclick="toggleLogWindow()">×</button>
            </div>
            <div class="log-content" id="logContent">
                <div class="log-entry">Sistem başlatıldı...</div>
            </div>
        </div>
        
        <script>
            // WebSocket bağlantısı
            let ws = null;
            let mintCount = 0;
            
            function connectWebSocket() {
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = protocol + '//' + window.location.host + '/ws';
                
                ws = new WebSocket(wsUrl);
                
                ws.onopen = () => {
                    document.getElementById('status').textContent = 'Online';
                    console.log('WebSocket bağlandı');
                    addLog('WebSocket bağlantısı başarılı', 'success');
                };
                
                ws.onmessage = (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        if (data.type === 'new_mint') {
                            addMint(data.data);
                            addLog('Yeni mint bulundu: ' + data.data.mint.substring(0, 10) + '...', 'success');
                        } else if (data.type === 'log') {
                            addLog(data.data.message, data.data.type);
                        } else if (data.type === 'ack') {
                            addLog('Mesaj alındı', 'info');
                        }
                    } catch (e) {
                        console.error('WebSocket mesaj işleme hatası:', e);
                    }
                };
                
                ws.onerror = () => {
                    document.getElementById('status').textContent = 'Error';
                    addLog('WebSocket bağlantı hatası', 'error');
                };
                
                ws.onclose = () => {
                    document.getElementById('status').textContent = 'Offline';
                    addLog('WebSocket bağlantısı kapatıldı, yeniden bağlanılıyor...', 'warning');
                    setTimeout(connectWebSocket, 3000);
                };
            }
            
            function addMint(mintData) {
                mintCount++;
                document.getElementById('totalMints').textContent = mintCount;
                document.getElementById('freshMints').textContent = mintCount;
                
                const mintList = document.getElementById('mintList');
                const mintDiv = document.createElement('div');
                mintDiv.className = 'mint-item';
                mintDiv.innerHTML = `
                    <div class="mint-address">${mintData.mint}</div>
                    <div style="color: #666; font-size: 0.85em; margin-top: 5px;">
                        ${new Date(mintData.foundAt).toLocaleString('tr-TR')}
                    </div>
                `;
                mintList.insertBefore(mintDiv, mintList.firstChild);
            }
            
            // API'den mevcut mint'leri çek
            async function loadMints() {
                try {
                    const response = await fetch('/api/mints');
                    const mints = await response.json();
                    document.getElementById('totalMints').textContent = mints.length;
                    document.getElementById('freshMints').textContent = mints.length;
                    
                    const mintList = document.getElementById('mintList');
                    if (mints.length > 0) {
                        mintList.innerHTML = '';
                        mints.forEach(mint => addMint(mint));
                    }
                } catch (error) {
                    console.error('Mint yüklenemedi:', error);
                }
            }
            
            // Log window toggle
            function toggleLogWindow() {
                const logWindow = document.getElementById('logWindow');
                const logToggle = document.querySelector('.log-toggle');
                
                if (logWindow.style.display === 'none') {
                    logWindow.style.display = 'flex';
                    logToggle.style.display = 'none';
                    addLog('Log penceresi açıldı', 'info');
                } else {
                    logWindow.style.display = 'none';
                    logToggle.style.display = 'block';
                }
            }
            
            // Log ekle fonksiyonu
            function addLog(message, type = 'info') {
                const logContent = document.getElementById('logContent');
                const logEntry = document.createElement('div');
                logEntry.className = 'log-entry ' + type;
                logEntry.textContent = '[' + new Date().toLocaleTimeString('tr-TR') + '] ' + message;
                logContent.appendChild(logEntry);
                
                // Otomatik scroll
                logContent.scrollTop = logContent.scrollHeight;
                
                // Maksimum 100 satır tut
                while (logContent.children.length > 100) {
                    logContent.removeChild(logContent.firstChild);
                }
            }
            
            // Sayfa yüklendiğinde
            window.addEventListener('load', () => {
                loadMints();
                connectWebSocket();
                addLog('WebSocket bağlantısı kuruluyor...', 'info');
            });
        </script>
    </body>
    </html>
    """

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Client'tan mesaj alındı
            await websocket.send_json({"type": "ack", "message": "Received"})
    except WebSocketDisconnect:
        websocket_clients.discard(websocket)

# API endpoints
@app.get("/api/mints")
async def get_mints():
    return JSONResponse(list(tracked_mints.values()))

@app.get("/api/stats")
async def get_stats():
    return JSONResponse({
        "total_mints": len(tracked_mints),
        "websocket_clients": len(websocket_clients)
    })

@app.get("/api/logs")
async def get_logs():
    return JSONResponse(log_buffer[-50:])  # Son 50 log

def add_log(message: str, log_type: str = "info"):
    """Log ekle ve WebSocket client'lara gönder"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "message": message,
        "type": log_type
    }
    log_buffer.append(log_entry)
    
    # Son 100 log'u tut
    if len(log_buffer) > 100:
        log_buffer.pop(0)
    
    # Tüm WebSocket client'lara gönder
    if websocket_clients:
        import asyncio
        disconnected = set()
        for client in websocket_clients:
            try:
                asyncio.create_task(client.send_json({"type": "log", "data": log_entry}))
            except:
                disconnected.add(client)
        # Bağlantısı kopanları temizle
        websocket_clients -= disconnected

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "solana-py-v2",
        "timestamp": datetime.now().isoformat()
    }

# API status
@app.get("/api/status")
async def get_status():
    return {
        "service": "solana-py-v2",
        "version": "1.0.0",
        "status": "running",
        "tracked_mints": len(tracked_mints),
        "active_connections": len(websocket_clients)
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)