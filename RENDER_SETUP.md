# 🚀 Render.com Deployment Guide

Bu proje Render.com'da deploy edilmek için optimize edilmiştir (512 MB RAM).

## 📋 Oluşturulan Dosyalar

✅ **main.py** - FastAPI backend (Port 8080)
✅ **requirements.txt** - Python bağımlılıkları
✅ **Dockerfile** - Docker container yapılandırması
✅ **Procfile** - Render için process tanımı
✅ **render.yaml** - Render yapılandırma dosyası (opsiyonel)

## 🔧 Render'da Setup Adımları

### 1. GitHub Repo'ya Push Et

```bash
git add .
git commit -m "Add Render-optimized FastAPI backend"
git push origin main
```

### 2. Render Dashboard'da

1. **New** → **Web Service**
2. GitHub repo'nu seç: `solana-py-v2`
3. Ayarlar:
   - **Name**: `solana-py-v2`
   - **Region**: `Singapore` (Tokyo yakını)
   - **Branch**: `main`
   - **Root Directory**: (boş bırak)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`

### 3. Environment Variables Ekle

Render Dashboard → **Environment** → **Add Secret**:

```
PORT=8080
HELIOUS_API_KEY=xxx
BINANCE_API_KEY=yyy
BINANCE_SECRET_KEY=zzz
PYTHONUNBUFFERED=1
```

### 4. Deploy

**Deploys** → **Manual Deploy** → **Deploy latest commit**

## ✅ Test Et

Deploy tamamlandıktan sonra:

```bash
curl https://solana-py-v2.onrender.com/health
```

Yanıt:
```json
{"ok": true, "timestamp": "...", "mints_tracked": 0, "clients_connected": 0}
```

## 📊 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/mints` - Tüm mint adresleri
- `GET /api/logs` - Son loglar
- `POST /api/mints/{address}` - Manuel mint ekle
- `WS /ws` - WebSocket (real-time updates)

## 🔄 Cursor → GitHub → Render Otomatik Deploy

1. **Render Settings** → **Auto-Deploy**: `Yes`
2. Cursor'da değişiklik yap
3. Git push:

```bash
git add .
git commit -m "update"
git push origin main
```

Render otomatik olarak yeni deploy başlatır! 🎉

## ⚠️ Sorun Giderme

### Build Hatası: "Exited with status 1"

- ✅ `requirements.txt` var mı kontrol et
- ✅ `Dockerfile` doğru mu kontrol et
- ✅ PORT 8080 kullanıldığından emin ol
- ✅ `main.py` içinde `if __name__ == "__main__"` kısmı var mı?

### Health Check Fail

- Render'da **Health Check Path**: `/health` olarak ayarla
- `main.py` içinde `/health` endpoint'i mevcut

### Out of Memory (512 MB limit)

- `--workers 1` kullanıyoruz (Dockerfile ve Procfile'da)
- Büyük log buffer'ları sınırlandırıldı (MAX_LOG_BUFFER = 100)
- In-memory storage hafif tutuldu

## 🎯 Sonraki Adımlar

1. ✅ Solana WebSocket bağlantısını `background_mint_tracker()` fonksiyonuna ekle
2. ✅ Helious/Binance API entegrasyonunu tamamla
3. ✅ Database ekle (PostgreSQL - Render'da ücretsiz plan var)

---

**Hazır! 🚀 Render'da backend'iniz çalışıyor olmalı.**

