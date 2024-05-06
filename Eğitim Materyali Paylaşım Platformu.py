from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QMessageBox, QListWidget, QListWidgetItem, QTextBrowser
import sqlite3

class Ders:
    def __init__(self, ad, icerik, ogretmen):
        self.ad = ad  # Dersin adı
        self.icerik = icerik  # Dersin içeriği
        self.ogretmen = ogretmen  # Dersin öğretmeni
        self.materyaller = []  # Dersin materyallerini saklamak için liste
        self.sorular = []  # Dersle ilgili soruları saklamak için liste

    def materyal_yukle(self, materyal):
        self.materyaller.append(materyal)  # Yeni bir materyal ekler

    def materyal_eris(self):
        return self.materyaller  # Dersin materyallerini döndürür

    def soru_sor(self, soru):
        self.sorular.append(soru)  # Yeni bir soru ekler

    def sorulari_goruntule(self):
        return self.sorular  # Dersle ilgili soruları döndürür

class Ogrenci:
    def __init__(self, ad, sinif):
        self.ad = ad  # Öğrencinin adı
        self.sinif = sinif  # Öğrencinin sınıfı

class Materyal:
    def __init__(self, ad, tur, icerik):
        self.ad = ad  # Materyalin adı
        self.tur = tur  # Materyalin türü
        self.icerik = icerik  # Materyalin içeriği

