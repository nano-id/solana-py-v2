# Solana Meme Coin Mint Tracker 🪙

Bu sistem, Solana WebSocket üzerinden logları çeker, 44 karakterlik mint adreslerini ayrıştırır ve meme coinlerin doğumundan 0.6 saniye içinde oluşturulanları filtreler.

**✨ Yeni: Güzel bir web arayüzü ile mint'leri görüntüleyin!**

## Özellikler

- ✅ Solana WebSocket üzerinden gerçek zamanlı log takibi
- ✅ 44 karakterlik mint adreslerini otomatik ayrıştırma
- ✅ Token doğumundan 0.6 saniye içindeki fresh mint'leri filtreleme
- ✅ **Modern web arayüzü ile mint'leri görüntüleme**
- ✅ Gerçek zamanlı istatistikler
- ✅ Bulunan mint adreslerini CSV dosyasına kaydetme
- ✅ Otomatik yeniden bağlanma
- ✅ Duplicate kontrolü

## Gereksinimler

- Node.js 16 veya üzeri
- npm (Node.js ile birlikte gelir)

## Kurulum

### 1. Node.js Kurulumu

Node.js kurulu değilse:
1. https://nodejs.org adresinden Node.js LTS sürümünü indirin
2. Kurulum sihirbazını takip edin
3. PowerShell'i kapatıp yeniden açın

### 2. Bağımlılıkları Yükleme

```bash
npm install
```

### 3. Uygulamayı Başlatma

```bash
npm start
```

### 4. Web Arayüzüne Erişim

Tarayıcınızda şu adrese gidin:

**http://localhost:3000**

## Nasıl Çalışır?

1. **WebSocket Bağlantısı**: Solana mainnet'e WebSocket ile bağlanır
2. **Log Takibi**: SPL Token programından gelen logları dinler
3. **Adres Ayrıştırma**: Loglar içinden 44 karakterlik Solana adreslerini bulur
4. **Yaş Kontrolü**: Bulunan mint adreslerinin yaşını kontrol eder
5. **Filtreleme**: 0.6 saniye içinde oluşturulanları filtreler
6. **Kaydetme**: Geçerli mint adreslerini `mint_addresses.csv` dosyasına kaydeder
7. **Görüntüleme**: Web arayüzünde gerçek zamanlı olarak gösterir

## Web Arayüzü Özellikleri

- 📊 Toplam mint sayısı, fresh mint sayısı gibi istatistikler
- 🔔 Yeni mint geldiğinde animasyonlu bildirim
- 🔗 Solscan'da görüntüleme linki
- 📱 Responsive tasarım
- 🌈 Modern ve güzel gradyan tasarım

## Çıktı Formatı

CSV dosyası şu formatta kayıt tutar:
```
timestamp,mint_address,transaction_signature
```

## Konfigürasyon

`app.js` dosyasında şu parametreleri değiştirebilirsiniz:

- `MAX_AGE_SECONDS`: Mint yaşı filtresi (varsayılan: 0.6)
- `SOLANA_WS_ENDPOINT`: WebSocket endpoint
- `HTTP_ENDPOINT`: HTTP RPC endpoint
- `PORT`: Web sunucusu portu (varsayılan: 3000)

## Dosya Yapısı

```
memee/
├── app.js              # Ana sunucu ve WebSocket işlemleri
├── index.js            # Eski konsol versiyonu
├── public/
│   └── index.html      # Web arayüzü
├── package.json        # Bağımlılıklar
├── README.md          # Bu dosya
└── KURULUM.md         # Detaylı kurulum talimatları
```

## Notlar

- Public Solana RPC endpoint'leri rate limit'e takılabilir
- Daha iyi performans için kendi RPC endpoint'inizi kullanın
- Meme coin tracking için özel program ID'leri ekleyebilirsiniz

## Yardım

Detaylı kurulum ve sorun giderme için `KURULUM.md` dosyasına bakın.

## Lisans

MIT
