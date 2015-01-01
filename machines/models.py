# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import F, Count
from django.db.models.signals import post_save
import datetime

class MachineProfile(models.Model) :
	
	nom = models.CharField(max_length=128, verbose_name="nom de la machine")
	#Si la machine est en libre, etat est à true
	etat = models.BooleanField()