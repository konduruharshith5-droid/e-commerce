from django.db import models

# Create your models here.

class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default=" ")
    subcategory = models.CharField(max_length=50, default=" ")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=500)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    mag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default = " ")
    email = models.CharField(max_length=50, default = " ")
    password = models.CharField(max_length=50, default =  " ")

    def __str__(self):
        return self.name

class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=500,default = " ")
    amount = models.IntegerField()
    name = models.CharField(max_length=50, default=" ")
    email = models.CharField(max_length=50, default=" ")
    address = models.CharField(max_length=100, default=" ")
    city = models.CharField(max_length=50, default=" ")
    state = models.CharField(max_length=100)
    zip = models.IntegerField()
    phone = models.CharField(max_length=25, default=" ")

    def __str__(self):
        return self.name

class updateorders(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default = "")
    update_desc = models.CharField(max_length=5000)
    tiem_stamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
