import s3format
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class AesCbcS3(s3format):
  def __init__(self, file_path):
    self.__enc_data_bytes = []
    pass
  
  # AES-128 CBC encodig
  def EncodeCBC(self, key, iv):
    # 暗号化
    cipher = AES.new(key, AES.MODE_CBC, iv)
    self.__enc_data_bytes = cipher.encrypt(pad(self.GetByte(), AES.block_size))
  
  # 暗号化したデータを取得
  def GetEncodedData(self):
    return self.__enc_data_bytes
  