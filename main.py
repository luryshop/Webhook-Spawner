import customtkinter as ctk
import threading
import time
import requests
from datetime import datetime


ctk.set_appearance_mode("Orange")
ctk.set_default_color_theme("blue")

class WebhookManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        
        self.title("LuryShop")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.webhook_listesi = []
        self.is_running = False

    
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.sidebar, text="Webhook Spawner Panel", font=("Arial", 20, "bold")).pack(pady=20)


        ctk.CTkLabel(self.sidebar, text="Mesaj İçeriği:", anchor="w").pack(fill="x", padx=15, pady=(10,0))
        self.entry_message = ctk.CTkTextbox(self.sidebar, height=80)
        self.entry_message.pack(fill="x", padx=15, pady=5)
        self.entry_message.insert("0.0", "discord.gg/luryshop")

        ctk.CTkLabel(self.sidebar, text="Tekrar sayısı:", anchor="w").pack(fill="x", padx=15, pady=(15,0))
        self.entry_count = ctk.CTkEntry(self.sidebar)
        self.entry_count.pack(fill="x", padx=15, pady=5)
        self.entry_count.insert(0, "1")


        self.lbl_stats = ctk.CTkLabel(self.sidebar, text="Webhook Sayısı: 0", font=("Arial", 12, "bold"), text_color="#1fcf7a")
        self.lbl_stats.pack(pady=20)


        self.btn_start = ctk.CTkButton(self.sidebar, text="BAŞLAT (Hızlı)", fg_color="green", hover_color="darkgreen", height=40, command=self.baslat_thread)
        self.btn_start.pack(padx=15, pady=10, fill="x")

        self.btn_stop = ctk.CTkButton(self.sidebar, text="DURDUR", fg_color="red", hover_color="darkred", height=30, state="disabled", command=self.durdur)
        self.btn_stop.pack(padx=15, pady=5, fill="x")

        self.btn_clear_log = ctk.CTkButton(self.sidebar, text="Logları Temizle", fg_color="gray", command=self.loglari_temizle)
        self.btn_clear_log.pack(padx=15, pady=20, fill="x", side="bottom")

 
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


        self.top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.entry_url = ctk.CTkEntry(self.top_bar, placeholder_text="Webhook Linki Yapıştır...", width=500)
        self.entry_url.pack(side="left", padx=(0, 10), fill="x", expand=True)

        self.btn_add = ctk.CTkButton(self.top_bar, text="+ Ekle", width=100, command=self.webhook_ekle)
        self.btn_add.pack(side="right")


        self.scroll_list = ctk.CTkScrollableFrame(self.main_frame, label_text="Ekli Webhook Listesi")
        self.scroll_list.grid(row=1, column=0, sticky="nsew")

  
        self.log_box = ctk.CTkTextbox(self.main_frame, height=150)
        self.log_box.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        self.log_box.configure(state="disabled")

        self.log_yaz("Sistem Hazır.")



    def webhook_ekle(self):
        url = self.entry_url.get().strip()
        if not url.startswith("http"):
            self.log_yaz("HATA: Geçersiz Link!")
            return
        
        if url in self.webhook_listesi:
            self.log_yaz("BİLGİ: Bu link zaten ekli.")
            return

        self.webhook_listesi.append(url)
        self.listeyi_guncelle()
        self.entry_url.delete(0, "end")
        self.log_yaz(f"Eklendi: ...{url[-10:]}")

    def webhook_cikar(self, url):
        if url in self.webhook_listesi:
            self.webhook_listesi.remove(url)
            self.listeyi_guncelle()
            self.log_yaz("Webhook silindi.")

    def listeyi_guncelle(self):
        self.lbl_stats.configure(text=f"Webhook Sayısı: {len(self.webhook_listesi)}")
        

        for widget in self.scroll_list.winfo_children():
            widget.destroy()


        for url in self.webhook_listesi:
            row = ctk.CTkFrame(self.scroll_list)
            row.pack(fill="x", pady=2)

            lbl = ctk.CTkLabel(row, text=url, anchor="w")
            lbl.pack(side="left", padx=10, fill="x", expand=True)


            btn_del = ctk.CTkButton(row, text="SİL", width=60, fg_color="#c92a2a", hover_color="#8f1e1e",
                                    command=lambda u=url: self.webhook_cikar(u))
            btn_del.pack(side="right", padx=5, pady=5)

    def log_yaz(self, mesaj):
        self.log_box.configure(state="normal")
        zaman = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{zaman}] {mesaj}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def loglari_temizle(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("0.0", "end")
        self.log_box.configure(state="disabled")
        self.log_yaz("Loglar temizlendi.")

    def durdur(self):
        self.is_running = False
        self.log_yaz("!!! İşlem Durduruluyor... !!!")

    def baslat_thread(self):
        if not self.webhook_listesi:
            self.log_yaz("HATA: Liste boş!")
            return
        threading.Thread(target=self.gonderim_islemi, daemon=True).start()

    def gonderim_islemi(self):
        try:
            adet = int(self.entry_count.get())
            mesaj = self.entry_message.get("0.0", "end").strip()
        except:
            self.log_yaz("HATA: Sayı veya mesaj hatalı.")
            return

        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.entry_count.configure(state="disabled")

        self.log_yaz(f"--- BAŞLATILDI: {adet} Tur ---")

        toplam_basarili = 0

        for i in range(adet):
            if not self.is_running: break
            
   
            for url in self.webhook_listesi:
                if not self.is_running: break
                
                payload = {"content": mesaj}
                
                try:
  
                    r = requests.post(url, json=payload, timeout=5)

                    if r.status_code == 204:
                        toplam_basarili += 1

                    elif r.status_code == 429:

                        bekle = r.json().get('retry_after', 1)
                        self.log_yaz(f"HIZ LİMİTİ! {bekle}sn bekleniyor...")
                        time.sleep(bekle) 
                    else:
                        self.log_yaz(f"Hata: {r.status_code}")

                except Exception as e:
                    self.log_yaz(f"Bağlantı sorunu: {e}")

        self.is_running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.entry_count.configure(state="normal")
        self.log_yaz(f"--- BİTTİ. Toplam {toplam_basarili} mesaj gönderildi. ---")

if __name__ == "__main__":
    app = WebhookManagerApp()
    app.mainloop()