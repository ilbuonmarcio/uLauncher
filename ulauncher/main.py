import json
import os


def get_db():
    try:
        with open('db.json', 'r') as db_file:
            content = "".join(db_file.readlines())
            db = json.loads(content)
            return db
    except Exception as e:
        print(e)
        print("db.json file not found, exiting.")
        exit(-1)

    
def choose_region(db):
    regions = set([elem['region'] for elem in db if elem['region'] is not None])
    print(f"Available regions: {', '.join(list(regions))}")
    region = input("Insert the region of your choice: ")

    if region in regions:
        return region
    else:
        print(f"Region {region} not found, exiting.")
        exit(-1)


def choose_game_loop(db, region):
    games = [elem for elem in db if elem['region'] == region]
    print(f"There are {len(games)} items available to download.\n")

    selected_games = []
    while True:
        print(f"[x] You currently have {len(selected_games)} in your queue ready to download.")
        search_text = input("Search for a game here: ")
        print(f"Searching for '{search_text}' in the database...\n\n")

        # Searching for game
        global_filtered = []
        for game in games:
            results = []
            for token in search_text.lower().split():
                results.append(token in game['name'].lower())
            if all(results):
                global_filtered.append(game)

        # Showing them
        print(f"There are {len(global_filtered)} search results!")
        for i, elem in enumerate(global_filtered):
            print()
            print(f"[{i+1}]\t({elem['titleKey']})", elem['name'].replace('\n', ' - '), end='')

        # Adding them to the download list
        to_download = input("\n\nWrite the ID of which one to download, separated by a comma: ")
        for i in [int(elem)-1 for elem in to_download.split(',')]:
            if global_filtered[i]['titleKey'] not in [game['titleKey'] for game in selected_games]:
                selected_games.append(global_filtered[i])

        continue_selecting = input("Games added to the download queue! Do you wanna continue? (y/n) ")
        if continue_selecting != 'y':
            print("Let's start downloading, then, shall we? :)\n\n")
            break

    print(f"We will start downloading {len(selected_games)} games right now...\n\n")
    for game in selected_games:
        print(f"Game to download: ({game['titleKey']})", game['name'].replace("\n", ' - '))
        os.system(f"start cmd.exe /k python FunKiiU.py -title {game['titleID']} -key {game['titleKey']}")
    
    print(f"\nAll {len(selected_games)} downloads started concurrently, helper will now exit, have fun!")


if __name__ == "__main__":
    db = get_db()
    region = choose_region(db)
    choose_game_loop(db, region)