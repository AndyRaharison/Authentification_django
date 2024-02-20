from django.core import validators
from django import forms
from .models import Beneficiaire

# class BeneficiaireForm(forms.Form):
#     class Meta:
#         model = beneficiaire
#         fields = '__all__'
        
class BeneficiaireRegistration(forms.ModelForm):
    class Meta:
        model = Beneficiaire
        fields = ['nom', 'prenom','matricule','numero_piece','type_piece','date_livrance','email','date_naissance','code_postal','sexe','adresse']
        widgets = {
                  'nom': forms.TextInput(attrs={'class': 'form-control'}),
                  'prenom':forms.TextInput(attrs={'class': 'form-control'}),
                  'matricule':forms.TextInput(attrs={'class': 'form-control'}),
                  'numero_piece':forms.TextInput(attrs={'class': 'form-control'}),
                  'type_piece':forms.TextInput(attrs={'class': 'form-control'}),
                  'date_livrance':forms.DateTimeInput(attrs={'format': '%d-%m-%Y'}),
                  'email':forms.EmailInput(attrs={'class': 'form-control'}),
                  'date_naissance':forms.TextInput(attrs={'format': '%d-%m-%Y'}),
                  'code_postal':forms.TextInput(attrs={'class': 'form-control'}),
                  'sexe':forms.TextInput(attrs={'class': 'form-control'}),
                  'adresse':forms.TextInput(attrs={'class': 'form-control'}),
                  }