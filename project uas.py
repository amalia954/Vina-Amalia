import csv
import os
from collections import defaultdict

# nama file csv, untuk simpan data keuangan
file_name = 'keuangan.csv'

def memuat_data():
    data = []
    if not os.path.exists(file_name):
        return data
    with open(file_name, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for baris in reader:
            baris['id'] = int(baris['id'])
            baris['jumlah'] = int(baris['jumlah'])
            data.append(baris)
    return data

def simpan_data(data):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        kolom = ['id', 'tanggal', 'jenis', 'kategori', 'jumlah']
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        for baris in data:
            writer.writerow(baris)

def tambah_data(data):
    id_baru = max([d['id'] for d in data], default=0) + 1
    tanggal = input("Masukan Tanggal (YYYY-MM-DD): ")
    jenis = input("Masukan jenisJenis (pemasukan/pengeluaran): ").lower()
    kategori = input("Masukan Kategori: ")
    try:
        jumlah = int(input("Masukan Jumlah: "))
    except ValueError:
        print("Jumlah harus angka")
    data.append({'id': id_baru, 'tanggal': tanggal, 'jenis': jenis, 'kategori': kategori, 'jumlah': jumlah})
    simpan_data(data)
    print("Data berhasil ditambahkan\n")

def lihat_data(data):
    print("\nid | Tanggal     | Jenis      | Kategori   | Jumlah")
    print("-"*56)
    for d in data:
        print(f"{d['id']:2} | {d['tanggal']} | {d['jenis']:<10} | {d['kategori']:<10} | {d['jumlah']:8}")
    print()

def update_data(data):
    lihat_data(data)
    id_update = int(input("Masukkan id data yang ingin diupdate: "))
    for d in data:
        if d['id'] == id_update:
            d['tanggal'] = input(f"Tanggal ({d['tanggal']}): ") or d['tanggal']
            d['jenis'] = input(f"Jenis ({d['jenis']}): ") or d['jenis']
            d['kategori'] = input(f"Kategori ({d['kategori']}): ") or d['kategori']
            jumlah_input = input(f"Jumlah ({d['jumlah']}): ")
            d['jumlah'] = int(jumlah_input) if jumlah_input else d['jumlah']
            simpan_data(data)
            print("Data berhasil diupdate!\n")
            return
    print("id tidak ditemukan, silahakan coba lagi\n")

def hapus_data(data):
    lihat_data(data)
    id_hapus = int(input("Masukkan id data yang ingin dihapus: "))
    baru = [d for d in data if d['id'] != id_hapus]
    if len(baru) < len(data):
        simpan_data(baru)
        print("Data berhasil dihapus\n")
        data[:] = baru
    else:
        print("id tidak ditemukan, silahkan coba lagi\n")

def laporan(data):
    print("\nLaporan Bulanan/Tahunan")
    tahun = input("Masukkan tahun (YYYY): ")
    bulan = input("Masukkan bulan (MM, Jika ingin laporan tahunan bagian ini kosongkan): ")
    total_pemasukan = 0
    total_pengeluaran = 0
    per_kategori = defaultdict(int)
    for d in data:
        if d['tanggal'].startswith(tahun) and (bulan == "" or d['tanggal'][5:7] == bulan):
            if d['jenis'] == 'pemasukan':
                total_pemasukan += d['jumlah']
            elif d['jenis'] == 'pengeluaran':
                total_pengeluaran += d['jumlah']
                per_kategori[d['kategori']] += d['jumlah']
    print(f"Total pemasukan: {total_pemasukan}")
    print(f"Total pengeluaran: {total_pengeluaran}")
    print(f"Saldo: {total_pemasukan - total_pengeluaran}")
    print("\nPengeluaran per kategori:")
    for k, v in per_kategori.items():
        print(f"- {k}: {v}")
    print()

def main():
    data = memuat_data()
    while True:
        print("Manajemen Keuangan Pribadi")
        print("1. Tambah Data")
        print("2. Lihat Data")
        print("3. Update Data")
        print("4. Hapus Data")
        print("5. Laporan Bulanan/Tahunan")
        print("6. Keluar")
        pilihan = input("Pilih menu: ")
        if pilihan == '1':
            tambah_data(data)
        elif pilihan == '2':
            lihat_data(data)
        elif pilihan == '3':
            update_data(data)
        elif pilihan == '4':
            hapus_data(data)
        elif pilihan == '5':
            laporan(data)
        elif pilihan == '6':
            print("Terima kasih")
            break
        else:
            print("Pilihan tidak valid, silahkan coba lagi\n")

if __name__ == "__main__":
    main()
