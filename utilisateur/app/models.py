from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Beneficiaire(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255, blank=True, null=True)
    matricule = models.CharField(max_length=255, blank=True, null=True)
    numero_piece = models.CharField(max_length=255, blank=True, null=True)
    type_piece = models.CharField(max_length=255, blank=True, null=True)
    date_livrance = models.CharField(max_length=10, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_naissance = models.CharField(max_length=10, blank=True, null=True)
    code_postal = models.CharField(max_length=10, blank=True, null=True)
    sexe = models.CharField(max_length=10, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    
class BeneficiaireModifie(models.Model):
    beneficiaire = models.OneToOneField(Beneficiaire, on_delete=models.CASCADE)
    date_modification = models.DateTimeField(auto_now_add=True)

# Signal pour détecter les modifications et enregistrer dans BeneficiaireModifie

# post_save.connect(detecter_et_enregistrer_modifications, sender=Beneficiaire)
@receiver(post_save, sender=Beneficiaire)
def detecter_et_enregistrer_modifications(sender, instance, **kwargs):
    beneficiaire_modifie, created = BeneficiaireModifie.objects.get_or_create(beneficiaire=instance)

    # Comparer les attributs de Beneficiaire et BeneficiaireModifie pour détecter les modifications
    if (
        instance.nom != beneficiaire_modifie.beneficiaire.nom or
        instance.prenom != beneficiaire_modifie.beneficiaire.prenom or
        instance.matricule != beneficiaire_modifie.beneficiaire.matricule or
        instance.numero_piece != beneficiaire_modifie.beneficiaire.numero_piece or
        instance.type_piece != beneficiaire_modifie.beneficiaire.type_piece or
        instance.date_livrance != beneficiaire_modifie.beneficiaire.date_livrance or
        instance.telephone != beneficiaire_modifie.beneficiaire.telephone or
        instance.email != beneficiaire_modifie.beneficiaire.email or
        instance.date_naissance != beneficiaire_modifie.beneficiaire.date_naissance or
        instance.code_postal != beneficiaire_modifie.beneficiaire.code_postal or
        instance.sexe != beneficiaire_modifie.beneficiaire.sexe or
        instance.adresse != beneficiaire_modifie.beneficiaire.adresse
    ):
        # Si les attributs sont différents, enregistrer dans BeneficiaireModifie
        beneficiaire_modifie.date_modification = datetime.now()
        beneficiaire_modifie.save()

    
    