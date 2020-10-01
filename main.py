"""
Created by: arecastudio
Jakarta, September 30, 2020

This python script created to make easy printing
for delivery and order control purpose in warehouse

"""
from flask import Flask, render_template,request
import shopify
from config.key import DOMAIN, API_KEY, PASSWORD, API_VER
#from escpos.printer import Usb
from escpos.connections import getNetworkPrinter
from escpos.printer import Network


import os
import tempfile



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
        #print("PRINT ORDER:",item_id)
        #p = Usb(0x04b8,0x0202,0)
        #p.text("Hello World\n")
        #p.image("logo.gif")
        #p.barcode('1324354657687','EAN13',64,2,'','')
        #p.cut()

        


        printer = getNetworkPrinter()(host='192.168.192.168',port=9100)

        printer.text("Hello World")
        printer.lf()
    return index()

@app.route('/printwp/<item_id>',methods=['GET','POST'])
def goPrintWP(item_id):
    if request.method=='GET':
        url = "https://%s:%s@%s/admin/api/%s" %(API_KEY,PASSWORD,DOMAIN,API_VER)
        shopify.ShopifyResource.set_site(url)
        #filename=tempfile.mktemp(".txt")
        #open(filename,"w").write("hello")
        #os.startfile(filename,"print")
        kitchen = Network("192.168.192.168") #Printer IP Address
        #kitchen.text("\nHello World "+item_id)
        #kitchen.barcode('1324354657687', 'EAN13', 64, 2, '', '')
        #https://python-escpos.readthedocs.io/en/latest/api/escpos.html
        kitchen.set(align="left")
        ordx = shopify.Order.find(item_id)
        kitchen.text("\n"+ordx.name)
        kitchen.text("\n"+ordx.created_at)
        kitchen.text("\n"+ordx.financial_status)
        kitchen.text("\n"+ordx.shipping_address.name)
        kitchen.text("\n"+str(ordx.shipping_address.phone))
        kitchen.text("\n"+str(ordx.shipping_address.address1))
        kitchen.text("\n"+str(ordx.shipping_address.address2))
        for lin in ordx.line_items:
            kitchen.text("\n"+str(lin.quantity))
            kitchen.text(" "+str(lin.price))
            kitchen.text(" "+lin.title)
        kitchen.text("\n"+str(ordx.total_price))
        kitchen.text("\n")
        kitchen.text("\nNote:"+ordx.note)
        kitchen.cut()
        print("PRINT ORDER:",item_id)
    return index()

@app.errorhandler(404)
def not_found(e):
    return index()

if __name__=='__main__':
    app.run(debug=True)