class EgitimMateryaliPlatformu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eğitim Materyali Paylaşım Platformu")
        self.init_ui()
        self.create_db()  # Veritabanını oluştur

    def init_ui(self):
        # Arayüz öğeleri oluşturuluyor
        self.layout = QVBoxLayout()
        self.label_ders_ad = QLabel("Ders Adı:")
        self.input_ders_ad = QLineEdit()
        self.label_materyal_ad = QLabel("Materyal Adı:")
        self.input_materyal_ad = QLineEdit()
        self.label_materyal_icerik = QLabel("Materyal İçeriği:")
        self.input_materyal_icerik = QTextEdit()
        self.label_soru = QLabel("Soru:")
        self.input_soru = QLineEdit()
        self.button_ders_olustur = QPushButton("Ders Oluştur")
        self.button_ders_olustur.clicked.connect(self.ders_olustur)
        self.button_materyal_yukle = QPushButton("Materyal Yükle")
        self.button_materyal_yukle.clicked.connect(self.materyal_yukle)
        self.button_soru_sor = QPushButton("Soru Sor")
        self.button_soru_sor.clicked.connect(self.soru_sor)
        self.liste_dersler = QListWidget()
        self.liste_dersler.itemClicked.connect(self.ders_secildi)
        self.label_materyaller = QLabel("Materyaller:")
        self.text_materyaller = QTextBrowser()
        self.label_sorular = QLabel("Sorular:")
        self.text_sorular = QTextBrowser()

        # Arayüz öğeleri düzenleniyor
        self.layout.addWidget(self.label_ders_ad)
        self.layout.addWidget(self.input_ders_ad)
        self.layout.addWidget(self.button_ders_olustur)
        self.layout.addWidget(self.label_materyal_ad)
        self.layout.addWidget(self.input_materyal_ad)
        self.layout.addWidget(self.label_materyal_icerik)
        self.layout.addWidget(self.input_materyal_icerik)
        self.layout.addWidget(self.button_materyal_yukle)
        self.layout.addWidget(self.label_soru)
        self.layout.addWidget(self.input_soru)
        self.layout.addWidget(self.button_soru_sor)
        self.layout.addWidget(self.liste_dersler)
        self.layout.addWidget(self.label_materyaller)
        self.layout.addWidget(self.text_materyaller)
        self.layout.addWidget(self.label_sorular)
        self.layout.addWidget(self.text_sorular)
        self.setLayout(self.layout)

        self.dersler = {}  # Derslerin saklanacağı sözlük

    def ders_olustur(self):
        ders_ad = self.input_ders_ad.text()
        if not ders_ad:
            QMessageBox.warning(self, "Uyarı", "Lütfen ders adını girin!")
            return

        if ders_ad in self.dersler:
            QMessageBox.warning(self, "Uyarı", "Bu ders zaten var!")
            return

        self.dersler[ders_ad] = Ders(ders_ad, "", "")
        self.liste_dersler.addItem(ders_ad)
        self.insert_course_to_db(ders_ad)  # Veritabanına dersi ekle
        QMessageBox.information(self, "Bilgi", "Ders başarıyla oluşturuldu!")

    def ders_secildi(self, item):
        ders_ad = item.text()
        ders = self.dersler[ders_ad]
        materyaller = ders.materyal_eris()
        sorular = ders.sorulari_goruntule()
        self.text_materyaller.clear()
        self.text_sorular.clear()
        for materyal in materyaller:
            self.text_materyaller.append(f"Materyal Adı: {materyal.ad}\nMateryal Türü: {materyal.tur}\nMateryal İçeriği:\n{materyal.icerik}\n")
        for soru in sorular:
            self.text_sorular.append(f"Soru: {soru}\n")

    def materyal_yukle(self):
        ders_ad = self.input_ders_ad.text()
        materyal_ad = self.input_materyal_ad.text()
        materyal_icerik = self.input_materyal_icerik.toPlainText()

        if not ders_ad or not materyal_ad or not materyal_icerik:
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurun!")
            return

        if ders_ad not in self.dersler:
            QMessageBox.warning(self, "Uyarı", "Belirtilen ders bulunamadı!")
            return

        ders = self.dersler[ders_ad]
        materyal = Materyal(materyal_ad, "pdf", materyal_icerik)
        ders.materyal_yukle(materyal)
        self.insert_material_to_db(ders_ad, materyal_ad, "pdf", materyal_icerik)  # Veritabanına materyali ekle

        QMessageBox.information(self, "Bilgi", "Materyal başarıyla yüklendi!")

    def soru_sor(self):
        ders_ad = self.input_ders_ad.text()
        soru = self.input_soru.text()

        if not ders_ad or not soru:
            QMessageBox.warning(self, "Uyarı", "Lütfen ders adını ve soruyu girin!")
            return

        if ders_ad not in self.dersler:
            QMessageBox.warning(self, "Uyarı", "Belirtilen ders bulunamadı!")
            return

        ders = self.dersler[ders_ad]
        ders.soru_sor(soru)
        self.insert_question_to_db(ders_ad, soru)  # Veritabanına soruyu ekle

        QMessageBox.information(self, "Bilgi", "Soru başarıyla gönderildi!")

    def create_db(self):
        # Veritabanını oluştur ve bağlan
        self.conn = sqlite3.connect("egitim_materyalleri.db")
        self.cursor = self.conn.cursor()

        # Dersler tablosunu oluştur
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS dersler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL UNIQUE
            )
        """)

        # Materyaller tablosunu oluştur
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS materyaller (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_id INTEGER NOT NULL,
                ad TEXT NOT NULL,
                tur TEXT NOT NULL,
                icerik TEXT NOT NULL,
                FOREIGN KEY(ders_id) REFERENCES dersler(id)
            )
        """)

        # Sorular tablosunu oluştur
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sorular (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ders_id INTEGER NOT NULL,
                soru TEXT NOT NULL,
                FOREIGN KEY(ders_id) REFERENCES dersler(id)
            )
        """)

        self.conn.commit()

    def insert_course_to_db(self, ders_ad):
        # Dersi veritabanına ekle
        self.cursor.execute("INSERT INTO dersler (ad) VALUES (?)", (ders_ad,))
        self.conn.commit()

    def insert_material_to_db(self, ders_ad, materyal_ad, tur, icerik):
        # Dersin ID'sini al
        self.cursor.execute("SELECT id FROM dersler WHERE ad=?", (ders_ad,))
        ders_id = self.cursor.fetchone()[0]

        # Materyali veritabanına ekle
        self.cursor.execute("INSERT INTO materyaller (ders_id, ad, tur, icerik) VALUES (?, ?, ?, ?)",
                            (ders_id, materyal_ad, tur, icerik))
        self.conn.commit()

    def insert_question_to_db(self, ders_ad, soru):
        # Dersin ID'sini al
        self.cursor.execute("SELECT id FROM dersler WHERE ad=?", (ders_ad,))
        ders_id = self.cursor.fetchone()[0]

        # Soruyu veritabanına ekle
        self.cursor.execute("INSERT INTO sorular (ders_id, soru) VALUES (?, ?)", (ders_id, soru))
        self.conn.commit()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = EgitimMateryaliPlatformu()
    window.show()
    sys.exit(app.exec_())
