from PIL import Image

def remove_background(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Pega pixels brancos ou muito claros
        if item[0] > 235 and item[1] > 235 and item[2] > 235:
            newData.append((255, 255, 255, 0)) # Transparente
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(image_path, "PNG")

remove_background(r"c:\Dev\JAVA\Naviê Vibe\static\images\logo.png")
print("Fundo removido.")
