#-*- coding: utf-8 -*-
from django.core.files import File
from django.db import models
import subprocess
import os

class Vendome(models.Model):
    """
        Le Vendôme, journal hebdomadaire de l'école.

        Les fichiers doivent être envoyés au format pdf, et peser de
        préférence moins de 10mo pour alléger le serveur et diminuer les temps
        de téléchargement. Un thumbnail est généré automatiquement à l'envoi
        d'un nouveau Vendôme (voir la méthode save())
    """
    titre = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='vendome', help_text="Au format pdf, ne doit pas dépasser 10mo environ")
    date = models.DateField(verbose_name="Date de parution")
    thumbnail = models.ImageField(max_length=300, upload_to='vendome/thumbnail/', blank=True, null=True, verbose_name="Miniature", help_text="Image générée automatiquement à l'envoi d'un Vendôme")
    is_hidden_1A = models.BooleanField(verbose_name="Caché aux 1A")

    class Meta:
        ordering = ['-date']
        verbose_name = "vendôme"
    
    def __unicode__(self):
        return self.titre
	
    def save(self, *args, **kwargs):
        """
            Sauvegarder un vendôme.

            S'il ne possède pas de thumbnail on en génère un via ImageMagick
            en exportant au format png la première de couverture
        """
        super(Vendome, self).save(*args, **kwargs)
        if not self.thumbnail:
            # Génération du fichier image par ligne de commande
            path_destination = os.path.dirname(self.fichier.path) + '/thumbnail/' # Chemin du dossier
            path_destination += os.path.basename(self.fichier.path).partition('.')[0] + '_thumb' + '.png' # Nom du fichier
            command = 'convert -thumbnail x300 ' + self.fichier.path + '[0] ' + path_destination
            if subprocess.call(command,shell=True) == 0:
                # On récupère le fichier généré pour mettre à jour le champ thumbnail
                f = File(open(path_destination,'r'))
                self.thumbnail.save(path_destination, f, True)
                print 'Thumbnail created!'

    def image_tag(self):
        """Tag html de l'image du thumbnail, utilisé dans l'administration des Vendômes."""
        return u'<img src="%s" />' % self.thumbnail.url
    image_tag.allow_tags = True