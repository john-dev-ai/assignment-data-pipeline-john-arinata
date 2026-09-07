# Assignment Documentation

## 1. Deskripsi Singkat Dataset

Dataset yang digunakan adalah dataset otomotif:
`automobileEDA_dirty_training.csv`.

Dataset memiliki **205 baris dan 30 kolom**.

## 2. Sumber Dataset

Dataset utama yang digunakan dalam assignment adalah:

`automobileEDA_dirty_training.csv`

Dataset ditempatkan pada:

`data/raw/automobileEDA_dirty_training.csv`

Dataset mentah tidak diubah atau ditimpa secara langsung. Hasil pengolahan
disimpan sebagai file baru.

## 3. Struktur Folder

```text
data-pipeline-assignment/
├── data/
│   ├── processed/
│   │   └── automobileEDA_processed.csv
│   └── raw/
│       └── automobileEDA_dirty_training.csv
├── documentation/
│   └── data-flow-diagram.png
├── src/
│   └── pipeline.py
├── README.md
└── requirements.txt
```

## 4. Kondisi Dataset & Permasalahan Yang Ditemukan

- Dataset memiliki **205 data dan 30 kolom**.
- Terdapat berbagai tipe data, yaitu `int64`, `float64`, dan `str`.
- Ditemukan **17 missing values** yang tersebar pada 7 kolom:
  - `transaction_date`: 2 missing values
  - `make`: 2 missing values
  - `num-of-doors`: 2 missing values
  - `stroke`: 4 missing values
  - `horsepower`: 3 missing values
  - `price`: 3 missing values
  - `horsepower-binned`: 1 missing value
- Ditemukan **4 baris duplikat**.
- Kolom `transaction_date` memiliki **format tanggal yang tidak konsisten**, seperti `2025-01-01` dan `02/01/2025`.
- Kolom `make` memiliki **penulisan huruf besar dan kecil yang tidak konsisten**, contohnya `alfa-romero` dan `ALFA-ROMERO`.

## 5. Data Cleaning

### 5.1 Permasalahan yang Ditemukan

Berdasarkan hasil pemeriksaan awal, ditemukan beberapa permasalahan pada dataset:

- Terdapat **205 baris data** dengan **4 duplicate records**.
- Terdapat missing values pada kolom `transaction_date`, `make`, `num-of-doors`, `stroke`, `horsepower`, `price`, dan `horsepower-binned`.
- Beberapa kolom kategorikal memiliki penulisan yang tidak konsisten, seperti penggunaan huruf besar dan kecil.
- Beberapa nilai kategorikal memiliki spasi yang tidak diperlukan.

### 5.2 Kolom yang Dibersihkan

Beberapa kolom yang akan dibersihkan yaitu:

`transaction_date`
`make`
`num-of-doors`
`horsepower-binned`
`aspiration`
`body-style`
`drive-wheels`
`engine-location`
`engine-type`
`num-of-cylinders`
`fuel-system`
`stroke`
`horsepower`
`price`

### 5.3 Metode Cleaning

Proses cleaning yang diterapkan sebagai berikut.

#### 5.3.1 Menghapus Duplicate Records

Data duplikat dihapus menggunakan metode `drop_duplicates()`.

```python
data = data.drop_duplicates().reset_index(drop=True)
```

Metode ini digunakan agar setiap record dalam dataset hanya muncul satu kali dan tidak menyebabkan pengulangan data pada proses analisis atau pemodelan berikutnya.

#### 5.3.2 Menghapus Kolom `transaction_date`

Kolom `transaction_date` dihapus dari dataset menggunakan:

```python
data = data.drop(columns=["transaction_date"])
```

Karena kolom tanggal tidak digunakan dalam proses transformation berdasarkan dataset pembanding, maka kolom ini dihapus sehingga tidak diteruskan ke dataset hasil.

#### 5.3.3 Menyeragamkan Penulisan Data Kategorikal

Beberapa kolom kategorikal memiliki perbedaan penggunaan huruf besar dan kecil serta spasi tambahan. Untuk menyeragamkan format tersebut, dilakukan konversi menjadi string, penghapusan spasi di awal/akhir, dan perubahan seluruh karakter menjadi huruf kecil.

Proses dilakukan menggunakan:

```python
data[col] = data[col].astype("string").str.strip().str.lower()
```

