from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Profile
from app.settings import settings_bp

@settings_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        openai_api_key = request.form.get('openai_api_key')
        gemini_api_key = request.form.get('gemini_api_key')
        
        current_app.logger.debug(f"Received Gemini API key: {gemini_api_key[:5]}...")
        
        if not profile:
            profile = Profile(user_id=current_user.id)
            db.session.add(profile)
            current_app.logger.debug("Created new profile")
        
        profile.openai_api_key = openai_api_key
        profile.gemini_api_key = gemini_api_key
        
        try:
            db.session.commit()
            current_app.logger.debug("Successfully saved profile with Gemini API key")
            flash('Profile settings updated successfully!', 'success')
            return redirect(url_for('settings.profile'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error saving profile: {str(e)}")
            flash('An error occurred while updating your profile settings.', 'error')
    
    return render_template('settings/profile.html', profile=profile) 