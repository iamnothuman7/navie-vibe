import shutil
from PIL import Image

original_path = r"C:\Users\mateu\.gemini\antigravity\brain\17f010dd-1797-4f03-8d92-2926629161a6\navie_logo_1776308739412.png"
target_path = r"c:\Dev\JAVA\Naviê Vibe\static\images\logo.png"

# Puxa a original de volta
shutil.copy(original_path, target_path)

img = Image.open(target_path)
width, height = img.size

# Corta 15% das bordas (onde a IA desenhou a linha)
left = int(width * 0.15)
top = int(height * 0.15)
right = width - left
bottom = height - top

img = img.crop((left, top, right, bottom))
img = img.convert("RGBA")
datas = img.getdata()

newData = []
for item in datas:
    # Ajusta o limiar pra garantir fundo todo fora
    if item[0] > 230 and item[1] > 230 and item[2] > 230:
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

img.putdata(newData)
img.save(target_path, "PNG")

print("Nova logo processada sem a linha de borda!")
