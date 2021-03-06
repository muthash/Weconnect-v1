from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_jwt_extended import get_raw_jwt, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from app.models import User
from app.baseview import BaseView

auth = Blueprint('auth', __name__, url_prefix='/api/v1')
users = []
blacklist = set()


class RegisterUser(BaseView):
    """Method to Register a new user"""
    def post(self):
        """Endpoint to save the data to the database"""
        if self.validate_json():
            return self.validate_json()

        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        user_data = {'email': email, 'username': username,
                     'password': password}

        if self.validate_null(**user_data):
            return self.validate_null(**user_data)

        if self.check_email(email):
            return self.check_email(email)

        if self.check_password(password):
            return self.check_password(password)

        email = self.normalize_email(email)
        norm_name = self.remove_extra_spaces(name=username)
        username = norm_name['name']

        emails = [user.email for user in users]
        if email in emails:
            response = {'message': 'User already exists. Please login'}
            return jsonify(response), 409
        user = User(email, username, password)
        users.append(user)
        response = {'message': 'Account created successfully'}
        return jsonify(response), 201


class LoginUser(BaseView):
    """Method to Login a user"""
    def post(self):
        """Endpoint to save the data to the database"""
        if self.validate_json():
            return self.validate_json()

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_data = {'email': email, 'password': password}
        if self.validate_null(**user_data):
            return self.validate_null(**user_data)

        user_ = [user for user in users
                 if user.email == email and
                 Bcrypt().check_password_hash(user.password, password)]

        if not user_:
            response = {'message': 'Invalid email or password'}
            return jsonify(response), 401
        user = user_[0]
        return self.generate_token(user.email, user.username)


class LogoutUser(MethodView):
    """Method to logout a user"""
    @jwt_required
    def post(self):
        """Endpoint to logout a user"""
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        response = {'message': 'Successfully logged out'}
        return jsonify(response), 200


class ResetPassword(BaseView):
    """Method to reset a user password"""
    def post(self):
        """Endpoint to reset a user password"""
        if self.validate_json():
            return self.validate_json()

        data = request.get_json()
        email = data.get('email')
        user_data = {'email': email}

        if self.validate_null(**user_data):
            return self.validate_null(**user_data)

        email = self.normalize_email(email)
        for user in users:
            if user.email == email:
                password = self.random_string()
                user.update_password(password)
                self.send_reset_password(email, password)
                response = {'message': 'Password reset successfull.' +
                                       ' Check your email for your' +
                                       ' new password'}
                return jsonify(response), 201
        response = {'message': 'Email address not registered'}
        return jsonify(response), 401


class ChangePassword(BaseView):
    """Method to change a user password"""
    @jwt_required
    def put(self):
        """Endpoint to change a user password"""
        if self.validate_json():
            return self.validate_json()

        data = request.get_json()
        old_pass = data.get('old_password')
        new_pass = data.get('new_password')
        current_user = get_jwt_identity()
        jti = get_raw_jwt()['jti']
        user_data = {'old_password': old_pass, 'new_password': new_pass}

        if self.validate_null(**user_data):
            return self.validate_null(**user_data)

        user_ = [user for user in users if user.email == current_user]
        if not user_:
            response = {'message': 'The user is not registered'}
            return jsonify(response), 401
        user = user_[0]
        if not Bcrypt().check_password_hash(user.password, old_pass):
            response = {'message': 'The initial password is not correct'}
            return jsonify(response), 401
        for usr in users:
            if current_user == usr.email:
                usr.update_password(new_pass)
                blacklist.add(jti)
                response = {'message': 'Password change successfull' +
                                       ' Login to continue'}
        return jsonify(response), 201


auth.add_url_rule('/register', view_func=RegisterUser.as_view('register'))
auth.add_url_rule('/login', view_func=LoginUser.as_view('login'))
auth.add_url_rule('/logout', view_func=LogoutUser.as_view('logout'))
auth.add_url_rule('/reset-password',
                  view_func=ResetPassword.as_view('reset-password'))
auth.add_url_rule('/change-password',
                  view_func=ChangePassword.as_view('Change-password'))
