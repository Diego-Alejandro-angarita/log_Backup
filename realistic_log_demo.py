import requests
import time
import os
import sys
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://rust-backup-api-94438501352.us-central1.run.app")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_URL_BACKUP = f"{API_BASE_URL}/backup"
HEADERS = {"X-RapidAPI-Proxy-Secret": RAPIDAPI_KEY} if RAPIDAPI_KEY else {}

LOG_LEVELS = ["INFO", "INFO", "INFO", "WARN", "ERROR", "DEBUG"]
COMPONENTS = ["AuthService", "Database", "PaymentGateway", "FrontendAPI", "WorkerQueue"]
MESSAGES = [
    "User authentication successful for user_id={}.",
    "Query execution took {} ms.",
    "Connection timeout reaching external service.",
    "Processed job {} successfully.",
    "Cache miss for key user_profile_{}.",
    "Memory usage spiking to {}%."
]

def generate_realistic_logs(filename, target_size_mb, start_time):
    """Generates realistic server logs with changing timestamps and data."""
    target_bytes = target_size_mb * 1024 * 1024
    current_time = start_time
    bytes_written = 0
    
    # If file exists, get its current size to append properly
    mode = 'a' if os.path.exists(filename) else 'w'
    if mode == 'a':
        bytes_written = os.path.getsize(filename)
        target_bytes += bytes_written # Target is absolute new size
    
    with open(filename, mode) as f:
        while bytes_written < target_bytes:
            # Advance time by a few seconds randomly
            current_time += timedelta(seconds=random.randint(1, 15))
            
            level = random.choice(LOG_LEVELS)
            comp = random.choice(COMPONENTS)
            msg = random.choice(MESSAGES).format(random.randint(1000, 9999))
            
            log_line = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] {level} [{comp}] {msg}\n"
            
            f.write(log_line)
            bytes_written += len(log_line)
            
    return current_time

def backup_file(filepath, recipe_name):
    print(f"\n🚀 Backing up {filepath} as '{recipe_name}'...")
    with open(filepath, 'rb') as f:
        start_time = time.time()
        response = requests.post(f"{API_URL_BACKUP}/{recipe_name}", headers=HEADERS, files={'file': f})
        elapsed = time.time() - start_time
        
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Success! (Took {elapsed:.2f}s)")
        return stats
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
        sys.exit(1)

def print_visual_stats(day, file_size, stats):
    total_chunks = stats['chunks_total']
    new_chunks = stats['chunks_new']
    dedup_chunks = stats['chunks_dedup']
    saved_mb = stats['bytes_saved'] / (1024 * 1024)
    file_mb = file_size / (1024 * 1024)
    
    print(f"\n📊 --- {day} BACKUP STATS --- 📊")
    print(f"Original File Size : {file_mb:.2f} MB")
    print(f"Total Chunks (4KB): {total_chunks}")
    
    if total_chunks > 0:
        new_pct = int((new_chunks / total_chunks) * 20)
        dedup_pct = 20 - new_pct
        bar = ("🟥" * new_pct) + ("🟩" * dedup_pct)
        print(f"\nStorage Impact: {bar}")
        print(f"🟥 New Data Stored   : {new_chunks} chunks")
        print(f"🟩 Deduplicated Data : {dedup_chunks} chunks (NO EXTRA COST)")
    
    print(f"\n💰 SPACE SAVED ON CLOUD: {saved_mb:.2f} MB")
    print("-" * 30)

def main():
    print("🌟 REALISTIC Log Deduplication Demo 🌟")
    print("Generating logs with dynamic timestamps, unique IDs, and random events.\n")
    
    log_file = "production_server.log"
    if os.path.exists(log_file):
        os.remove(log_file)
        
    start_dt = datetime(2026, 4, 10, 8, 0, 0)
    
    # --- DAY 1 ---
    print("--- DAY 1: Initial Backup (1 MB of realistic logs) ---")
    end_dt_day1 = generate_realistic_logs(log_file, target_size_mb=1.0, start_time=start_dt)
    size_day1 = os.path.getsize(log_file)
    stats_v1 = backup_file(log_file, "real_logs_day1")
    print_visual_stats("DAY 1", size_day1, stats_v1)
    
    # --- DAY 2 ---
    print("\n--- DAY 2: Appending new realistic logs (200 KB of new data) ---")
    # We append 0.2 MB of NEW logs to the SAME file.
    generate_realistic_logs(log_file, target_size_mb=0.2, start_time=end_dt_day1)
    size_day2 = os.path.getsize(log_file)
    stats_v2 = backup_file(log_file, "real_logs_day2")
    print_visual_stats("DAY 2", size_day2, stats_v2)

    os.remove(log_file)
    print("\n🎉 Notice how block-level deduplication works perfectly for append-only files, even when the content itself is highly dynamic and unpredictable!")

if __name__ == "__main__":
    main()
