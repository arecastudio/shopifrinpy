"""
Created by: arecastudio
Jakarta, September 30, 2020

This python script created to make easy printing
for delivery and order control purpose in warehouse

"""
from flask import Flask, render_template,request
import shopify
from config.key import DOMAIN, API_KEY, PASSWORD, API_VER
from escpos.printer import Usb

app=Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='GET':
        url = "https://%s:%s@%s/admin/api/%s" %(API_KEY,PASSWORD,DOMAIN,API_VER)
        shopify.ShopifyResource.set_site(url)
        anyOrders = shopify.Order.find(fulfillment_status="all")
        return render_template('index.html',data=anyOrders,pjg=len(anyOrders))

@app.route('/print/<int:item_id>',methods=['GET','POST'])
def goPrint(item_id):
    if request.method=='GET':
        print("PRINT ORDER:",item_id)
        p = Usb(0x04b8,0x0202,0)
        p.text("Hello World\n")
        #p.image("logo.gif")
        #p.barcode('1324354657687','EAN13',64,2,'','')
        p.cut()
    return index()

@app.route('/printwp/<int:item_id>',methods=['GET','POST'])
def goPrintWP(item_id):
    if request.method=='GET':
        print("PRINT ORDER:",item_id)
    return index()

@app.errorhandler(404)
def not_found(e):
    return index()

if __name__=='__main__':
    app.run(debug=True)
