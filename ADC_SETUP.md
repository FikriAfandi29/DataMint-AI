# Google Cloud Application Default Credentials (ADC) Setup

## ✓ ADC Setup Completed

Anda telah berhasil mengkonfigurasi Google Cloud Application Default Credentials untuk DataMint AI.

### Kredensial Tersimpan
```
📁 Windows: C:\Users\vokal\AppData\Roaming\gcloud\application_default_credentials.json
```

## 🔄 Perubahan yang Dilakukan

### 1. **`.env` File**
- ❌ **Dihapus**: `GEMINI_API_KEY` hardcoded (keamanan lebih baik tanpa API key di file)
- ✅ **Ditambahkan**: Komentar dokumentasi tentang ADC
- **Alasan**: API key di file .env sangat risiko (bisa ter-commit ke git)

### 2. **`server.ts` (Node.js/TypeScript)**
```typescript
// Sebelum: Menggunakan API key dari environment
const apiKey = process.env.GEMINI_API_KEY;
ai = new GoogleGenAI({ apiKey: apiKey });

// Sekarang: Menggunakan ADC (lebih aman)
process.env.GOOGLE_APPLICATION_CREDENTIALS = adcPath;
ai = new GoogleGenAI(); // Otomatis membaca ADC
```

### 3. **`backend.py` (Python)**
```python
# Sebelum: Prioritas API key dulu
if API_KEY:
    client = genai.Client(api_key=API_KEY)

# Sekarang: Prioritas ADC
client = genai.Client()  # Otomatis membaca ADC
# Fallback ke Vertex AI jika diperlukan
```

## 🔐 Keuntungan ADC

| Aspek | API Key | ADC |
|-------|---------|-----|
| **Keamanan** | ⚠️ Hardcoded (risiko exposure) | ✅ Sistem tercentralisasi |
| **Rotasi** | ❌ Manual | ✅ Otomatis oleh Google |
| **Deployment** | ❌ Harus simpan secret di setiap ENV | ✅ Cloud-native, transparan |
| **Git Risk** | ⚠️ Mudah ter-commit | ✅ File local, di .gitignore |
| **Multi-service** | ❌ Satu API key untuk semua | ✅ Project-scoped permissions |

## 📋 Cara Menggunakan

### Untuk Development Local
Sudah selesai! ADC credentials sudah tersimpan. Cukup jalankan aplikasi:
```bash
npm run dev      # Node.js/TypeScript
python backend.py  # Python
```

### Untuk Deployment di Cloud Run
ADC otomatis terdeteksi karena Cloud Run menyediakan credentials:
```bash
gcloud run deploy datamint-ai \
  --source . \
  --runtime nodejs \
  --allow-unauthenticated
```

### Untuk Deployment di Compute Engine / GKE
1. Pastikan VM/Pod memiliki Service Account dengan role:
   - `Vertex AI User` (untuk Vertex AI)
   - `Generative Language API Service Agent` (untuk Gemini API)

2. ADC otomatis ditemukan dari metadata service

## ⚙️ Environment Variables Opsional

```env
# Untuk menggunakan Vertex AI instead of Gemini API
USE_VERTEX_AI=true
GCP_PROJECT=your-project-id
GCP_LOCATION=asia-southeast1

# Atau untuk override ADC path (jarang diperlukan)
GOOGLE_APPLICATION_CREDENTIALS=/custom/path/to/credentials.json
```

## 🔍 Testing ADC Setup

### Node.js:
```typescript
// Cek apakah ADC terdeteksi
import { GoogleGenAI } from "@google/genai";

try {
  const ai = new GoogleGenAI();
  console.log("✓ ADC terdeteksi dan siap digunakan");
} catch (error) {
  console.error("✗ ADC tidak terdeteksi", error);
}
```

### Python:
```python
from google import genai

try:
  client = genai.Client()
  print("✓ ADC terdeteksi dan siap digunakan")
except Exception as error:
  print(f"✗ ADC tidak terdeteksi: {error}")
```

## 📝 Migrasi dari API Key (Jika diperlukan di masa depan)

Jika perlu mengembalikan API key:
```bash
# Dapatkan API key baru dari:
# https://aistudio.google.com/apikey

# Simpan ke .env
echo 'GEMINI_API_KEY="your-new-api-key"' >> .env

# Update code untuk menggunakan API key lagi:
# server.ts & backend.py sudah ada fallback support
```

## 🆘 Troubleshooting

### "Could not initialize GenAI client"
1. Cek ADC file tersimpan:
   ```powershell
   Get-Item "$env:APPDATA\gcloud\application_default_credentials.json"
   ```

2. Re-setup ADC:
   ```bash
   gcloud auth application-default login
   ```

### "Authentication failed"
1. Pastikan credentials tidak expired:
   ```bash
   gcloud auth list
   ```

2. Refresh credentials:
   ```bash
   gcloud auth application-default login --no-launch-browser
   ```

## 📚 Referensi
- [Google Cloud ADC Documentation](https://cloud.google.com/docs/authentication/provide-credentials-adc)
- [Gemini API Node.js Client](https://github.com/google-gemini/generative-ai-js)
- [Google Generative AI Python Client](https://github.com/google-gemini/generative-ai-python)
