from flask import request, Blueprint
from flask_restful import Resource, reqparse, Api
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.models import User, Note, user_schema, users_schema, note_schema, notes_schema

from app import db

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument("page", type=int, default=1, location="args")
pagination_parser.add_argument("per_page", type=int, default=10, location="args")


class UserResourse(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users), 200
class SignupResource(Resource):
    def post(self):
        request_json = request.get_json()

        username = request_json.get('username')
        password = request_json.get('password')

        user = User (
            username=username
        )

        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()
            access_token = create_access_token(identity=str(user.id))
            return {"token" :access_token, "user":user_schema.dump(user)}, 201
        except IntegrityError:
            return {"error" : ["422 Unprocessable entity"]}, 422

class LoginResource(Resource):
    def post(self):
        request_json = request.get_json()

        username = request_json.get("username")
        password = request_json.get("password")

        user = User.query.filter_by(username = username).first()

        if user and user.authenticate(password):
            access_token = create_access_token(identity=str(user.id))
            return {"message" : "Login Successful", "access_token" : access_token, "user" : user_schema.dump(user)}, 200

        return {"error" : "Invalid username or password"}, 401



class NotelistResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()

        args = pagination_parser.parse_args()
        page = args["page"]
        per_page = args["per_page"]

        user_notes = db.Select(Note).where(Note.user_id == int(current_user_id))

        pagination_query = db.paginate(user_notes, page=page, per_page=per_page, error_out=False)

        return {
            "total": pagination_query.total,
            "page": pagination_query.page,
            "per_page": pagination_query.per_page,
            "pages": pagination_query.pages,
            "has_next": pagination_query.has_next,
            "has_prev": pagination_query.has_prev,
            "items" : notes_schema.dump(pagination_query.items)
        }, 200
    
    @jwt_required()
    def post(self):
        request_json = request.get_json()
        current_user_id = get_jwt_identity()

        request_json["user_id"] = int(current_user_id)
        
        errors = note_schema.validate(request_json)
        if errors:
            return {"errors" : errors}, 400
        
        note = note_schema.load(request_json)
        db.session.add(note)
        db.session.commit()

        return note_schema.dump(note)

class NoteResource(Resource): 
    @jwt_required()
    def delete(self, id):
        note = Note.query.get(id)

        if not note:
            return {"error" : "Note not found"}, 404
        
        if str(note.user_id) != get_jwt_identity():
            return {"error": "Unauthorized to delete this note"}, 403
        
        db.session.delete(note)
        db.session.commit()

        return {"success" : "Note deleted successfully"}, 200

api.add_resource(UserResourse, '/users', endpoint="users")
api.add_resource(SignupResource, '/signup', endpoint="signup")
api.add_resource(LoginResource, '/login', endpoint="login")
api.add_resource(NotelistResource, '/notes', endpoint='notes')
api.add_resource(NoteResource, '/notes/<int:id>', endpoint="note")