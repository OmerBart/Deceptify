import os
import uuid

from flask import redirect as flask_redirect
from werkzeug.utils import secure_filename

from Server.Forms.general_forms import *
from Server.Forms.upload_data_forms import *
from flask import render_template, url_for, flash, request, send_from_directory

from Server.data.Models.attack import Attack
from Server.data.Models.profile import *


def error_routes(app):  # Error handlers routes
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500


def general_routes(app, data_storage):  # This function stores all the general routes.
    @app.route('/', methods=['GET', 'POST'])  # The root router (welcome page).
    def index():
        return render_template('index.html')

    @app.route('/new_profile', methods=['GET', 'POST'])
    def new_profile():
        form = ProfileForm()
        if form.validate_on_submit():
            name = form.name_field.data
            role = form.role_field.data
            gen_info = form.gen_info_field.data
            data_type = form.data_type_selection.data
            data = form.recording_upload.data
            new_prof = Profile(profile_name=name, role=role, general_info=gen_info,
                               data_type=data_type, data=data)
            data_storage.add_profile(new_prof)
            flash("Profile created successfully")
            return flask_redirect(url_for('index'))
        return render_template('attack_pages/new_profile.html', form=form)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        email = None
        contact_field = None
        passwd = None
        form = ContactForm()
        if form.validate_on_submit():
            email = form.email.data
            contact_field = form.contact_field.data
            passwd = form.passwd.data
            return flask_redirect(url_for('index'))
        return render_template('contact.html', form=form)

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/profiles')
    def profiles():
        profs = data_storage.get_profiles()
        return render_template('_profiles.html', profiles=profs)

    @app.route('/attacks')
    def attacks():
        attacks = data_storage.get_attacks()
        return render_template('_attacks.html', attacks=attacks)

    @app.route('/recordings')
    def recordings():
        data_storage.update_records_list(app.config['UPLOAD_FOLDER'])  # Updating the list before returning the page
        recordings = data_storage.get_recordings()  # Get all the recordings.
        return render_template('_recordings.html', recordings=recordings)

    @app.route('/mp3/<path:filename>')  # Serve the MP3 files statically
    def serve_mp3(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def attack_generation_routes(app, data_storage):
    @app.route('/newattack', methods=['GET', 'POST'])  # The new chat route.
    def newattack():
        # omer 11/5/24 added form and capturing data + generating unique id
        form = CampaignForm()
        if form.validate_on_submit():
            campaign_name = form.campaign_name.data
            mimic_profile = form.mimic_profile.data
            target_profile = form.target_profile.data
            campaign_description = form.campaign_description.data
            campaign_unique_id = str(uuid.uuid4())
            new_attack = Attack(campaign_name=campaign_name, mimic_profile=mimic_profile,
                                target=target_profile, description=campaign_description, camp_id=campaign_unique_id)
            data_storage.add_attack(new_attack)
            flash("Campaign created successfully using")
            return flask_redirect(url_for('attack_dashboard'))
        return render_template('attack_pages/newattack.html', form=form)

    @app.route('/attack_dashboard', methods=['GET', 'POST'])
    def attack_dashboard():
        form = AttackDashboardForm()
        return render_template('attack_pages/attack_dashboard.html', form=form)

    @app.route('/information_gathering', methods=['GET', 'POST'])
    def information_gathering():
        form = InformationGatheringForm()
        if form.validate_on_submit():
            choice = form.selection.data.lower()
            if 'datasets' in choice:
                return flask_redirect(url_for('collect_dataset'))
            elif 'recordings' in choice:
                return flask_redirect(url_for('new_voice_attack'))
            elif 'video' in choice:
                return flask_redirect(url_for('collect_video'))
        return render_template('data_collection_pages/information_gathering.html', form=form)

    @app.route('/collect_video', methods=['GET', 'POST'])
    def collect_video():
        form = VideoUploadForm()
        if form.validate_on_submit():
            video = form.video_field.data
            return flask_redirect(url_for('newattack'))
        return render_template('data_collection_pages/collect_video.html', form=form)

    @app.route('/collect_dataset', methods=['GET', 'POST'])
    def collect_dataset():
        form = DataSetUploadForm()
        if form.validate_on_submit():
            dataset = form.file_field.data
            return flask_redirect(url_for('newattack'))
        return render_template('data_collection_pages/collect_dataset.html', form=form)

    @app.route('/new_voice_attack', methods=['GET', 'POST'])  # New voice attack page.
    def new_voice_attack():
        passwd = None
        form = VoiceChoiceForm()
        if form.validate_on_submit():
            passwd = form.passwd.data
            choice = form.selection.data
            if 'upload' in choice.lower():
                return flask_redirect(url_for('upload_voice_file'))
            else:
                return flask_redirect(url_for('record_voice'))
        return render_template('attack_pages/new_voice_attack.html', form=form)

    @app.route('/upload_voice_file', methods=['GET', 'POST'])  # Route for uploading an existing voice rec file.
    def upload_voice_file():
        voice_file = None
        passwd = None
        form = VoiceUploadForm()
        if form.validate_on_submit():
            voice_file = form.file_field.data
            passwd = form.passwd.data
            if voice_file.filename == '':
                flash('No selected file')
                return flask_redirect(request.url)
            file_name = secure_filename(voice_file.filename)
            full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            voice_file.save(full_file_name)
            flash('Voice uploaded to the server!')
            return flask_redirect(url_for('newattack'))
        return render_template('data_collection_pages/upload_voice_file.html', form=form)

    @app.route('/record_voice', methods=['GET', 'POST'])  # Route for record a new voice file.
    def record_voice():
        if request.method == 'POST':  # If a new recording uploaded to the directory, we have to update the list.
            data_storage.update_records_list(dir_name=app.config['UPLOAD_FOLDER'])
        return render_template('data_collection_pages/record_voice.html')

    @app.route('/save-record', methods=['GET', 'POST'])
    def save_record():
        # check if the post-request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return flask_redirect(request.url)
        file = request.files['file']
        # if a user does not select file, the browser also
        # submits an empty part without a filename
        if file.filename == '':
            flash('No selected file')
            return flask_redirect(request.url)
        file_name = str(uuid.uuid4()) + ".mp3"
        full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        file.save(full_file_name)
        return '<h1>File saved</h1>'


def execute_routes(app, data_storage):  # Function that executes all the routes.
    general_routes(app, data_storage)  # General pages navigation
    attack_generation_routes(app, data_storage)  # Attack generation pages navigation
    error_routes(app)  # Errors pages navigation
