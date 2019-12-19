from flask import render_template, url_for, flash, redirect ,request , abort ,session
from Store import app , db , bcrypt ,mail ,Session
from Store.forms import RegistrationForm, LoginForm , PostForm , UpdateAccount ,RequestResetForm ,ResetPasswordForm
from Store.models import User, Item
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os
from PIL import Image
from flask_mail import Message

Store_name = "PC-cam.dz"
# Home Route - Route For The Home Page
@app.route('/')
@app.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    items = Item.query.order_by(Item.date_posted.desc()).paginate(per_page=9,page=page)
    return render_template('index.html',Store_name=Store_name,title='Store',items=items)

@app.route('/add_cmp1/<int:post_id>')
def add_comp1(post_id):
    session["comp1"]=post_id
    flash('Added Element To The Comparaison As Element 1','success')
    return redirect(url_for('home'))

@app.route('/add_cmp2/<int:post_id>')
def add_comp2(post_id):
    session["comp2"]=post_id
    flash('Added Element To The Comparaison As Element 2','success')
    return redirect(url_for('home'))

@app.route('/comparator')
def compare():
    if not "comp1" in session:
        session["comp1"] = 0
    if not "comp2" in session:
        session["comp2"] = 0
    comp1 = session.get("comp1")
    if comp1 == 0 :
        flash('add elements to compare first !','warning')
        return redirect('home')
    comp2 = session.get("comp2")
    if comp2 == 0 :
        flash('add elements to compare first !','warning')
        return redirect('home')
    try:
        item1 = Item.query.get(comp1)
    except:
        session["comp1"]=0
        return redirect(url_for('home'))
    try:
        item2 = Item.query.get(comp2)
    except:
        session["comp2"]=0
        return redirect(url_for('home'))
    return render_template('compare.html',Store_name=Store_name,title="Comaprator",item1=item1,item2=item2)
