import os
from flask import Flask
from flask import (
 render_template
)
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from os.path import join, dirname, realpath
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url
from flask_talisman import Talisman
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import DisconnectionError
# from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables from .env file
load_dotenv()

# create the extension
db = SQLAlchemy()

# Modify the drivername to match SQLAlchemy's PostgreSQL dialect
heroku_database_url = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://")

# Create a URL object from the Heroku database URL
# parsed_url = make_url(heroku_database_url)

# Modify the drivername to match SQLAlchemy's PostgreSQL dialect
# parsed_url_str = str(parsed_url).replace("postgres://", "postgresql://")

# upload path
UPLOADS_PATH = join(dirname(realpath(__file__)), u'static\\uploads')






def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),    
    )

    # upload folder
    app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
    # app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db' #os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SQLALCHEMY_DATABASE_URI"] = heroku_database_url
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299 # Recycle connections every 30 seconds
    app.config['SQLALCHEMY_POOL_SIZE'] = 100  # Maximum number of connections to keep in the pool
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 299  # Timeout for acquiring a connection from the pool
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True  # Check the connection before using it
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    # app.config['SQLALCHEMY_ECHO'] = True
    # app.config["SQLALCHEMY_DATABASE_URI"] = heroku_database_url

    # init flask migrate
    migrate = Migrate(app, db)


    # initialize the app with the extension
    db.init_app(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # import db models
    from .database.models import User

    with app.app_context():
        db.create_all()

    #  register views
    from .views.front import frontend
    from .views.dashboard import dashboard


    app.register_blueprint(frontend)
    app.register_blueprint(dashboard)

    # setup login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'dashboard.sign_in'    
    login_manager.login_message_category ='info'

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            db.session.rollback()
            print(f'==========={e}===========')
    # error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template("error/pages-misc-error.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        # note that we set the 500 status explicitly
        return render_template("error/pages-misc-error.html"), 500

    @app.errorhandler(401)
    def unauthorized(e):
        # note that we set the 500 status explicitly
        return render_template("error/page-misc-unauthorized.html"), 500
    
    # force SSL
    # Talisman(app, force_https=True, content_security_policy=None)

        #  Initializing scheduler for intrest
    # from .views.view_utils.auto_increase import increase_account_balance_by_interest_rate

    # def test_job():
        
    #     with app.app_context():
    #         from .database.models import TetherAccount,BitcoinAccount,EthereumAccount
    #         increase_account_balance_by_interest_rate(TetherAccount)  # Increase Tether account balances 
    #         increase_account_balance_by_interest_rate(BitcoinAccount)  # Increase Bitcoin account balances
    #         increase_account_balance_by_interest_rate(EthereumAccount)  # Increase Ethereum account balances

    # scheduler = BackgroundScheduler()
    # job       = scheduler.add_job(test_job, 'interval', days=1)
    # scheduler.start()


    return app

app = create_app()
