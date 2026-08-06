from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserInfo
from django.utils.html import format_html

# Register your models here.
class UserInfoAdmin(admin.ModelAdmin):
    # 列表中显示的字段
    list_display = (
        'username',
        'uemail',
        'uphone',
        'uaddress',
        'created_at',
        'show_avatar'
    )
    # 可以点击进入编辑页面的字段
    list_display_links = ('username', 'uemail')
    # 可筛选的字段
    list_filter = ('created_at',)
    # 可搜索的字段
    search_fields = (
        'username',
        'uemail',
        'uphone'
    )
    # 分页设置（每页显示多少条记录）
    list_per_page = 20
    # 按创建时间排序（默认排序）
    ordering = ('-created_at',)

    # 编辑页面的字段分组布局
    fieldsets = (
        ('基本信息', {
            'fields': ('username', 'password', 'uemail', 'avatar')
        }),
        ('联系信息', {
            'fields': ('uphone', 'uaddress', 'uyoubian')
        }),
        ('其他信息', {
            'fields': ('created_at',)
        }),
    )

    # 自定义头像显示方法（使用format_html安全渲染HTML）
    def show_avatar(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-height:50px;max-width:50px;border-radius:50%;" />',
                obj.avatar.url if hasattr(obj.avatar, 'url') else obj.avatar
            )
        return format_html('<span style="color:gray;">无头像</span>')

    show_avatar.short_description = '头像预览'
    show_avatar.admin_order_field = 'avatar'

# 注册模型和对应的Admin类
admin.site.register(UserInfo, UserInfoAdmin)