Cleaning diterapkan pada kolom:

- `make`
- `aspiration`
- `num-of-doors`
- `body-style`
- `drive-wheels`
- `engine-location`
- `engine-type`
- `num-of-cylinders`
- `fuel-system`
- `horsepower-binned`

Sebagai contoh, nilai:

| Sebelum | Sesudah |
|---|---|
| `ALFA-ROMERO` | `alfa-romero` |
| `Audi` | `audi` |
| `BMW` | `bmw` |
| `dodge  ` | `dodge` |
| `SEDAN` | `sedan` |
| `Sedan` | `sedan` |
| `RWD` | `rwd` |
| `MPFI` | `mpfi` |
| `Mpfi` | `mpfi` |
| `Medium` | `medium` |

Metode ini dipilih karena permasalahan yang ditemukan berupa ketidakkonsistenan format penulisan kategori, terutama perbedaan kapitalisasi dan spasi tambahan.

#### 5.3.4 Menangani Missing Values pada Data Kategorikal

Missing values pada kolom `make`, `num-of-doors`, dan `horsepower-binned` ditangani menggunakan **mode** atau nilai yang paling sering muncul.

```python
for col in ["make", "num-of-doors", "horsepower-binned"]:
    data[col] = data[col].fillna(data[col].mode()[0])
```

Metode mode dipilih karena ketiga kolom tersebut merupakan data kategorikal. Pengisian menggunakan kategori yang paling sering muncul (modus) dapat mempertahankan bentuk kategori yang sudah tersedia pada dataset.

Jumlah missing values yang ditemukan pada tahap awal:

| Kolom | Missing Values |
|---|---:|
| `make` | 2 |
| `num-of-doors` | 2 |
| `horsepower-binned` | 1 |

Ketiga kolom tersebut diisi menggunakan nilai modus pertama sehingga missing values pada kolom tersebut dapat ditangani sebelum proses transformation.

#### 5.3.5 Menangani Missing Values pada Data Numerik

Missing values pada kolom numerik `stroke`, `horsepower`, dan `price` ditangani menggunakan **median**.

```python
for col in ["stroke", "horsepower", "price"]:
    data[col] = data[col].fillna(data[col].median())
```

Metode median dipilih karena dketiga kolom merupakan data numerik dan tidak terpengaruh oleh nilai ekstrem (terlalu besar atau terlalu kecil).

Jumlah missing values yang ditemukan pada tahap awal:

| Kolom | Missing Values |
|---|---:|
| `stroke` | 4 |
| `horsepower` | 3 |
| `price` | 3 |

### 5.4 Hasil Cleaning

Hasil proses cleaning menunjukkan:

| Kondisi | Sebelum Cleaning | Sesudah Cleaning |
|---|---:|---:|
| Jumlah baris | 205 | 201 |
| Duplicate records | 4 | 0 |
| Missing values | 17 | 0 |

## 6. Data Transformation

Transformasi yang dilakukan meliputi:

1. Encoding ordinal pada `num-of-doors`
2. Encoding ordinal pada `num-of-cylinders`
3. Pembuatan fitur ordinal `horsepower_ordinal`
4. Normalisasi beberapa kolom numerik menggunakan Min-Max Scaling
5. One-Hot Encoding pada beberapa kolom kategorikal
6. Frequency Encoding pada kolom `make`

### 6.1 Encoding Kolom `num-of-doors`

Kolom `num-of-doors` awalnya berisi data kategorikal:

- `two`
- `four`

Transformasi dilakukan menggunakan `np.select()`.

```python
data["num-of-doors"] = np.select(
    [
        data["num-of-doors"].eq("two"),
        data["num-of-doors"].eq("four"),
    ],
    [
        0,
        1,
    ],
    default=np.nan,
)
```

Transformasi ini dilakukan karena `num-of-doors` merupakan fitur kategorikal dengan dua kategori yang dapat direpresentasikan dalam bentuk numerik untuk mempermudah penggunaan data pada tahap analisis atau pemodelan.

Kolom tersebut diubah menjadi nilai numerik menggunakan ordinal encoding:

| Nilai Sebelum | Nilai Sesudah |
|---|---:|
| `two` | 0 |
| `four` | 1 |

### 6.2 Encoding Kolom `num-of-cylinders`

