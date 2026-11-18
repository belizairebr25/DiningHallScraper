#!/usr/bin/env python3
import argparse
import requests
from datetime import datetime
from parser import parse_menu
#colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
ORANGE = "\033[38;5;208m"
BG = "\33[44m" #blue

RESET = "\033[0m"
REVERSE = "\033[7m"
CLEAR_SCREEN = "\033[2J\033[H"

#clear screen
print(f"{CLEAR_SCREEN} Fetching Dining Services Data\n")
BASE_URL = "https://nutritionanalysis.dds.uconn.edu/shortmenu.aspx"

HALLS = {
	"south": {
		"name": "South Campus Marketplace",
		"id": "16",
	},
	
	"ct": {
		"name": "Connecticut Dining Hall",
		"id": "03",
	},
	"whitney": {
		"name": "Whitney Dining Hall",
		"id": "01",
	},
	"northwest": {
		"name": "Northwest Marketplace",
		"id": "15",
	},
	"north": {
		"name": "North Campus Dining Hall",
		"id": "07",
	},
	"towers": {
		"name": "Gelfenbien Commons",
		"id": "42",
	}
	
}


def fetch_menu(hall, day, now, veg):
	#get datetime
	month = now.month
	year = now.year
	dtdate = f"{month:02d}/{day:02d}/{year}"
	#retreive target web page
	info = HALLS[hall]
	if(day == -1):
	#today's menu
		params = {
			"sName": "UCONN Dining Services",
			"locationNum": info["id"],
			"locationName": info["name"],
			"naFlag": 1
		}
	else:
		params = {
			"sName": "UCONN Dining Services",
			"locationNum": info["id"],
			"locationName": info["name"],
			"WeeksMenus": "This Week's Menus",
			"naFlag": 1,
			"myaction": "read",
			"dtdate": dtdate
		}

	response = requests.get(BASE_URL, params=params, timeout=15)
	response.raise_for_status()
	print(f"{GREEN}Data received\n {RESET} Parsing Data\n")
	return parse_menu(response.text, veg)


def display_menu(hall, meal, menu, day, now):
	print(f"\n{CLEAR_SCREEN}{BOLD}{REVERSE}{MAGENTA}{HALLS[hall]['name'].upper()}{RESET}")
	print(f"{CYAN}{meal.upper()}{RESET}")
	if day == -1:
		day = now.day
	print(f"\n{ORANGE}{now.month}/{day}/{now.year}{RESET}")
	print("=" * 40)

	items = menu.get(meal.title(), [])

	if not items:
		print(f"{RED}No matching vegetarian/vegan items found.")
		return

	category = None

	for item in items:
		if item["category"] != category:
			category = item["category"]
			print(f"\n{BOLD}{CYAN}{REVERSE}{category}{RESET}")

		print(f"  {item['name']}")


def main():
	parser = argparse.ArgumentParser(
		description="UConn Dining menu viewer"
	)

	parser.add_argument("hall", choices=HALLS.keys())
	parser.add_argument(
		"meal",
		choices=["breakfast", "lunch", "dinner"]
	)
	parser.add_argument("-day", "--day", type=int, default="-1", choices=range(1, 32), help="Day in this week: usage: -d <int>")
	parser.add_argument("-v", "--v", type=int, default="1", choices=range(0, 2), help="usage: -v <0 for not veggie>")

	args = parser.parse_args()

	try:
		now = datetime.now()
		menu = fetch_menu(args.hall, args.day, now, args.v)
		display_menu(args.hall, args.meal, menu, args.day, now)
		#insert space between finish and prompt
		print("\n", "=" * 40, "\n" * 4)
	except requests.RequestException as error:
		print(f"{RED}Failed to retrieve menu: {RESET}{error}")


if __name__ == "__main__":
	main()
