# Kurulum Talimatları 📦

## 1. Node.js Kurulumu

**Node.js** henüz kurulu değil. Lütfen aşağıdaki adımları takip edin:

### Windows için:
1. https://nodejs.org adresinden Node.js LTS sürümünü indirin
2. İndirilen `.msi` dosyasını çalıştırın
3. Kurulum sihirbazını takip edin (Next tuşlarına basın)
4. Kurulum tamamlandıktan sonra **PowerShell'i kapatıp yeniden açın**

### Doğrulama:
Kurulumun başarılı olduğunu kontrol etmek için:
```bash
node --version
npm --version
```

## 2. Projeyi Çalıştırma

Kurulum tamamlandıktan sonra:

```bash
# Bağımlılıkları yükle
npm install

# Uygulamayı başlat
npm start
```

## 3. Web Arayüzüne Erişim

Uygulama başladıktan sonra tarayıcınızda şu adrese gidin:

**http://localhost:3000**

## Özellikler ✨

- 🎨 Modern ve güzel bir web arayüzü
- 📊 Gerçek zamanlı istatistikler
- 🔔 Yeni mint'lerde bildirim animasyonu
- 🌐 WebSocket ile canlı güncellemeler
- 📝 CSV dosyasına otomatik kayıt
- ⚡ 0.6 saniye filtreleme

## Sorun Giderme

### Node.js kurulu ama çalışmıyor:
- PowerShell'i kapatıp yeniden açın
- Bilgisayarı yeniden başlatın

### Port 3000 kullanımda:
- `app.js` dosyasında `PORT` değişkenini değiştirin
- Veya farklı bir port numarası deneyin

### Bağlantı hatası:
- İnternet bağlantınızı kontrol edin
- Firewall ayarlarınızı kontrol edin


