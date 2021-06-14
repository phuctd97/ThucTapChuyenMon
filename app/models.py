from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from phonenumber_field.modelfields import PhoneNumberField

PROVINCE_CHOICE = (
    ('An Giang', 'An Giang'),
    ('Bà Rịa - Vũng Tàu', 'Bà Rịa - Vũng Tàu'),
    ('Bắc Giang', 'Bắc Giang'),
    ('Bắc Kạn', 'Bắc Kạn'),
    ('Bạc Liêu', 'Bạc Liêu'),
    ('Bắc Ninh', 'Bắc Ninh'),
    ('Bến Tre', 'Bến Tre'),
    ('Bình Định', 'Bình Định'),
    ('Bình Dương', 'Bình Dương'),
    ('Bình Phước', 'Bình Phước'),
    ('Bình Thuận', 'Bình Thuận'),
    ('Cà Mau', 'Cà Mau'),
    ('Cao Bằng', 'Cao Bằng'),
    ('Đắk Lắk', 'Đắk Lắk'),
    ('Đắk Nông', 'Đắk Nông'),
    ('Điện Biên', 'Điện Biên'),
    ('Đồng Nai', 'Đồng Nai'),
    ('Đồng Tháp', 'Đồng Tháp'),
    ('Gia Lai', 'Gia Lai'),
    ('Hà Giang', 'Hà Giang'),
    ('Hà Nam', 'Hà Nam'),
    ('Hà Tĩnh', 'Hà Tĩnh'),
    ('Hải Dương', 'Hải Dương'),
    ('Hậu Giang', 'Hậu Giang'),
    ('Hòa Bình', 'Hòa Bình'),
    ('Hưng Yên', 'Hưng Yên'),
    ('Khánh Hòa', 'Khánh Hòa'),
    ('Kiên Giang', 'Kiên Giang'),
    ('Kon Tum', 'Kon Tum'),
    ('Lai Châu', 'Lai Châu'),
    ('Lâm Đồng', 'Lâm Đồng'),
    ('Lạng Sơn', 'Lạng Sơn'),
    ('Lào Cai', 'Lào Cai'),
    ('Long An', 'Long An'),
    ('Nam Định', 'Nam Định'),
    ('Nghệ An', 'Nghệ An'),
    ('Ninh Bình', 'Ninh Bình'),
    ('Ninh Thuận', 'Ninh Thuận'),
    ('Phú Thọ', 'Phú Thọ'),
    ('Quảng Bình', 'Quảng Bình'),
    ('Quảng Nam', 'Quảng Nam'),
    ('Quảng Ngãi', 'Quảng Ngãi'),
    ('Quảng Ninh', 'Quảng Ninh'),
    ('Quảng Trị', 'Quảng Trị'),
    ('Sóc Trăng', 'Sóc Trăng'),
    ('Sơn La', 'Sơn La'),
    ('Tây Ninh', 'Tây Ninh'),
    ('Thái Bình', 'Thái Bình'),
    ('Thái Nguyên', 'Thái Nguyên'),
    ('Thanh Hóa', 'Thanh Hóa'),
    ('Thừa Thiên Huế', 'Thừa Thiên Huế'),
    ('Tiền Giang', 'Tiền Giang'),
    ('Trà Vinh', 'Trà Vinh'),
    ('Tuyên Quang', 'Tuyên Quang'),
    ('Vĩnh Long', 'Vĩnh Long'),
    ('Vĩnh Phúc', 'Vĩnh Phúc'),
    ('Yên Bái', 'Yên Bái'),
    ('Phú Yên', 'Phú Yên'),
    ('Cần Thơ', 'Cần Thơ'),
    ('Đà Nẵng', 'Đà Nẵng'),
    ('Hải Phòng', 'Hải Phòng'),
    ('Hà Nội', 'Hà Nội'),
    ('TP HCM', 'TP HCM')
)


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    district = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    province = models.CharField(choices=PROVINCE_CHOICE, max_length=100)
    phone = PhoneNumberField(null=True)
    def __str__(self):
        return str(self.id)


BRAND_CHOICES = (
    ('Asus', 'Asus'),
    ('Lenovo', 'Lenovo'),
    ('Macbook', 'Macbook'),
    ('Acer', 'Acer'),
    ('Dell', 'Dell'),
    ('HP', 'HP'),
    ('MSI','MSI'),
    ('LG','LG'),
    ('SN','Sony'),
    ('AP','Apple'),
    ('SS','Samsung'),
    ('LGT','Logitech'),
    ('TCN','Tucano'),
    ('TOM','Tomtoc'),
    ('WW','Wiwu'),
    ('MZ','Mozard'),
    ('PTO','Patriot'),
    ('KL','Kalevv'),
    ('TEA','Teamgroup'),
    ('GG','Gigabyte'),
    ('KST','Kingston')
    
)

CATEGORY_CHOICES = (
    ('LT', 'Laptop'),
    ('C','Components'),
    ('ACC', 'Accessories'),
)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    desception = models.TextField()
    brand = models.CharField(choices =BRAND_CHOICES ,max_length=9)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICE = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivared'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICE, default='Pending')

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price