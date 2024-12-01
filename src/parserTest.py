import re

line = ': True, \'review\': "It\'s like Skyrim but with guns :D :D :D10/10"}]}'
line = re.sub(r", 'review': .*?}", '}', line)
print(line)
