import pymongo
from bson.json_util import dumps
from flask import Flask, Response, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
mongo = PyMongo(app)

def get_student(student_id):
    student = mongo.db.student.find_one({'_id':student_id})
    if student is None:
        return Response(dumps({'error': 'Student not found'}), status=404)
    return Response(dumps(student),status=200)

def student_create():
    data = request.get_json()
    if not data:
        return Response(dumps({'error': 'No data provided'}), status=400)
    id = data.get('id')
    name = data.get('name')
    rollno = data.get('rollno')
    dob = data.get('dob')
    if not all([id, rollno, name, dob]):
        return Response(dumps({'error': 'Incomplete student data'}), status=400)

    data['_id'] = data.pop('id')
    try:
        mongo.db.student.insert_one(data)
        return Response(dumps({'Message': 'Student created'}), status=400)
    except pymongo.errors.DuplicateKeyError:
        return Response(dumps({'error': 'Duplicate id/rollno'}), status=400)

def student_update(student_id):
    data = request.get_json()
    if not data:
        return Response(dumps({'error': 'No data provided'}), status=400)
    try:
        mongo.db.student.update_one({'_id': student_id}, {'$set': data})
        return Response(dumps({'Message': 'Student updated'}), status=400)
    except pymongo.errors.DuplicateKeyError:
        return Response(dumps({'error': 'Duplicate id/rollno'}), status=400)

def student_delete(student_id):
    result = mongo.db.student.delete_one({'_id': student_id})
    if result.deleted_count == 0:
        return Response(dumps({'error': 'Student not found'}), status=400)
    return Response(dumps({'message': 'Student deleted'}), status=200)

app.add_url_rule('/student/<string:student_id>', view_func=get_student, methods=['GET'])
app.add_url_rule('/student', view_func=student_create, methods=['POST'])
app.add_url_rule('/student/<string:student_id>', view_func=student_update, methods=['PUT'])
app.add_url_rule('/student/<string:student_id>', view_func=student_delete, methods=['DELETE'])

if __name__ == "__main__":
    app.run()
