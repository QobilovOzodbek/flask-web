from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    github = db.Column(db.String(120), nullable=True)
    youtube = db.Column(db.String(120), nullable=True)
    telegram = db.Column(db.String(120), nullable=True)
    instagram = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        author = request.form['author']
        github = request.form['github']
        youtube = request.form['youtube']
        telegram = request.form['telegram']
        instagram = request.form['instagram']
        
        image = request.files['image']
        image_filename = datetime.now().strftime("%Y%m%d%H%M%S") + '_' + image.filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        
        post = Post(title=title, description=description, content=content, author=author,
                    github=github, youtube=youtube, telegram=telegram, instagram=instagram,
                    image=image_filename)
        db.session.add(post)
        db.session.commit()
        flash('Post muvaffaqiyatli qo\'shildi!', 'success')
        return redirect(url_for('index'))
    
    return render_template('post_create.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.description = request.form['description']
        post.content = request.form['content']
        post.author = request.form['author']
        post.github = request.form['github']
        post.youtube = request.form['youtube']
        post.telegram = request.form['telegram']
        post.instagram = request.form['instagram']

        image = request.files['image']
        if image:
            image_filename = datetime.now().strftime("%Y%m%d%H%M%S") + '_' + image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
            post.image = image_filename

        db.session.commit()
        flash('Post muvaffaqiyatli tahrirlandi!', 'success')
        return redirect(url_for('index'))
    
    return render_template('post_edit.html', post=post)

@app.route('/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post muvaffaqiyatli o\'chirildi!', 'success')
    return redirect(url_for('view_post', post_id=post.id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin'))
        flash('Noto‘g‘ri login yoki parol', 'danger')

    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    posts = Post.query.all()
    total_posts = len(posts)
    return render_template('admin.html', posts=posts, total_posts=total_posts)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']

        admin = Admin.query.first()
        if not admin:
            admin = Admin(username=new_username)
            db.session.add(admin)
        else:
            admin.username = new_username
        admin.set_password(new_password)
        db.session.commit()

        flash('Admin login va parol muvaffaqiyatli yangilandi!', 'success')
        return redirect(url_for('admin'))

    return render_template('admin_settings.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ma'lumotlar bazasini yaratish
with app.app_context():
    db.create_all()

    # Yangi admin foydalanuvchi yaratish
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(username='admin')
        admin.set_password('admin')  # Parol: admin
        db.session.add(admin)
        db.session.commit()
        print("Admin foydalanuvchi yaratildi: admin/admin")

if __name__ == '__main__':
    app.run(debug=True)
