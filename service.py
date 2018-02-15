import pymongo
from flask import Flask , request
from flask_restful import Resource , Api,reqparse
from datetime import datetime
import json

url = "mongodb://mumu:handsome1234@localhost:27017/admin"
client = pymongo.MongoClient(url)
app = Flask (__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('information')


db = client.admin.cpe_company_limited

class Registration(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		db.update_one({"id":data['id']},{'$set':{"id":data['id'],"firstname":data['firstname'],"lastname":data['lastname'],"password":data['password']}},upsert=True)
		return {'firstname': data['firstname']}

class Login(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		result = db.find_one({"id":data['id'],"password":data['password']})
		print result
		print datetime.now()
		if result is None:
			return {'Error': 'id or password incorrect'}
		db.update({ "id":data['id']},{'$push': {'list_work': {'datetime':datetime.now().strftime("%d-%m-%Y %H:%M:%S")}}})
		return {'firstname': result['firstname'],'Status':'Login Successful!'}

class CheckListWork(Resource):
	def post(self):
		args = parser.parse_args()
		data = json.loads(args['information'])
		result = db.find_one({"id":data['id']})
		if result is None:
			return {'Error': 'id incorrect'}
		return {'list_work':result['list_work'],'firstname': result['firstname']}

api.add_resource(Registration,'/api/regis')
api.add_resource(Login,'/api/login')
api.add_resource(CheckListWork,'/api/employee_list_work')

if __name__ == '__main__':
	app.run(host='0.0.0.0' , port = 5559)

