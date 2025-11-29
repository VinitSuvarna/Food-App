from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# ----------------------------------------------------------------------------------------------

class FoodItemsModel(models.Model):
    prod_code = models.IntegerField(default=100)
    restaurant_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=1
    )
    admin = models.CharField(null=True, max_length=50)
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(
        max_length=500,
        default="Lorem, ipsum dolor sit amet consectetur adipisicing elit. Explicabo magni, nihil assumenda sit praesentium repellendus autem culpa aliquid sequi beatae eveniet voluptatum exercitationem a aspernatur, illo placeat fugiat ducimus voluptas."
    )
    item_price = models.IntegerField()
    item_image = models.CharField(
        max_length=500,
        default="https://cdn.dribbble.com/userupload/22570626/file/original-379b4978ee41eeb352e0ddacbaa6df96.jpg"
    )

    def __str__(self):
        return str((self.item_name, self.item_price))


# log history model
# ----------------------------------------------------------------------------------------------

class LogHistoryModel(models.Model):
    log_username = models.CharField(max_length=50)
    log_prod_code = models.IntegerField(default=100)
    log_item_name = models.CharField(max_length=100)
    log_operation_type = models.CharField(max_length=50)

    def __str__(self):
        return str(
            (
                self.log_prod_code,
                self.log_username,
                self.log_item_name,
                self.log_operation_type,
            )
        )


# orders model (for "Order Now" + payment later)
# ----------------------------------------------------------------------------------------------

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    item = models.ForeignKey(
        FoodItemsModel,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveIntegerField(default=1)
    # store price at the time of order so if you change item_price later,
    # old orders keep their original price
    price_at_order = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.item.item_name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price_at_order
