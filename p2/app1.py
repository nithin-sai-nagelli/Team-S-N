import psycopg2
from flask import Flask, request, redirect
from flask.templating import render_template

app = Flask(__name__,template_folder='template')
app.debug = True

con=psycopg2.connect(host="localhost",database="pro",user="postgres",password="ss@369")
cursor_obj=con.cursor()

@app.route('/')
def start():
    return render_template('login.html')

@app.route('/select/<int:a>')
def select(a):
   sql= '''select subcategory.subcat_id,subcategory.subcategory from cathassubcat,subcategory where cathassubcat.category_id=''' +str(a)+ '''and cathassubcat.subcat_id=subcategory.subcat_id limit ''' + str(9)
   cursor_obj.execute(sql)
   profiles=cursor_obj.fetchall()
   return render_template('subcat.html',profiles=profiles)

@app.route('/selectb/<int:a>')
def selectb(a):
   sql= '''select brand.brand_id,brand.brand from subcathasbrand,brand where subcathasbrand.subcat_id=''' +str(a)+ '''and subcathasbrand.brand_id=brand.brand_id '''
   cursor_obj.execute(sql)
   profiles=cursor_obj.fetchall()
   return render_template('brand.html',profiles=profiles)

@app.route('/selectp/<int:a>')
def selectp(a):
   sql= '''select product.no_of_likes,product.product_id,image from brandhaspdt,product,productlink where brandhaspdt.brand_id=''' +str(a)+ '''and brandhaspdt.product_id=product.product_id and product.product_id=productlink.product_id '''
   cursor_obj.execute(sql)
   profiles=cursor_obj.fetchall()
   return render_template('product.html',profiles=profiles)

@app.route('/selecti/<int:a>')
def selecti(a):
    sql='''select actual_price,current_price,discount,no_of_likes,image,product.product_id,quantity from product,productlink where product.product_id='''+str(a)+'''and productlink.product_id='''+str(a)
    cursor_obj.execute(sql)
    profiles=cursor_obj.fetchall()
    return render_template("image.html",profiles=profiles)

@app.route('/login',methods=["POST"])
def login():
    a=request.form.get("username")
    s="'" + a + "'"
    b=request.form.get("password")
    d="'" + str(b) + "'"
    #print(s)
    #print(d)
    #sql = '''SELECT * FROM customer WHERE name = ''' + s + ''' and password = ''' + d
    sql = '''SELECT * FROM customer WHERE name = ''' + s 
    cursor_obj.execute(sql)
    res = cursor_obj.fetchall()
    #print(res)
    #return render_template('ls.html')
    if(len(res)>0):
        if(res[0][3]!=str(b)):
            return render_template("lf2.html")
        global uid 
        uid =res[0][0]
        sql='''SELECT * FROM category'''
        cursor_obj.execute(sql)
        profiles = cursor_obj.fetchall()
        return render_template('home.html',profiles=profiles)
    else:
       return render_template('lf.html')
   
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html') 

# @app.route('/profile')
# def profile():
#     return render_template('profile.html')        

@app.route('/create_account',methods=["POST"])
def create_account():
    a=request.form.get("username")
    a="'"+a+"'"
    b=request.form.get("password")
    b="'"+b+"'"
    c=request.form.get("phone_no")
    c="'"+c+"'"
    d=request.form.get("email_id")
    d="'"+d+"'"
    e=request.form.get("address")
    e="'"+e+"'"
    
    sql='''SELECT user_id from customer order by user_id desc'''
    cursor_obj.execute(sql)
    result=cursor_obj.fetchall()
    id=result[0][0]+1

    sql='''INSERT INTO customer (user_id,type,name,password,phone_no,email_id,address) VALUES ('''+str(id)+''','customer','''+a+''','''+b+''','''+c+''','''+d+''','''+e+''')'''
    cursor_obj.execute(sql)
    
    return render_template('login.html')

@app.route('/cart')
def cart():
    s="'"+str(uid)+"'"
    sql='''SELECT carthaspdt.product_id from carthaspdt where carthaspdt.user_id='''+s
    cursor_obj.execute(sql)
    profiles=cursor_obj.fetchall()
    print(uid)
    print(profiles)
    return render_template('cart.html',profiles=profiles)

@app.route('/wl')
def wl():
    s="'"+str(uid)+"'"
    sql='''SELECT wlhaspdt.product_id,image from wlhaspdt,productlink where wlhaspdt.user_id='''+s+''' and wlhaspdt.product_id=productlink.product_id'''
    cursor_obj.execute(sql)
    profiles=cursor_obj.fetchall()
    print(uid)
    print(profiles)
    return render_template('wl.html',profiles=profiles)

@app.route('/add_to_cart/<int:a>')
def add_to_cart(a):
    sql = '''INSERT into carthaspdt (user_id,product_id,pdt_quantity) VALUES ('''+str(uid)+''','''+ str(a)+''','''+str(1)+''')'''
    cursor_obj.execute(sql)
    sql = '''select quantity from product where product_id='''+str(a)
    cursor_obj.execute(sql)
    q=cursor_obj.fetchall()
    s=q[0][0]
    s=s-1
    sql='''update product set quantity='''+str(s)+'''where product_id='''+str(a)
    cursor_obj.execute(sql)
    return redirect('/cart')

@app.route('/add_to_wl/<int:a>')
def add_to_wl(a):
    sql = '''INSERT into wlhaspdt (user_id,product_id) VALUES ('''+str(uid)+''','''+ str(a)+''')'''
    cursor_obj.execute(sql)
    return redirect('/wl')

@app.route('/rmv_from_cart/<int:a>')
def rmv_from_cart(a):
    s1=str(a)
    s2=str(uid)
    sql = '''DELETE FROM carthaspdt WHERE carthaspdt.user_id =  ''' + s2 + '''and carthaspdt.product_id=''' + s1
    cursor_obj.execute(sql)
    return redirect('/cart')

@app.route('/rmv_from_wl/<int:a>')
def rmv_from_wl(a):
    s1=str(a)
    s2=str(uid)
    sql = '''DELETE FROM wlhaspdt WHERE wlhaspdt.user_id =  ''' + s2 + '''and wlhaspdt.product_id=''' + s1
    cursor_obj.execute(sql)
    return redirect('/wl')

if __name__ == '__main__':
	app.run()