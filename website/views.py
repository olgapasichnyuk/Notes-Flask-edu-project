import json

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from website import db
from website.models import Note

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note,
                            user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    note_id = data['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
