import pandas as pd

class CSVModel:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        """Membaca data dari file CSV."""
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            # Jika file tidak ditemukan, kembalikan DataFrame kosong dengan kolom default
            return pd.DataFrame()

    def write_data(self, data):
        """Menulis data ke file CSV."""
        try:
            data.to_csv(self.file_path, index=False)
        except Exception as e:
            print(f"Error writing data to {self.file_path}: {e}")
        
    def delete_data(self, user_id):
        """Menghapus data berdasarkan user_id."""
        try:
            # Baca data dari file CSV
            data = self.read_data()

            # Filter data untuk menghapus baris dengan user_id yang sesuai
            data = data[data["user_id"] != user_id]

            # Simpan kembali data yang sudah dihapus ke file CSV
            self.write_data(data)
            print(f"Data with user_id {user_id} has been deleted successfully.")
        except Exception as e:
            print(f"Error deleting data: {e}")
