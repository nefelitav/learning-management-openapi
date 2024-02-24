import os
import tempfile
from functools import reduce

# from tinydb import TinyDB, Query

# db_dir_path = tempfile.gettempdir()
# db_file_path = os.path.join(db_dir_path, "students.json")
# student_db = TinyDB(db_file_path)

# def add(student=None):
#     queries = []
#     query = Query()
#     queries.append(query.first_name == student.first_name)
#     queries.append(query.last_name == student.last_name)
#     query = reduce(lambda a, b: a & b, queries)
#     res = student_db.search(query)
#     if res:
#         return 'already exists', 409

#     doc_id = student_db.insert(student.to_dict())
#     student.student_id = doc_id
#     return student.student_id


# def get_by_id(student_id=None, subject=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student['student_id'] = student_id
#     print(student)
#     return student


# def delete(student_id=None):
#     student = student_db.get(doc_id=int(student_id))
#     if not student:
#         return 'not found', 404
#     student_db.remove(doc_ids=[int(student_id)])
#     return student_id

from bson import json_util
import json
from pymongo import MongoClient, ASCENDING

client = MongoClient('mongodb://mongo:27017')
db = client['students']  
collection = db['students']  

def get_student_count():
    return collection.count_documents({})

def add(student=None):
    existing_student = collection.find_one({'first_name': student.first_name, 'last_name': student.last_name})
    if existing_student:
        return 'already exists', 409

    result = collection.insert_one(student.to_dict())
    student_count = get_student_count()
    return student_count

def get_by_id(student_id=None):
    student = collection.find_one({}, {'_id': 0}, sort=[("timestamp", ASCENDING)], skip=int(student_id)-1)
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    return json.loads(json_util.dumps(student))
    

def delete(student_id=None):
    student = collection.find_one({}, sort=[("timestamp", ASCENDING)], skip=int(student_id)-1)
    if student:
        result = collection.delete_one({'_id': student['_id']})
        if result.deleted_count != 0:
            return student_id
    return 'not found', 404