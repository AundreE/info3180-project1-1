from app import app, db
from flask import render_template, request, redirect, url_for, flash
from forms import LoginForm
from models import UserProfile

@app.route('/')
def index():
    print "Hello World"