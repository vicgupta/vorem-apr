from flask import render_template, url_for
from flask_login import login_required, current_user
from app.dashboard import dashboard_bp

@dashboard_bp.route('/')
@login_required
def index():
    # Define available features
    features = [
        {
            'name': 'Easy Blog',
            'description': 'Create and manage your blog posts with AI assistance',
            'url': url_for('blog.index'),
            'icon': 'bi-pencil-square'  # Bootstrap icon class
        },
        # More features will be added here
    ]
    
    user_data = {
        'email': current_user.email,
        'has_api_key': bool(current_user.profile and current_user.profile.openai_api_key)
    }
    
    return render_template('dashboard/index.html', user_data=user_data, features=features) 