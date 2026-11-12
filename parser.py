from bs4 import BeautifulSoup


def parse_menu(html):
    soup = BeautifulSoup(html, "html.parser")

    menu = {}
    current_meal = None
    current_category = None

    elements = soup.select(
        ".shortmenumeals, .shortmenucats, .shortmenurecipes"
    )

    for element in elements:
        classes = element.get("class", [])
        text = element.get_text(" ", strip=True)

        if "shortmenumeals" in classes:
            current_meal = text
            menu[current_meal] = []
            current_category = None

        elif "shortmenucats" in classes:
            current_category = text.strip("- ").title()

        elif "shortmenurecipes" in classes:
            if current_meal is None:
                continue

            # Find the row containing the recipe and its icons.
            inner_row = element.find_parent("tr")
            icons = []

            if inner_row:
                icons = [
                    img["src"].split("/")[-1].removesuffix(".gif")
                    for img in inner_row.find_all("img")
                ]

                # Find the outer row to locate its description.
                outer_table = inner_row.find_parent("table")
                outer_row = (
                    outer_table.find_parent("tr")
                    if outer_table else None
                )

            description = None

            if outer_row:
                next_row = outer_row.find_next_sibling("tr")
                if next_row:
                    desc = next_row.select_one(".shortmenuproddesc")
                    if desc:
                        description = desc.get_text(" ", strip=True)

            # Only include vegetarian or vegan items.
            if not any(
                indicator in ("vegetarian", "vegan")
                for indicator in icons
            ):
                continue

            menu[current_meal].append({
                "name": text,
                "category": current_category,
                "indicators": icons,
                "description": description
            })
    return menu
