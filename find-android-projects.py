#!/usr/bin/env python

import requests
import json
import time

### Constants ###
# Repository search url
repositorySerchUrl = 'https://api.github.com/search/repositories'
codeSearchUrl = 'https://api.github.com/search/code'

# Auth Header
access_token = 'ACCESS_TOKEN'

# Output File Name
filename = 'android_repos.json'
log_file = "output.log"
failed_log = "error.log"

class AndoridRepo:
    name=''
    repo=''
    stars=0

    def __init__(self, name, repo, stars):
        self.name = name
        self.repo = repo
        self.stars = stars

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

### Functions ###
def main():

    f = open(filename, 'w')
    log = open(log_file, 'w')
    error = open(failed_log, 'w')
    total = 0
    for pageNumber in range(1, 100):
        repositorySearchUrlParameters = {
                'q': 'Android+language:java+topic:android+topic:java',
                'sort': 'stars',
                'order': 'desc',
                'per_page': '100',
                'page': str(pageNumber)
        }
        respositoryPage = requests.get(repositorySerchUrl,
                params=repositorySearchUrlParameters,
                verify=False).json()

        if 'items' in respositoryPage:
            for item in respositoryPage['items']:
                total = total + 1
                write_log(log, 'Checking {} out of 10000: {}'.format(total, item['full_name']))
                if is_an_andorid_project(item, error):
                    write_to_file(f, AndoridRepo(item['full_name'], item['clone_url'], item['stargazers_count']))
        else:
            write_log(log, 'items not found while reading page {}'.format(pageNumber))
        time.sleep(60)

    f.close()
    log.close()
    error.close()


def is_an_andorid_project(item, errorLog):
    time.sleep(5)
    mySearchUrl = codeSearchUrl + "?q=" + 'filename:AndroidManifest.xml+path:/app/src/main+repo:' + item['full_name'] + "&access_token=" + access_token
    codeSearchResult = requests.get(mySearchUrl, verify=False).json()

    if 'total_count' in codeSearchResult:
        return codeSearchResult['total_count'] > 0
    else:
        write_log(errorLog, mySearchUrl)

def write_to_file(outputFile, repo):
    outputFile.write(repo.toJSON())
    outputFile.write('\n')
    outputFile.flush()

def read_from_file():
    data = []
    with open(filename,'rU') as f:
        for line in f:
           data.append(json.loads(line))
    return data

def write_log(file, message):
    file.write(message)
    file.write('\n')
    file.flush()
    print message

def jsonToString(jsonInput):
    return json.dumps(jsonInput, indent=4)

### Main ###
main()

# put your username/password here
# auth = ('myUsername', 'myPassword')

# Repositories
#respositoryPage = requests.get(repositorySerchUrl,
#        params=repositorySearchUrlParameters,
#        verify=False).json()

# get the token from the response
#for item in respositoryPage['items']:
#    print item

#print json.dumps(respositoryPage['items'], indent=4)
#print len(respositoryPage['items'])
#print json.dumps(respositoryPage['items'][0])
