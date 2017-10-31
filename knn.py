import csv
import operator
import random


def bukaSetData(
    namafile,
    rasio,
    jmlAtribut,
    setDataLatih=[],
    setDataUji=[],
):
    with open(namafile, 'rb') as csvfile:
        data = csv.reader(csvfile)
        setData = list(data)
        for baris in range(1, len(setData)):
            for kolom in range(2, 4):
                setData[baris][kolom] = str(setData[baris][kolom])
            for kolom in range(4, jmlAtribut):
                setData[baris][kolom] = float(setData[baris][kolom])
            if random.random() < rasio:
                setDataLatih.append(setData[baris])
            else:
                setDataUji.append(setData[baris])


def hitungEuclideanDist(a, b, jumlah):
    jarak = 0
    for x in range(2, 4):
        if a[x] != b[x]:
            jarak += 1
    for x in range(4, jumlah):
        jarak += pow(a[x] - b[x], 2)
    return jarak ** 0.5


def cariTetangga(setDataLatih, dataX, k):
    jarak = []
    tetanggaDekat = []
    jumlah = len(dataX) - 1

    # hitung EuclideanDistance

    for x in range(len(setDataLatih)):
        hasil = hitungEuclideanDist(dataX, setDataLatih[x], jumlah)
        jarak.append((setDataLatih[x], hasil))

    # urutkan hasil perhitungan EuclideanDistance

    jarak.sort(key=operator.itemgetter(1))
    for x in range(k):
        tetanggaDekat.append(jarak[x][0])

    # voting kelas dari tetangga paling dekat

    votingKelas = {}
    for x in range(len(tetanggaDekat)):
        respons = tetanggaDekat[x][-1]
        if respons in votingKelas:
            votingKelas[respons] += 1
        else:
            votingKelas[respons] = 1
    hasilVoting = sorted(votingKelas.iteritems(), key=operator.itemgetter(1),
                         reverse=True)
    return hasilVoting[0][0]


def hitungAkurasi(setDataUji, prediksi):
    benar = 0
    for x in range(len(setDataUji)):
        if setDataUji[x][-1] == prediksi[x]:
            benar += 1
    hasil = benar / float(len(setDataUji))
    return hasil * 100


def main():
    setDataLatih = []
    setDataUji = []
    atribut = 11
    rasio = 0.7  # 70% datalatih, 30% datauji
    namafile = 'Pokemon.csv'
    bukaSetData(namafile, rasio, atribut + 1, setDataLatih, setDataUji)
    print 'Jumlah data latih: ', len(setDataLatih)
    print 'Jumlah data uji: ', len(setDataUji)

    prediksi = []
    k = 13
    for x in range(len(setDataUji)):
        hasil = cariTetangga(setDataLatih, setDataUji[x], k)
        prediksi.append(hasil)
        print 'Pokemon', setDataUji[x][1], '--> IS_LEGENDARY ( fakta= ', \
            setDataUji[x][-1], '; prediksi= ', hasil, ')'
    print 'Tingkat Akurasi: ', hitungAkurasi(setDataUji, prediksi), '%'

main()
