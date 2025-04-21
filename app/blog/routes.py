from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.blog import blog_bp
from app.models import BlogPost, Profile
from app import db
from openai import OpenAI
import json

# Available models for text and image generation
TEXT_MODELS = [
    {'id': 'gpt-4o-mini', 'name': 'GPT-4o Mini'},
    {'id': 'gpt-3.5-turbo', 'name': 'GPT-3.5 Turbo'}
]

IMAGE_MODELS = [
    {'id': 'dall-e-3', 'name': 'DALL-E 3'},
    {'id': 'dall-e-2', 'name': 'DALL-E 2'}
]

@blog_bp.route('/')
@login_required
def index():
    posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts, text_models=TEXT_MODELS, image_models=IMAGE_MODELS)

@blog_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        # Get form data
        topic = request.form.get('topic')
        text_model = request.form.get('text_model')
        image_model = request.form.get('image_model')
        prompt = request.form.get('prompt')

        # Validate API key
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if not profile or not profile.openai_api_key:
            flash('Please configure your OpenAI API key in settings first.', 'warning')
            return redirect(url_for('settings.profile'))

        try:
            # Initialize OpenAI client
            client = OpenAI(api_key=profile.openai_api_key)

            # Generate blog content
            response = client.chat.completions.create(
                model=text_model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Write a blog post about: {topic}"}
                ]
            )

            # Parse the response
            content = response.choices[0].message.content
            try:
                # Try to parse as JSON first
                blog_data = json.loads(content)
                title = blog_data.get('title', topic)
                blog_content = blog_data.get('content', content)
            except json.JSONDecodeError:
                # If not JSON, use the whole content
                title = topic
                blog_content = content

            # Generate image
            image_response = client.images.generate(
                model=image_model,
                prompt=f"Create a blog header image for a post about: {topic}",
                n=1,
                size="1024x1024"
            )
            image_url = image_response.data[0].url

            # Create blog post
            blog_post = BlogPost(
                title=title,
                content=blog_content,
                image_url=image_url,
                text_model=text_model,
                image_model=image_model,
                prompt=prompt,
                user_id=current_user.id
            )

            db.session.add(blog_post)
            db.session.commit()

            flash('Blog post created successfully!', 'success')
            return redirect(url_for('blog.index'))

        except Exception as e:
            flash(f'Error creating blog post: {str(e)}', 'danger')
            return redirect(url_for('blog.create'))

    return render_template('blog/create.html', text_models=TEXT_MODELS, image_models=IMAGE_MODELS) 