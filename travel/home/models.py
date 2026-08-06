from django.db import models

# Create your models here.
from django.db import models

class TravelInfo(models.Model):
    # 唯一标识
    unique_id = models.BigIntegerField(null=True, verbose_name='唯一标识')
    # 所在区域
    area = models.CharField(max_length=255, null=True, verbose_name='所在区域')
    # 景点名称
    name = models.CharField(max_length=255, null=True, verbose_name='景点名称')
    # 评论数量
    review_count = models.IntegerField(null=True, verbose_name='评论数量')
    # 评分
    rating = models.CharField(max_length=50, null=True, verbose_name='评分')
    # 是否为广西内容
    is_ad = models.BooleanField(default=False, null=True, verbose_name='是否为广告')
    # 是否被推荐
    is_recommended = models.BooleanField(default=False, null=True, verbose_name='是否被推荐')
    # 城市名称
    city = models.CharField(max_length=50, null=True, verbose_name='城市名称')
    # 图片链接
    image_url = models.CharField(max_length=255, null=True, verbose_name='图片链接')
    # 与市中心的距离
    distance_from_center = models.CharField(max_length=255, null=True, verbose_name='与市中心的距离')
    # 标签
    tags = models.CharField(max_length=255, null=True, verbose_name='标签')
    # 详情页链接
    detail_link = models.CharField(max_length=500, null=True, verbose_name='详情页链接')
    # 市场票价
    market_price = models.CharField(null=True, verbose_name='市场票价', max_length=255)
    # 优惠价格
    discount_price = models.CharField(null=True, verbose_name='优惠价格', max_length=255)
    # 优惠描述
    discount_description = models.CharField(null=True, verbose_name='优惠描述', max_length=255)
    # 实际票价
    actual_price = models.CharField(null=True, verbose_name='实际票价', max_length=255)
    # 价格类型
    price_type = models.CharField(null=True, verbose_name='价格类型', max_length=255)
    # 价格类型描述
    price_type_description = models.CharField(max_length=100, null=True, verbose_name='价格类型描述')
    # 是否免费
    is_free = models.BooleanField(default=False, null=True, verbose_name='是否免费')
    # 经度
    longitude = models.FloatField(null=True, verbose_name='经度')
    # 纬度
    latitude = models.FloatField(null=True, verbose_name='纬度')
    # 热度评分
    popularity_score = models.CharField(null=True, verbose_name='热度评分', max_length=255)
    # 省份
    province = models.CharField(max_length=100, null=True, verbose_name='省份')

    class Meta:
        verbose_name_plural = '旅游景点管理'
