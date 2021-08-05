from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init db and libraries
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_data.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)



# db syntax
class customerData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(20))
    l_name = db.Column(db.String(20))

    def __repr__(self):
        return f"Customer name: {self.f_name}, {self.l_name}"


# schema's for data and inits
class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "f_name", "l_name")
        model = customerData


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


class CustomerListResource(Resource):
    # Get all customers
    def get(self):
        customers = customerData.query.all()
        return customers_schema.dump(customers)

    # Create a customer
    def post(self):
        new_customer = customerData(
            f_name=request.json["f_name"],
            l_name=request.json["l_name"]
        )
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer)


class CustomerResource(Resource):
    # Get individual customer by ID
    def get(self, id):
        customer = customerData.query.get_or_404(id)
        return customer_schema.dump(customer)

    # Update individual Customer
    def patch(self, id):
        customer = customerData.query.get_or_404(id)

        if "f_name" in request.json:
            customerData.f_name = request.json["f_name"]
        if "l_name" in request.json:
            customerData.l_name = request.json["l_name"]

        db.session.commit()
        return customer_schema.dump(customer)

    # Delete individual customer
    def delete(self, id):
        customer = customerData.query.get_or_404(id)
        db.session.delete(customer)
        db.session.commit()
        return " ", 204


# init classes
api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)














