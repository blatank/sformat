import random
import struct
import argparse

def generate_random_data(size: int) -> bytes:
    """
    ランダムなバイナリデータを生成する
    :param size: 生成するデータのサイズ（バイト単位）
    :return: ランダムなバイナリデータ
    """
    return bytes(random.getrandbits(8) for _ in range(size))

def calculate_checksum(data: bytes) -> int:
    """
    データのチェックサムを計算する
    :param data: チェックサムを計算するデータ
    :return: チェックサム（1バイト）
    """
    return sum(data) & 0xFF  # バイト単位で加算し、1バイトの範囲に収める

def create_s3_record(start_address: int, random_data: bytes) -> bytes:
    """
    1つのS3レコードを作成する
    :param start_address: アドレス
    :param random_data: 16バイトのランダムデータ
    :return: 作成したS3レコード
    """
    data_length = 21  # 全体のレコード長が21バイト
    address = struct.pack(">I", start_address)  # アドレスは4バイトでエンコード（ビッグエンディアン）
    checksum = calculate_checksum(random_data)
    
    # S3レコード作成（データ長1バイト + アドレス4バイト + データ16バイト + チェックサム1バイト）
    s3_record = struct.pack(">B", data_length) + address + random_data + struct.pack(">B", checksum)
    
    return s3_record

def main(start_address: int, random_data_size: int):
    """
    指定した開始アドレスから、指定したサイズ分のランダムデータを使ってS3レコードを生成する
    :param start_address: 開始アドレス（16進数）
    :param random_data_size: 生成するランダムデータのサイズ（バイト単位）
    """
    current_address = start_address
    for _ in range(random_data_size // 16):  # 16バイト単位でデータを生成
        random_data = generate_random_data(16)  # 16バイトのランダムデータ
        s3_record = create_s3_record(current_address, random_data)
        print(f"S3{s3_record.hex()}")
        current_address += 16  # 16バイト進める

def parse_hex(value: str) -> int:
    """
    16進数の文字列を整数に変換する
    :param value: 16進数文字列（0x付き）
    :return: 整数
    """
    return int(value, 16)

if __name__ == "__main__":
    # argparseを使ってコマンドライン引数を受け取る
    parser = argparse.ArgumentParser(description="S3レコードを生成するプログラム")
    parser.add_argument("start_address", type=parse_hex, help="開始アドレス（16進数形式で指定、例: 0x10）")
    parser.add_argument("random_data_size", type=int, help="ランダムデータのサイズ（バイト単位）")
    
    args = parser.parse_args()
    
    # 引数を使ってメイン関数を実行
    main(args.start_address, args.random_data_size)