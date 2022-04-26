from django.forms import ModelForm
from .models import exam_inv
class exam_invi(ModelForm):
	class Meta:#returns fields
		model=exam_inv
		fields='__all__'


