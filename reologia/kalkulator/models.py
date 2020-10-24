from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator,int_list_validator,MinLengthValidator

class InputData(models.Model):
    kąty = models.CharField(validators=[int_list_validator(sep=','),MinLengthValidator(limit_value=11)],max_length=36)
    uklad_cylindrów_RB = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)])
    typ_sprężyny = models.IntegerField(validators=[MaxValueValidator(6),MinValueValidator(1)])
    rodzaj_cylindra_wewnętrznego = models.IntegerField(validators=[MaxValueValidator(4),MinValueValidator(1)])


