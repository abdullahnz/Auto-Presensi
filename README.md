# Auto Absen E-Learning SMK

Simple code, writen with python3.7 for automatically absen in my school's e-learning system.

## Usage
 
Just run it at the time, it will be automatically comment with `pesan_absen` in active session discuss.

```bash
$ python3 main.py 
INFO: Trying to login with user 'nizamabdullah@smkn2-solo.net' ... 
INFO: Successfully login with username 'nizamabdullah@smkn2-solo.net'.
INFO: Checking 'mapel' for today ...
INFO: Found 3 mapel for today.

INFO: Pendidikan Pancasila dan Kewarganegaraan Kelas XII (ID: 4722)
      Guru   : Budi Yuli Esti, S.Pd.
      Time   : 07:00:00 - 09:00:00
      Status : berakhir
      Materi : BAB 4. DINAMIKA PERAN iNDONESIADALAM PERDAMAIAN DUNIA | B. Persatuan dan Kesatuan Bangsa Indonesia dari Masa ke Masa

INFO: Basis Data Kelas XII (ID: 3659)
      Guru   : Wiji Khurniawati, S.Kom
      Time   : 09:00:00 - 11:00:00
      Status : berakhir
      Materi : Administrasi Server Part 2 | Mysqldump untuk BackUp dan Restore Database

INFO: Bahasa Jepang Kelas XII (ID: 4928)
      Guru   : Rizqyana Saraswati, S.Pd
      Time   : 13:00:00 - 15:00:00
      Status : sedang berlangsung
      Materi : Gakkou no Seikatsu (Kehidupan Sekolah) | Pertanyaan ya/tidak (hai/iie)

INFO: Do absen and get all discussion (ID: 4928)
   - [13:18:51] "Nizam Abdullah / 23 - Hadir" (from: nizamabdullah)
   - [13:16:48] "Darudriyo Bhanu 09 hadir" (from: darudriyosuryolaksono)
   - [13:08:38] "Alfian Cahya Firdaus/03/Hadir" (from: alfianfirdaus)
   - [13:03:02] "ramasya alief 29 hadir" (from: ramasyaraihan)
   - [13:02:55] "Fuaidil Ikhrom / 12" (from: fuaidilikhrom)
   - [13:02:22] "ramasya alief 29 hadir" (from: ramasyaraihan)
```

## Note

Still under development.
