from github import *

class Updater:
    def __init__(self):
        repo = Github('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', verify=False).get_repo('ChrisHairstonBnR/Python-Successor-Finder')
        releases = repo.get_releases()
        self.latestVersion = releases[0].title
        #self.latestVersion = repo.get_latest_release().title
        self.latestVersionLink = releases[0].zipball_url
        
        