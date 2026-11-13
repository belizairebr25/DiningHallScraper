
#!/usr/bin/env python3
import argparse
import random
import time
import requests
from parser import parse_menu

# Hacker Phosphor Palette
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
REVERSE = "\033[7m"
BLINK = "\033[5m"

GREEN = "\033[32m"
BRIGHT_GREEN = "\033[92m"
RED = "\033[91m"

CLEAR_SCREEN = "\033[2J\033[H"
BASE_URL = "https://nutritionanalysis.dds.econn.edu/shortmenu.aspx"

HALLS = {
    "south": {"name": "SOUTH_CAMPUS_MARKETPLACE", "id": "16"},
    "ct": {"name": "CONNECTICUT_DINING_HALL", "id": "03"},
    "whitney": {"name": "WHITNEY_DINING_HALL", "id": "01"},
    "northwest": {"name": "NORTHWEST_MARKETPLACE", "id": "15"},
    "north": {"name": "NORTH_CAMPUS_DINING_HALL", "id": "07"},
    "towers": {"name": "GELFENBIEN_COMMONS", "id": "42"},
}


def sys_log(tag, msg, delay=0.06):
    addr = f"0x{random.randint(0x1000, 0xFFFF):04X}"
    print(f"{DIM}{GREEN}[{addr}]{RESET} {BRIGHT_GREEN}[{tag}]{RESET} {GREEN}{msg}{RESET}")
    time.sleep(delay)


def fetch_menu(hall):
    info = HALLS[hall]
    params = {
        "sName": "UCONN Dining Services",
        "locationNum": info["id"],
        "locationName": info["name"],
        "naFlag": 1,
    }

    print(CLEAR_SCREEN, end="")
    sys_log("INIT", "BOOTING UCONN_DDS_SCRAPER v0.9.4-alpha...")
    sys_log("NET ", f"TARGET_NODE={info['name']} (LOC_ID: 0x{info['id']})")
    sys_log("HTTP", "INJECTING GET PAYLOAD -> nutritionanalysis.dds.uconn.edu...")

    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()

    sys_log("RECV", f"200 OK :: {len(response.text)} BYTES CAPTURED")
    sys_log("PARS", "DUMPING DOM NODES...", delay=0.15)
    return parse_menu(response.text)


def display_menu(hall, meal, menu):
    info = HALLS[hall]
    items = menu.get(meal.title(), [])

    print(CLEAR_SCREEN, end="")
    print(f"{DIM}{GREEN}+{'-' * 54}+{RESET}")
    print(f"{GREEN}| {BRIGHT_GREEN}{BOLD}>> UCONN_DDS // {info['name']}{RESET}")
    print(f"{GREEN}| {DIM}SECTOR: {meal.upper()}  ::  NODES_FOUND: {len(items):02d}  ::  STATUS: {BRIGHT_GREEN}LIVE{RESET}")
    print(f"{DIM}{GREEN}+{'-' * 54}+{RESET}")

    if not items:
        print(f"\n{RED}{BOLD}[ERR_404] NO MATCHING RATIONS IN SECTOR.{RESET}\n")
        return

    category = None
    for idx, item in enumerate(items, start=1):
        if item["category"] != category:
            category = item["category"]
            print(f"\n{BRIGHT_GREEN}{REVERSE} // {category.upper()} {RESET}")

        # Index numbers styled like memory offsets
        print(f"  {DIM}{GREEN}[{idx:02d}]{RESET} {BRIGHT_GREEN}>{RESET} {GREEN}{item['name']}{RESET}")

    print(f"\n{DIM}{GREEN}EOF // CONNECTION TERMINATED {BLINK}_{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="UCONN_DDS // TERMINAL UPLINK")
    parser.add_argument("hall", choices=HALLS.keys())
    parser.add_argument("meal", choices=["breakfast", "lunch", "dinner"])
    args = parser.parse_args()

    try:
        menu = fetch_menu(args.hall)
        display_menu(args.hall, args.meal, menu)
    except requests.RequestException as error:
        print(f"\n{RED}{BOLD}[FATAL_EXCEPTION] UPLINK SEVERED:{RESET} {error}\n")


if __name__ == "__main__":
    main()
