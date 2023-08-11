from django import forms
from .models import MUNChallengeTable, ImpactChallengeTable

class BaseChallengeModelAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        # Add your custom validation logic here
        c = cleaned_data.get('committee')
        p = cleaned_data.get('portfolio')
        
        combination = self.Meta.model.objects.filter(committee=c, portfolio=p, status='AL')
        if combination:
            raise forms.ValidationError('This combination of committee and portfolio is already alloted')
        
        return cleaned_data
    
    class Meta:
        abstract = True

class MUNModelAdminForm(BaseChallengeModelAdminForm):
    class Meta(BaseChallengeModelAdminForm.Meta):
        model = MUNChallengeTable
        fields = '__all__'

class ImpactModelAdminForm(BaseChallengeModelAdminForm):
    class Meta(BaseChallengeModelAdminForm.Meta):
        model = ImpactChallengeTable
        fields = '__all__'


