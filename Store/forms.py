from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField , TextAreaField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo , ValidationError
from Store.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_pw = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register New Admin')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Admin Login')

# Item Form - Important
class PostForm(FlaskForm):
    # Main Components :
    manufact = StringField('Manufacturer',validators=[DataRequired()])
    product_name = StringField('Product Name',validators=[DataRequired()])
    product_price = IntegerField('Price - Number Only')
    prd_des = TextAreaField('Product Description')
    img1 = FileField('Main Photo',validators=[FileAllowed(['jpg','png'])])
    img2 = FileField('Photo 1',validators=[FileAllowed(['jpg','png'])])
    img3 = FileField('Photo 2',validators=[FileAllowed(['jpg','png'])])
    img4 = FileField('Photo 3',validators=[FileAllowed(['jpg','png'])])
    img5 = FileField('Photo 4',validators=[FileAllowed(['jpg','png'])])
    img6 = FileField('Photo 5',validators=[FileAllowed(['jpg','png'])])
    # CPI
    cpu_name = StringField('CPU Name',validators=[DataRequired()])
    cpu_gen = IntegerField('CPU Generation - Number Only')
    cpu_cores = IntegerField('CPU Core Count',validators=[DataRequired()])
    cpu_threads = IntegerField('CPU Threads',validators=[DataRequired()])
    cpu_hypthr = BooleanField('HyperThreading')
    cpu_sc_score = IntegerField('Cinebench R15 Single-Core Score')
    cpu_mc_score = IntegerField('Cinebench R15 MultiCore Score')
    #Screen
    screen_size = StringField('Screen Size',validators=[DataRequired()])
    screen_res = StringField('Screen Resolution (ex : "1920x1080 - FHD" )',validators=[DataRequired()])
    screen_type = StringField('Screen Type')
    #RAM
    ram_amm = IntegerField('RAM Ammount - Number Only ',validators=[DataRequired()])
    ram_slots_filled = StringField('RAM Slots Filled (ex : 1 of 2 slots)')
    ram_config = StringField('RAM Configuration ("Dual Channel / SIngle Channel")')
    ram_type = StringField('RAM Type (DDR??)',validators=[DataRequired()])
    ram_speed = IntegerField('RAM Speed - Number Only')
    #Storage :
    strg_amm = IntegerField('Storage Ammount',validators=[DataRequired()])
    strg_type = StringField('Storage Type (SSD / HDD)')
    strg_interface = StringField('Storage Interface (NVME / M.2 / SATA ... etc)')
    strg_sec = BooleanField('Secondary Storage')
    strg_sec_amm = IntegerField('Secondary Storage Ammount')
    strg_sec_type = StringField('Secondary Storage Type')
    strg_sec_inter = StringField('Secondary Storage Interface')
    # Graphic Card 
    gpu_name = StringField('Integrated Graphics Name',validators=[DataRequired()])
    gpu_vram = IntegerField('Integrated Graphics VRAM - Number Only ',validators=[DataRequired()])
    dgpu = BooleanField('Dedicated Graphics Card')
    dgpu_name = StringField('Dedicated GPU Name')
    dgpu_vram = IntegerField('Dedicated GPu VRAM - Number Only')
    dgpu_vram_type = StringField('VRAM Type (DDR3 GDDR .. etc)')
    #Ports:
    available_ports = TextAreaField('Available Ports')
    #Upgradability
    up_cpu = BooleanField('CPU Upgrade')
    up_gpu = BooleanField('GPU Upgrade')
    up_RAM = BooleanField('RAM Upgrade')
    up_Storage = BooleanField('Storage Upgrade')
    rep_battery = BooleanField('Battery Replacing')
    #Keyboard
    keyb_layout = StringField('Keyboard Layout')
    keyb_backlit = BooleanField('Backlighting')
    keyb_num = BooleanField('Number Row')
    #LTE
    lte_modem = BooleanField('LTE Model')
    #Battery
    battery_size = StringField('Battery Capacity')
    battery_life = StringField('Battery Life')
    #Product State
    product_state = StringField('Product State')
    #Accessories
    charger = BooleanField('With Charger')
    extra_acc = TextAreaField('Exrat Accessories')
    # Submit 
    submit = SubmitField('Submit')

class UpdateAccount(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pw = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')