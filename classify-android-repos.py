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

# File Names
filename = 'repos-to-classify.json'
info_log_file = "class-info.log"
error_log_file = "class-error.log"
result_log_file = 'classified-repos.json'

# Classes
class_query_map={
    'rx-java': ['RxJava'],
    'async-task': ['.AsyncTask%3B'],
    'loader' : ['.LoaderManager%3B'],
    'async-task-loader': ['.AsyncTaskLoader%3B'],
    'intent-service': ['.IntentService'],
    'job-intent-service': ['.JobIntentService'],
    'external-storage': ['WRITE_EXTERNAL_STORAGE', 'READ_EXTERNAL_STORAGE'],
    'internal-storage': ['WRITE_INTERNAL_STORAGE', 'READ_INTERNAL_STORAGE'],
    'internet': ['permission.INTERNET']
}

def main():

    info = open(info_log_file, 'w')
    error = open(error_log_file, 'w')
    result = open(result_log_file, 'w')

    with open(filename,'rU') as f:
        for line in f:
            repoJson = json.loads(line)
            classes = get_classes(repoJson['name'], info, error)
            write_log(result, RepoClass(repoJson['name'], repoJson['repo'], repoJson['stars'], classes).toJSON())

    info.close()
    error.close()
    result.close()

def get_classes(repo_name, info_log, error_log):
    classes=[]
    for key,value in class_query_map.iteritems():
        for query in value:
            if check_repo_for_query(repo_name, query, info_log, error_log):
                classes.append(key)
                break

    if len(classes) < 1:
        classes.append('none')

    return classes

def check_repo_for_query(repo_name, query, info_log, error_log):
    time.sleep(5)
    mySearchUrl = codeSearchUrl + "?q="  + query + '+repo:' + repo_name + "&access_token=" + access_token
    codeSearchResult = requests.get(mySearchUrl, verify=False).json()

    if 'total_count' in codeSearchResult:
        return codeSearchResult['total_count'] > 0
    else:
        write_log(errorLog, mySearchUrl)


def write_log(file, message):
    file.write(message)
    file.write('\n')
    file.flush()
    print message

class RepoClass:
    name=''
    repo=''
    stars=0
    classes=[]

    def __init__(self, name, repo, stars, classes):
        self.name = name
        self.repo = repo
        self.stars = stars
        self.classes = classes

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

### Main ###
main()
