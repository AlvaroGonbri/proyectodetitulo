from django.db import models

class Tecnico(models.Model):
    rut_trab = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    fono = models.CharField(max_length=15, blank=True, null=True)
    especialidad = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'Tecnico'   # <--- Esto es lo importante

    def __str__(self):
        return self.full_name or str(self.rut_trab)

    class Meta:
        managed = False
        db_table = 'Tecnico'
