from flask import render_template, redirect, url_for, flash, request
from .. import db
from .models import Post
from .forms import PostForm
from . import post_bp

@post_bp.route('/')
def index():
    posts = db.session.scalars(
        db.select(Post).filter_by(is_active=True).order_by(Post.posted.desc())
    ).all()
    return render_template('all_posts.html', posts=posts)

@post_bp.route('/<int:id>')
def detail(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post)

@post_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.posted.data,
            author='Stefanyshyn'
        )
        db.session.add(post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.index'))
    return render_template('add_post.html', form=form, title='Новий пост')

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.posted = form.posted.data
        db.session.commit()
        flash('Пост оновлено!', 'info')
        return redirect(url_for('posts.detail', id=post.id))

    form.posted.data = post.posted
    return render_template('add_post.html', form=form, title='Редагувати пост')

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    post = db.get_or_404(Post, id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост видалено!', 'danger')
        return redirect(url_for('posts.index'))
    return render_template('delete_confirm.html', post=post)