# dialect+driver://username:password@host:port/database
from flask import Flask,jsonify,request
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import json

db_string = "postgres://postgres:postgres@localhost:5432/Northwind"

db = create_engine(db_string)  
base = declarative_base()
app = Flask(__name__)
Session = sessionmaker(db)  
session = Session()
base.metadata.create_all(db)


class Customers(base):  
    __tablename__ = 'customers'


    customerid=Column(String, primary_key=True)
    companyname=Column(String)
    contactname=Column(String)
    contacttitle=Column(String)
    address=Column(String)
    city=Column(String)
    region=Column(String)
    postalcode=Column(String)
    country=Column(String)
    phone=Column(String)
    fax=Column(String)

    def serialize(self):
        return {"customerid": self.customerid,
                "companyname": self.companyname}
     
    @app.route('/displayCustomers/<string:id>', methods=['GET'])
    def display_customers(id):
        result = session.query(Customers).filter_by(customerid = id).first()
        response = jsonify({'customer details':result.serialize()})
        response.status_code=200
        return response
        

    @app.route('/insertCustomers', methods=['POST'])
    def insert_customers():
        json = request.get_json(force=True)

        new_customer = Customers(customerid=json['customerid'], companyname=json['companyname'], contactname=json['contactname'],
        contacttitle=json['contacttitle'],address=json['address'],city=json['city'],region=json['region'],postalcode=json['postalcode'],
        country=json['country'],phone=json['phone'],fax=json['fax'])  
        session.add(new_customer)  
        session.commit()

        response = jsonify('customer added successfully')
        response.status_code=200
        return response

    

    @app.route('/updateCustomers', methods=['PUT'])
    def update_customers():
        json = request.get_json(force=True)
        c_id = json['customerid']
        c_name= json['contactname']

        customer_to_be_updated = session.query(Customers).filter_by(customerid = c_id).first()

        customer_to_be_updated.contactname=c_name
        c_id=customer_to_be_updated.customerid
        session.commit()

        response = jsonify('customer updated successfully')
        response.status_code=200
        return response


if __name__ == '__main__':
    app.run(debug=True)



# http://127.0.0.1:5000/displayCustomers/PURMO
# {
#     "customer details": {
#         "companyname": "datagrokr",
#         "customerid": "PURMO"
#     }
# }

# Added body using postman
# http://127.0.0.1:5000/insertCustomers
# customer added successfully (response code =200)


# http://127.0.0.1:5000/insertCustomers
# customer updated successfully (response code =200)
