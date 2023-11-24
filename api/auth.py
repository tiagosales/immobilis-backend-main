# auth.py
from urllib.parse import urlencode
from flask_restx import Namespace, Resource, fields
from flask import abort, redirect, request, session, url_for, flash
from models.usuario import Usuario,Favorito
from config import app
auth_ns = Namespace('auth', description='Operações de autenticação')
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
import secrets
import requests
from config import db,bcrypt
from datetime import datetime
from flask_jwt_extended import (
    create_access_token
)
import os


login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='Nome de usuário'),
    'senha': fields.String(required=True, description='Senha'),
})



@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.doc('login')
    @auth_ns.expect(login_model)
    def post(self):
        '''Efetuar login'''
        login_data = request.json
        email = login_data.get('email')
        senha = login_data.get('senha')

        usuario = db.session.scalar(db.select(Usuario).where(Usuario.email == email))
        print(usuario.email)
        if not usuario is None:
            is_valid = bcrypt.check_password_hash(usuario.senha, senha)
            novo_usuario = False
        else:
            usuario = Usuario(email=email, nome=email.split('@')[0], senha=bcrypt.generate_password_hash(senha).decode('utf-8'),id_perfil=1,data_cadastro=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
            db.session.add(usuario)
            db.session.commit()
            is_valid = True
            novo_usuario = True
        if is_valid:
                identity=str(usuario.id)+';'+str(usuario.id_perfil)
                access_token = create_access_token(identity=identity)
                if novo_usuario:
                    return {"user_id": usuario.id, "perfil_id": usuario.id_perfil, "access_token": access_token , "message": "Registro bem-sucedido"}, 201
                else:
                    return {"user_id": usuario.id, "perfil_id": usuario.id_perfil, "access_token": access_token , "message": "Login bem-sucedido"}, 200
                    
        return {"message": "Login falhou, por favor verifique suas credenciais"}, 401


login = LoginManager(app)

@login.user_loader
def load_user(id):
    return db.session.get(Usuario, int(id))

url_busca = os.getenv('URL_FRONTEND')+'/busca'
url_login = os.getenv('URL_FRONTEND')+'/loginpost'
url_login_sistema = os.getenv('URL_FRONTEND')+'/login'

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_login_sistema)

@login.user_loader
def load_user(id):
    return db.session.get(Usuario, int(id))

@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        logout_user()
        return redirect(url_for('logout'))

    provider_data = app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session['oauth2_state'] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True,_scheme='https'),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data['authorize_url'] + '?' + qs)


@app.route('/callback/<provider>')
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_login+'?access_token='+oauth2_idtoken+'&user_id='+str(usuario.id))

    provider_data = app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_busca)

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    # make sure that the authorization code is present
    if 'code' not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider,
                                _external=True),
    }, headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    oauth2_idtoken = response.json().get('id_token')

    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())
    # find or create the user in the database

    usuario = db.session.scalar(db.select(Usuario).where(Usuario.email == email))
    if usuario is None:
        usuario = Usuario(email=email, nome=email.split('@')[0], senha=secrets.token_urlsafe(16),id_perfil=1,data_cadastro=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        db.session.add(usuario)
        db.session.commit()

     # log the user in
    login_user(usuario)
    identity=str(usuario.id)+';'+str(usuario.id_perfil)
    access_token = create_access_token(identity=identity)
    return redirect(url_login+'?access_token='+access_token+'&id_token='+oauth2_idtoken+'&user_id='+str(usuario.id)+'&perfil_id='+str(usuario.id_perfil))