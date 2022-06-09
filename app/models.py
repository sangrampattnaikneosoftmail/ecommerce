from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

import os
from uuid import uuid4
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # managed = True
        abstract = True


def path_and_rename(instance, filename):
    upload_to = "media_files"
    ext = filename.split(".")[-1]
    # get filename
    if instance.pk:
        filename = f"{instance.pk}.{ext}"
    else:
        # set filename as random string
        filename = f"{uuid4().hex}.{ext}"
    # return the whole path to the file
    return os.path.join(upload_to, filename)


STATE_CHOICES = (
    ("Andaman & Nicobar Islands", "Andaman & Nicobar Islands"),
    ("Andhra Pradesh", "Andhra Pradesh"),
    ("Arunachal Pradesh", "Arunachal Pradesh"),
    ("Assam", "Assam"),
    ("Bihar", "Bihar"),
    ("Chandigarh", "Chandigarh"),
    ("Chhattisgarh", "Chhattisgarh"),
    ("Dadra & Nagar Haveli", "Dadra & Nagar Haveli"),
    ("Daman and Diu", "Daman and Diu"),
    ("Delhi", "Delhi"),
    ("Goa", "Goa"),
    ("Gujarat", "Gujarat"),
    ("Haryana", "Haryana"),
    ("Himachal Pradesh", "Himachal Pradesh"),
    ("Jammu & Kashmir", "Jammu & Kashmir"),
    ("Jharkhand", "Jharkhand"),
    ("Karnataka", "Karnataka"),
    ("Kerala", "Kerala"),
    ("Lakshadweep", "Lakshadweep"),
    ("Madhya Pradesh", "Madhya Pradesh"),
    ("Maharashtra", "Maharashtra"),
    ("Manipur", "Manipur"),
    ("Meghalaya", "Meghalaya"),
    ("Mizoram", "Mizoram"),
    ("Nagaland", "Nagaland"),
    ("Odisha", "Odisha"),
    ("Puducherry", "Puducherry"),
    ("Punjab", "Punjab"),
    ("Rajasthan", "Rajasthan"),
    ("Sikkim", "Sikkim"),
    ("Tamil Nadu", "Tamil Nadu"),
    ("Telangana", "Telangana"),
    ("Tripura", "Tripura"),
    ("Uttarakhand", "Uttarakhand"),
    ("Uttar Pradesh", "Uttar Pradesh"),
    ("West Bengal", "West Bengal"),
)


class Customer(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='customer')
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        # return self.user.username
        return str(self.id)


CATEGORY_CHOICES = (
    ("M", "Mobile"),
    ("L", "Laptop"),
    ("TW", "Top Wear"),
    ("BW", "Bottom Wear"),
)


class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="sub_categories"
    )
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "SubCategory"
        verbose_name_plural = "SubCategories"


class Product(BaseModel):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    #  category = models.CharField( choices=CATEGORY_CHOICES, max_length=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to=path_and_rename)
    is_trending = models.BooleanField(default=False)
    is_recommoned = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=path_and_rename)


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

        # Below Property will be used by checkout.html page to show total cost in order summary

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On The Way", "On The Way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel"),
)


class OrderPlaced(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    # Below Property will be used by orders.html page to show total cost
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


class Coupon(BaseModel):
    code = models.CharField(max_length=15, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    minimum_amount = models.FloatField(default=1000)
    is_show_on_front_end = models.BooleanField(default=True)
    discount_amount = models.FloatField()

    def __str__(self):
        return self.code
