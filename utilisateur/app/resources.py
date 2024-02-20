from import_export import resources
from .models import Beneficiaire 

class BeneficiaireResource(resources.ModelResource):
    class Meta:
        model = Beneficiaire