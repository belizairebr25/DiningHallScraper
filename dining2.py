
#!/usr/bin/env python3
import argparse
import shutil
import time
import requests
from parser import parse_menu

# ANSI Styling & Colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
REVERSE = "\033[7m"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[97m"

# UConn Brand-Inspired Palette (Navy/Blue + White/Cyan accents)
BG_NAVY = "\033[44m"
CLEAR_SCREEN = "\033[2J\033[H"
CLEAR_LINE = "\033[2K\r"

BASE_URL = "https://nutritionanalysis.dds.uconn.edu/shortmenu.aspx"

HALLS = {
    "south": {"name": "South Campus Marketplace", "id": "16"},
    "ct": {"name": "Connecticut Dining Hall", "id": "03"},
    "whitney": {"name": "Whitney Dining Hall", "id": "01"},
    "northwest": {"name": "Northwest Marketplace", "id": "15"},
    "north": {"name": "North Campus Dining Hall", "id": "07"},
    "towers": {"name": "Gelfenbien Commons", "id": "42"},
}

MEAL_ICONS = {
    "breakfast": "☀",
    "lunch": "◈",
    "dinner": "☾",
}


def status(msg, color=CYAN):
    """Updates a single loading line in place."""
    print(f"{CLEAR_LINE}{color}◆ {msg}{RESET}", end="", flush=True)


def fetch_menu(hall):
    info = HALLS[hall]
    params = {
        "sName": "UCONN Dining Services",
        "locationNum": info["id"],
        "locationName": info["name"],
        "naFlag": 1,
    }

    status(f"Connecting to {info['name']}...", YELLOW)
    response = requests.get(BASE_URL, params=params, timeout=15)
    response.raise_for_status()

    status("Parsing menu data...", GREEN)
    return parse_menu(response.text)


def draw_header(hall_name, meal, item_count):
    # Adapt box width to terminal size (capped at 64 chars)
    term_width = shutil.get_terminal_size((60, 20)).columns
    width = min(max(term_width - 2, 44), 64)
    inner = width - 2

    icon = MEAL_ICONS.get(meal, "•")
    title = f" 🐺 UCONN DINING  │  {hall_name.upper()} "
    subtitle = f" {icon} {meal.upper()} MENU  •  {item_count} ITEMS "

    print(f"{BLUE}╭{'─' * inner}╮{RESET}")
    print(f"{BLUE}│{RESET}{BOLD}{WHITE}{title.ljust(inner)}{RESET}{BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}{CYAN}{subtitle.ljust(inner)}{RESET}{BLUE}│{RESET}")
    print(f"{BLUE}╰{'─' * inner}╯{RESET}")


def display_menu(hall, meal, menu):
    items = menu.get(meal.title(), [])
    print(CLEAR_SCREEN, end="")
    draw_header(HALLS[hall]["name"], meal, len(items))

    if not items:
        print(f"\n  {RED}{BOLD}✕ No matching vegetarian/vegan items found.{RESET}\n")
        return

    # Group items by category while preserving order
    grouped = {}
    for item in items:
        grouped.setdefault(item["category"], []).append(item)

    for category, cat_items in grouped.items():
        # Padded reverse-video badge for each station
        print(f"\n  {BOLD}{CYAN}{REVERSE} {category.upper()} {RESET}")

        for idx, item in enumerate(cat_items):
            is_last = idx == len(cat_items) - 1
            branch = "╰─" if is_last else "├─"
            name = item["name"]

            # Highlight dietary keywords if present in item name/tags
            badge = ""
            if "vegan" in name.lower():
                badge = f" {GREEN}[VG]{RESET}"
            elif "vegetarian" in name.lower():
                badge = f" {YELLOW}[V]{RESET}"

            print(f"  {DIM}{BLUE}{branch}{RESET} {WHITE}{name}{RESET}{badge}")

    print(f"\n{DIM}{'─' * 46}{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="UConn Dining menu viewer")
    parser.add_argument("hall", choices=HALLS.keys())
    parser.add_argument("meal", choices=["breakfast", "lunch", "dinner"])
    args = parser.parse_args()

    try:
        menu = fetch_menu(args.hall)
        display_menu(args.hall, args.meal, menu)
    except requests.RequestException as error:
        print(f"\n{RED}{BOLD}✕ Failed to retrieve menu:{RESET} {error}\n")


if __name__ == "__main__":
    main()
