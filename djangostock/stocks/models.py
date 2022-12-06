from django.db import models
class StockInfo(models.Model):
    stock_name = models.CharField(primary_key=True, max_length=100)
    stock_cap = models.CharField(max_length=100)
    themas = models.CharField(max_length=300)

    def __str__(self) -> str:
        return  self.stock_name