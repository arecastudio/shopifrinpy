"""
Created by: arecastudio
Jakarta, September 30, 2020

This python script created to make easy printing
for delivery and order control purpose in warehouse

"""
from flask import Flask, render_template,request, redirect
import shopify
from config.key import DOMAIN, API_KEY, PASSWORD, API_VER
from escpos import printer
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

@app.route('/printwpX/<item_id>',methods=['GET','POST'])
def goPrint(item_id):
    if request.method=='GET':
        return redirect("/",code=302)
    return index()
    

@app.route('/printwp/<item_id>',methods=['GET','POST'])
def goPrintWP(item_id):
    if request.method=='GET':
        url = "https://%s:%s@%s/admin/api/%s" %(API_KEY,PASSWORD,DOMAIN,API_VER)
        shopify.ShopifyResource.set_site(url)
        ordx = shopify.Order.find(item_id)
        kitchen=printer.Network("192.168.51.144")
        #https://python-escpos.readthedocs.io/en/latest/api/escpos.html        
        #kitchen.set(align="left")        
        #kitchen.text("TEST AUTOMATIC PRINTING \n")
        kitchen.text("FISHOP "+ordx.name)
        kitchen.text("\nStatus: "+ordx.financial_status)
        kitchen.text("\nDate  : "+ordx.created_at)
        kitchen.text("\n: "+ordx.shipping_lines[0].title)
        kitchen.text("\n\n"+ordx.shipping_address.name)
        kitchen.text("-"+str(ordx.shipping_address.phone))
        kitchen.text("\n"+str(ordx.shipping_address.province))
        _addr1=str(ordx.shipping_address.address1)
        _addr2=str(ordx.shipping_address.address2)
        if _addr1=='None':
            _addr1="-"
        if _addr2=='None':
            _addr2="-"
        #192.168.52.137
        kitchen.text("\nAddr: "+_addr1)
        kitchen.text("\n    : "+_addr2)
        kitchen.text("\n")
        kitchen.text("-"*32)
        kitchen.text("\nQty  Price   Name")
        for lin in ordx.line_items:
            kitchen.text("\n  "+str(lin.quantity))
            _price=int(float(lin.price))
            kitchen.text("  "+format(_price,",d"))
            kitchen.text("  "+lin.title)
        #print("\n")
        kitchen.text("\n")
        kitchen.text("-"*32)
        _total=int(float(ordx.total_price))
        kitchen.text("\nTOTAL: "+format(_total,",d"))
        kitchen.text("\n")
        kitchen.text("\nNote:"+ordx.note)
        kitchen.text("\n\n\ndfsfsfdf")
        kitchen.cut()
        #print("PRINT ORDER:",item_id)
        return redirect("/",code=302)
    return index()

@app.errorhandler(404)
def not_found(e):
    return index()

if __name__=='__main__':
    app.run(debug=True)
