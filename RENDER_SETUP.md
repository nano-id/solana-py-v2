# 🚀 Render Setup Kontrol Listesi

## ✅ Yapıldı
1. ✅ Dockerfile düzeltildi - Render PORT support
2. ✅ requirements.txt güncellendi (solana kaldırıldı)
3. ✅ main.py hazır (mavi tema + Solana tracker)
4. ✅ GitHub'a push edildi

## 📋 Render Dashboard'da Yapmanız Gerekenler

### 1. Auto-Deploy Kontrolü
**Path:** Service Settings → Deploys
- ✅ Auto Deploy: **ON** olmalı
- ✅ Branch: **main**
- Eğer OFF ise → "Enable Auto-Deploy" butonuna tıklayın

### 2. Repo/Branch Kontrolü
**Path:** Service Settings → Git
- Repository: `nano-id/solana-py-v2` 
- Branch: `main`
- "Change Repo" ile yanlışsa düzeltin

### 3. Manual Deploy (Hemen Test)
**Path:** Deploys tab
- "Manual Deploy" → "Deploy latest commit"
- VEYA
- "Clear build cache" → "Deploy latest commit"

### 4. Logs Kontrolü
**Path:** Logs tab
Başarılı olursa göreceğiniz:
```
INFO:     Uvicorn running on http://0.0.0.0:10000
INFO:     Application startup complete.
```

Hata varsa log'ları bana gönderin.

## 🔍 Test Etme

### Health Check
```
https://solana-py-v2.onrender.com/health
```
Bu sayfa `{"status":"healthy"}` döndürmeli.

### Ana Sayfa
```
https://solana-py-v2.onrender.com/
```
Mavi temalı Solana tracker sayfası görünmeli.

## ⏱️ Bekleme Süresi
- İlk deploy: 5-10 dakika
- Sonraki deploys: 2-5 dakika

## 🐛 Hala Çalışmıyorsa

1. **Events/Deploys** sekmesinde "Failed" var mı kontrol edin
2. **Logs** sekmesinde hata mesajını bulun
3. **Redeploy** → "Clear build cache" ile tekrar deneyin

## 📧 Hata Mesajı Gönderme
Render dashboard'dan hata mesajını kopyalayıp bana gönderin.