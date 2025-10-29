# 🔗 GitHub'a Bağlama Rehberi

## ⚠️ Mevcut Durum
- ❌ Git repository henüz oluşturulmadı
- ❌ GitHub'a bağlantı yok
- ❌ Render otomatik deploy çalışmıyor

## ✅ Adım Adım Bağlama

### 1️⃣ Git Kurulumu Kontrol Et

PowerShell'de kontrol et:
```powershell
git --version
```

Eğer hata verirse Git kur:
- https://git-scm.com/download/win
- Kurulum sonrası PowerShell'i yeniden başlat

### 2️⃣ GitHub'da Repo Oluştur

1. https://github.com/login → Giriş yap
2. **New Repository** butonuna tıkla
3. Repo adı: `solana-py-v2`
4. **Public** veya **Private** seç
5. ⚠️ **"Initialize with README" işaretleme!** (boş repo olsun)
6. **Create repository** tıkla

### 3️⃣ Cursor/Terminal'de Git Bağlantısı

**PowerShell'de şu komutları sırayla çalıştır:**

```powershell
# 1. Proje klasörüne git
cd C:\Users\idris\Desktop\memee

# 2. Git repository başlat
git init

# 3. Tüm dosyaları ekle
git add .

# 4. İlk commit
git commit -m "Initial commit: Render-optimized FastAPI backend"

# 5. GitHub repo'yu remote olarak ekle
# ⚠️ nano-id kullanıcı adınızla değiştirin!
git remote add origin https://github.com/nano-id/solana-py-v2.git

# 6. Ana branch'i main olarak ayarla
git branch -M main

# 7. GitHub'a push et
git push -u origin main
```

### 4️⃣ GitHub Authentication

Push yaparken GitHub kullanıcı adı/şifre veya token isteyebilir:

**Yöntem 1: Personal Access Token (Önerilen)**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Generate new token (classic)**
3. Scopes: `repo` seç
4. Token'ı kopyala
5. Push yaparken:
   - Username: GitHub kullanıcı adın
   - Password: Token'ı yapıştır

**Yöntem 2: GitHub CLI**
```powershell
winget install --id GitHub.cli
gh auth login
```

### 5️⃣ Render'a Bağla

1. Render Dashboard → **New** → **Web Service**
2. **Connect GitHub account** (eğer bağlı değilse)
3. **solana-py-v2** repo'sunu seç
4. Ayarları yap:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
5. **Environment Variables** ekle:
   - `PORT=8080`
   - `HELIOUS_API_KEY=xxx`
   - `BINANCE_API_KEY=yyy`
   - `BINANCE_SECRET_KEY=zzz`
6. **Create Web Service**

### 6️⃣ Otomatik Deploy Aktif Et

Render Dashboard → Settings → **Auto-Deploy**: `Yes`

Artık her `git push` yaptığında Render otomatik deploy edecek! 🎉

## 🔄 Günlük Kullanım

Dosyaları değiştirdikten sonra:

```powershell
cd C:\Users\idris\Desktop\memee
git add .
git commit -m "Açıklayıcı mesaj"
git push origin main
```

Render otomatik olarak yeni deploy başlatır!

## ❓ Sorun Giderme

### "git: command not found"
→ Git kurulmamış. https://git-scm.com/download/win adresinden kur.

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/nano-id/solana-py-v2.git
```

### "Authentication failed"
→ GitHub Personal Access Token kullan veya GitHub CLI ile login yap.

### "Repository not found"
→ GitHub'da repo adını kontrol et (`nano-id/solana-py-v2`)

