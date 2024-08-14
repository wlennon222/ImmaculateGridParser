import json
import urllib.request
import pprint

from prettytable import PrettyTable
from bs4 import BeautifulSoup

teams_dict = dict()  # TODO: turn this in to class instead of global dicts
grids = dict()


def open_url(grid_number):

    url = f'https://www.immaculategrid.com/football/grid-{grid_number}'
    fp = urllib.request.urlopen(url)
    html_bytes = fp.read()

    decoded_bytes = html_bytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(decoded_bytes, 'html.parser')

    # Find all buttons with the specified class
    buttons = soup.find_all('button', class_='focus:bg-yellow-200 w-full h-full')

    # Extract and print the aria-label attribute from each button
    grids[grid_number] = []
    for button in buttons:
        aria_label = button.get('aria-label')

        l1 = aria_label.split(' + ')
        l1 = [s.strip() for s in l1]
        grids[grid_number].append(l1)


def read_json():
    combos = dict()
    # Read the JSON file
    with open('grid_data.json', 'r') as json_file:
        loaded_data = json.load(json_file)

    # Print the loaded data
    for vals in loaded_data.values():
        for team_list_1 in vals:
            connection_tuple = tuple(sorted(team_list_1))
            if connection_tuple not in combos:
                combos[connection_tuple] = 1
            else:
                combos[connection_tuple] += 1
    print_table(combos)


def print_table(combos):
    # Create a PrettyTable instance
    combos = dict(sorted(combos.items(), key=lambda item: item[1], reverse=True))

    table = PrettyTable()
    table.field_names = ['Team 1', 'Team 2', 'Connection Count']
    # Add data to the table
    for connection, count in combos.items():
        table.add_row([connection[0], connection[1], count])

    # Set the alignment of columns
    table.align['Team 1'] = 'l'
    table.align['Team 2'] = 'l'

    # Print the table
    print(table)
    print_team_totals()


def print_team_totals():
    # Sort the dictionary by the values (integers) in descending order
    sorted_dict = dict(sorted(teams_dict.items(), key=lambda item: item[1], reverse=True))
    for key, value in sorted_dict.items():
        print(f"{key}: {value}")


def write_all_grids_to_json():
    most_recent_grid_number = 390  # TODO: replace this with dynamic value instead of hardcoded value.
    for i in range(most_recent_grid_number, 0, -1):
        print(f"Running grid: {i}")
        open_url(i)

    print(grids)

    json_data = json.dumps(grids, indent=2)

    # Write the JSON string to a file
    with open('grid_data.json', 'w') as json_file:
        json_file.write(json_data)


def run():
    # Writing to json and then reading from it to capture the data and process it
    # from the json rather than scraping every run.
    write_all_grids_to_json()
    read_json()


if __name__ == '__main__':
    run()
