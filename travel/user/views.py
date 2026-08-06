import os

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone

from .models import UserInfo
from django.conf import settings

# Create your views here.

def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = UserInfo.objects.get(username=username)
            except UserInfo.DoesNotExist:
                return JsonResponse({'code': 400, 'msg': '用户不存在'})

            if password != user.password:
                return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})

            request.session['uid'] = user.id
            request.session['uname'] = user.username
            request.session['avatar'] = user.avatar

            return JsonResponse({'code': 200, 'msg': '登录成功!'})

        except Exception as e:
            return JsonResponse({'code': 500, 'msg': f'服务器错误{str(e)}'})
    else:
        # GET请求返回登录页面
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(username, password, email)

            # 检查用户名是否已存在
            if UserInfo.objects.filter(username=username).exists():
                return JsonResponse({'code': 400, 'msg': '用户已存在'})
            # 检查邮箱是否已存在
            if UserInfo.objects.filter(uemail=email).exists():
                return JsonResponse({'code': 400, 'msg': '邮箱已存在'})

            # 创建新用户
            UserInfo.objects.create(
                username=username,
                password=password,
                uemail=email,
                uaddress='',
                uyoubian='',
                uphone='',
                avatar=''
            )
            return JsonResponse({'code': 200, 'msg': '注册成功!'})

        except Exception as e:
            return JsonResponse({'code': 500, 'msg': f'服务器错误{str(e)}'})
    else:
        return render(request, 'register.html')

def changeinfo(request):
    uid = request.session.get('uid')
    if request.method == 'POST':
        try:
            user = UserInfo.objects.get(id=uid)

            # 获取表单数据
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            youbian = request.POST.get('youbian')

            # 检查用户名是否已被其他用户使用
            if username and username != user.username:
                if UserInfo.objects.filter(username=username).exclude(id=uid).exists():
                    return render(request, 'changeInfo.html', {
                        'user': user,
                        'error': '用户名已被使用',
                        'success': None
                    })
                user.username = username

            # 检查邮箱是否已被其他用户使用
            if email and email != user.email:
                if UserInfo.objects.filter(email=email).exclude(id=uid).exists():
                    return render(request, 'changeInfo.html', {
                        'user': user,
                        'error': '邮箱已被使用',
                        'success': None
                    })
                user.email = email

            # 更新其他信息
            if phone is not None:
                user.uphone = phone
            if address is not None:
                user.uaddress = address
            if youbian is not None:
                user.uyoubian = youbian

            user.save()

            # 更新session中的用户名
            request.session['uname'] = user.username

            return render(request, 'changeInfo.html', {
                'user': user,
                'success': '个人信息更新成功',
                'error': None
            })

        except UserInfo.DoesNotExist:
            return render(request, 'changeInfo.html', {
                'error': '用户不存在',
                'success': None
            })
        except Exception as e:
            return render(request, 'changeInfo.html', {
                'error': f'服务器错误: {str(e)}',
                'success': None
            })
    else:
        # GET请求，显示个人信息
        try:
            user = UserInfo.objects.get(id=uid)
            return render(request, 'changeInfo.html', {
                'user': user,
                'success': None,
                'error': None
            })
        except UserInfo.DoesNotExist:
            return render(request, 'changeInfo.html', {
                'error': '用户不存在',
                'success': None
            })

def upload_avatar(request):
    """上传头像"""
    if request.method == 'POST':
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': 401, 'msg': '请先登录'})

        try:
            user = UserInfo.objects.get(id=uid)

            if 'avatar' not in request.FILES:
                return JsonResponse({'code': 400, 'msg': '请选择头像文件'})

            avatar_file = request.FILES['avatar']

            # 验证文件类型
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if avatar_file.content_type not in allowed_types:
                return JsonResponse({'code': 400, 'msg': '只支持JPEG、PNG、GIF、WEBP格式'})

            # 验证文件大小（最大2MB）
            if avatar_file.size > 2 * 1024 * 1024:
                return JsonResponse({'code': 400, 'msg': '图片大小不能超过2MB'})

            # 创建头像存储目录
            avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)

            # 生成文件名
            file_extension = os.path.splitext(avatar_file.name)[1]
            filename = f'avatar_{uid}_{int(timezone.now().timestamp())}{file_extension}'
            filepath = os.path.join(avatar_dir, filename)

            # 保存文件
            with open(filepath, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)

            # 更新用户头像路径（相对路径）
            avatar_url = f'/media/avatars/{filename}'
            user.avatar = avatar_url
            user.save()

            # 更新session中的头像
            request.session['avatar'] = avatar_url

            return JsonResponse({
                'code': 200,
                'msg': '头像上传成功',
                'avatar_url': avatar_url
            })

        except UserInfo.DoesNotExist:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': '服务器错误：' + str(e)})

    return JsonResponse({'code': 400, 'msg': '请求方法错误'})

def logout(request):
    request.session.clear()
    return redirect('user:login')