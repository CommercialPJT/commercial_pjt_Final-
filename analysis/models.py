from mimetypes import guess_all_extensions
from pyexpat import model
from tkinter.tix import Tree
from django.db import models
from django.forms import CharField
from sklearn.metrics import mean_absolute_percentage_error



# Create your models here.

class Locate_Info(models.Model) :

    data_date = models.CharField(max_length=10)
    division = models.CharField(max_length=20)
    name = models.CharField(max_length=100, unique=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    city = models.CharField(max_length=20)
    gu = models.CharField(max_length=20)
    dong = models.CharField(max_length=20)

    def __str__(request) :
        return request.name

    def to_json(self) :
        return {
            "divison" : self.division,
            "name" : self.name,
            "longtitude" : self.longitude,
            "latitude" : self.latitude,
            "city" : self.city,
            "gu" : self.gu,
            "dong" : self.dong
        }


# class full_data(models.Model) :
#     idx = models.IntegerField(unique=True)
#     year = models.IntegerField()
#     season = models.IntegerField()
#     local = models.IntegerField()
#     service = models.IntegerField()
#     season_profit = models.IntegerField()
#     season_count = models.IntegerField()
#     week_rate = models.IntegerField()
#     weeken_rate = models.IntegerField()
#     male_rate = models.IntegerField()
#     female_rate = models.IntegerField()
#     day_rate = models.IntegerField()
#     night_rate = models.IntegerField()
#     teen_rate = models.IntegerField()
#     youth_rate = models.IntegerField()
#     elder_rate = models.IntegerField()
#     old_rate = models.IntegerField()
#     gu = models.CharField(max_length=20)
#     dong = models.CharField(max_length=20)

#     def __str__(request) :
#         return request.season 

#     def to_json(self) :
#         return {
#             "year" : self.year,
#             "season" : self.season,
#             "local" : self.local,
#             "service" : self.service,
#             "season_profit" : self.season_profit,
#             "season_count" : self.season_count,
#             "week_rate" : self.week_rate,
#             "male_rate" : self.male_rate,
#             "female_rate" : self.female_rate,
#             "day_rate" : self.day_rate,
#             "night_rate" : self.night_rate,
#             "teen_rate" : self.teen_rate,
#             "youth_rate" : self.youth_rate,
#             "elder_rate" : self.elder_rate,
#             "old_rate" : self.old_rate,
#             "gu" : self.gu,
#             "dong" : self.dong
#         }



class full_data_model(models.Model) :
    idx = models.IntegerField(unique=True)
    year = models.IntegerField()
    season = models.IntegerField()
    local = models.IntegerField()
    service = models.IntegerField()
    service_name = models.CharField(max_length=20)
    season_profit = models.IntegerField()
    season_count = models.IntegerField()
    week_rate = models.IntegerField()
    week_count = models.IntegerField()
    weeken_rate = models.IntegerField()
    weeken_count = models.IntegerField()
    male_rate = models.IntegerField()
    male_count = models.IntegerField()
    female_rate = models.IntegerField()
    female_count = models.IntegerField()
    day_rate = models.IntegerField()
    day_count = models.IntegerField()
    night_rate = models.IntegerField()
    night_count = models.IntegerField()
    young_rate = models.IntegerField()
    young_count = models.IntegerField()
    youth_rate = models.IntegerField()
    youth_count = models.IntegerField()
    elder_rate = models.IntegerField()
    elder_count = models.IntegerField()
    old_rate = models.IntegerField()
    old_count = models.IntegerField()
    gu = models.CharField(max_length=20)
    dong = models.CharField(max_length=20)

    def __str__(request) :
        return request.gu 

    def to_json(self) :
        return {
            "year" : self.year,
            "season" : self.season,
            "local" : self.local,
            "service" : self.service,
            "service_name" : self.service_name,
            "season_profit" : self.season_profit,
            "season_count" : self.season_count,
            "week_rate" : self.week_rate,
            "male_rate" : self.male_rate,
            "female_rate" : self.female_rate,
            "day_rate" : self.day_rate,
            "night_rate" : self.night_rate,
            "teen_rate" : self.teen_rate,
            "youth_rate" : self.youth_rate,
            "elder_rate" : self.elder_rate,
            "old_rate" : self.old_rate,
            "gu" : self.gu,
            "dong" : self.dong
        }




class realty_data(models.Model) :
    idx = models.IntegerField(unique=True)
    bd_type1 = models.CharField(max_length=6)
    bd_type2 = models.CharField(max_length=15)
    city = models.CharField(max_length=10)
    gu = models.CharField(max_length=10)
    dong = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    trade_type = models.CharField(max_length=6)
    deposit = models.IntegerField()
    month_price = models.IntegerField()
    leasable_area = models.IntegerField()
    total_area = models.IntegerField()
    floor = models.IntegerField()
    total_floor = models.IntegerField()
    direction = models.CharField(max_length=5)
    detail = models.CharField(max_length=200)

    def __str__(request) :
        return request.detail
    def to_json(self) :
        return {
            "idx" : self.idx,
            "bd_type1" : self.bd_type1,
            "bd_type2" : self.bd_type2,
            "city" : self.city,
            "gu" : self.gu,
            "dong" : self.dong,
            "name" : self.name,
            "trade_type" : self.trade_type,
            "deposit" : self.deposit,
            "month_price" : self.month_price,
            "leasable_area" : self.leasable_area,
            "total_area" : self.total_area,
            "floor" : self.floor,
            "total_floor" : self.total_floor,
            "direction" : self.direction,
            "detail" : self.detail,
        }