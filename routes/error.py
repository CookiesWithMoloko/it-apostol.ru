from app import app
from flask import render_template, request, redirect

@app.errorhandler(404)
def on404(e):
    """Not Found"""
    return render_template('./error/404.html', error=e), 404

@app.errorhandler(401)
def on401(e):
    """Unauthorized"""
    return render_template('./error/401.html', error=e), 401
