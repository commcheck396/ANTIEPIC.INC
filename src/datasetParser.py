import re
import json
import os
import subprocess
# modify all the files under the path ../data/
# fetch all the files under the path ../data/
path = '../data/'
files = os.listdir(path)

for file in files:
    if not os.path.isdir(file):
        if file == 'steam_games.json':
            with open(path + file, 'r') as f:
                lines = f.readlines()
            data = ['[']
            for line in lines:
                # replace all the True to true
                line = re.sub(r'True', 'true', line)
                # replace all the False to false
                line = re.sub(r'False', 'false', line)
                # replace all the u' to '
                line = re.sub(r"u'", "'", line)
                # replace all the u" to "
                line = re.sub(r'u"', '"', line)

                # delete title info with ' and "
                # format #1: 'title': 'Angry Video Game Nerd: The Movie'
                # format #2: 'title': "Garry's Mod"
                line = re.sub(r"'title': '(?:\\.|[^'])*',", '', line)
                line = re.sub(r"'title': '(?:\\.|[^'])*'", '', line)
                line = re.sub(r'\'title\': "(.+?)",', '', line)
                line = re.sub(r'\'title\': "(.+?)"', '', line)
                
                line = re.sub(r"'app_name': '(?:\\.|[^'])*',", '', line)
                line = re.sub(r"'app_name': '(?:\\.|[^'])*'", '', line)
                line = re.sub(r'\'app_name\': "(.+?)",', '', line)
                line = re.sub(r'\'app_name\': "(.+?)"', '', line)

                # delete all the ".*" info
                line = re.sub(r'"(.+?)"', '\'Unknown\'', line)

                # delete all the \x
                line = re.sub(r'\\x', '', line)

                data.append(line + ',')
            data[-1] = data[-1][:-1]
            data.append(']')
            with open(path + file, 'w') as file:
                file.writelines(data)

        elif file == 'australian_users_items.json':
            with open(path + file, 'r') as f:
                lines = f.readlines()
            proUsers = []
            data = ['[']
            for line in lines:
                # if line is longer than 1000, record the user_id and steam_id to file ../data/pro_user.json, then skip this line
                # Format: 'user_id': 'btuty8trgt', 'items_count': 99, 'steam_id': '76561198054746068', 'user_url': 'http://steamcommunity.com/id/btuty8trgt',
                if len(line) > 3000:
                    user_id = re.search(r"'user_id': '(.+?)'", line).group(1)
                    steam_id = re.search(r"'steam_id': '(.+?)'", line).group(1)
                    proUsers.append([user_id, steam_id])
                    continue
                # replace all the True to true
                line = re.sub(r'True', 'true', line)
                # replace all the False to false
                line = re.sub(r'False', 'false', line)
                # delete item_name info with ' and "
                # format #1: 'item_name': 'Angry Video Game Nerd: The Movie'
                # format #2: 'item_name': "Garry's Mod"
                line = re.sub(r"'item_name': '(?:\\.|[^'])*',", '', line)
                line = re.sub(r"'item_name': '(?:\\.|[^'])*'", '', line)
                line = re.sub(r'\'item_name\': "(.+?)",', '', line)
                line = re.sub(r'\'item_name\': "(.+?)"', '', line)
                data.append(line + ',')
            data[-1] = data[-1][:-1]
            data.append(']')
            with open(path + file, 'w') as file:
                file.writelines(data)
            # print(proUsers)
            with open(path + 'pro_user.json', 'w') as file:
                json.dump(proUsers, file)


        else:
            with open(path + file, 'r') as f:
                lines = f.readlines()
            data = ['[']
            for line in lines:
                if len(line) > 5000:
                    continue
                # replace all the True to true
                line = re.sub(r'True', 'true', line)
                # replace all the False to false
                line = re.sub(r'False', 'false', line)
                # delete all the {LINK REMOVED}
                line = re.sub(r'{LINK REMOVED}', '', line)
                # delete all the review
                # format: 'review': .* }
                line = re.sub(r", 'review': .*?}", '}', line)
                # delete all the \' and \"
                # line = re.sub(r"\\'", '', line) 
                # line = re.sub(r'\\"', '', line)
                # line = re.sub(r", 'review': .*}", '', line)
                # line = re.sub(r"'review': '(.+?)'", '', line)
                # line = re.sub(r'\'review\': "(.+?)",', '', line)
                # line = re.sub(r'\'review\': "(.+?)"', '', line)
                data.append(line + ',')
            data[-1] = data[-1][:-1]
            data.append(']')
            with open(path + file, 'w') as file:
                file.writelines(data)

        # result = subprocess.run(
        #         ["bash", 'v ./formatDataset.sh'],
        #         check=True,             
        #         stdout=subprocess.PIPE, 
        #         stderr=subprocess.PIPE  
        #     )