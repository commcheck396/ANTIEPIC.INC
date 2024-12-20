import json
import json5
import demjson
import time
from datetime import datetime

startTime = time.time()

with open('../../data/australian_user_reviews.json', 'r') as f:
    # user_reviews = demjson.decode(f.read())
    user_reviews = json.load(f)

with open('../../data/australian_users_items.json', 'r') as f:
    # user_items = demjson.decode(f.read())
    user_items = json.load(f)

with open('../../data/steam_games.json', 'r') as f:
    # steam_games = demjson.decode(f.read())
    steam_games = json.load(f)

# with open('../../data/steam_review.json', 'r') as f:
#     steam_reviews = demjson.decode(f.read())
steam_games[0]
game_details = {
    game.get('id', None): {
        'developer': game.get('developer', None),
        'tags': game.get('tags', None)
    } for game in steam_games if game.get('id') is not None
}

user_data_map = {}

for user in user_reviews:
    user_id = user['user_id']
    user_data_map[user_id] = {
        'reviews': {},
        'items': {}
    }

    for review in user['reviews']:
        game_id = review['item_id']
        game_info = game_details.get(game_id, {})
        date = datetime.strptime(review['posted'], "Posted %B %d, %Y.")
        user_data_map[user_id]['reviews'][game_id] = {
            'posted': date,
            'recommend': review['recommend']
        }
# print(user_data_map["76561197970982479"])

for user in user_items:
    user_id = user['user_id']
    if user_id in user_data_map:
        for item in user['items']:
            game_id = item['item_id']
            game_info = game_details.get(game_id, {})
            if user_id not in user_data_map:
                user_data_map[user_id] = {
                    'reviews': {},
                    'items': {}
                }
            user_data_map[user_id]['items'][game_id] = {
                'game_id': game_id,
                'playtime_forever': item['playtime_forever'],
            }

user_data = {}

for user in user_reviews:
    user_id = user['user_id']
    user_data[user_id] = {
        'reviews': []
    }

    for review in user['reviews']:
        game_id = review['item_id']
        game_info = game_details.get(game_id, {})
        date = datetime.strptime(review['posted'], "Posted %B %d, %Y.")
        user_data[user_id]['reviews'].append({
            'game_id': game_id,
            'posted': date,
            'recommend': review['recommend']
        })

for user in user_items:
    user_id = user['user_id']
    if user_id in user_data:
        user_data[user_id]['items'] = []
        for item in user['items']:
            game_id = item['item_id']
            game_info = game_details.get(game_id, {})
            user_data[user_id]['items'].append({
                'game_id': game_id,
                'playtime_forever': item['playtime_forever'],
            })

gameToTag = {}
gameToDeveloper = {}
# print(len(steam_games))
for game in steam_games:
    game_id = game.get('id')
    tags = game.get('tags')
    developer = game.get('developer')
    if game_id is not None and tags is not None:
        gameToTag[game_id] = tags
        # gameToTag[game['id']] = game['tags']
    if game_id is not None and developer is not None:
        gameToDeveloper[game_id] = developer
        # gameToDeveloper[game['id']] = game['developer']
# print(len(gameToTag))
# print(len(gameToDeveloper))
endTime = time.time()
print(f"ReadDataTime: {endTime - startTime}")


def get_user_game_playtime(user_data_map, user_id, game_id):
    """
    获取用户在特定游戏的总游戏时长

    参数:
    - user_data_map: 用户游戏数据映射
    - user_id: 用户ID
    - game_id: 游戏ID

    返回:
    - 游戏时长（分钟），如果没有找到则返回0
    """
    # 检查用户是否存在于用户数据映射中
    if user_id not in user_data_map:
        return 0

    # 检查用户是否玩过该游戏
    user_items = user_data_map[user_id].get('items', {})
    if game_id not in user_items:
        return 0

    # 返回游戏时长
    return user_items[game_id].get('playtime_forever', 0)


def get_game_tags(game_details, game_id):
    """
    获取游戏的标签

    参数:
    - game_details: 游戏详情数据
    - game_id: 游戏ID

    返回:
    - 游戏标签列表，如果没有找到则返回空列表
    """
    # 检查游戏是否存在于游戏详情数据中
    if game_id not in game_details:
        return []

    tags = game_details[game_id].get('tags', [])
    return tags if tags else []


def get_game_developer(game_details, game_id):
    """
    获取游戏的开发者

    参数:
    - game_details: 游戏详情数据
    - game_id: 游戏ID

    返回:
    - 游戏开发者，如果没有找到则返回空字符串
    """
    # 检查游戏是否存在于游戏详情数据中
    if game_id not in game_details:
        return ''

    return game_details[game_id].get('developer', '')


def get_tags_user_played(user_data_map, user_id):
    """
    获取用户玩过的游戏标签

    参数:
    - user_data_map: 用户游戏数据映射
    - user_id: 用户ID

    返回:
    - 用户玩过的游戏标签列表
    """
    # 检查用户是否存在于用户数据映射中
    if user_id not in user_data_map:
        return []

    # 获取用户玩过的游戏ID列表
    user_items = user_data_map[user_id].get('items', {})
    game_ids = user_items.keys()

    # 获取用户玩过的游戏标签
    tags = []
    for game_id in game_ids:
        game_tags = get_game_tags(game_details, game_id)
        if game_tags:
            tags.extend(game_tags)

    return tags


