# BMD Daily Weather Report Scraper 🌧️

Automatically downloads the **Bangladesh Meteorological Department (BMD)**
daily Weather Forecast PDF every evening and saves it to this repository.

## How it works

- **Runs every day at 8:00 PM Bangladesh time** via GitHub Actions
- Visits `server8.bmd.gov.bd/en/p/Weather-Forecast`
- Finds the PDF download link automatically
- Saves the PDF as `pdfs/YYYY/MM/YYYY-MM-DD.pdf`
- Logs every download in `download_log.csv`

## Folder structure

```
pdfs/
  2026/
    06/
      2026-06-13.pdf
      2026-06-14.pdf
      ...
download_log.csv
scraper.py
```

## Run manually

You can trigger a download anytime:
1. Go to **Actions** tab in this repo
2. Click **Daily BMD Weather PDF Download**
3. Click **Run workflow**

## Data source

Bangladesh Meteorological Department  
https://server8.bmd.gov.bd/en/p/Weather-Forecast
