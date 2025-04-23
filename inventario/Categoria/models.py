from django.db import models
from autoslug import AutoSlugField
# Create your models here.


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column='id_categoria')
    nom_categoria = models.CharField(max_length=50, db_column='nom_categoria')
    slug = AutoSlugField(populate_from='id_categoria')

    def __str__(self):
        return str(self.id_categoria)
    
    class Meta:
        db_table='Categoria'
        verbose_name='Categoria'
        verbose_name_plural='Categorias'
        managed = False


class Producto(models.Model):
    cod_material = models.AutoField(primary_key=True, db_column='cod_material')
    nom_producto = models.CharField(max_length=50)
    cant_existencia = models.IntegerField()
    descripcion = models.CharField(max_length=50, db_column='descripcion')
    stock_minimo = models.IntegerField(default=20)
    stock_maximo = models.IntegerField(default=100)
    categoria_id = models.IntegerField()

    def __str__(self):
        return str(self.cod_material)

    class Meta:
        db_table='Producto'
        verbose_name='Producto'
        verbose_name_plural='Productos'
        managed = False

