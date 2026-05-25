with open('navievibe/settings.py', encoding='utf-8') as f:
    content = f.read()

content = content.replace("    'api',\r\n]", "    'api',\r\n    'parceiros',\r\n]")

with open('navievibe/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('settings.py atualizado com sucesso')
