import requests
import pytablewriter

session = requests.Session()
headers = {'X-HockeyAppToken': ''}


def apps():
    response = session.get('https://rink.hockeyapp.net/api/2/apps', headers=headers)
    return response.json()['apps']


def app_versions(app_id):
    versions_url = 'https://rink.hockeyapp.net/api/2/apps/' + app_id + '/app_versions'
    versions_response = session.get(versions_url, headers=headers)
    return versions_response.json()['app_versions']


writer = pytablewriter.MarkdownTableWriter()
writer.table_name = "HockeyApp Apps"
writer.header_list = ["Title", "Platform", "Bundle identifier", "HockeyApp ID", "Last updated"]

app_list = []

for app in apps():
    versions = app_versions(app['public_identifier'])

    line = [app['title'], app['platform'], app['bundle_identifier'], app['public_identifier']]

    if versions:
        line.append(versions[0]['timestamp'])
    else:
        line.append('')

    app_list.append(line)

writer.value_matrix = app_list
writer.write_table()

