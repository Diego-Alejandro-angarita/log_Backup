## 🚀 Reduce your log storage costs by up to 95%

Stop paying for duplicate data. This API automatically detects and removes repeated log data, saving you money on every backup.

![Rust](https://img.shields.io/badge/Powered%20By-Rust-orange?style=for-the-badge&logo=rust)
![Savings](https://img.shields.io/badge/Storage%20Savings-Up%20to%2099%25-brightgreen?style=for-the-badge)
![API](https://img.shields.io/badge/API-RapidAPI-blue?style=for-the-badge)

Welcome to the **Log Backup Demo**! This repository demonstrates the use of a simple **API to reduce log storage costs automatically**. 

## ⚡ Try it now

👉 https://rapidapi.com/DiegoAlejandroangarita/api/deduplication-system-api

### ⚡ Quick Start (Try it in 10 seconds)

Don't want to run the python scripts? No problem. Open your terminal, replace `YOUR_RAPIDAPI_KEY` with your free key from the link above, and copy-paste this:

```bash
# 1. Create a more realistic log file
for i in {1..1000}; do echo "2026-04-10 [INFO] User logged in" >> quick_test.log; done

# 2. Upload it and see the savings instantly!
curl --request POST \
  --url 'https://deduplication-system-api.p.rapidapi.com/backup/quick_test_recipe' \
  --header 'X-RapidAPI-Key: YOUR_RAPIDAPI_KEY' \
  --header 'Content-Type: multipart/form-data' \
  --form 'file=@quick_test.log'
```
⏱ Takes less than 2 seconds to run
If you want more realistic logs, check the full demo below. 

If you manage servers, you know that log files grow constantly. Backing up a 5GB log file every day means storing 35GB a week. **What if you only had to store the new lines appended each day?**

That's exactly what this API does natively, without you having to write complex `rsync` or diffing logic!

---

## 💸 Translating Bytes into Dollars (The ROI)

Saving space isn't just about freeing up disk capacity; it's about drastically reducing your monthly AWS, Azure, or Google Cloud billing. Every GB you send over the network and store costs money. 

**Let's look at a real-world scenario:**
You are backing up a 10 GB log file daily for a month (30 days). The file grows by roughly 500 MB of *new* logs each day.

| Backup Method | Total Data Uploaded (Network) | Total Data Stored (Disk) | Estimated Monthly Cost ($0.10/GB) |
|---------------|-------------------------------|--------------------------|----------------------------------|
| ❌ Traditional | 300 GB | 300 GB | **$30.00 / month** |
| ✅ **Our API** | **15 GB** *(Only the deltas!)* | **15 GB** | **$1.50 / month** |

**That is a 95% reduction in your cloud storage and egress billing!**

*Costs are approximate and depend on cloud provider pricing.

---

## 📉 The Problem vs. The Solution

### ❌ Traditional Backup (Wasteful)
Every time you backup, the whole file is saved.
* **Day 1:** 5 MB stored 
* **Day 2:** 5.1 MB stored (5 MB identical + 0.1 MB new logs)
* **Total Cloud Storage Billed:** **10.1 MB** 💸

### ✅ Smart Deduplication API (Efficient)
Files are split into tiny 4KB blocks. We only save blocks we haven't seen before.
* **Day 1:** 5 MB stored
* **Day 2:** 0.1 MB stored (Only the new chunks are saved; identical chunks are ignored)
* **Total Cloud Storage Billed:** **5.1 MB** 💰 (50% savings in just two days!)

---

## 🎨 Visualizing the Savings

When you run our demo script, you will see exactly how the API treats your data. Even when appending highly dynamic logs with changing timestamps and IDs, the API isolates the new data perfectly:

```text
📊 --- DAY 1 BACKUP STATS --- 📊
Original File Size : 5.00 MB
Storage Impact: 🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥
🟥 New Data Stored   : 1280 chunks
🟩 Deduplicated Data : 0 chunks 
💰 SPACE SAVED ON CLOUD: 0.00 MB

📊 --- DAY 2 BACKUP STATS --- 📊
Original File Size : 5.00 MB
Storage Impact: 🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
🟥 New Data Stored   : 1 chunks
🟩 Deduplicated Data : 1280 chunks (NO EXTRA COST)
💰 SPACE SAVED ON CLOUD: 5.00 MB
```
*(Only 1 red block was saved on Day 2! The green blocks mean free storage!)*

---

---

## ⚡ Why developers use this

- Reduce AWS S3 costs instantly
- No need to build custom backup logic
- Works with existing pipelines

---

---

## 🧪 What makes this different?

- Block-level deduplication (4KB precision)
- Works even with dynamic logs (timestamps, IDs)
- No complex setup (no rsync, no diffing)
- Real-time storage savings

---

---

## 🎯 Who is this for?

- DevOps engineers managing logs
- Backend developers handling backups
- SaaS teams optimizing cloud costs
- Anyone storing large log files in AWS/GCP/Azure

---

## 💻 How to Run the Demo

Want to see it in action on your own machine? It takes 10 seconds!

### Prerequisites
* Python 3 installed
* The `requests` and `python-dotenv` libraries (`pip install -r requirements.txt`)

### Run It!
1. Clone this repository.
2. Create a `.env` file and insert your `RAPIDAPI_KEY` and `API_BASE_URL`.
3. Execute the realistic script:
   ```bash
   python3 realistic_log_demo.py
   ```

Watch as the script generates a fake server log, backs it up, appends new dynamic errors (with varying timestamps), and backs it up again. **You will instantly see the deduplication magic happen in your terminal!**

---

## 🚀 Ready to drop your cloud bills?

Stop paying for identical data. Integrate our 4KB block-level deduplication engine into your workflows today and watch your storage costs plummet.

### 👉 [Start reducing your storage costs now! Try the API on RapidAPI](https://rapidapi.com/DiegoAlejandroangarita/api/deduplication-system-api) 👈

