# Input :
# img = array numpy dari citra
# height = tinggi citra
# width = lebar citra
# color = jumlah channel atau warna citra
# message = pesan teks yang ingin disisipkan

# Output :
# Numpy array citra dengan ukuran yang sama seperti citra input
def encode(img, height, width, color, message):
    # Pertama, kita perlu mengubah nilai piksel citra yang mungkin berupa bilangan real
    # karena pemrosesan pada modul computer vision yang lain
    # ini diperlukan karena hanya bilangan integer yang dapat dikonversi ke biner
    arrayimg = img.astype('uint8')

    # Menghitung jumlah piksel yang dapat disisipi pesan
    piksel_total = height * width * color

    # Delimiter pesan sebagai penanda dari akhir pesan
    message += "$t3g4n0gr4f1"
    # Decoding pesan ke bilangan biner
    b_message = ''.join([format(ord(i), "08b") for i in message])
    # Menghitung panjang pesan untuk mengetahui berapa jumlah piksel
    # yang dibutuhkan untuk menyisipkan pesan
    req_pixels = len(b_message)

    # Cek apakah pesan melebihi jumlah piksel
    if req_pixels > piksel_total:
        # Jika ya, tampilkan pesan di terminal dan urungkan proses
        print("Ukuran citra terlalu kecil untuk pesan tersebut !")
        return arrayimg.astype('uint8')
    else:
        # Jika tidak, lakukan proses penyisipan pesan
        # Penyisipan dilakukan dengan mengiterasi masing-masing channel pada piksel citra

        # Variabel untuk mengatur indeks pesan string yang disisipkan
        index=0
        for i in range(height):
            for j in range(width):
                for k in range(color):
                    # Piksel akan disisipkan jika indeks saat ini kurang dari
                    # panjang pesan yang disisipkan
                    if index < req_pixels:
                        # Proses penyisipan pesan, diawali dengan konversi piksel citra ke bilangan biner
                        # kemudian ditambahkan dengan bilangan biner dari pesan yang disisipkan
                        # setelah itu, dikonversi kembali ke integer
                        arrayimg[i][j][k] = int(bin(arrayimg[i][j][k])[2:9] + b_message[index], 2)
                        # Increment nilai index untuk bersiap menyisipkan pesan berikutnya
                        index += 1
        # Proses selesai, return citra dalam numpy array
        return arrayimg.astype('uint8')

# Input :
# img = array numpy dari citra
# height = tinggi citra
# width = lebar citra
# color = jumlah channel atau warna citra

# Output :
# Pesan yang disisipkan
def decode(img, height, width, color):
    # Pertama, kita perlu mengubah nilai piksel citra yang mungkin berupa bilangan real
    # karena pemrosesan pada modul computer vision yang lain
    # ini diperlukan karena hanya bilangan integer yang dapat dikonversi ke biner
    array = img.astype('uint8')

    # Kemudian kita membuat variabel untuk menempatkan bilangan biner dari citra
    # untuk melakukan pencarian pesan dalam satu array
    hidden_bits = ""

    # Iterasi citra untuk mendapatkan nilai piksel masing-masing channel nya
    for i in range(height):
        for j in range(width):
            for k in range(color):
                # Ubah nilai piksel ke bilangan biner, dan tempatkan nilai LSB
                # atau bit terakhir ke variabel hidden_bits
                hidden_bits += (bin(array[i][j][k])[2:][-1])

    # Kemudian, pecah variabel hidden bit yang telah didapatkan
    # menjadi beberapa bagian per 8 bit (1 byte)
    # karena pesan yang disisipkan merupakan pesan teks ASCII 8 bit
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    # Buat variabel untuk menyimpan pesan yang didapatkan
    message = ""
    # Kemudian, lakukan iterasi pada pesan dalam hidden_bits
    for i in range(len(hidden_bits)):
        # Jika ditemukan delimiter penanda akhir dari pesan
        if message[-12:] == "$t3g4n0gr4f1":
            # Maka akhiri iterasi karena pesan sudah ditemukan
            break
        else:
            # Jika belum, tambahkan karakter ASCII yang dibaca dari nilai
            # biner hidden_bits ke dalam variabel pesan
            message += chr(int(hidden_bits[i], 2))
    # Stelah menemukan pesan, cek kembali apakah terdapat pesan
    # dalam citra ini, dengan mengecek apakah terdapat delimiter pada
    # pesan yang berhasil dibaca
    if "$t3g4n0gr4f1" in message:
        # Jika ya, maka pesan ketemu dan tinggal dikembalikan nilainya
        return message[:-12]
    else:
        # Jika tidak ketemu, return None
        return None
