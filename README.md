# Shodan Monitor

This script automates daily threat hunting by querying [Shodan](https://www.shodan.io) for a list of ASNs (Autonomous System Numbers), saving the exposed services found, and comparing them with the previous day's results to detect newly exposed services.

## 📁 Files Structure

```
shodan-monitor/
│
├── queries/                  # Output folder for daily results and alerts
│   ├── YYYY-MM-DD.csv          # Full results for the day
│   └── YYYY-MM-DD_alerts.csv   # Only new results compared to the previous day
│
├── asns.csv                    # List of ASNs to monitor (one per line, with column header 'asn')
├── shodan_query.py             # Main Python script that performs the monitoring
├── requirements.txt            # Required Python libraries
└── .github/
    └── workflows/
        └── monitor.yml         # GitHub Actions workflow to run the script daily
```

## ⚙️ How It Works

1. **Reads `asns.csv`**: Contains a list of ASNs you want to monitor.
2. **Queries Shodan**: For each ASN, it collects exposed IPs and service banners.
3. **Saves daily CSV**: Results are stored in `queries/YYYY-MM-DD.csv`.
4. **Compares with yesterday**:
   - If any **new services** are found (based on IP:port), they are saved in `YYYY-MM-DD_alerts.csv`.
   - This file can be ingested by tools like **Splunk**, **SIEMs**, or monitoring pipelines.

## 📥 Requirements

Install dependencies locally using:

```bash
pip install -r requirements.txt
```

Required environment variable:

- `SHODAN_API_KEY`: Your Shodan API key (can be stored as a GitHub secret).

## 🚀 Running Locally

```bash
export SHODAN_API_KEY=your_api_key
python3 shodan_query.py
```

## 🤖 GitHub Actions (CI/CD)

This project includes a GitHub Actions workflow (`.github/workflows/monitor.yml`) that runs daily at 11:00 UTC.

### Setup Instructions:

1. Go to your GitHub repository.
2. Navigate to **Settings > Secrets and variables > Actions > New repository secret**.
3. Add:
   - Name: `SHODAN_API_KEY`
   - Value: your real API key

The workflow will automatically:
- Run the script daily.
- Save results and alerts in `queries/`.
- Commit and push changes back to the repository.

## 📄 Sample `asns.csv` format

```csv
asn
AS15169
AS32934
```

You can edit this file to monitor any ASN of interest.

---

Made for automated threat surface monitoring using Shodan.
