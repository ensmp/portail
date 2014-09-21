#-*- coding: utf-8 -*-
from django.core.files import File
from django.db import models
import subprocess
import os
from django import forms
from trombi.models import UserProfile

   
class UpdateSoldeForm(forms.Form):
    eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    credit = forms.FloatField()
    debit = forms.FloatField()

