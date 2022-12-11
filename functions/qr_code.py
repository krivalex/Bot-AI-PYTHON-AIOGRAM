def qr_code(link):
  import qrcode
  # имя конечного файла
  filename = "qr_code.png"
  # генерируем qr-код
  img = qrcode.make(link)
  # сохраняем img в файл
  img.save(filename)
