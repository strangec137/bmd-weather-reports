# BMD Daily Weather Report Scraper 🌧️

An automated pipeline that downloads the **Bangladesh Meteorological Department (BMD)** daily Weather Forecast PDF every evening and saves it to this repository — building a long-term archive of Bangladesh weather data.

---

## 📋 What's in the PDFs?

Each daily PDF contains **2 pages**:

**Page 1 — 5-Day Weather Forecast**
- Synoptic situation (monsoon activity, weather systems)
- Division-wise rainfall forecast for next 5 days
- Temperature outlook
- Wind speed & direction at Dhaka
- Sunrise & sunset times

**Page 2 — Station Observation Data**
- Rainfall (mm) for last 24 hours
- Maximum & minimum temperature (°C)
- Data from **50+ weather stations** across all 8 divisions:
  Dhaka, Chattogram, Rajshahi, Rangpur, Mymensingh, Sylhet, Khulna, Barishal

---

## ⚙️ How it works

- **Runs every day at 10:00 PM Bangladesh time (16:00 UTC)** via GitHub Actions
- Visits `server8.bmd.gov.bd/en/p/Weather-Forecast`
- Automatically finds and downloads the daily PDF
- Validates the file is a real PDF before saving
- Saves as `pdfs/YYYY/MM/YYYY-MM-DD.pdf`
- Logs every download in `download_log.csv`

---

## 📁 Folder structure

```
pdfs/
  2026/
    06/
      2026-06-13.pdf
      2026-06-14.pdf
      ...
    07/
      2026-07-01.pdf
      ...
download_log.csv    ← status log of every run
scraper.py          ← Python download script
requirements.txt    ← Python dependencies
```

---

## 🗂️ Download log

`download_log.csv` tracks every run:

| date | status | pdf_url | saved_path |
|------|--------|---------|------------|
| 2026-06-13 | OK | https://... | pdfs/2026/06/2026-06-13.pdf |

Status codes:
- `OK` — PDF downloaded and saved successfully
- `PAGE_ERROR` — Could not load BMD website
- `NO_PDF_FOUND` — No PDF link found on page
- `INVALID_PDF` — Downloaded file was not a valid PDF
- `DOWNLOAD_ERROR` — PDF URL failed to download

---

## 🖱️ Run manually

You can trigger a download anytime:
1. Go to **Actions** tab in this repo
2. Click **Daily BMD Weather PDF Download**
3. Click **Run workflow** → **Run workflow**

---

## 🔮 Future plans

- [ ] Extract station observation data into structured CSV/Excel dataset
- [ ] Parse 5-day forecast text into structured format
- [ ] Build historical dataset going back as far as possible

---

## 📡 Data source

Bangladesh Meteorological Department (BMD)  
🌐 https://server8.bmd.gov.bd/en/p/Weather-Forecast  
📧 info@bmd.gov.bd
