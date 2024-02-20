
from django.contrib import admin
from .models import Beneficiaire , BeneficiaireModifie
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# @admin.register(Beneficiaire)

class beneficiaireAdmin (ImportExportModelAdmin):
    
     list_display = ('id', 'nom', 'prenom','matricule','numero_piece','type_piece','date_livrance','email','date_naissance','code_postal','sexe','adresse')
# class beneficiaireAdmin(ImportExportMixin, admin.ModelAdmin):
#     pass

admin.site.register(Beneficiaire, beneficiaireAdmin)


admin.site.register(BeneficiaireModifie)