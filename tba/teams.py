import tbaapiv3client
import requests

client_key = requests.get("https://api.retrylife.ca/auth/tba").json()["key"]

configuration = tbaapiv3client.Configuration()
configuration.api_key['X-TBA-Auth-Key'] = client_key

list_api = tbaapiv3client.ListApi(tbaapiv3client.ApiClient(configuration))
team_api = tbaapiv3client.TeamApi(tbaapiv3client.ApiClient(configuration))

def getTeamKeys(page: int):
    """Get a list of team keys in a page size of 500"""
    return list_api.get_teams_keys(page)

def readTeamGithubURL(key: str):
    global client_key

    # API issue, use requests
    response = requests.get("https://www.thebluealliance.com/api/v3/team/" + key + "/social_media", headers={"X-TBA-Auth-Key": client_key}).json()
    # response = team_api.get_team_social_media(key)

    # Check for a github account
    for media in response:
        if media["type"] == "github-profile":
            return media["foreign_key"] 
    else:
        return None