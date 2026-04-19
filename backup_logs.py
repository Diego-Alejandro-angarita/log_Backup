import requests
import time
import os
import sys
import json

# Fallback en caso de que python-dotenv no este instalado localmente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://rust-backup-api-94438501352.us-central1.run.app")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

API_URL_BACKUP = f"{API_BASE_URL}/backup"
API_URL_RESTORE = f"{API_BASE_URL}/restore"

# El servidor de Axum que configuramos espera X-RapidAPI-Proxy-Secret para proteger la ruta
HEADERS = {"X-RapidAPI-Proxy-Secret": RAPIDAPI_KEY} if RAPIDAPI_KEY else {}

# Si estuvieras apuntando al endpoint real de rapidapi.com, el header seria:
# HEADERS = {"X-RapidAPI-Key": RAPIDAPI_KEY} if RAPIDAPI_KEY else {}

def generate_dummy_log(filename, size_mb, append_lines=None):
    """Generates a dummy log file to simulate server logs."""
    chunk = b"2026-04-10 10:00:00 INFO [Server] Connection established to DB.\n"
    target_size = size_mb * 1024 * 1024
    
    with open(filename, 'wb') as f:
        # Write bulk data
        while f.tell() < target_size:
            f.write(chunk)
            
        # Append new lines if simulating a growing log
        if append_lines:
            for line in append_lines:
                f.write(line.encode('utf-8') + b"\n")
    return os.path.getsize(filename)

def backup_file(filepath, recipe_name):
    """Uploads a file to the deduplication API."""
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

def restore_file(recipe_name, output_filename):
    """Restores a file from the deduplication API."""
    print(f"\n📥 Restoring '{recipe_name}' to {output_filename}...")
    start_time = time.time()
    response = requests.get(f"{API_URL_RESTORE}/{recipe_name}", headers=HEADERS)
    elapsed = time.time() - start_time

    if response.status_code == 200:
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Success! Restored {len(response.content) / (1024*1024):.2f} MB (Took {elapsed:.2f}s)")
    else:
         print(f"❌ Failed to restore: {response.status_code} - {response.text}")
         sys.exit(1)

def print_visual_stats(day, file_size, stats):
    """Prints a beautiful visual representation of the savings."""
    total_chunks = stats['chunks_total']
    new_chunks = stats['chunks_new']
    dedup_chunks = stats['chunks_dedup']
    saved_mb = stats['bytes_saved'] / (1024 * 1024)
    file_mb = file_size / (1024 * 1024)
    
    print(f"\n📊 --- {day} BACKUP STATS --- 📊")
    print(f"Original File Size : {file_mb:.2f} MB")
    print(f"Total Chunks (4KB): {total_chunks}")
    
    # Calculate percentages for the bar chart
    if total_chunks > 0:
        new_pct = int((new_chunks / total_chunks) * 20)
        dedup_pct = 20 - new_pct
        
        # ASCII Progress Bar
        bar = ("🟥" * new_pct) + ("🟩" * dedup_pct)
        print(f"\nStorage Impact: {bar}")
        print(f"🟥 New Data Stored   : {new_chunks} chunks")
        print(f"🟩 Deduplicated Data : {dedup_chunks} chunks (NO EXTRA COST)")
    
    print(f"\n💰 SPACE SAVED ON CLOUD: {saved_mb:.2f} MB")
    print("-" * 30)

def main():
    print("🌟 Log Deduplication Demo 🌟")
    print("This script simulates backing up a server log file over two days.\n")
    
    # Day 1: The initial backup
    print("--- DAY 1: Initial Log Backup ---")
    log_v1 = "server_day1.log"
    # Cambiado a 1 MB temporalmente para que funcione con el servidor actual
    size_v1 = generate_dummy_log(log_v1, size_mb=1)
    stats_v1 = backup_file(log_v1, "logs_day1")
    print_visual_stats("DAY 1", size_v1, stats_v1)
    
    # Day 2: The log grows
    print("\n--- DAY 2: Appended Log Backup ---")
    log_v2 = "server_day2.log"
    # We copy the Day 1 log and append just 2 new log entries
    new_logs = [
        "2026-04-11 11:00:01 ERROR [App] User login failed.",
        "2026-04-11 11:05:00 WARN [Memory] High memory usage detected."
    ]
    size_v2 = generate_dummy_log(log_v2, size_mb=1, append_lines=new_logs)
    stats_v2 = backup_file(log_v2, "logs_day2")
    print_visual_stats("DAY 2", size_v2, stats_v2)

    # Restore the Day 2 log to prove it works
    print("\n--- VERIFICATION: Restoring Day 2 Log ---")
    restored_log = "restored_server_day2.log"
    restore_file("logs_day2", restored_log)
    
    # Simple check to verify it matches
    original_size = os.path.getsize(log_v2)
    restored_size = os.path.getsize(restored_log)
    
    if original_size == restored_size:
        print("\n✅ Verification Passed: Restored file size perfectly matches the original!")
    else:
        print(f"\n❌ Verification Failed: Original is {original_size} bytes, restored is {restored_size} bytes.")

    
    # Cleanup
    os.remove(log_v1)
    os.remove(log_v2)
    os.remove(restored_log)
    print("\n🎉 Demo finished! Notice how Day 2 cost almost 0 bytes of extra storage!")

if __name__ == "__main__":
    main()
