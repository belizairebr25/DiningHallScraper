#!/usr/bin/env python3
import argparse
import requests

from parser import parse_menu


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

	return parse_menu(response.text)


def display_menu(hall, meal, menu):
	print(f"\n{HALLS[hall]['name'].upper()}")
	print(f"{meal.upper()}")
	print("=" * 40)

	items = menu.get(meal.title(), [])

	if not items:
		print("No matching vegetarian/vegan items found.")
		return

	category = None

	for item in items:
		if item["category"] != category:
			category = item["category"]
			print(f"\n{category}")

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

	except requests.RequestException as error:
		print(f"Failed to retrieve menu: {error}")


if __name__ == "__main__":
	main()
