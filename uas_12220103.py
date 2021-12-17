"""
Aplikasi Streamlit untuk menggambarkan statistik jumlah produksi minyak mentah di berbagai negara

Sumber data berasal dari file ujian akhir semester IF2112 Pemrograman Komputer
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
Nama        : Muhammad Naufal Aqil Zuhdi
NIM         : 12220103
Kelas       : 01
Mata Kuliah : IF2112 Pemrograman Komputer
UJIAN AKHIR SEMESTER
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import streamlit as st
from PIL import Image

#fungsi mengconvert data yang ada di csv ke list
def convert_DataToList():
    df = pd.read_csv('produksi_minyak_mentah.csv')
    list_datatolist = [[row[col] for col in df.columns] for row in df.to_dict('records')]
    return list_datatolist

#fungsi yang menghasilkan list yang isinya negara yang kode negara pada csv terdapat di json
def Nama_lengkapNegara():
    List_data = convert_DataToList()
    ListKodeNegara = []
    ListNamaLengkapNegara = []
    for i in List_data:
        if i[0] not in ListKodeNegara:
            ListKodeNegara.append(i[0])
    with open("kode_negara_lengkap.json") as f:
        data = json.load(f)
    for i in range(len(ListKodeNegara)):
        for Negara in data:
            if ListKodeNegara[i] == Negara["alpha-3"]:
                ListNamaLengkapNegara.append([Negara["alpha-3"], Negara["name"]])
                break
    return ListNamaLengkapNegara

#fungsi list semua nama negara
def List_NamaNegara():
    List = []
    List_NamaNegara = Nama_lengkapNegara()
    for i in List_NamaNegara:
        List.append(i)
    return List

#fungsi convert nama negara menjadi kode negara untuk keperluan input pada parameter fungsi grafik
def convert_NamaNegaraToKodeNegara(Nama_Lengkap):
    List = Nama_lengkapNegara()
    for i in List:
        if i[1] == Nama_Lengkap:
            return i[0]

#fungsi list data produksi setiap kode negara pada csv
def get_data(kode_negara):
    List = convert_DataToList()
    List_Data = []
    for i in range(len(List)):
        if List[i][0] == kode_negara:
            List_Data.append(List[i])
    return List_Data

#fungsi list semua negara untuk di pengaturan tampilan
List_semua_negara = []
for i in Nama_lengkapNegara():
    List_semua_negara.append(i[1])

#Bagian A
#untuk mendapatkan semua warna pada bar plot
cmap_name = 'tab20'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(List_semua_negara)]

#fungsi grafik jumlah produksi minyak mentah untuk negara N
def Grafik_JumlahProduksiMinyak(nama_lengkap):
    List_tahun_xy = get_data(convert_NamaNegaraToKodeNegara(nama_lengkap))
    X = []
    for i in range(len(List_tahun_xy)):
        X.append(List_tahun_xy[i][1])
    Y = []
    for i in range(len(List_tahun_xy)):
        Y.append(List_tahun_xy[i][2])
    if P == 'Chart Tipe 1':
        plt.title("Line Plot Merepresentasikan Jumlah Produksi Minyak Mentah untuk Setiap Tahun di Negara " +str(N)+ "\n")
        plt.plot(X,Y, color = "black")
        plt.xlabel('Tahun')
        plt.ylabel('Produksi')
        plt.legend(labels = ["Jumlah Produksi Minyak Mentah"], loc = "best")
        st.pyplot(plt)
    else:
        plt.clf()
        plt.scatter(X, Y, marker="o", color = "black")
        plt.title("Scatter Plot Merepresentasikan Jumlah Produksi Minyak Mentah untuk Setiap Tahun di Negara " +str(N)+ "\n")
        plt.xlabel('Tahun')
        plt.ylabel('Produksi')
        plt.legend(labels = ["Jumlah Produksi\nMinyak Mentah"], loc = "best")
        st.pyplot(plt)

#Bagian B
#fungsi untuk mendapatkan data produksi negara pada tahun tertentu
def get_tahun(Tahun):
    List = convert_DataToList()
    List_Tahun = []
    for i in List:
        if i[1] == Tahun:
            List_Tahun.append(i)
    return List_Tahun

#fungsi transisi untuk mengambil elemen ketiga pada suatu list
def take_tirth(elem):
    return elem[2]

#fungsi transisi untuk mengambil elemen kedua pada suatu list
def take_second(elem):
    return elem[1]

#fungsi untuk data produksi negara yang disort pada tahun tertentu
def get_NbesarNegara(N, tahun):
    List_NamaLengkap_Negara = Nama_lengkapNegara()
    List_data = get_tahun(tahun)
    sorted_list = sorted(List_data, key=take_tirth)
    List_Nterbesar = []
    count = 0
    penunjuk = 0
    while count < N:
        for i in List_NamaLengkap_Negara:
            if sorted_list[len(sorted_list) - 1 - penunjuk][0] == i[0]:
                List_Nterbesar.append([i[1], sorted_list[len(sorted_list) - 1 - penunjuk][2]])
                count += 1
                break
        penunjuk += 1
    return List_Nterbesar

#fungsi untuk list produksi negara pada tahun tertentu
def get_ValueNbesarNegara(N, tahun):
    List = get_NbesarNegara(N, tahun)
    List_ValueNbesarNegara = []
    for i in List:
        List_ValueNbesarNegara.append(i[1])
    return List_ValueNbesarNegara

#fungsi untuk list nama negara pada tahun tertentu
def get_NamaLengkap_NbesarNegara(N, tahun):
    List = get_NbesarNegara(N, tahun)
    List_NamaLengkap_NbesarNegara = []
    for i in List:
        List_NamaLengkap_NbesarNegara.append(i[0])
    return List_NamaLengkap_NbesarNegara

#fungsi grafik B besar negara yang memproduksi minyak mentah
def Grafik_NbesarNegara(N, Tahun):
    X = get_NamaLengkap_NbesarNegara(N, Tahun)
    Y = get_ValueNbesarNegara(N, Tahun)
    if P == 'Chart Tipe 1':
        plt.clf()
        plt.bar(X, Y, alpha = 1.0, width=0.9, bottom=None, align="center", color=colors, data=None, zorder=3)

        plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)

        for i in range(len(Y)):
            plt.annotate(f'{Y[i]}\n', xy=(X[i], Y[i]),ha="center", va="center", size=9, rotation = 20)
        plt.legend(labels=["Total Produksi Minyak Mentah di\n" + str(int(N))+" Besar Negara"], loc="best")
        plt.title("Bar Plot Merepresentasikan Grafik Produksi Minyak Mentah di " +str(int(N))+ " Besar Negara\n")
        plt.xlabel("Negara")
        plt.xticks(size=8, rotation = 65)
        plt.ylabel("Produksi")
        st.pyplot(plt)
    else:
        cmap_name1 = 'tab20'
        cmap1 = cm.get_cmap(cmap_name1)
        colors1 = cmap1.colors[:len(X)]
        plt.clf()
        plt.scatter(X, Y, alpha=1.0, marker="o", color=colors1)
        plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
        for i in range(len(Y)):
            plt.annotate(f'{Y[i]}\n', xy=(X[i], Y[i]),ha="center", va="center", size=9, rotation = 20)
        plt.xlabel("Negara")
        plt.xticks(size=8, rotation = 65)
        plt.ylabel("Produksi")
        plt.title("Scatter Plot Merepresentasikan Grafik Produksi Minyak Mentah di " +str(int(N))+ " Besar Negara\n")
        plt.legend(labels=["Total Produksi Minyak Mentah di\n" + str(int(N))+ " Besar Negara"], loc="best")
        st.pyplot(plt)

#Bagian C
#fungsi untuk mendapatkan data produksi negara pada keseluruhan tahun
def get_JumlahProduksiKumulatif(N):
    List = convert_DataToList()
    List_NamaLengkap_Negara = Nama_lengkapNegara()
    kode_negara = List[0][0]
    List_KumulatifNegara = []
    Value = []
    Value2 = []
    Nbesar = []
    sum = 0
    count = 0
    index = 0
    #Menghasilkan List Jumlah produksi Kumulatif dari setiap Negara
    for ListOfData in List:
        if index != len(List) - 1:
            if kode_negara == ListOfData[0]:
                sum += ListOfData[2]
            else:
                sum = round(sum, 3)
                List_KumulatifNegara.append([kode_negara, sum])
                Value.append(sum)
                Value2.append(sum)
                kode_negara = ListOfData[0]
                sum = 0
                sum += ListOfData[2]
        else:
            sum += ListOfData[2]
            sum = round(sum, 3)
            List_KumulatifNegara.append([kode_negara, sum])
        index += 1
    sorted_list = sorted(List_KumulatifNegara, key=take_second)
    #Menghasilkan List berupa N besar Jumlah produksi Kumulatif sebelumnya
    penunjuk = 0
    while count < N:
        for j in List_NamaLengkap_Negara:
            if sorted_list[len(sorted_list) - 1 - penunjuk][0] == j[0]:
                Nbesar.append([j[1], sorted_list[len(sorted_list) - 1 - penunjuk][1]])
                count += 1
                break
        penunjuk += 1
    return Nbesar


#fungsi untuk mendapatkan jumlah produksi negara pada keseluruhan tahun
def get_Value_JumlahProduksiKumulatif(N):
    List = get_JumlahProduksiKumulatif(N)
    List_Value = []
    for i in List:
        List_Value.append(i[1])
    return List_Value

#fungsi untuk mendapatkan nama negara pada keseluruhan tahun
def get_NamaLengkapnegara_JumlahProduksiKumulatif(N):
    List = get_JumlahProduksiKumulatif(N)
    List_NamaLengkapNegara = []
    for i in List:
        List_NamaLengkapNegara.append(i[0])
    return List_NamaLengkapNegara

#fungsi grafik untuk B besar negara pada keseluruhan tahun
def Grafik_NbesarNegaraKumulatif(N):
    X = get_NamaLengkapnegara_JumlahProduksiKumulatif(N)
    Y = get_Value_JumlahProduksiKumulatif(N)
    if P == "Chart Tipe 1":
        plt.clf()
        plt.bar(X, Y, alpha = 1.0, width=0.9, bottom=None, align="center", color=colors, data=None, zorder=3)

        plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)

        for i in range(len(Y)):
            plt.annotate(f'{Y[i]}\n', xy=(X[i], Y[i]),ha="center", va="center", size=9, rotation = 20)
        plt.legend(labels=["Total Produksi Minyak Mentah di\n" +str(int(N))+ " Besar Negara Secara Kumulatif"], loc="best")
        plt.title("Bar Plot Merepresentasikan Grafik Produksi Minyak Mentah di " + str(int(N)) + " Besar Negara Secara Kumulatif\n", size = 10)
        plt.xlabel("Negara")
        plt.xticks(size=8, rotation = 65)
        plt.ylabel("Produksi Kumulatif")
        st.pyplot(plt)
    else:
        cmap_name2 = 'tab20'
        cmap2 = cm.get_cmap(cmap_name2)
        colors2 = cmap2.colors[:len(X)]
        plt.clf()
        plt.scatter(X, Y, alpha=1.0, marker="o", color=colors2)
        plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
        for i in range(len(Y)):
            plt.annotate(f'{Y[i]}\n', xy=(X[i], Y[i]), ha="center", va="center", size=9, rotation = 20)
        plt.xlabel("Negara")
        plt.xticks(size=8, rotation = 65)
        plt.ylabel("Produksi Kumulatif")
        plt.title("Scatter Plot Merepresentasikan Grafik Produksi Minyak Mentah di " +str(int(N))+ " Besar Negara Secara Kumulatif\n", size = 10)
        plt.legend(labels=["Total Produksi Minyak Mentah di\n" +str(int(N))+ " Besar Negara Secara Kumulatif"], loc="best")
        st.pyplot(plt)

# Bagian D
#fungsi untuk mendapatkan data minimum pada tahun tertentu
def getMinimumPadaTahun(Tahun):
    List = convert_DataToList()
    List_NamaLengkap_Negara = Nama_lengkapNegara()
    List_data = get_tahun(Tahun)
    List_Nilai = [List[i][2] for i in range(len(List))]
    List_jumlahProduksi = []
    for j in List_data:
        List_jumlahProduksi.append(j[2])
    List_Nterkecil = []
    Minimum = min(List_jumlahProduksi)
    while Minimum == 0:
        List_jumlahProduksi.remove(Minimum)
        Minimum = min(List_jumlahProduksi)
    for i in List_NamaLengkap_Negara:
        if List[List_Nilai.index(Minimum)][0] == i[0]:
            List_Nterkecil.append([i[1], Minimum])
            break
    List_jumlahProduksi.remove(Minimum)
    return List_Nterkecil

#fungsi untuk mendapatkan data nol pada tahun tertentu
def getListNol(Tahun):
    List_NegaraNol = []
    List_NamaLengkapNegaraNol = []
    List = convert_DataToList()
    for i in List:
        if i[2] == 0 and i[1] == Tahun:
            List_NegaraNol.append([i[0], i[2]])
    for j in List_NegaraNol:
        for i in Nama_lengkapNegara():
            if i[0] == j[0]:
                List_NamaLengkapNegaraNol.append([i[1], j[1]])
    return List_NamaLengkapNegaraNol

#fungsi untuk informasi data maks, min, dan nol pada tahun tertentu
def informasi_Tahuntertentu(Tahun, extreme):
    Informasi = []
    List = []
    if extreme == "maksimum":
        List.extend(get_NbesarNegara(1, Tahun))
    elif extreme == "minimum":
        List.extend(getMinimumPadaTahun(Tahun))
    elif extreme == "Nol":
        List.extend(getListNol(Tahun))
    with open("kode_negara_lengkap.json") as f:
        data = json.load(f)
    for i in range(len(List)):
        for Negara in data:
            if Negara["name"] == List[i][0]:
                if extreme != "Nol":
                    Informasi.extend([Negara["name"], Negara["alpha-3"], Negara["region"], Negara["sub-region"]])
                    break
                else:
                    Informasi.append([Negara["name"], Negara["alpha-3"], Negara["region"], Negara["sub-region"]])
    return Informasi

#fungsi untuk data maks, min, dan nol pada tahun tertentu
def getExtremeAll(ModeExtreme):
    List = convert_DataToList()
    List_NamaLengkap_Negara = Nama_lengkapNegara()
    kode_negara = List[0][0]
    List_KumulatifNegara = []
    Value = []
    Value2 = []
    Extreme = []
    sum = 0
    index = 0
    # Menghasilkan List Jumlah produksi Kumulatif dari setiap Negara
    for ListOfData in List:
        if index != len(List) - 1:
            if kode_negara == ListOfData[0]:
                sum += ListOfData[2]
            else:
                sum = round(sum, 3)
                List_KumulatifNegara.append([kode_negara, sum])
                Value.append(sum)
                Value2.append(sum)
                kode_negara = ListOfData[0]
                sum = 0
                sum += ListOfData[2]
        else:
            sum += ListOfData[2]
            sum = round(sum, 3)
            List_KumulatifNegara.append([kode_negara, sum])
            Value.append(sum)
            Value2.append(sum)
        index += 1
    if (ModeExtreme == "maksimum"):
        Extreme = get_JumlahProduksiKumulatif(1)
    elif (ModeExtreme == "minimum"):
        Minimum = min(Value)
        # cek bahwa nilai minimum != 0
        while Minimum == 0:
            Value.remove(Minimum)
            Minimum = min(Value)
        for i in List_NamaLengkap_Negara:
            if List_KumulatifNegara[Value2.index(Minimum)][0] == i[0]:
                Extreme.append([i[1], Minimum])
                break
            else:
                while Minimum == 0:
                    Value.remove(Minimum)
                    Minimum = min(Value)
    elif (ModeExtreme == "Nol"):
        List_NegaraProduksiNol = []
        for i in List_KumulatifNegara:
            if i[1] == 0:
                List_NegaraProduksiNol.append(i)
        for i in List_NegaraProduksiNol:
            for j in List_NamaLengkap_Negara:
                if i[0] == j[0]:
                    Extreme.append([j[1], 0])
                    break
    return Extreme

#fungsi untuk informasi data maks, min, dan nol pada tahun tertentu
def Informasi_ForAll(extreme):
    Informasi = []
    List = getExtremeAll(extreme)
    with open("kode_negara_lengkap.json") as f:
        data = json.load(f)
    for i in range(len(List)):
        for Negara in data:
            if Negara["name"] == List[i][0]:
                if extreme != "Nol":
                    Informasi.extend([Negara["name"], Negara["alpha-3"], Negara["region"], Negara["sub-region"]])
                    break
                else:
                    Informasi.append([Negara["name"], Negara["alpha-3"], Negara["region"], Negara["sub-region"]])
    return Informasi

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("APLIKASI UJIAN AKHIR SEMESTER IF2112 PEMROGRAMAN KOMPUTER")
st.title("Statistik Jumlah Produksi Minyak Mentah di Berbagai Negara")
st.markdown("*Sumber data berasal dari file Ujian Akhir Semester IF2112 Pemrograman Komputer*")
st.markdown("Oleh: Muhammad Naufal Aqil Zuhdi")
st.markdown("NIM: 12220103")
st.markdown("Kelas: 01")
st.markdown("Mata Kuliah: IF2112 Pemrograman Komputer")
st.write("\n")
st.write("\n")
st.write("\n")
############### title ###############

############### sidebar ###############
image = Image.open('TM_2020.jpeg')
st.sidebar.image(image)

st.sidebar.title("Pengaturan")
## User inputs on the control panel
st.sidebar.subheader("Pengaturan Konfigurasi Tampilan")
P = st.sidebar.selectbox('Pilih Tipe Chart',['Chart Tipe 1','Chart Tipe 2'])
N = st.sidebar.selectbox('Pilih Nama Negara', List_semua_negara)
B = st.sidebar.number_input("Pilih Berapa Besar Negara", min_value=1, max_value=137, value = 5)
T = st.sidebar.number_input("Pilih Tahun Produksi", min_value=1971, max_value=2015)
############### sidebar ###############

############### content ###############
st.subheader("Tabel Data Informasi Jumlah Produksi Minyak Mentah di Negara " +str(N))
st.markdown("Adapun tabel data tersebut adalah sebagai berikut.")
list_produk = get_data(convert_NamaNegaraToKodeNegara(N))
df = pd.DataFrame(list_produk, columns = ['Kode Negara', 'Tahun', 'Produksi'])
st.write(df)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Tabel Data Nama Negara pada File *csv* yang Tersedia")
st.markdown("Adapun tabel data tersebut adalah sebagai berikut.")
list_neg = List_semua_negara
df2 = pd.DataFrame(list_neg, columns = ['Nama Negara'])
st.write(df2)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Grafik Data Jumlah Produksi Minyak Mentah di Negara " +str(N))
st.markdown("Adapun grafik tersebut adalah sebagai berikut.")
convert_DataToList()
convert_NamaNegaraToKodeNegara(N)
Nama_lengkapNegara()
List_NamaNegara()
get_data(convert_NamaNegaraToKodeNegara(N))
Grafik_JumlahProduksiMinyak(N)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Grafik Data Jumlah Produksi Minyak Mentah di " +str(int(B))+ " Besar Negara pada Tahun " +str(int(T)))
st.markdown("Adapun grafik tersebut adalah sebagai berikut.")
get_tahun(T)
get_NbesarNegara(B, T)
get_ValueNbesarNegara(B, T)
get_NamaLengkap_NbesarNegara(B, T)
Grafik_NbesarNegara(B, T)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Grafik Data Jumlah Kumulatif Produksi Minyak Mentah di "+str(int(B))+ " Besar Negara pada Keseluruhan Tahun")
st.markdown("Adapun grafik tersebut adalah sebagai berikut.")
get_JumlahProduksiKumulatif(B)
get_Value_JumlahProduksiKumulatif(B)
get_NamaLengkapnegara_JumlahProduksiKumulatif(B)
Grafik_NbesarNegaraKumulatif(B)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Informasi Negara dengan Jumlah Produksi Minyak Mentah Terbesar pada Tahun " +str(int(T)))
st.markdown("Adapun informasi tersebut adalah sebagai berikut.")
getMinimumPadaTahun(T)
getListNol(T)
list_maks_T = informasi_Tahuntertentu(T, "maksimum")
df3 = pd.DataFrame([list_maks_T], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
st.write(df3)
    
st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Informasi Negara dengan Jumlah Produksi Minyak Mentah Terkecil pada Tahun " +str(int(T)))
st.markdown("Adapun informasi tersebut adalah sebagai berikut.")
list_min_T = informasi_Tahuntertentu(T, "minimum")
df4 = pd.DataFrame([list_min_T], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
st.write(df4)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Informasi Negara dengan Jumlah Produksi Minyak Mentah Sama Dengan Nol pada Tahun " +str(int(T)))
st.markdown("Adapun informasi tersebut adalah sebagai berikut.")
list_nol_T = informasi_Tahuntertentu(T, "Nol")
df5 = pd.DataFrame(list_nol_T)
df5.columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region']
st.write(df5)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Informasi Negara dengan Jumlah Produksi Minyak Mentah Terbesar pada Keseluruhan Tahun")
st.markdown("Adapun informasi tersebut adalah sebagai berikut.")
list_maks_allT = Informasi_ForAll("maksimum")
df6 = pd.DataFrame([list_maks_allT], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
st.write(df6)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Informasi Negara dengan Jumlah Produksi Minyak Mentah Terkecil pada Keseluruhan Tahun")
st.markdown("Adapun informasi tersebut adalah sebagai berikut.")
list_min_allT = Informasi_ForAll("minimum")
df7 = pd.DataFrame([list_min_allT], columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region'])
st.write(df7)

st.write("\n")
st.write("\n")
st.write("\n")
st.subheader("Informasi Negara dengan Jumlah Produksi Minyak Mentah Sama Dengan Nol pada Keseluruhan Tahun")
st.markdown("Adapun informasi tersebut adalah sebagai berikut.")
list_nol_allT = Informasi_ForAll("Nol")
df8 = pd.DataFrame(list_nol_allT)
df8.columns = ['Nama Negara', 'Kode Negara', 'Region', 'Sub-Region']
st.write(df8)
############### content ###############
