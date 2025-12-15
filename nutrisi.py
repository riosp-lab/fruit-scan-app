# nutrisi.py
# DAFTAR LENGKAP 50 KELAS (SESUAI URUTAN TRAINING MODEL ANDA)
CLASS_NAMES = [
    'Apple 10',
    'Apple 11',
    'Apple 12',
    'Apple 13',
    'Apple 14',
    'Apple 17',
    'Apple 18',
    'Apple 19',
    'Apple 5',
    'Apple 6',
    'Apple 7',
    'Apple 8',
    'Apple 9',
    'Apple Braeburn 1',
    'Apple Core 1',
    'Apple Crimson Snow 1',
    'Apple Golden 1',
    'Apple Golden 2',
    'Apple Golden 3',
    'Apple Granny Smith 1',
    'Apple Pink Lady 1',
    'Apple Red 1',
    'Apple Red 2',
    'Apple Red 3',
    'Apple Red Delicious 1',
    'Apple Red Yellow 1',
    'Apple Red Yellow 2',
    'Apple Rotten 1',
    'Apple hit 1',
    'Apple worm 1',
    'Apricot 1',
    'Avocado 1',
    'Avocado Black 1',
    'Avocado Black 2',
    'Avocado Green 1',
    'Avocado ripe 1',
    'Banana 1',
    'Banana 3',
    'Banana 4',
    'Banana Lady Finger 1',
    'Banana Red 1',
    'Beans 1',
    'Beetroot 1',
    'Blackberrie 1',
    'Blackberrie 2',
    'Blackberrie half rippen 1',
    'Blackberrie not rippen 1',
    'Blueberry 1',
    'Cabbage red 1',
    'Cabbage white 1',
]

