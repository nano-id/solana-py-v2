# 🚨 Render Manuel Deploy Rehberi

## Durum: Otomatik deploy çalışmıyor

Manuel deploy yapmanız gerekiyor.

## 📋 Adım Adım Manuel Deploy

### 1. Render Dashboard'a Gidin
https://dashboard.render.com/

### 2. Servisinizi Bulun
- Sol tarafta **"Web Services"** tıklayın
- **"solana-py-v2"** servisinizi bulun

### 3. Deploy Butonuna Tıklayın
- Servisinizin üzerine gelin
- **"Manual Deploy"** butonuna tıklayın
- **"Deploy latest commit"** seçin

VEYA

### 4. Clear Build Cache ile Deploy
1. Servis sayfasına girin
2. **Deploys** sekmesine gidin
3. Sağ üstte **"Clear build cache"** tıklayın
4. **"Manually deploy"** → **"Deploy latest commit"**

### 5. Bekleyin
- Build süresi: 3-5 dakika
- Logs sekmesinde ilerlemeyi izleyin

### 6. Sonucu Kontrol Edin

#### Logs'da görünen olumlu mesaj:
```
✓ Build successful
INFO:     Uvicorn running on http://0.0.0.0:xxxxx
```

#### Logs'da görünen hata mesajı:
Eğer hata varsa şu şekilde olacak:
```
✗ Build failed
Error: ...
```

## 🔍 Alternatif: Yeni Bir Servis Oluştur

Eğer mevcut servis çalışmıyorsa yeni bir tane oluşturun:

### 1. Yeni Web Service
Dashboard → **"New +"** → **"Web Service"**

### 2. GitHub Repo Seçin
- Repository: **nano-id/solana-py-v2**
- Branch: **main**

### 3. Ayarları Girin
- **Name:** solana-py-v2
- **Region:** Frankfurt (EU) veya herhangi bir
- **Branch:** main
- **Runtime:** Docker
- **Auto-Deploy:** Yes

### 4. Environment Variables (varsa)
Henüz eklemeyin, basit başlayalım.

### 5. Create Web Service
Oluştur butonuna tıklayın.

## 🎯 Hangi Durumda Olduğunuzu Anlamak İçin

Render Dashboard'da:
1. Servis sayfanıza gidin
2. **Events** sekmesine bakın
3. En son deploy'un durumunu kontrol edin:
   - ✅ Success → Site çalışmalı (cache sorunu olabilir)
   - ❌ Failed → Logs'a bakın
   - 🟡 In Progress → Bekleyin

## 📞 Bana Göndermeniz Gerekenler

Eğer hala çalışmıyorsa:

1. **Deploy durumu:** Success/Failed/In Progress
2. **Logs'tan son 20 satır** (kopyalayın)
3. **Settings → Deploys ayarları:** Auto-deploy ON/OFF?

## 🚀 Hızlı Test

Tarayıcıda:
```
https://solana-py-v2.onrender.com/health
```
Eğer bu bile boşsa, servis hiç ayağa kalkmamış demektir.
