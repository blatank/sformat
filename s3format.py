
class S3Format:
  def __init__(self, file_path):
    self.__file_path = file_path
    self.__data_bytes = []

    # ファイル解析
    self.Parse()
    pass
  
  # ファイルパスを返す
  def FilePath(self):
    return self.__file_path
  
  # データを追加する
  def AppendData(self, data):
    self.__data_bytes.append(data)

  # ファイル解析
  def Parse(self):
    with open(self.FilePath(), 'r') as f:
      for line in f:
        line = line.strip()
        if line.startswith('S3'):
          byte_count = int(line[2:4], 16)
          address = line[4:12]  # 32-bit address
          data_end = 4 + 8 + (byte_count - 5) * 2  # -5 accounts for address (4 bytes) and checksum (1 byte)
          data_hex = line[12:data_end]

          # 分割してバイナリに変換
          for i in range(0, len(data_hex), 2):
            byte = int(data_hex[i:i+2], 16)
            self.AppendData(byte)

  # データ部分のByteArrayを返す
  def GetByteArray(self):
    return bytearray(self.__data_bytes)

  # バイナリデータファイルを出力する
  def WriteBinFile(self, output_file_path):
    with open(output_file_path, 'wb') as f:
      f.write(self.GetByteArray())
