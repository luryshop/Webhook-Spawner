# 🚀 LuryShop Webhook Manager

**LuryShop Webhook Manager**, Discord Webhook'larını yönetmek, test etmek ve toplu mesaj gönderimi sağlamak için **Python** ve **CustomTkinter** ile geliştirilmiş modern bir masaüstü uygulamasıdır.

Kullanıcı dostu arayüzü sayesinde kod bilgisi gerektirmeden webhook işlemlerinizi gerçekleştirebilirsiniz.

---

## 🌟 Özellikler

* **🎨 Modern Arayüz:** CustomTkinter altyapısı ile şık, "Dark/Orange" temalı tasarım.
* **📋 Webhook Listesi Yönetimi:** Sınırsız sayıda Webhook ekleyip listeden tek tıkla silebilirsiniz.
* **⚡ Multi-Thread Yapısı:** Gönderim işlemi sırasında arayüz donmaz, durdurma işlemi anlık çalışır.
* **🛡️ Rate Limit Koruması:** Discord'un hız limitine (429 Too Many Requests) takıldığında sistem otomatik olarak bekler ve devam eder.
* **📝 Canlı Log Sistemi:** Gönderim durumunu, hataları ve başarı oranlarını anlık olarak takip edebilirsiniz.
* **🔢 Tekrar Ayarı:** Mesajın kaç kez gönderileceğini belirleyebilirsiniz.

---

## 🛠️ Kurulum

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin.

### Gereksinimler
* Python 3.x
* İnternet bağlantısı

### 1. Kütüphanelerin Yüklenmesi
Terminal veya komut istemcisine (CMD) aşağıdaki komutu yazarak gerekli kütüphaneleri yükleyin:

```bash
pip install customtkinter requests