from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) :
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) :
        return self.name



veg_NonVeg_choice= (
        ('Only Veg', 'Only Veg'),
        ('Only Non-Veg', 'Only Non-Veg'),
   
    )
class Product(models.Model):
    name = models.CharField(max_length=25)
    img = models.ImageField(upload_to='Products/')
    category = models.ManyToManyField(Category)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=9999)
    
    veg_nonveg = models.CharField(max_length=20, choices=veg_NonVeg_choice,null=True,blank=True)

    meta_tags = models.TextField()
    meta_description = models.TextField()
    
    def __str__(self):
        return self.name