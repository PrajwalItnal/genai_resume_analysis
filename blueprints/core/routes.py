from flask import Blueprint, redirect, url_for

core = Blueprint('core', __name__, template_folder='template')

@core.route('/')
def index():
    return redirect(url_for('analyse.index'))