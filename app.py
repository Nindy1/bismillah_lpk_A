from flask import Flask, request, jsonify
import pandas as pd

# Inisialisasi Flask app
app = Flask(__name__)

# Baca data Excel saat server start
df = pd.read_excel('LIST BAHAN KIMIA ORGANIK LPK.xlsx')

@app.route('/')
def home():
    return '''
    <h1>Aplikasi Pencari Bahaya Bahan Kimia Organik</h1>
    <p>Gunakan endpoint <code>/cari?nama=nama_senyawa</code> atau <code>/cari?cas=CAS_number</code></p>
    '''

@app.route('/cari')
def cari():
    nama = request.args.get('nama')
    cas = request.args.get('cas')

    if nama:
        hasil = df[df['Nama Senyawa'].str.contains(nama, case=False, na=False)]
    elif cas:
        hasil = df[df['CAS Number'].astype(str).str.contains(cas, case=False, na=False)]
    else:
        return jsonify({"error": "Berikan parameter ?nama= atau ?cas="})

    if hasil.empty:
        return jsonify({"message": "Data tidak ditemukan."})
    else:
        return hasil.to_json(orient='records', force_ascii=False)

if __name__ == '__main__':
    app.run(debug=True)

