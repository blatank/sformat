from S3Format import S3Format
import json
from Crypto.Cipher import AES

class AesCbcS3(S3Format):
  def __init__(self, file_path):
    self.__enc_data_bytes = []

    # 設定ファイル(AesCbcS3.json)から読み出し
    with open("AesCbcS3.json", "r") as f:
      config = json.load(f)

    self.__key = bytes.fromhex(config["key"])
    self.__iv  = bytes.fromhex(config["iv"])
    # super(file_path)

  # IV取得
  def _GetIV(self):
    return self.__iv
  
  # Key取得
  def _GetKey(self):
    return self.__key
  
  # AES-128 CBC encodig
  def EncodeCBC(self):
    # 暗号化
    cipher = AES.new(self._GetKey(), AES.MODE_CBC, self._GetIV())
    self.__enc_data_bytes = cipher.encrypt(self.GetByte())
  
  # 暗号化したデータを取得
  def GetEncodedByte(self):
    return self.__enc_data_bytes
  
  # 暗号化したデータのbatearrayを取得
  def GetEncodedByteArray(self):
    return bytearray(self.GetEncodedByte())

  # バイナリデータファイルを出力する
  def WriteEncodedBinFile(self, output_file_path):
    with open(output_file_path, 'wb') as f:
      f.write(self.GetEncodedByteArray())