Kolom `num-of-cylinders` awalnya berisi nilai kategorikal dalam bentuk teks. Nilai tersebut diubah menjadi representasi numerik.

Transformasi dilakukan menggunakan `np.select()`, kemudian hasil encoding dibagi dengan 10.

```python
data["num-of-cylinders"] = np.select(
    [
        data["num-of-cylinders"].eq("two"),
        data["num-of-cylinders"].eq("three"),
        data["num-of-cylinders"].eq("four"),
        data["num-of-cylinders"].eq("five"),
        data["num-of-cylinders"].eq("six"),
        data["num-of-cylinders"].eq("eight"),
        data["num-of-cylinders"].eq("twelve"),
    ],
    [
        0,
        1,
        2,
        3,
        4,
        6,
        10,
    ],
    default=np.nan,
)

data["num-of-cylinders"] = data["num-of-cylinders"] / 10
```

Transformasi ini dilakukan untuk mengubah data kategorikal berbentuk teks menjadi data numerik. Setelah encoding, nilai dibagi dengan 10 agar berada pada rentang yang lebih kecil.

Contoh perubahan:

| Nilai Sebelum | Nilai Setelah Encoding | Nilai Setelah Dibagi 10 |
|---|---:|---:|
| `two` | 0 | 0.0 |
| `three` | 1 | 0.1 |
| `four` | 2 | 0.2 |
| `five` | 3 | 0.3 |
| `six` | 4 | 0.4 |
| `eight` | 6 | 0.6 |
| `twelve` | 10 | 1.0 |

### 6.3 Pembuatan Kolom `horsepower_ordinal`

Kolom `horsepower-binned` berisi kategori tingkat horsepower:

- `low`
- `medium`
- `high`

Transformasi dilakukan menggunakan:

```python
data["horsepower_ordinal"] = np.select(
    [
        data["horsepower-binned"].eq("low"),
        data["horsepower-binned"].eq("medium"),
        data["horsepower-binned"].eq("high"),
    ],
    [
        0,
        1,
        2,
    ],
    default=np.nan,
).astype(np.int64)
```

Metode ordinal encoding dipilih karena kategori `low`, `medium`, dan `high` memiliki urutan atau tingkatan yang jelas. Kolom hasil `horsepower_ordinal` kemudian disimpan sebagai fitur numerik pada processed dataset.

Contoh perubahan :

| `horsepower-binned` | `horsepower_ordinal` |
|---|---:|
| `low` | 0 |
| `medium` | 1 |
| `high` | 2 |

### 6.4 Normalisasi Menggunakan Min-Max Scaling

Beberapa kolom numerik memiliki rentang nilai yang berbeda. Oleh karena itu, dilakukan normalisasi menggunakan **Min-Max Scaling**.

Kolom yang dinormalisasi adalah:

- `symboling`
- `curb-weight`
- `num-of-cylinders`
- `engine-size`
- `horsepower`
- `peak-rpm`
- `city-mpg`
- `highway-mpg`
- `price`

Transformasi dilakukan menggunakan `MinMaxScaler` :

```python
scaler = MinMaxScaler()

data[scaled_cols] = scaler.fit_transform(data[scaled_cols])
```

Min-Max Scaling dipilih karena metode ini mengubah nilai numerik ke dalam rentang **0 hingga 1**. Normalisasi dilakukan agar fitur dengan skala besar tidak memiliki pengaruh yang terlalu dominan dibandingkan fitur dengan skala yang lebih kecil.

Contoh perubahan nilai:

| Kolom | Sebelum Transformation | Sesudah Min-Max Scaling |
|---|---:|---:|
| `symboling` | 3 | Nilai dalam rentang 0–1 |
| `curb-weight` | 2548 | Nilai dalam rentang 0–1 |
| `engine-size` | 130 | Nilai dalam rentang 0–1 |
| `horsepower` | Nilai asli | Nilai dalam rentang 0–1 |
| `price` | 13495.0 | Nilai dalam rentang 0–1 |

Nilai hasil normalisasi dapat dibandingkan secara langsung melalui output transformation pada saat pipeline dijalankan.

### 6.5 One-Hot Encoding

Beberapa kolom kategorikal tidak memiliki urutan tertentu sehingga dilakukan **One-Hot Encoding**.

Kolom yang diubah adalah:

