# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding

Perusahaan Edutech Jaya Jaya Maju menghadapi tantangan dalam mempertahankan karyawannya, dengan tingkat **attrition** (pengunduran diri karyawan) yang perlu dipahami dan dikelola. Tingkat attrition yang tinggi dapat berdampak signifikan pada biaya rekrutmen, produktivitas, dan moral karyawan secara keseluruhan. Berdasarkan data awal, sekitar **16.92%** karyawan mengalami attrition, yang menjadi fokus utama analisis ini. Manajemen Sumber Daya Manusia (SDM) di Edutech perlu memahami faktor-faktor pendorong attrition untuk merancang strategi retensi yang efektif dan menciptakan lingkungan kerja yang lebih baik.

### Permasalahan Bisnis

Permasalahan bisnis yang ingin diselesaikan melalui proyek ini adalah:
1.  Mengidentifikasi faktor-faktor demografis, pekerjaan, dan perilaku utama yang paling berpengaruh terhadap keputusan karyawan untuk keluar dari Edutech.
2.  Membangun model prediktif yang dapat mengidentifikasi karyawan dengan risiko attrition tinggi.
3.  Menyediakan dasar untuk pembuatan alat bantu (dashboard) bagi tim SDM untuk memantau tren attrition dan faktor risiko secara berkelanjutan, yang akan membantu dalam:
    *   Menurunkan tingkat attrition secara proaktif.
    *   Mengoptimalkan biaya terkait rekrutmen dan kehilangan talenta.
    *   Meningkatkan kepuasan dan loyalitas karyawan.

### Cakupan Proyek

