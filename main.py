import json
import os
from collections import Counter

from tba.teams import getTeamKeys, readTeamGithubURL
from github.account import getLangs

# Check for a save file
if not os.path.exists("./data.json"):
    # Create an empty json
    with open("./data.json", "w") as fp:
        data = {
            "config": {
                "latest_page": 0,
                "latest_github": 0,
                "latest_github_parse": 0,
                "langs_sorted": [],
                "langs_grouped": []
            },
            "keys": [],
            "githubs": [],
            "langs":[]
        }
        fp.write(json.dumps(data))
        fp.close()
    
# Load the save file as a json object
save_file = None
with open("./data.json", "r") as fp:
    save_file = json.load(fp)
    fp.close()


# Print info about savefile
print(f"Last session ended at {save_file['config']['latest_page']} pages")

# Main script
try:
    # Get keys
    while True:
        team_keys = getTeamKeys(save_file["config"]["latest_page"])
        
        # Check if we hit max
        if team_keys == []:
            break
        
        # save to keys list
        save_file["keys"] += team_keys

        # increment page
        save_file["config"]["latest_page"] += 1

        # print status
        print(f"Pulling teams from page: {save_file['config']['latest_page']}          ", end="\r")
    print()
    
    # Get githubs
    print(f"Last session parsed {save_file['config']['latest_github']} teams for github accounts")
    teams_to_parse = save_file["keys"][save_file['config']['latest_github']:]
    for team in teams_to_parse:
        # Check for invalid teams
        if team == None:
            continue

        # Get data
        github = readTeamGithubURL(team)
        save_file['config']['latest_github'] += 1

        # If they have an account, add to list
        if github != None:
            save_file["githubs"].append({"team": team, "account": github})
            print(f"Found github account for team {team}         ", end="\r")
    print()

    # Get Languages
    print(f"Last session parsed {save_file['config']['latest_github_parse']} valid github accounts")
    githubs_to_parse = save_file["githubs"][save_file['config']['latest_github_parse'] :]
    for account in githubs_to_parse:
        team_langs = getLangs(account["account"])

        save_file["langs"] += team_langs
        save_file['config']['latest_github_parse'] += 1
        print(f"Loaded languages for github account: {account['account']} ({save_file['config']['latest_github_parse']})                                        ", end="\r")
    print()

    # Sort
    print("Sorting Languages by usage")
    save_file["langs_sorted"] = [item for items, c in Counter(save_file["langs"]).most_common() for item in [items] * c]
    langs = list(dict.fromkeys(save_file["langs_sorted"]))

    # print number of occurenced
    for lang in langs:
        print(f"{save_file['langs_sorted'].count(lang)} occurrences of {lang}")
    
        
except KeyboardInterrupt as e:
    print("CTRL+C detected")

# Dump to savefile
print("\nSaving data...")
with open("./data.json", "w") as fp:
    fp.write(json.dumps(save_file))
    fp.close()