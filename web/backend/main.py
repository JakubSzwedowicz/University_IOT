from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

app=Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

migrate = Migrate(app, db)
api = Api(app, doc='/docs')
JWTManager(app)

recipe_model = api.model(
    'Recipe',
    {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String(),
    }
)

signup_model = api.model(
    'SignUp',
    {
        'username': fields.String(),
        'email': fields.String(),
        'password': fields.String(),
    }
)

login_model = api.model(
    'Login',
    {
        'username': fields.String(),
        'password': fields.String(),
    }
)

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        '''Call hello world'''
        return {'message': 'Hello, World!'}

@api.route('/signup')
class SignUp(Resource):
    
    @api.expect(signup_model)
    def post(self):
        data = request.get_json()
        
        username = data['username']
        db_user=User.query.filter_by(username=username).first()
        
        if db_user is not None:
            return jsonify({'message': f'User with username {username} already exists'})
        
        user = User(username=username, email=data['email'], password=generate_password_hash(data['password']))
        user.save()
        return jsonify({'message': 'User created successfully'})
        

@api.route('/login')
class Login(Resource):
    
    @api.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            refreash_token = create_refresh_token(identity=username)

            return jsonify({'access_token': access_token, 'refresh_token': refreash_token})
        return jsonify({'message': 'Invalid credentials'})


@api.route('/recipes')
class RecipesResource(Resource):
    
    @api.marshal_list_with(recipe_model)
    def get(self):
        '''Get all recipes'''
        recipes = Recipe.query.all() 
        return recipes
    
    @api.marshal_with(recipe_model)
    @api.expect(recipe_model)
    @jwt_required()
    def post(self):
        '''Create a recipe'''
        data = request.get_json()
        recipe = Recipe(title=data['title'], description=data['description'])
        recipe.save()
        return recipe, 201
    

@api.route('/recipe/<int:id>')
class RecipeResource(Resource):

    @api.marshal_with(recipe_model)
    def get(self, id):
        '''Get a recipe'''
        recipe = Recipe.query.get_or_404(id)
        return recipe
    
    @api.marshal_with(recipe_model)
    @jwt_required()
    def put(self, id):
        '''Put a recipe'''
        recipe = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe.update(data['title'], data['description'])
        return recipe, 200
    
    @api.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, id):
        '''Delete a recipe'''
        recipe = Recipe.query.get_or_404(id)
        recipe.delete()
        return recipe, 204


# backend$ flask shell 
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipe': Recipe}
    
if __name__ == '__main__':
    app.run()