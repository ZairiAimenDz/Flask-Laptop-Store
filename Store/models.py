from datetime import datetime
from Store import db , login_manager ,app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Item', backref='author', lazy=True)

    def get_reset_token(self,expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Item(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    manufact = db.Column(db.String(20))
    product_name = db.Column(db.String(60))
    product_price = db.Column(db.Integer)
    prd_des = db.Column(db.Text)
    img1 = db.Column(db.String(30),default='pst_def.png')
    img2 = db.Column(db.String(30))
    img3 = db.Column(db.String(30))
    img4 = db.Column(db.String(30))
    img5 = db.Column(db.String(30))
    img6 = db.Column(db.String(30))
    # CPI
    cpu_name = db.Column(db.String(30),nullable=False)
    cpu_gen = db.Column(db.String(30))
    cpu_cores = db.Column(db.Integer,nullable=False)
    cpu_threads = db.Column(db.Integer,nullable=False)
    cpu_hypthr = db.Column(db.Boolean)
    cpu_sc_score = db.Column(db.Integer,nullable=False,default=0)
    cpu_mc_score = db.Column(db.Integer,nullable=False,default=0)
    #Screen
    screen_size = db.Column(db.String(30),nullable=False)
    screen_res = db.Column(db.String(30),nullable=False)
    screen_type = db.Column(db.String(30))
    #RAM
    ram_amm = db.Column(db.Integer,nullable=False)
    ram_slots_filled = db.Column(db.String(30))
    ram_config = db.Column(db.String(30))
    ram_type = db.Column(db.String(30),nullable=False)
    ram_speed = db.Column(db.Integer)
    #Storage :
    strg_amm = db.Column(db.Integer,nullable=False)
    strg_type = db.Column(db.String(30))
    strg_interface = db.Column(db.String(30))
    strg_sec = db.Column(db.Boolean)
    strg_sec_amm = db.Column(db.Integer)
    strg_sec_type = db.Column(db.String(30))
    strg_sec_inter = db.Column(db.String(30))
    # Graphic Card 
    gpu_name = db.Column(db.String(30),nullable=False)
    gpu_vram = db.Column(db.Integer,nullable=False)
    dgpu = db.Column(db.Boolean)
    dgpu_name = db.Column(db.String(30))
    dgpu_vram = db.Column(db.Integer)
    dgpu_vram_type = db.Column(db.String(30))
    #Ports:
    available_ports = db.Column(db.Text)
    #Upgradability
    up_cpu = db.Column(db.Boolean)
    up_gpu = db.Column(db.Boolean)
    up_RAM = db.Column(db.Boolean)
    up_Storage = db.Column(db.Boolean)
    rep_battery = db.Column(db.Boolean)
    #Keyboard
    keyb_layout = db.Column(db.String(30))
    keyb_backlit = db.Column(db.Boolean)
    keyb_num = db.Column(db.Boolean)
    #LTE
    lte_modem = db.Column(db.Boolean)
    #Battery
    battery_size = db.Column(db.String(30))
    battery_life = db.Column(db.String(30))
    #Product State
    product_state = db.Column(db.String(30))
    #Accessories
    charger = db.Column(db.Boolean)
    extra_acc = db.Column(db.Text)
    #Extra
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post('{self.manufact}', '{self.product_name}')"