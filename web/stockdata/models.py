from django.db import models

# Create your models here.
class Corperations(models.Model):
    c_name = models.CharField(max_length=20)
    c_code = models.CharField(max_length=10, primary_key=True)
    c_price = models.IntegerField()
    sales_21 = models.IntegerField()
    operatingincome_21 = models.IntegerField()
    netincome_21 = models.IntegerField()
    sales_20 = models.IntegerField()
    operatingincome_20 = models.IntegerField()
    netincome_20 = models.IntegerField()
    market_cap = models.TextField()
    

# class Stocks(models.Model):
#     code = models.CharField(max_length=10)
#     date = models.DateField()
#     tradePrice = models.IntegerField()
#     openingPrice = models.IntegerField()
#     candleAccTradeVolume = models.IntegerField()
#     changePrice = models.IntegerField()
#     changeRate = models.FloatField()

class PriceinDate(models.Model):
    c_name = models.CharField(max_length=20)
    c_code = models.CharField(max_length=10)
    date = models.DateField()
    tradePrice = models.IntegerField()
    openingPrice = models.IntegerField()
    highPrice = models.IntegerField()
    lowPrice = models.IntegerField()


class Analyzed_Data(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    price = models.IntegerField()
    y_price = models.IntegerField()
    y_difference = models.IntegerField()
    w_price = models.IntegerField()
    w_differnece = models.IntegerField()
    oneday_tradevolume = models.IntegerField()
    y_tradevolume = models.IntegerField()
    w_tradevolume = models.IntegerField()
    nt_highest = models.IntegerField()
    nt_lowest = models.IntegerField()
    nt_percentage = models.DecimalField(decimal_places=3, max_digits=3)
    tt_highest = models.IntegerField()
    tt_lowest = models.IntegerField()
    tt_percentage = models.DecimalField(decimal_places=3, max_digits=3)

    
