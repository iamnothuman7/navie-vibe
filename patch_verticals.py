with open('navievibe/settings.py', encoding='utf-8') as f:
    content = f.read()

apps_to_add = ["cinema", "eventos", "parques"]
for app in apps_to_add:
    if f"'{app}'," not in content:
        content = content.replace("'parceiros',", f"'parceiros',\n    '{app}',")

with open('navievibe/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('settings.py atualizado com novos apps')
