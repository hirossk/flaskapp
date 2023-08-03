from flask import Flask,render_template,request
from PIL import Image, ImageDraw

from WordCloudMaker import WordCloudMaker
app = Flask(__name__,static_folder="./templates/images")
tictac = False
 
def saveimage(fid):
    wc = WordCloudMaker(font_path='./ipaexg.ttf')
    # ワードクラウドの作成
    wc.read_file(filename="file.txt")
    # Windowsパソコンのドライブ直下に画像を保存
    wc.create('templates/images/' + fid +'.jpg') 

@app.route('/')
def display():
    saveimage("imgdraw1")
    #im = Image.new("RGB", (800, 600), (128, 128, 128))
    #draw = ImageDraw.Draw(im)
    #draw.line((0, im.height, im.width, 0), fill=(255, 0, 0), width=8)
    #draw.rectangle((100, 100, 200, 200), fill=(0, 255, 0))
    #draw.ellipse((250, 300, 450, 400), fill=(0, 0, 255))
    #im.save('templates/images/imgdraw.jpg', quality=95)
    html = render_template('index.html',srcname = "images/imgdraw1.jpg")
    
    return html #'Hello, Remote Flask too!'

@app.route('/<int:id>')
def id_func(id):
    saveimage(str(id))
    return render_template('index.html',srcname = 'images/' + str(id) + '.jpg')
    
@app.route('/word',methods=['GET', 'POST'])
def put_words():
    global tictac
    if request.method == 'GET':
        words = request.args.get("word","")
        #print(words)
        with open('file.txt', mode='a', encoding='utf-8') as f:
            f.write(words + '\n')
            f.close()

    if tictac:
        fid = "imgdraw1"
    else:
        fid = "imgdraw2"
    tictac = not tictac
    saveimage(fid)
    html = render_template('index.html',srcname = "images/" + fid + ".jpg")
    
    return html

@app.route('/reset',methods=['GET', 'POST'])
def reset_words():
    with open('file.txt', mode='w') as f:
        f.close()
    im = Image.new("RGB", (800, 600), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    im.save('templates/images/imgdraw1.jpg', quality=95)
    im.save('templates/images/imgdraw2.jpg', quality=95)
    html = render_template('index.html',srcname = "images/imgdraw1.jpg")
    
    return html

if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=False)