# Server Side
from flask import Flask
from flask_restful import Api,Resource,abort,reqparse,marshal_with,fields
from flask_sqlalchemy import SQLAlchemy,Model
from flask_cors import CORS
app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Database config
db=SQLAlchemy(app)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
api=Api(app)

class HumanActionModel(db.Model):
    __tablename__ = 'HumanAction'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    classId=db.Column(db.String(100),nullable=False)
    dateTime=db.Column(db.String(100),nullable=False)
    face=db.Column(db.String(100),nullable=False)
    face_acc=db.Column(db.String(100),nullable=False)
    action=db.Column(db.String(100),nullable=False)
    action_acc=db.Column(db.String(100),nullable=False)
    position=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"HumanAction(classId={classId},name={dateTime},face={face},face_acc={face_acc},action={action},action_acc={action_acc},position={position})"

class TeracherModel(db.Model):
    __tablename__ = 'Teracher'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100),nullable=False)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"Teracher(name={name},username={username},password={password})"

class ClassRoomModel(db.Model):
    __tablename__ = 'ClassRoom'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    className=db.Column(db.String(100),nullable=False)
    teacherId=db.Column(db.String(100),nullable=False)
    time=db.Column(db.String(100),nullable=False)
    roomName=db.Column(db.String(100),nullable=False)
    numPerson=db.Column(db.String(100),nullable=False)
    classLevel=db.Column(db.String(100),nullable=False)
    school=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"ClassRoom(className={className},teacherId={teacherId},time={time},numPerson={numPerson},classLevel={classLevel},school={school})"

db.create_all()

# HumanAction Request Parser
add_args=reqparse.RequestParser()
add_args.add_argument("classId",type=str,required=True,help="")
add_args.add_argument("dateTime",type=str,required=True,help="")
add_args.add_argument("face",type=str,required=True,help="")
add_args.add_argument("face_acc",type=str,required=True,help="")
add_args.add_argument("action",type=str,required=True,help="")
add_args.add_argument("action_acc",type=str,required=True,help="")
add_args.add_argument("position",type=str,required=True,help="")

resource_field={
    "id":fields.Integer,
    "classId":fields.String,
    "dateTime":fields.String,
    "face":fields.String,
    "face_acc":fields.String,
    "action":fields.String,
    "action_acc":fields.String,
    "position":fields.String
}

# Teracher Request Parser
add_argsTeracher=reqparse.RequestParser()
add_argsTeracher.add_argument("name",type=str,required=True,help="")
add_argsTeracher.add_argument("username",type=str,required=True,help="")
add_argsTeracher.add_argument("password",type=str,required=True,help="")

resource_field_Teracher={
    "id":fields.Integer,
    "name":fields.String,
    "username":fields.String,
    "password":fields.String
}

# ClassRoom Request Parser
add_argsClassRoom=reqparse.RequestParser()
add_argsClassRoom.add_argument("className",type=str,required=True,help="")
add_argsClassRoom.add_argument("teacherId",type=str,required=True,help="")
add_argsClassRoom.add_argument("time",type=str,required=True,help="")
add_argsClassRoom.add_argument("roomName",type=str,required=True,help="")
add_argsClassRoom.add_argument("numPerson",type=str,required=True,help="")
add_argsClassRoom.add_argument("classLevel",type=str,required=True,help="")
add_argsClassRoom.add_argument("school",type=str,required=True,help="")

resource_field_classRoom={
    "id":fields.Integer,
    "className":fields.String,
    "teacherId":fields.String,
    "time":fields.String,
    "roomName":fields.String,
    "numPerson":fields.String,
    "classLevel":fields.String,
    "school":fields.String
}


# Design API
class HumanAction(Resource):
    @marshal_with(resource_field)
    def get(self):
        result=HumanActionModel.query.all()
        if not result:
            abort(404,message="ไม่มีข้อมูล")
        return result

    @marshal_with(resource_field)
    def post(self):
        args=add_args.parse_args()
        obj=HumanActionModel(
            classId=args["classId"],
            dateTime=args["dateTime"],
            face=args["face"],
            face_acc=args["face_acc"],
            action=args["action"],
            action_acc=args["action_acc"],
            position=args["position"]
            )
        db.session.add(obj)
        db.session.commit()
        return obj,201

class HumanActionID(Resource):
    @marshal_with(resource_field)
    def get(self,id):
        result=HumanActionModel.query.filter_by(id=id).first()
        if not result:
            abort(404,message="ไม่พบข้อมูล")
        return result

class HumanActionLastID(Resource):
    @marshal_with(resource_field)
    def get(self):
        # result=HumanActionModel.query.all()
        result=db.session.query(HumanActionModel).order_by(HumanActionModel.id.desc()).first()
        if not result:
            abort(404,message="ไม่พบข้อมูล")
        return result

# Design API
class Teracher(Resource):
    @marshal_with(resource_field_Teracher)
    def get(self):
        result=TeracherModel.query.all()
        if not result:
            abort(404,message="ไม่มีข้อมูล")
        return result

    @marshal_with(resource_field_Teracher)
    def post(self):
        args=add_argsTeracher.parse_args()
        obj=TeracherModel(
            name=args["name"],
            username=args["username"],
            password=args["password"],
            )
        db.session.add(obj)
        db.session.commit()
        return obj,201

# Design API
class ClassRoom(Resource):
    @marshal_with(resource_field_classRoom)
    def get(self):
        result=ClassRoomModel.query.all()
        if not result:
            abort(404,message="ไม่มีข้อมูล")
        return result

    @marshal_with(resource_field_classRoom)
    def post(self):
        args=add_argsClassRoom.parse_args()
        obj=ClassRoomModel(
            className=args["className"],
            teacherId=args["teacherId"],
            time=args["time"],
            roomName=args["roomName"],
            numPerson=args["numPerson"],
            classLevel=args["classLevel"],
            school=args["school"],
            )
        db.session.add(obj)
        db.session.commit()
        return obj,201

#call
api.add_resource(HumanAction,"/human-action/")
api.add_resource(HumanActionID,"/human-action/<int:id>/")
api.add_resource(HumanActionLastID,"/human-action/lastID/")
api.add_resource(Teracher,"/teracher/")
api.add_resource(ClassRoom,"/classRoom/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

## TEST POSTMAN - get Data All
# http://localhost:5000/human-action/
## TEST POSTMAN - search Data
# http://localhost:5000/human-action/1

# output [Body][JSON]

## TEST POSTMAN - add Data
# [POST] http://localhost:5000/human-action/1
# [Body][raw][JSON]
# {
#     "dateTime":"28/01/21 02:46:42",
#     "face":"Natthawat",
#     "face_acc":"96.32%",
#     "action":"sleeping",
#     "action_acc":"84.65%",
#     "position":"345,567,45,789"
# }

## TEST POSTMAN - add Update
# [PATCH] http://localhost:5000/human-action/1
# [Body][raw][JSON]
# {
#     "face":"Narin",
#     "face_acc":"53.32%",
# }

## TEST POSTMAN - add Delete
# [DELETE] http://localhost:5000/human-action/1
# [Body][raw][JSON]
# {
# }
