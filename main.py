import sys
import os
import shutil
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                            QWidget, QFileDialog, QMessageBox, QLabel, QLineEdit,
                            QHBoxLayout, QListWidget, QProgressBar, QFrame, QCheckBox,
                            QToolButton)
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor
from cryptography.fernet import Fernet
import base64

class EncryptionWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    password_error = pyqtSignal()

    def __init__(self, file_path, key, is_encrypt=True):
        super().__init__()
        self.file_path = file_path
        self.key = key
        self.is_encrypt = is_encrypt
        self.f = Fernet(key)
        self.output_path = None

    def run(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Dosya bulunamadı: {self.file_path}")

            file_size = os.path.getsize(self.file_path)
            if file_size == 0:
                raise ValueError("Dosya boş!")

            if self.is_encrypt:
                self.output_path = self.file_path + '.encrypted'
                with open(self.file_path, 'rb') as file:
                    data = file.read()
                encrypted_data = self.f.encrypt(data)
                with open(self.output_path, 'wb') as out_file:
                    out_file.write(encrypted_data)
            else:
                if not self.file_path.endswith('.encrypted'):
                    raise ValueError("Bu dosya şifrelenmiş bir dosya değil!")
                
                self.output_path = self.file_path.replace('.encrypted', '')
                with open(self.file_path, 'rb') as file:
                    data = file.read()
                try:
                    decrypted_data = self.f.decrypt(data)
                    with open(self.output_path, 'wb') as out_file:
                        out_file.write(decrypted_data)
                except Exception as e:
                    if os.path.exists(self.output_path):
                        os.remove(self.output_path)
                    self.password_error.emit()
                    return

            self.finished.emit(self.file_path)
        except Exception as e:
            self.error.emit(str(e))

class OKANShield(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OKAN Shield - Dosya Şifreleme")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QPushButton {
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            #addButton {
                background-color: #2ecc71;
            }
            #encryptButton {
                background-color: #e74c3c;
            }
            #decryptButton {
                background-color: #3498db;
            }
            #selectAllButton {
                background-color: #95a5a6;
            }
            #clearButton {
                background-color: #95a5a6;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                padding: 5px;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 4px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
            QToolButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QToolButton:hover {
                opacity: 0.9;
            }
        """)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık
        title_label = QLabel("OKAN Shield")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Şifre girişi alanı
        password_layout = QHBoxLayout()
        self.password_label = QLabel("Şifre:")
        self.password_label.setStyleSheet("font-size: 14px;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumWidth(300)
        
        # Şifre göster/gizle butonu
        self.toggle_password = QToolButton()
        self.toggle_password.setText("👁")
        self.toggle_password.setCheckable(True)
        self.toggle_password.clicked.connect(self.toggle_password_visibility)
        
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_password)
        main_layout.addLayout(password_layout)
        
        # Dosya listesi ve seçim kontrolleri
        file_controls_layout = QHBoxLayout()
        
        # Tümünü seç butonu
        self.select_all_button = QPushButton("Tümünü Seç")
        self.select_all_button.setObjectName("selectAllButton")
        self.select_all_button.clicked.connect(self.toggle_select_all)
        file_controls_layout.addWidget(self.select_all_button)
        
        # Temizle butonu
        self.clear_button = QPushButton("Listeyi Temizle")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.clicked.connect(self.clear_file_list)
        file_controls_layout.addWidget(self.clear_button)
        
        main_layout.addLayout(file_controls_layout)
        
        # Dosya listesi
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("font-size: 14px;")
        self.file_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        main_layout.addWidget(self.file_list)
        
        # Butonlar için yatay layout
        button_layout = QHBoxLayout()
        
        # Dosya ekle butonu
        self.add_files_button = QPushButton("📁 Dosya Ekle")
        self.add_files_button.setObjectName("addButton")
        self.add_files_button.clicked.connect(self.add_files)
        button_layout.addWidget(self.add_files_button)
        
        # Şifrele butonu
        self.encrypt_button = QPushButton("🔒 Seçili Dosyaları Şifrele")
        self.encrypt_button.setObjectName("encryptButton")
        self.encrypt_button.clicked.connect(self.encrypt_files)
        button_layout.addWidget(self.encrypt_button)
        
        # Çöz butonu
        self.decrypt_button = QPushButton("🔓 Seçili Dosyaları Çöz")
        self.decrypt_button.setObjectName("decryptButton")
        self.decrypt_button.clicked.connect(self.decrypt_files)
        button_layout.addWidget(self.decrypt_button)
        
        main_layout.addLayout(button_layout)
        
        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Durum çubuğu
        self.statusBar().showMessage("Hazır")

    def generate_key(self, password):
        try:
            # Şifreyi UTF-8'e çevir ve 32 byte'a tamamla
            password_bytes = password.encode('utf-8')
            if len(password_bytes) < 32:
                password_bytes = password_bytes + b'\0' * (32 - len(password_bytes))
            elif len(password_bytes) > 32:
                password_bytes = password_bytes[:32]
            
            # Base64 formatına çevir
            key = base64.urlsafe_b64encode(password_bytes)
            return key
        except Exception as e:
            self.show_message_box("Hata", f"Şifre oluşturma hatası: {str(e)}", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            return None

    def toggle_password_visibility(self):
        if self.toggle_password.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_password.setText("👁")
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_password.setText("👁")
    
    def toggle_select_all(self):
        if self.file_list.count() > 0:
            if self.file_list.selectedItems():
                self.file_list.clearSelection()
            else:
                self.file_list.selectAll()
    
    def clear_file_list(self):
        self.file_list.clear()
        self.statusBar().showMessage("Liste temizlendi")
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Dosya Seç",
            "",
            "Tüm Dosyalar (*.*)"
        )
        if files:
            self.file_list.addItems(files)
            self.statusBar().showMessage(f"{len(files)} dosya eklendi")
    
    def show_message_box(self, title, message, buttons, default_button=None):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f2f5;
                min-width: 400px;
                min-height: 150px;
            }
            QMessageBox QLabel {
                font-size: 14px;
                margin: 20px;
            }
            QMessageBox QPushButton {
                min-width: 120px;
                min-height: 40px;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid transparent;
            }
            QMessageBox QPushButton:hover {
                border: 2px solid white;
            }
            QMessageBox QPushButton[text="Evet"] {
                background-color: #2ecc71;
                color: white;
            }
            QMessageBox QPushButton[text="Hayır"] {
                background-color: #e74c3c;
                color: white;
            }
            QMessageBox QPushButton[text="Tamam"] {
                background-color: #3498db;
                color: white;
            }
            QMessageBox QPushButton[text="İptal"] {
                background-color: #95a5a6;
                color: white;
            }
        """)
        
        for button_text, button_role in buttons:
            button = msg_box.addButton(button_text, button_role)
            if default_button and button_text == default_button:
                button.setDefault(True)
        
        msg_box.exec()
        clicked_button = msg_box.clickedButton()
        return clicked_button.text() if clicked_button else None
    
    def encrypt_files(self):
        if not self.password_input.text():
            self.show_message_box("Uyarı", "Lütfen bir şifre girin!", [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            return
            
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.show_message_box("Uyarı", "Lütfen şifrelenecek dosyaları seçin!", [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            return
            
        # Şifrelenmiş dosyaları kontrol et
        for item in selected_items:
            if item.text().endswith('.encrypted'):
                self.show_message_box("Uyarı", 
                    f"{os.path.basename(item.text())} zaten şifrelenmiş bir dosya!\nŞifrelenmiş dosyaları tekrar şifreleyemezsiniz.",
                    [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
                return
            
        reply = self.show_message_box('Onay',
            "Seçili dosyalar şifrelenecek ve orijinal dosyalar silinecek. Devam etmek istiyor musunuz?",
            [("Evet", QMessageBox.ButtonRole.YesRole), ("Hayır", QMessageBox.ButtonRole.NoRole)],
            "Evet")
            
        if reply == "Hayır":
            return
            
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        try:
            key = self.generate_key(self.password_input.text())
            if key is None:
                return
            
            for item in selected_items:
                file_path = item.text()
                self.statusBar().showMessage(f"Şifreleniyor: {os.path.basename(file_path)}")
                
                worker = EncryptionWorker(file_path, key, is_encrypt=True)
                worker.progress.connect(self.update_progress)
                worker.finished.connect(lambda f=file_path: self.encryption_finished(f))
                worker.error.connect(self.handle_encryption_error)
                worker.start()
                
                while worker.isRunning():
                    QApplication.processEvents()
                
                # Şifreleme başarılı olduysa orijinal dosyayı sil
                if worker.output_path and os.path.exists(worker.output_path):
                    try:
                        os.remove(file_path)
                        self.statusBar().showMessage(f"Orijinal dosya silindi: {os.path.basename(file_path)}")
                    except Exception as e:
                        self.show_message_box("Uyarı", f"Orijinal dosya silinemedi: {str(e)}", 
                            [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            
            self.show_message_box("Başarılı", "Seçili dosyalar başarıyla şifrelendi ve orijinal dosyalar silindi!", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            
        except Exception as e:
            self.show_message_box("Hata", f"Şifreleme sırasında bir hata oluştu: {str(e)}", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
        
        finally:
            self.progress_bar.setVisible(False)
            self.statusBar().showMessage("Hazır")
            self.file_list.clear()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        QApplication.processEvents()

    def encryption_finished(self, original_file_path):
        self.statusBar().showMessage(f"Şifreleme tamamlandı: {os.path.basename(original_file_path)}")

    def handle_encryption_error(self, error_message):
        self.show_message_box("Hata", f"Şifreleme sırasında bir hata oluştu:\n{error_message}", 
            [("Tamam", QMessageBox.ButtonRole.AcceptRole)])

    def decrypt_files(self):
        if not self.password_input.text():
            self.show_message_box("Uyarı", "Lütfen bir şifre girin!", [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            return
            
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.show_message_box("Uyarı", "Lütfen çözülecek dosyaları seçin!", [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            return
            
        # Şifrelenmemiş dosyaları kontrol et
        for item in selected_items:
            if not item.text().endswith('.encrypted'):
                self.show_message_box("Uyarı", 
                    f"{os.path.basename(item.text())} şifrelenmemiş bir dosya!\nSadece şifrelenmiş dosyaları çözebilirsiniz.",
                    [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
                return
            
        # İlk dosyanın bulunduğu dizini al ve Çözüldü klasörünü oluştur
        first_file = selected_items[0].text()
        base_dir = os.path.dirname(first_file)
        output_dir = os.path.join(base_dir, "Çözüldü")
        
        try:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                self.statusBar().showMessage(f"'{output_dir}' klasörü oluşturuldu")
        except Exception as e:
            self.show_message_box("Hata", f"Çıkış klasörü oluşturulamadı: {str(e)}", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            return
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        
        try:
            key = self.generate_key(self.password_input.text())
            if key is None:
                return
            
            # İlk dosyayı test et
            test_file = selected_items[0].text()
            test_worker = EncryptionWorker(test_file, key, is_encrypt=False)
            test_worker.password_error.connect(self.handle_password_error)
            test_worker.start()
            
            while test_worker.isRunning():
                QApplication.processEvents()
            
            if hasattr(self, 'password_error_occurred') and self.password_error_occurred:
                return
            
            # Test başarılı olduysa diğer dosyaları işle
            for item in selected_items:
                file_path = item.text()
                self.statusBar().showMessage(f"Çözülüyor: {os.path.basename(file_path)}")
                
                worker = EncryptionWorker(file_path, key, is_encrypt=False)
                worker.progress.connect(self.update_progress)
                worker.finished.connect(lambda f=file_path: self.decryption_finished(f, output_dir))
                worker.error.connect(self.handle_decryption_error)
                worker.start()
                
                while worker.isRunning():
                    QApplication.processEvents()
            
            try:
                subprocess.run(['open', output_dir])
            except Exception as e:
                self.statusBar().showMessage(f"Klasör açılamadı: {str(e)}")
            
            self.show_message_box("Başarılı", f"Seçili dosyalar başarıyla çözüldü ve '{output_dir}' klasörüne kaydedildi!", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
            
        except Exception as e:
            self.show_message_box("Hata", f"Çözme sırasında bir hata oluştu: {str(e)}", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
        
        finally:
            self.progress_bar.setVisible(False)
            self.statusBar().showMessage("Hazır")
            self.file_list.clear()
            if hasattr(self, 'password_error_occurred'):
                delattr(self, 'password_error_occurred')

    def decryption_finished(self, encrypted_file_path, output_dir):
        try:
            original_filename = os.path.basename(encrypted_file_path).replace('.encrypted', '')
            decrypted_file_path = os.path.join(output_dir, original_filename)
            
            # Eğer dosya zaten varsa, yeni bir isim oluştur
            counter = 1
            while os.path.exists(decrypted_file_path):
                name, ext = os.path.splitext(original_filename)
                decrypted_file_path = os.path.join(output_dir, f"{name}_{counter}{ext}")
                counter += 1
            
            # Çözülmüş dosyayı taşı
            temp_decrypted_path = encrypted_file_path.replace('.encrypted', '')
            if os.path.exists(temp_decrypted_path):
                shutil.move(temp_decrypted_path, decrypted_file_path)
                self.statusBar().showMessage(f"Çözülmüş dosya taşındı: {original_filename}")
            else:
                self.statusBar().showMessage(f"Çözülmüş dosya bulunamadı: {original_filename}")
        except Exception as e:
            self.show_message_box("Uyarı", f"Çözülmüş dosya taşınamadı: {str(e)}", 
                [("Tamam", QMessageBox.ButtonRole.AcceptRole)])

    def handle_decryption_error(self, error_message):
        self.show_message_box("Hata", f"Çözme sırasında bir hata oluştu:\n{error_message}", 
            [("Tamam", QMessageBox.ButtonRole.AcceptRole)])

    def handle_password_error(self):
        self.password_error_occurred = True
        self.show_message_box("Hata", "Yanlış şifre! Lütfen doğru şifreyi girin.", 
            [("Tamam", QMessageBox.ButtonRole.AcceptRole)])
        self.progress_bar.setVisible(False)
        self.statusBar().showMessage("Hazır")
        self.file_list.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OKANShield()
    window.show()
    sys.exit(app.exec()) 