- `body-style`
- `drive-wheels`
- `aspiration`
- `engine-type`
- `engine-location`
- `fuel-system`

Transformasi dilakukan menggunakan:

```python
dummies = pd.get_dummies(
    data[onehot_cols],
    prefix=onehot_cols,
    dtype=int,
)
```

One-Hot Encoding dipilih karena kategori pada kolom tersebut bersifat nominal dan tidak memiliki tingkatan. Setiap kategori diubah menjadi kolom baru dengan nilai `0` atau `1`.

Contoh pada kolom `body-style`:

| `body-style` Sebelum | `body-style_sedan` | `body-style_hatchback` | `body-style_wagon` |
|---|---:|---:|---:|
| `sedan` | 1 | 0 | 0 |
| `hatchback` | 0 | 1 | 0 |
| `wagon` | 0 | 0 | 1 |

Kolom-kolom hasil One-Hot Encoding disimpan sebagai bagian dari processed dataset.

### 6.6 Frequency Encoding pada Kolom `make`

Kolom `make` memiliki beberapa kategori produsen mobil. Untuk mengubahnya menjadi representasi numerik tanpa membuat terlalu banyak kolom baru, digunakan **Frequency Encoding**.

Transformasi dilakukan dengan menghitung proporsi kemunculan setiap kategori:

```python
make_frequency = data["make"].value_counts(normalize=True)

result["make_freq"] = data["make"].map(make_frequency)
```

Nilai pada `make_freq` menunjukkan frekuensi relatif dari masing-masing kategori `make` dalam dataset.

Metode ini dipilih agar informasi mengenai kategori produsen tetap dipertahankan dalam bentuk numerik tanpa menambahkan banyak kolom seperti pada One-Hot Encoding.

## 7. Jumlah Data Dari Proses Yang Telah Dilakukan

Setelah seluruh proses cleaning dan transformation dijalankan, ukuran dataset mengalami perubahan.

### Perbandingan Dataset

|  #    | Sebelum | Sesudah |
| ----- | ------: | ------: |
| Baris |     205 |      30 |
| Kolom |     201 |      50 |

## 8. Instalasi Depedencies

Pastikan sudah membuat virtual environment terlebih dahulu, jika belum dapat melakukan dengan mengguanakan perintah berikut :

```text
    python3 -m venv venv
```

atau

```text
    python -m venv venv
```

Kemudian aktifkan virtual environment jika diperlukan dengan perintah berikut :

MacOS / Linux

```text
    source venv/bin/activate
```

Windows

```text
    venv\Scripts\activate
```

kemudian install dependency dengan perintah berikut :

```text
    pip3 install -r requirements.txt
```

atau

```text
    pip3 install -r requirements.txt
```

## 10. Menjalankan Pipeline

Dari root project, jalankan perintah berikut:

```text
    python3 src/pipeline.py
```

atau

```text
    python src/pipeline.py
```

## 11. Alur ETL


```text
EXTRACT
Raw Data
   ↓
Load Data

TRANSFORM
   ↓
Data Inspection
   ↓
Data Cleaning
   ↓
Data Transformation

LOAD
   ↓
Processed CSV
```

Gambar tersebut menunjukkan **alur proses data (data pipeline)** dari data mentah hingga menjadi dataset yang siap digunakan.

1. **Raw Data** : Data awal yang masih dalam kondisi mentah.
2. **Load Data** : Data dimuat agar dapat diproses.
3. **Data Inspection** : Melakukan pemeriksaan terhadap data untuk mengetahui struktur, tipe data, nilai kosong, dan potensi masalah.
4. **Data Cleaning** : Melakukan pembersihan data, seperti menangani missing value, duplikasi, atau data yang tidak sesuai.
5. **Data Transformation** : Data diubah ke format yang sesuai, misalnya melakukan **normalisasi data numerik** dan **encoding data kategorikal**.
6. **Processed Dataset** : Hasil akhir berupa dataset yang telah dibersihkan dan ditransformasi sehingga siap digunakan untuk analisis atau proses machine learning.


## 12. Output Processed Dataset

File yang dihasilkan:

`data/processed/automobileEDA_processed.csv`

Dataset raw tetap berada di:

`data/raw/automobileEDA_dirty_training.csv`

dan tidak ditimpa oleh pipeline.