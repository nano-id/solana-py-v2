# 🔧 Render Deploy Sorun Giderme

## ⚠️ Yaygın Sorunlar ve Çözümler

### 1. Build Command Hatası

**Sorun:** `pip install` çalışmıyor

**Çözüm:** Render Dashboard'da:
- Build Command: `pip install --upgrade pip && pip install -r requirements.txt`

### 2. PORT Sorunu

**Sorun:** Port belirtilmemiş veya yanlış

**Çözüm:** 
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
- Environment Variable: `PORT=8080` (Render otomatik ayarlar, ama manuel de eklenebilir)

### 3. Python Version Sorunu

**Sorun:** Yanlış Python versiyonu

**Çözüm:** `runtime.txt` dosyası eklendi: `python-3.11.0`

### 4. Dockerfile vs Procfile

Render iki yöntem destekler:

**Yöntem 1: Native Build (Önerilen - Daha Hızlı)**
- `Procfile` kullanır
- `render.yaml` opsiyonel
- Dockerfile gereksiz

**Yöntem 2: Docker Build**
- `Dockerfile` kullanır
- Daha kontrollü ama yavaş

## ✅ Render Dashboard Ayarları

### Build & Deploy

**Build Command:**
```
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
```

### Environment Variables

Ekle:
- `PYTHONUNBUFFERED=1` (log'lar için önemli)
- `PORT=8080` (opsiyonel - Render otomatik ayarlar)

### Health Check

- **Health Check Path:** `/health`

### Plan

- Free plan kullanıyorsanız: **Auto-Deploy: OFF** (manuel deploy daha güvenilir)
- Starter/Standard plan: **Auto-Deploy: ON** yapabilirsiniz

## 🔍 Build Log Kontrolü

Render Dashboard → Deploys → Son deploy'a tıkla → Build Logs:

✅ **Başarılı build:**
```
Successfully installed fastapi uvicorn...
```

❌ **Hata varsa:**
- `pip install` hatası → requirements.txt kontrol et
- `Module not found` → requirements.txt'e ekle
- `Port already in use` → Procfile/startCommand kontrol et

## 🚀 Manuel Deploy

1. Render Dashboard → **solana-py-v2** service
2. **Deploys** sekmesi
3. **Manual Deploy** → **Deploy latest commit**

## 📋 Checklist

- [ ] `Procfile` mevcut ve doğru
- [ ] `requirements.txt` mevcut ve güncel
- [ ] `runtime.txt` mevcut (opsiyonel ama önerilir)
- [ ] `main.py` içinde `if __name__ == "__main__"` var
- [ ] Health check endpoint `/health` mevcut
- [ ] PORT environment variable kullanılıyor
- [ ] CORS middleware aktif

## 💡 Hızlı Çözüm

Eğer hala çalışmıyorsa:

1. **Render'da service'i sil**
2. **Yeni service oluştur:**
   - Type: **Web Service**
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
3. **Environment Variables ekle:**
   - `PYTHONUNBUFFERED=1`
4. **Deploy et**

