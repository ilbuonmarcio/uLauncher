import json
import multiprocessing
from re import sub
import subprocess
import FunKiiU
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
        try:
            for i in [int(elem)-1 for elem in to_download.split(',')]:
                if global_filtered[i]['titleKey'] not in [game['titleKey'] for game in selected_games]:
                    selected_games.append(global_filtered[i])

            continue_selecting = input("Games added to the download queue! Do you wanna continue? (y/n) ")
            if continue_selecting != 'y':
                print("Let's start downloading, then, shall we? :)\n\n")
                break
        except:
            print("Error format on ID to download, passing")        

    if len(selected_games) > 0:
        print(f"We will start downloading {len(selected_games)} games right now...\n\n")
        download_processes = []
        for game in selected_games:
            print(f"Downloading: ({game['titleKey']})", game['name'].replace("\n", ' - '))
            p = multiprocessing.Process(target=download_worker, args=(game['titleID'], game['titleKey']))
            p.start()
            download_processes.append(p)

        print(f"\nAll {len(selected_games)} downloads started concurrently, helper will now wait before decrypting!")
        print("Wait the script to finish downloading all games, please hang tight...")
        [p.join() for p in download_processes]

        print("All files downloaded successfully!")
    else:
        print("No games to download, skipping this step")

    # Decryption step
    decrypt_all_encrypted_games()


def download_worker(title, key):
    FunKiiU.main(titles=[title], keys=[key])


def decrypt_all_encrypted_games():
    decrypt_processes = []
    for path in os.listdir('./install/'):
        print(f"Launching decrypting files at {path}", end="")
        if os.path.isdir(f'./install/{path}/code/'):
            print("-> Game already decrypted, skipping...")
            continue

        # Decryption step (asynchronous, be sure to avoid memory swap on low end devices!)
        p = multiprocessing.Process(target=decrypt_game, args=(path,))
        p.start()
        decrypt_processes.append(p)
        print("-> done!")

    print("\nWaiting for decryption of all files to end...")

    [p.join() for p in decrypt_processes]
    print("\n\nAll games decrypted successfully!\n")


def decrypt_game(gamepath):
    # Copying decryptor files
    subprocess.Popen(f"powershell -Command Copy-Item ./decrypt.bat, ./CDecrypt_v2.0b.exe, ./libeay32.dll, ./msvcr120d.dll -Destination ./install/{gamepath}/").wait()
    
    # Running decrypt
    subprocess.Popen(f"powershell -Command cd ./install/{gamepath}/; ./decrypt.bat").wait()

    print(f"Game at path {gamepath} decrypted successfully!")


if __name__ == "__main__":
    db = get_db()
    region = choose_region(db)
    choose_game_loop(db, region)