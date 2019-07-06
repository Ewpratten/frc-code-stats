import json
import os

from tba.teams import getTeamKeys, readTeamGithubURL

# Check for a save file
if not os.path.exists("./data.json"):
    # Create an empty json
    with open("./data.json", "w") as fp:
        data = {
            "config": {
                "latest_page": 0,
                "latest_github":0
            },
            "keys": [],
            "githubs":[]
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
        
except KeyboardInterrupt as e:
    print("CTRL+C detected")

# Dump to savefile
print("\nSaving data...")
with open("./data.json", "w") as fp:
    fp.write(json.dumps(save_file))
    fp.close()