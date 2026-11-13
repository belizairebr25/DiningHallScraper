#!/usr/bin/env python3
import argparse
import requests

from parser import parse_menu
#colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
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


def fetch_menu(hall):
	info = HALLS[hall]

	params = {
		"sName": "UCONN Dining Services",
		"locationNum": info["id"],
		"locationName": info["name"],
		"naFlag": 1
	}

	response = requests.get(BASE_URL, params=params, timeout=15)
	response.raise_for_status()
	print(f"{GREEN}Data received\n {RESET} Parsing Data\n")
	return parse_menu(response.text)


def display_menu(hall, meal, menu):
	print(f"\n{CLEAR_SCREEN}{BOLD}{MAGENTA}{HALLS[hall]['name'].upper()}{RESET}")
	print(f"{CYAN}{meal.upper()}{RESET}")
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

	args = parser.parse_args()

	try:
		menu = fetch_menu(args.hall)
		display_menu(args.hall, args.meal, menu)
		#insert space between finish and prompt
		print("\n", "=" * 40, "\n" * 4)
	except requests.RequestException as error:
		print(f"{RED}Failed to retrieve menu: {RESET}{error}")


if __name__ == "__main__":
	main()
