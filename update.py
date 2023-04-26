import requests
class Updater:
    def __init__(self):
        # repo = Github(login_or_token='Iv1.5aae7b1280a26a63', password='77b68bc95eca67303216027b84d73be8db46d4b9', verify=False).get_repo('ChrisHairstonBnR/Python-Successor-Finder')
        # releases = repo.get_releases()
        # self.latestVersion = releases[0].title
        # self.latestVersionLink = releases[0].zipball_url
        
        response = requests.get("https://api.github.com/repos/ChrisHairstonBnR/Python-Successor-Finder/releases", verify=False)
        responseJSON = response.json()
        self.latestVersion = responseJSON[0]['tag_name']
        self.latestVersionLink = responseJSON[0]['assets'][0]['browser_download_url']

        
        