from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    pass

@auth_bp.route('/logout')
def logout():
    pass

@auth_bp.route('/login/google')
def google_login():
    pass

@auth_bp.route('/login/google/callback')
def google_callback():
    pass