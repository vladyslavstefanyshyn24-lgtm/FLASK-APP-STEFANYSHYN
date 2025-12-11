from flask import render_template, redirect, url_for, flash
from . import post_bp
from .forms import PostForm
from .models import Post, Tag
from app import db


@post_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            posted=form.posted.data,
            user_id=form.author_id.data
        )
        db.session.add(post)
        db.session.commit()

        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
            post.tags.extend(selected_tags)
            db.session.commit()

        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.list_posts'))

    return render_template('add_post.html', form=form)


@post_bp.route('/post', endpoint='list_posts')
def all_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('all_posts.html', posts=posts)

@post_bp.route('/post/<int:id>', endpoint='detail')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template('detail_post.html', post=post)