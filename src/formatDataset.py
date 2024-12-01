import re
import json
import os
import subprocess
# modify all the files under the path ../data/
# fetch all the files under the path ../data/
path = '../data/'
files = os.listdir(path)
files.sort()
SAMPLE_SIZE = 2000
sampledUsers = set()
sampledGames = set()
for file in files:
    if not os.path.isdir(file):
        if file == 'steam_games.json':
            with open(path + file, 'r') as f:
                lines = f.readlines()
            lines.sort()
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
                # get the game_id
                # pattern: 'id': '761140'
                curGame = re.search(r"'id': '(.+?)'", line)
                if curGame:
                    curGame = curGame.group(1)
                    if curGame not in sampledGames:
                        continue
                else:
                    continue
                data.append(line + ',')
            data[-1] = data[-1][:-1]
            data.append(']')
            with open(path + file, 'w') as file:
                file.writelines(data)
        elif file == 'australian_users_items.json':
            with open(path + file, 'r') as f:
                lines = f.readlines()
            lines.sort()
            if len(lines) > SAMPLE_SIZE:
                lines = lines[:SAMPLE_SIZE]
            proUsers = []
            data = ['[']
            for line in lines:
                # if line is longer than 1000, record the user_id and steam_id to file ../data/pro_user.json, then skip this line
                # Format: 'user_id': 'btuty8trgt', 'items_count': 99, 'steam_id': '76561198054746068', 'user_url': 'http://steamcommunity.com/id/btuty8trgt',
                if len(line) > 2500:
                    user_id = re.search(r"'user_id': '(.+?)'", line).group(1)
                    steam_id = re.search(r"'steam_id': '(.+?)'", line).group(1)
                    proUsers.append([user_id, steam_id])
                    continue
                # replace all the True to true
                line = re.sub(r'True', 'true', line)
                # replace all the False to false
                line = re.sub(r'False', 'false', line)
                # pattern: 'user_id': '76561198028895010'
                curUser = re.search(r"'user_id': '(.+?)'", line)
                if curUser:
                    curUser = curUser.group(1)
                    if curUser not in sampledUsers:
                        continue
                else:
                    continue
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
            lines.sort()
            if len(lines) > SAMPLE_SIZE:
                lines = lines[:SAMPLE_SIZE]
            data = ['[']
            for line in lines:
                # pattern: 'user_id': '76561197970982479'
                curUser = re.search(r"'user_id': '(.+?)'", line)
                if curUser:
                    curUser = curUser.group(1)
                    sampledUsers.add(curUser)
                # pattern: 'item_id': '1250'
                curGame = re.findall(r"'item_id': '(.+?)'", line)
                if curGame:
                    for game in curGame:
                        sampledGames.add(game)
                # replace all the True to true
                line = re.sub(r'True', 'true', line)
                # replace all the False to false
                line = re.sub(r'False', 'false', line)
                data.append(line + ',')
            data[-1] = data[-1][:-1]
            data.append(']')
            with open(path + file, 'w') as file:
                file.writelines(data)

