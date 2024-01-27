from re import L
from flask import Flask, request, render_template,redirect,url_for
from werkzeug.utils import secure_filename
from SearchFiles_origin import search, init
from imhsearch import imgsearch
kinds=['功能机','手机','相机','电脑','音响','鼠标','键盘','手环','内存']
others=['iphone','骁龙','256GB','128GB','拍照手机','5G','mate50','蓝牙','单反防抖','4K高清','酷睿i','MateBook13英寸','10英寸','智能','记步','睡眠心率']
brands=['小米','华为','荣耀','苹果','vivo','oppo','三星','联想','宏碁','华硕','佳能','索尼']
sort=['price_i','price_d','comprehensive,0.5','default','score']
app = Flask(__name__)

@app.before_first_request
def initialize():
    init()    

@app.route("/")
def homepage():
    return render_template("homepage.html", kinds=kinds, brands=brands, others=others)

@app.route('/upload')
def upload_file():
     return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
         f = request.files['file']
         securename=secure_filename(f.filename)
         f.save(securename)
         #return imgsearch(securename)
         return redirect(url_for('fanye',page=1,keyword=imgsearch(securename),h='999999',l='1',sort='default'))

@app.route("/search/page=<int:page>", methods=["GET"])
def result(page):
    brand_i = []
    kind_i = []
    other_i = []
    keyword = request.args.get("keyword")
    keyword_i = keyword
    if not keyword:
        return render_template("homepage.html", brands=brands, kinds=kinds, others=others)
    tmp=''
    for i in kinds:
        if (request.args.get(i)):
            tmp+="OR{}".format(i)
            kind_i.append(i)
    if(tmp):
        keyword+="AND({})".format(tmp[2:])
    
    tmp = ''
    for i in brands:
        if (request.args.get(i)):
            tmp += "OR{}".format(i)
            brand_i.append(i)
    if(tmp):
        keyword = "({})AND({})".format(keyword,tmp[2:])

    tmp = ''
    for i in others:
        if (request.args.get(i)):
            tmp += "OR{}".format(i)
            other_i.append(i)
    if(tmp):
        keyword = "({})AND({})".format(keyword, tmp[2:])
    
    l=request.args.get('lower-bound')
    if not l:
        l='1'
    h = request.args.get('upper-bound')
    if not h:
        h='999999'
    
    sort=request.args.get("sort","default")
    if sort=='comprehensive':
        n=float(request.args.get("comprehensive"))/10
        sort+=',{}'.format(n)
    
    total, ans = search(keyword,l,h,sort, page - 1)
    # for ele in ans:
    #     ele["name"] = ele["name"].replace(keyword, '<span style="color: red;">'+keyword+'</span>')
    return render_template("result.html", keyword=keyword, ans=ans, current_page=page, pages=[i for i in range(1, 11)], 
        total=total,l=l,h=h,sort=sort, brands=brands, kinds=kinds, others=others)
        # brand_i=brand_i, kind_i=kind_i, other_i=other_i)

@app.route("/search/page=<int:page>?keyword=<string:keyword>&sort=<string:sort>&lower-bound=<string:l>&upper-bound=<string:h>")
def fanye(keyword, l,h,sort,page):
    total, ans = search(keyword, l,h,sort,page - 1)
    return render_template("result.html", keyword=keyword, ans=ans, current_page=page, pages=[i for i in range(1, 11)], 
        total=total,l=l, h=h, sort=sort, brands=brands, kinds=kinds, others=others)
        # brand_i=brand_i, kind_i=kind_i, other_i=other_i)

if __name__ == "__main__":
    app.run(debug=True)
