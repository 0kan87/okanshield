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

### Windows için:
```
pyinstaller --onefile --windowed main.py
```

Derlenmiş uygulama `dist` klasöründe oluşturulacaktır.

### MacOS için DMG Oluşturma:

1. Önce uygulamayı MacOS uygulaması olarak derleyin:
```bash
pyinstaller --windowed --name "OKAN Shield" --icon=icon.icns main.py
```

2. DMG oluşturmak için `create-dmg` paketini yükleyin:
```bash
brew install create-dmg
```

3. DMG oluşturma komutunu çalıştırın:
```bash
create-dmg \
  --volname "OKAN Shield" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "OKAN Shield.app" 200 190 \
  --hide-extension "OKAN Shield.app" \
  --app-drop-link 600 185 \
  "OKAN Shield.dmg" \
  "dist/OKAN Shield.app"
```

4. DMG dosyası oluşturulacak ve Applications klasörüne sürüklenerek kurulum yapılabilecektir.

Not: DMG oluşturmadan önce bir `icon.icns` dosyası oluşturmanız gerekmektedir. Bu dosyayı oluşturmak için:
1. PNG formatında bir ikon hazırlayın
2. `iconutil` komutunu kullanarak icns dosyasına dönüştürün:
```bash
iconutil -c icns icon.iconset
``` 
