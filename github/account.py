import re
import requests

language_re = re.compile('programmingLanguage"\>(.*)\<')

def isOrgAccount(user):
    response = requests.get("https://github.com/" + user).text
    # print(response)
    return not bool(re.search("\?tab=following(.*)", response))

def getLangs(user):
    response = requests.get("https://github.com/" + user).text

    output = []
    for lang in re.findall('programmingLanguage"\>(.*)\<', response):
        output.append(lang)
    
    return output