def get_developer_user_played(user_data_map, user_id):
    """
    获取用户玩过的游戏开发者

    参数:
    - user_data_map: 用户游戏数据映射
    - user_id: 用户ID

    返回:
    - 用户玩过的游戏开发者列表
    """
    # 检查用户是否存在于用户数据映射中
    if user_id not in user_data_map:
        return []

    # 获取用户玩过的游戏ID列表
    user_items = user_data_map[user_id].get('items', {})
    game_ids = user_items.keys()

    # 获取用户玩过的游戏开发者
    developers = []
    for game_id in game_ids:
        developers.append(get_game_developer(game_details, game_id))

    return developers


def get_user_recommend_rate(user_data_map, user_id):
    """
    获取用户推荐率

    参数:
    - user_data_map: 用户游戏数据映射
    - user_id: 用户ID

    返回:
    - 用户推荐率
    """
    # 检查用户是否存在于用户数据映射中
    if user_id not in user_data_map:
        return 0

    # 获取用户的所有评价
    user_reviews = user_data_map[user_id].get('reviews', {})
    reviews = user_reviews.values()

    # 计算用户的推荐率
    total_reviews = len(reviews)
    if total_reviews == 0:
        return 0

    total_recommend = 0
    for review in reviews:
        total_recommend += review.get('recommend', False)

    return total_recommend / total_reviews


def get_game_recommend_rate(user_data_map, game_id):
    """
    获取游戏的推荐率

    参数:
    - user_data_map: 用户游戏数据映射
    - game_id: 游戏ID

    返回:
    - 游戏推荐率
    """
    # 获取玩过该游戏的用户ID列表
    user_ids = [user_id for user_id, user_data in user_data_map.items() if game_id in user_data['items']]

    # 计算游戏的推荐率
    total_users = len(user_ids)
    if total_users == 0:
        return 0

    total_recommend = 0
    for user_id in user_ids:
        total_recommend += get_user_recommend_rate(user_data_map, user_id)

    return total_recommend / total_users


def get_game_jaccard_similarity(game_id_1, game_id_2):
    """
    获取两个游戏的Jaccard相似度

    参数:
    - game_id_1: 游戏ID1
    - game_id_2: 游戏ID2

    返回:
    - 两个游戏的Jaccard相似度
    """
    # 获取两个游戏的标签
    tags_1 = set(get_game_tags(game_details, game_id_1))
    tags_2 = set(get_game_tags(game_details, game_id_2))

    # 计算Jaccard相似度
    union = tags_1.union(tags_2)
    intersection = tags_1.intersection(tags_2)
    return len(intersection) / len(union) if len(union) > 0 else 0


def get_user_jaccard_similarity(user_id_1, user_id_2):
    """
    获取两个用户的Jaccard相似度

    参数:
    - user_id_1: 用户ID1
    - user_id_2: 用户ID2

    返回:
    - 两个用户的Jaccard相似度
    """
    # 获取两个用户的标签
    tags_1 = set(get_tags_user_played(user_data_map, user_id_1))
    tags_2 = set(get_tags_user_played(user_data_map, user_id_2))

    # 计算Jaccard相似度
    union = tags_1.union(tags_2)
    intersection = tags_1.intersection(tags_2)
    return len(intersection) / len(union) if len(union) > 0 else 0


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def extract_features(user_id, game_id):
    """
    提取用户和游戏的特征
    """
    features = {}

    features["playtime"] = get_user_game_playtime(user_data_map, user_id, game_id)

    user_tags = set(get_tags_user_played(user_data_map, user_id))
    game_tags = set(get_game_tags(game_details, game_id))
    features["tag_similarity"] = len(user_tags.intersection(game_tags)) / len(
        user_tags.union(game_tags)) if user_tags and game_tags else 0

    game_dev = get_game_developer(game_details, game_id)
    user_devs = set(get_developer_user_played(user_data_map, user_id))
    features["developer_similarity"] = 1 if game_dev in user_devs else 0

    features["game_recommend_rate"] = get_game_recommend_rate(user_data_map, game_id)

    features["user_recommend_rate"] = get_user_recommend_rate(user_data_map, user_id)

    recommended_games = [g_id for g_id in user_data_map[user_id].get('items', {}).keys() if
                         user_data_map[user_id]['reviews'].get(g_id, {}).get('recommend', False)]
    game_jaccard = [get_game_jaccard_similarity(game_id, rec_game) for rec_game in recommended_games]
    features["game_jaccard_similarity"] = np.mean(game_jaccard) if game_jaccard else 0

    recommenders = [uid for uid, udata in user_data_map.items() if
                    game_id in udata.get('items', {}) and udata['reviews'].get(game_id, {}).get('recommend', False)]
    user_jaccard = [get_user_jaccard_similarity(user_id, recommender) for recommender in recommenders]
    features["user_jaccard_similarity"] = np.mean(user_jaccard) if user_jaccard else 0

    return features


X = []
y = []
print(1)
startTime = time.time()
for user_id, user_data in user_data_map.items():
    for game_id in user_data.get('items', {}):
        features = extract_features(user_id, game_id)
        X.append(features)

        is_recommended = user_data['reviews'].get(game_id, {}).get('recommend', False)
        y.append(1 if is_recommended else 0)
endTime = time.time()
print(f"循环时间: {endTime - startTime}")
X = pd.DataFrame(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))