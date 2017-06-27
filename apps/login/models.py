# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
import re
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
ALPHASPACE_REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z ]+[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validate(self, form_data):
        errors = []
        if (len(form_data['name']) < 3 or
                not ALPHASPACE_REGEX.match(form_data['name'])):
            errors.append(
                'Name must include at least three characters ' +
                '(only letters and spaces allowed--must begin and end with a ' +
                'letter).')
        if (len(form_data['reg_username']) < 3 or
                not form_data['reg_username'].isalpha()):
            errors.append('Username must include at least three ' +
                          'characters (letters only).')
        if len(form_data['reg_password']) < 8:
            errors.append('Password must include at least eight characters.')
        if form_data['reg_password'] != form_data['confirm']:
            errors.append('Passwords do not match.')
        return errors
    def register(self, user_data):
        new_user = User(
            name=user_data['name'],
            username=user_data['reg_username'],
            password=bcrypt.hashpw(
                user_data['reg_password'].encode(), bcrypt.gensalt()
            )
        )
        new_user.save()
        return new_user
    def log_validate(self, form_data):
        found_user = User.objects.get(username__iexact=form_data['log_username'])
        return found_user
    def check_password(self, user_data, form_data):
        if user_data.password == bcrypt.hashpw(
                form_data['log_password'].encode(),
                user_data.password.encode()):
            return True
        else:
            return False
    def login(self, user_data):
        logged_user = User.objects.get(username__iexact=user_data['log_username'])
        return logged_user.id

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
