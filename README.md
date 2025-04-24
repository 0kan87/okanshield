# OKAN Shield - Dosya Şifreleme Programı

OKAN Shield, dosyalarınızı güvenli bir şekilde şifrelemek ve şifrelenmiş dosyaları çözmek için tasarlanmış kullanıcı dostu bir programdır.

## Özellikler

- Dosyaları AES-256 şifreleme ile güvenli bir şekilde şifreleme
- Şifrelenmiş dosyaları çözme
- Kullanıcı dostu arayüz
- Şifre göster/gizle özelliği
- Toplu dosya işleme desteği
- İlerleme çubuğu ile işlem takibi
- Otomatik klasör oluşturma ve açma
- Türkçe arayüz ve hata mesajları

## Kurulum

1. Python 3.8 veya üstü sürümünün yüklü olduğundan emin olun
2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Kullanım

1. Programı başlatın:
   ```bash
   python main.py
   ```

2. Şifreleme için:
   - "Dosya Ekle" butonuna tıklayarak şifrelenecek dosyaları seçin
   - Şifre alanına bir şifre girin
   - "Seçili Dosyaları Şifrele" butonuna tıklayın
   - Şifreleme tamamlandığında orijinal dosyalar otomatik olarak silinecektir

3. Çözme için:
   - "Dosya Ekle" butonuna tıklayarak şifrelenmiş dosyaları seçin
   - Şifre alanına doğru şifreyi girin
   - "Seçili Dosyaları Çöz" butonuna tıklayın
   - Çözülen dosyalar otomatik olarak "Çözüldü" klasörüne kaydedilecektir

## Güvenlik Özellikleri

- Şifrelenmiş dosyalar .encrypted uzantısı ile kaydedilir
- Yanlış şifre girişinde işlem otomatik olarak durdurulur
- Şifrelenmiş dosyalar tekrar şifrelenemez
- Şifrelenmemiş dosyalar çözülemez
- Orijinal dosyalar şifreleme sonrası otomatik silinir

## Notlar

- Şifrenizi güvenli bir yerde saklayın, unutursanız dosyalarınıza erişemezsiniz
- Büyük dosyaların şifrelenmesi/çözülmesi biraz zaman alabilir
- Program çalışırken dosyaları kapatın
- Şifreleme/çözme işlemi sırasında programı kapatmayın

## Hata Durumunda

Eğer bir hata ile karşılaşırsanız:
1. Hata mesajını okuyun
2. Şifrenizi kontrol edin
3. Dosyaların erişilebilir olduğundan emin olun
4. Programı yeniden başlatın

## Geliştirici

Bu program OKAN tarafından geliştirilmiştir.

## Lisans

Bu program özgür yazılımdır ve GNU General Public License v3.0 altında dağıtılmaktadır.

## Taşınabilir Uygulama Oluşturma

Uygulamayı tek bir exe dosyası olarak derlemek için:

```
pyinstaller --onefile --windowed main.py
```

Derlenmiş uygulama `dist` klasöründe oluşturulacaktır. 
