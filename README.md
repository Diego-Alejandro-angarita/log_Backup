# 🚀 Smart Log Backup Demo

![Rust](https://img.shields.io/badge/Powered%20By-Rust-orange?style=for-the-badge&logo=rust)
![Savings](https://img.shields.io/badge/Storage%20Savings-Up%20to%2099%25-brightgreen?style=for-the-badge)
![API](https://img.shields.io/badge/API-RapidAPI-blue?style=for-the-badge)

Welcome to the **Log Backup Demo**! This repository demonstrates the raw power of the **Rust Deduplication Backup API**. 

If you manage servers, you know that log files grow constantly. Backing up a 5GB log file every day means storing 35GB a week. **What if you only had to store the new lines appended each day?**

That's exactly what this API does natively, without you having to write complex `rsync` or diffing logic!

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

When you run our demo script, you will see exactly how the API treats your data:

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

## 💻 How to Run the Demo

Want to see it in action on your own machine? It takes 10 seconds!

### Prerequisites
* Python 3 installed
* The `requests` library (`pip install requests`)

### Run It!
1. Clone this repository.
2. Open `backup_logs.py` and insert your RapidAPI Key if using the public gateway.
3. Execute the script:
   ```bash
   python3 backup_logs.py
   ```

Watch as the script generates a fake 5MB server log, backs it up, appends a couple of errors, and backs it up again. **You will instantly see the deduplication magic happen in your terminal!**