# DATABASE NUTRISI SEDERHANA (Per 100g)
NUTRISI_DATA = {
    # Apel (semua varian Apple*)
    'Apple 10': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel segar, kaya serat dan vitamin C."},
    'Apple 11': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel segar, mendukung kesehatan pencernaan."},
    'Apple 12': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel dengan kandungan antioksidan tinggi."},
    'Apple 13': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Baik untuk camilan sehat sehari-hari."},
    'Apple 14': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Membantu menjaga rasa kenyang lebih lama."},
    'Apple 17': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Varian apel dengan rasa manis-segar."},
    'Apple 18': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Kaya fitonutrien yang baik untuk jantung."},
    'Apple 19': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Baik dikonsumsi langsung atau dijus."},
    'Apple 5': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel renyah dengan kandungan air tinggi."},
    'Apple 6': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Membantu asupan serat harian."},
    'Apple 7': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Cocok untuk diet rendah kalori."},
    'Apple 8': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Mengandung antioksidan alami."},
    'Apple 9': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Dapat membantu mengontrol kadar gula darah."},
    'Apple Braeburn 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Varietas Braeburn dengan rasa manis-asam yang seimbang."},
    'Apple Core 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Bagian tengah apel tetap mengandung serat dan vitamin."},
    'Apple Crimson Snow 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Varietas apel dengan warna merah mencolok dan renyah."},
    'Apple Golden 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel Golden dengan rasa manis lembut."},
    'Apple Golden 2': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Cocok dimakan langsung atau untuk salad buah."},
    'Apple Golden 3': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Varian Golden yang kaya antioksidan."},
    'Apple Granny Smith 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.8 g", "Keterangan": "Apel hijau dengan rasa asam-segar, baik untuk pencernaan."},
    'Apple Pink Lady 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel dengan kombinasi rasa manis dan asam yang khas."},
    'Apple Red 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel merah klasik dengan kulit kaya pigmen."},
    'Apple Red 2': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Sumber serat larut yang baik untuk kolesterol."},
    'Apple Red 3': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Rasa manis lembut, cocok untuk jus."},
    'Apple Red Delicious 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Varietas Red Delicious dengan rasa manis dominan."},
    'Apple Red Yellow 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel merah-kuning dengan rasa seimbang."},
    'Apple Red Yellow 2': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Kaya fitonutrien dari kulit berwarna."},
    'Apple Rotten 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel yang sudah rusak tidak disarankan dikonsumsi."},
    'Apple hit 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel yang memar sebaiknya dipotong bagian rusaknya."},
    'Apple worm 1': {"Kalori (100g)": "52 kcal", "Vitamin Utama": "C", "Serat": "2.4 g", "Keterangan": "Apel terinfestasi ulat tidak dianjurkan untuk dimakan."},

    # Aprikot
    'Apricot 1': {"Kalori (100g)": "48 kcal", "Vitamin Utama": "A, C", "Serat": "2.0 g", "Keterangan": "Buah aprikot kaya beta-karoten dan serat."},

    # Alpukat (semua varian Avocado*)
    'Avocado 1': {"Kalori (100g)": "160 kcal", "Vitamin Utama": "K, E", "Serat": "6.7 g", "Keterangan": "Sumber lemak sehat tak jenuh tunggal."},
    'Avocado Black 1': {"Kalori (100g)": "160 kcal", "Vitamin Utama": "K, E", "Serat": "6.7 g", "Keterangan": "Varietas kulit gelap dengan lemak sehat tinggi."},
    'Avocado Black 2': {"Kalori (100g)": "160 kcal", "Vitamin Utama": "K, E", "Serat": "6.7 g", "Keterangan": "Cocok untuk salad dan guacamole."},
    'Avocado Green 1': {"Kalori (100g)": "160 kcal", "Vitamin Utama": "K, E", "Serat": "6.7 g", "Keterangan": "Alpukat hijau dengan tekstur lembut."},
    'Avocado ripe 1': {"Kalori (100g)": "160 kcal", "Vitamin Utama": "K, E", "Serat": "6.7 g", "Keterangan": "Alpukat matang, siap dikonsumsi langsung."},

    # Pisang (semua varian Banana*)
    'Banana 1': {"Kalori (100g)": "89 kcal", "Vitamin Utama": "B6, C", "Serat": "2.6 g", "Keterangan": "Pisang matang, sumber energi cepat dan kalium."},
    'Banana 3': {"Kalori (100g)": "89 kcal", "Vitamin Utama": "B6, C", "Serat": "2.6 g", "Keterangan": "Pisang cocok untuk olahraga dan pemulihan."},
    'Banana 4': {"Kalori (100g)": "89 kcal", "Vitamin Utama": "B6, C", "Serat": "2.6 g", "Keterangan": "Baik untuk camilan sehat rendah lemak."},
    'Banana Lady Finger 1': {"Kalori (100g)": "96 kcal", "Vitamin Utama": "B6, C", "Serat": "2.8 g", "Keterangan": "Pisang ambon kecil dengan rasa sangat manis."},
    'Banana Red 1': {"Kalori (100g)": "90 kcal", "Vitamin Utama": "B6, C", "Serat": "2.6 g", "Keterangan": "Pisang merah dengan kandungan beta-karoten lebih tinggi."},

    # Kacang panjang / buncis (Beans)
    'Beans 1': {"Kalori (100g)": "31 kcal", "Vitamin Utama": "C, K", "Serat": "3.4 g", "Keterangan": "Sumber serat nabati dan vitamin K."},

    # Bit
    'Beetroot 1': {"Kalori (100g)": "43 kcal", "Vitamin Utama": "Folat, C", "Serat": "2.8 g", "Keterangan": "Akar bit kaya nitrat alami baik untuk sirkulasi."},

    # Blackberry (semua varian Blackberrie*)
    'Blackberrie 1': {"Kalori (100g)": "43 kcal", "Vitamin Utama": "C, K", "Serat": "5.3 g", "Keterangan": "Buah beri gelap kaya antioksidan."},
    'Blackberrie 2': {"Kalori (100g)": "43 kcal", "Vitamin Utama": "C, K", "Serat": "5.3 g", "Keterangan": "Membantu asupan serat harian."},
    'Blackberrie half rippen 1': {"Kalori (100g)": "40 kcal", "Vitamin Utama": "C", "Serat": "5.0 g", "Keterangan": "Blackberry setengah matang dengan rasa lebih asam."},
    'Blackberrie not rippen 1': {"Kalori (100g)": "38 kcal", "Vitamin Utama": "C", "Serat": "5.0 g", "Keterangan": "Blackberry belum matang, rasa sangat asam."},

    # Blueberry
    'Blueberry 1': {"Kalori (100g)": "57 kcal", "Vitamin Utama": "C, K", "Serat": "2.4 g", "Keterangan": "Buah beri biru dengan antioksidan tinggi."},

    # Kubis
    'Cabbage red 1': {"Kalori (100g)": "31 kcal", "Vitamin Utama": "C, K", "Serat": "2.1 g", "Keterangan": "Kubis merah kaya antosianin dan vitamin C."},
    'Cabbage white 1': {"Kalori (100g)": "25 kcal", "Vitamin Utama": "C, K", "Serat": "2.5 g", "Keterangan": "Kubis putih rendah kalori dan kaya serat."},
}