# Login Route - Route For The Login Page
@app.route('/admin',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Change With Code For Real DataBase Entry :
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
            flash('Successfully LoggedIn , Welcome Back Admin ','success')
            return redirect(url_for('home'))
        else:
            flash('Sorry Not An Admin, Your Account Must Be Made By The Admin','danger')
    else:
        flash('Check The Informations Given Again !','warning')
    return render_template('login.html',Store_name=Store_name,title='Admin Login',form=form)


#Register Route - Route For Adding New Admins
@app.route('/register',methods=['GET','POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data , email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Added The New Admin Successfully,If You Want To Modify The Account Of This Admin You Have To Login As That Account','info')
        return redirect(url_for('login'))
    else :
        flash('Check The Informations Entered Again','warning')
    return render_template('register.html',Store_name=Store_name,title='Registering A New Admin',form=form)





def save_pic_item(form_picture):
    if form_picture:
        rndm_hex = secrets.token_hex(10) 
        _,f_ext = os.path.splitext(form_picture.filename)
        picture_fn = rndm_hex + f_ext
        picture_path = os.path.join(app.root_path , 'static/img',picture_fn)
        # Resizing :
        output_size = (960,640)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        #
        i.save(picture_path)
        return picture_fn
    else:
        return None


@app.route('/newpost',methods=['GET','POST'])
@login_required
def newpost():
    form = PostForm()
    if form.validate_on_submit():
        im1 = save_pic_item(form.img1.data)
        im2 = save_pic_item(form.img2.data)
        im3 = save_pic_item(form.img3.data)
        im4 = save_pic_item(form.img4.data)
        im5 = save_pic_item(form.img5.data)
        im6 = save_pic_item(form.img6.data)
        post = Item( product_name = form.product_name.data,manufact = form.manufact.data,product_price = form.product_price.data ,img1 = im1,
                    img2 = im2 , img3 = im3 , img4 = im4, prd_des=form.prd_des.data,
                    img5 =im5,img6 = im6 ,cpu_name = form.cpu_name.data,cpu_gen = form.cpu_gen.data,
                    cpu_cores = form.cpu_cores.data , cpu_threads = form.cpu_threads.data , cpu_hypthr = form.cpu_hypthr.data , cpu_sc_score = form.cpu_sc_score.data ,
                    cpu_mc_score = form.cpu_mc_score.data , screen_size = form.screen_size.data ,screen_res = form.screen_res.data ,screen_type  = form.screen_type.data,
                    ram_amm = form.ram_amm.data ,ram_slots_filled = form.ram_slots_filled.data,ram_config = form.ram_config.data ,
                    ram_type = form.ram_type.data ,ram_speed = form.ram_speed.data , strg_amm = form.strg_amm.data,strg_type = form.strg_type.data ,strg_interface = form.strg_interface.data,
                    strg_sec = form.strg_sec.data ,strg_sec_amm = form.strg_sec_amm.data,
                    strg_sec_inter = form.strg_sec_inter.data , strg_sec_type = form.strg_sec_type.data,
                    gpu_name = form.gpu_name.data , gpu_vram = form.gpu_vram.data,
                    dgpu = form.dgpu.data , dgpu_name = form.dgpu_name.data , dgpu_vram = form.dgpu_vram.data,
                    dgpu_vram_type = form.dgpu_vram_type.data , available_ports = form.available_ports.data,
                    up_cpu = form.up_cpu.data , up_gpu = form.up_gpu.data,
                    up_RAM = form.up_RAM.data , up_Storage = form.up_Storage.data,
                    rep_battery = form.rep_battery.data,
                    keyb_layout = form.keyb_layout.data , keyb_backlit = form.keyb_backlit.data , keyb_num = form.keyb_num.data,
                    lte_modem = form.lte_modem.data , battery_life = form.battery_life.data , battery_size = form.battery_size.data,
                    product_state = form.product_state.data , charger = form.charger.data , extra_acc = form.extra_acc.data ,user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Item has Been Added Successfully','success')
        return redirect(url_for('home'))
    return render_template('newpost.html',Store_name=Store_name,title="Adding A New Item",form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_pic(form_picture):
    rndm_hex = secrets.token_hex(10) 
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = rndm_hex + f_ext
    picture_path = os.path.join(app.root_path , 'static/img',picture_fn)
    # Resizing :
    output_size = (300 ,300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    #
    i.save(picture_path)
    return picture_fn


@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data :
            if current_user.image_file != "default.png" :
                os.remove(os.path.join(app.root_path , 'static/img',current_user.image_file))
            pic_fn = save_pic(form.picture.data)
            current_user.image_file = pic_fn
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated','success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='img/'+ current_user.image_file)

    return render_template('profile.html',Store_name=Store_name,title='Profile',img_file = image_file , form=form)

@app.route('/item/<int:post_id>')
def post(post_id):
    post = Item.query.get_or_404(post_id)
    return render_template('post.html',Store_name=Store_name,title=post.product_name,item=post)

@app.route('/item/<int:id>/delete',methods=['POST'])
@login_required
def delete_post(id):
    post = Item.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    if post.img1:
        os.remove(os.path.join(app.root_path , 'static/img',post.img1))
    if post.img2:
        os.remove(os.path.join(app.root_path , 'static/img',post.img2))
    if post.img3:
        os.remove(os.path.join(app.root_path , 'static/img',post.img3))
    if post.img4:
        os.remove(os.path.join(app.root_path , 'static/img',post.img4))
    if post.img5:
        os.remove(os.path.join(app.root_path , 'static/img',post.img5))
    if post.img6:
        os.remove(os.path.join(app.root_path , 'static/img',post.img6))
    db.session.delete(post)
    db.session.commit()
    if session["comp1"] == id:
        session["comp1"] = 0
    if session["comp2"] == id:
        session["comp2"] = 0
    flash('Item Has Been Deleted','success')
    return redirect(url_for('home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.errorhandler(404)
def error404(e):
    return render_template('404.html',Store_name=Store_name,title="404 - Page Not Found"),404

@app.errorhandler(403)
def error403(e):
    return render_template('404.html',Store_name=Store_name,title="403 - Forbidden Access"),403

@app.errorhandler(500)
def error500(e):
    return render_template('404.html',Store_name=Store_name,title="404 - Server Error"),500
