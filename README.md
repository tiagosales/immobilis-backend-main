# immobilis-backend-main
Projeto integrado da pós graduação de Desenv. Web Full Stack da PUC Minas<br>
- Para iniciar a aplicação<br>
  1. Crie o arquivo .env com as variáveis abaixo, o endereço da variável URL_FRONTEND deve apontar para o endereço da API iniciada no repositorio immobilis-frontend-main.<br>
     echo "SECRET_KEY=minhasecretkey<br>
     DATABASE_URL=postgresql://usuario:senha@hostBD/banco<br>
     GOOGLE_CLIENT_ID=OauthClientID<br>
     GOOGLE_CLIENT_SECRET=OauthClientSecret<br>
     URL_FRONTEND=https://meu.endereco.de.frontend:porta" > .env<br>
  3. Crie um virtualenv com o comando:<br>
     $ python3 -m venv "nomeDoVenv"<br>
  4. Execute o comando de activate respectivo do sistema operacional.<br>
     Ex: Linux:<br>
       $ . ./venv/bin/activate<br>
  6. Instale os pacotes requeridos:<br>
     (venv)$ pip install -r requirements.txt<br>
  7. Caso seja a primeira execução, precisa ser aplicado o modelo no banco de dados postgresql:<br>
     (venv)$ flask db init<br>
     (venv)$ flask db migrate<br>
     (venv)$ flask db upgrade<br>
  7. Iniciar o Flask:<br>
     (venv)$ flask run<br>