Proyek ini mencakup langkah-langkah berikut:
1.  **Eksplorasi Data Awal (EDA)**: Memahami dataset `employee_data.csv`, distribusi variabel, dan pola awal terkait attrition.
2.  **Persiapan Data**: Membersihkan data (menangani nilai yang hilang, outlier jika relevan), melakukan encoding pada fitur kategorikal, dan penskalaan fitur numerik.
3.  **Analisis Faktor Penyebab Attrition**: Menggunakan analisis statistik (Cramér's V) dan *feature importance* dari model machine learning untuk mengidentifikasi prediktor kunci.
4.  **Pemodelan Prediktif**: Membangun dan mengevaluasi beberapa model klasifikasi, dengan fokus pada `ExtraTreesClassifier` yang dioptimasi menggunakan Optuna, untuk memprediksi attrition.
5.  **Persiapan Output untuk Dashboard**: Mengekspor hasil prediksi dan data relevan ke format CSV dan database SQLite untuk visualisasi lebih lanjut.
6.  **Kesimpulan dan Rekomendasi**: Merangkum temuan dan memberikan rekomendasi strategis kepada manajemen Edutech.

### Persiapan

**Sumber data**: Dataset yang digunakan adalah `employee_data.csv` yang disediakan oleh Dicoding, berisi informasi demografis, pekerjaan, dan kepuasan karyawan. Tautan: [https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/refs/heads/main/employee/employee_data.csv](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/refs/heads/main/employee/employee_data.csv)

**Setup environment**:
Proyek ini dikerjakan menggunakan Python dalam lingkungan Jupyter Notebook.
1.  **Menjalankan `notebook.ipynb`**:
    *   Pastikan semua dependensi dan library yang tercantum dalam file `requirements.txt` telah terinstal di environment Anda. File ini dapat dibuat dengan menjalankan `pip freeze > requirements.txt` di akhir notebook.
    *   Jalankan sel-sel dalam notebook secara berurutan untuk mereplikasi analisis, pemodelan, dan hasil yang diperoleh. Ini akan menghasilkan file database SQLite di direktori `model/metabase.db`.
2.  **Menjalankan Dashboard (menggunakan Metabase dengan Docker)**:
    Data hasil prediksi dan analisis fitur disimpan dalam database SQLite (`model/metabase.db`) yang dapat dihubungkan ke Metabase.
    *   Pastikan Docker sudah terinstal di sistem Anda.
    *   Tarik image Metabase (jika belum ada): `docker pull metabase/metabase:latest` (atau versi spesifik yang Anda gunakan, misal v0.46.4).
    *   Jalankan container Metabase dengan perintah berikut dari direktori utama proyek Anda (yang berisi folder `model`):
        ```bash
        docker run -d \
          --name dashboard_employee \
          -p 3000:3000 \
          -v ${PWD}/model:/metabase-data \
          metabase/metabase
        ```
        *   **Penjelasan Perintah:**
            *   `-d`: Menjalankan container di background (detached mode).
            *   `--name dashboard_employee`: Memberi nama pada container.
            *   `-p 3000:3000`: Memetakan port 3000 di host ke port 3000 di container.
            *   `-v ${PWD}/model:/metabase-data`: Ini adalah bagian penting. Perintah ini me-mount direktori `model` dari direktori kerja Anda saat ini (`${PWD}/model`) ke direktori `/metabase-data` di dalam container Metabase. File `metabase.db` Anda yang ada di `model/metabase.db` akan dapat diakses dari dalam container melalui path `/metabase-data/metabase.db`.
    *   Akses Metabase melalui browser di `http://localhost:3000`.
    *   Saat pertama kali setup Metabase (atau jika menambahkan database baru):
        1.  Pilih "Let's get set up".
        2.  Isi informasi pengguna admin.
        3.  Pada bagian "Add your data", pilih "I'll add my data later" atau jika langsung menambahkan:
            *   Pilih Database type: **SQLite**.
            *   Display name: (misalnya) `Employee Attrition DB`
            *   Filename: `/metabase-data/metabase.db` (Ini adalah path ke file SQLite Anda *di dalam container Docker*, sesuai dengan volume mapping di atas).
    *   Buat pertanyaan dan dashboard di Metabase menggunakan tabel `employee_predictions`, `feature_importance`, dan `employee_data` (cleaned) dari database yang baru saja Anda hubungkan.

---

## Business Dashboard

Dashboard interaktif yang dibangun di Metabase akan membantu tim SDM Edutech untuk:
1.  **Memantau Tingkat Attrition**: Melihat proporsi karyawan yang diprediksi akan attrition dan perbandingannya dengan data aktual (jika tersedia secara periodik).
2.  **Menganalisis Faktor Risiko Utama**:
    *   Visualisasi *feature importance* yang menunjukkan faktor-faktor seperti `OverTime`, `MaritalStatus`, dan `TotalWorkingYears` sebagai pendorong utama.
    *   Distribusi karyawan berisiko tinggi berdasarkan karakteristik kunci.
3.  **Identifikasi Segmen Karyawan Berisiko**: Memfilter dan melihat detail karyawan yang diprediksi memiliki probabilitas attrition tinggi.

Untuk mengakses dashboard (setelah setup lokal seperti panduan di atas):
*   **Link Akses Lokal (Metabase via Docker):** `http://localhost:3000`
    *   Setelah login dan menghubungkan database SQLite (`model/metabase.db` yang diakses sebagai `/metabase-data/metabase.db` di dalam Metabase), navigasi ke koleksi atau dashboard yang telah dibuat untuk analisis attrition karyawan Edutech.

---

## Conclusion

Jelaskan konklusi dari proyek yang dikerjakan.
Proyek ini berhasil mengidentifikasi faktor-faktor signifikan yang memengaruhi attrition di Edutech dan membangun model `ExtraTreesClassifier` untuk memprediksi karyawan yang berisiko keluar.

**Faktor-Faktor Utama Penyebab Attrition:**
Berdasarkan analisis *feature importance* dari model `ExtraTreesClassifier`:
1.  **`OverTime`**: Menjadi prediktor terkuat (skor ~0.42), menunjukkan bahwa karyawan yang sering bekerja lembur memiliki risiko attrition yang sangat tinggi.
2.  **`MaritalStatus`**: Status pernikahan merupakan prediktor signifikan kedua (skor ~0.20). Analisis lebih lanjut dari data sebelumnya menunjukkan status 'Single' memiliki proporsi attrition tertinggi.
3.  **`TotalWorkingYears`**: Total masa kerja karyawan secara keseluruhan juga menunjukkan kontribusi penting terhadap prediksi (skor ~0.09).
4.  Fitur lain seperti **`MonthlyIncome`** (skor ~0.06) dan **`Age`** (skor ~0.06) juga berkontribusi secara moderat.

**Model Prediktif Terbaik (`ExtraTreesClassifier`):**
Model `ExtraTreesClassifier`, setelah optimasi hyperparameter menggunakan Optuna (dengan parameter terbaik: `{'n_estimators': 215, 'max_depth': 11, 'min_samples_split': 0.13399970021595703, 'min_samples_leaf': 0.04206053437992983}`), menunjukkan performa berikut pada data uji:
*   **Accuracy**: 74.06%
*   **Recall (untuk Attrition=Yes)**: 0.61 (Model berhasil mengidentifikasi 61% dari karyawan yang sebenarnya attrition)
*   **F1-Score (untuk Attrition=Yes)**: 0.44
*   **Precision (untuk Attrition=Yes)**: 0.35
*   **Confusion Matrix**: Model mengidentifikasi 22 True Positives dan 135 True Negatives, dengan 14 False Negatives dan 41 False Positives. Fokus pada recall (0.61) penting untuk meminimalkan risiko kehilangan karyawan potensial, meskipun presisi (0.35) menunjukkan adanya prediksi positif yang salah.

### Rekomendasi Action Items (Optional)

Berikan beberapa rekomendasi action items yang harus dilakukan perusahaan guna menyelesaikan permasalahan atau mencapai target mereka.
- **Prioritaskan Manajemen `OverTime`**:
    Mengingat `OverTime` adalah faktor dominan, evaluasi kebijakan dan budaya lembur secara mendalam. Identifikasi penyebab lembur berlebihan (beban kerja, efisiensi, kekurangan staf) dan cari solusi untuk menguranginya. Perhatikan bahwa simulasi pengurangan lembur (dari analisis sebelumnya) dapat meningkatkan akurasi keseluruhan tetapi menurunkan kemampuan deteksi kasus attrition sebenarnya (Recall). Strategi pengurangan harus cermat.
- **Fokus pada `MaritalStatus`**:
    Selidiki lebih lanjut mengapa karyawan dengan status pernikahan tertentu (misalnya, 'Single') lebih rentan attrition. Pertimbangkan program dukungan, tunjangan, atau fleksibilitas kerja yang mungkin relevan untuk segmen ini.
- **Analisis Mendalam Faktor `TotalWorkingYears`, `MonthlyIncome`, dan `Age`**:
    Pahami bagaimana kombinasi total masa kerja, tingkat pendapatan, dan usia berkontribusi terhadap risiko *attrition*. Karyawan dengan masa kerja total lebih sedikit mungkin membutuhkan program mentoring dan pengembangan karir yang lebih intensif. Kaji ulang struktur kompensasi untuk `MonthlyIncome` pada berbagai level pengalaman dan usia.
- **Pemanfaatan Model Prediktif secara Berkelanjutan**:
    Implementasikan model `ExtraTreesClassifier` sebagai bagian dari sistem HR untuk identifikasi proaktif karyawan yang berisiko tinggi melakukan *attrition*. Ini memungkinkan intervensi retensi yang lebih dini dan tertarget. Gunakan dashboard yang terhubung ke hasil prediksi untuk pemantauan berkelanjutan oleh tim SDM.