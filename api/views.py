from main.models import *
from rest_framework import authentication, permissions
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from bot.main import *


@api_view(['POST'])
def register(request):
    try:
        username = request.data['username']
        password = request.data['password']
        country = request.data['country']
        users = User.objects.create_user(username=username, password=password, country=country )
        token = Token.objects.create(user=users)
        data = {
            'username': username,
            'user_id': users.id,
            'token': token.key,
        }
        return Response(data)

    except Exception as err:
        return Response({'error': f'{err}'})


@api_view(['POST'])
def login(request):
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            usr = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                status = 200
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'username': username,
                    'user_id': usr.id,
                    'token': token.key,
                }
            else:
                status = 403
                message = 'Username Or Password Is Wrong!'
                data = {
                    'status': status,
                    'message': message,
                }
        except User.DoesNotExist:
            status = 404
            message = "This User Is Doesn't exist!"
            data = {
                'status': status,
                'message': message,
            }
        return Response(data)
    except Exception as er:
        return Response({"error": f'{er}'})


@api_view(['GET'])
def club_api(request):
    context = {
        'club': ClubOne(Club.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def news_api(request):
    news = News.objects.all().order_by('-date')
    context = {
        'news': NewOne(news, many=True).data
    }
    return Response(context)


@api_view(['GET'])
def video_api(request):
    report = Report.objects.all()
    for i in report:
        if i.video is not None:
            videos = i
    context = {
        'video': Report(videos, many=True).data
    }
    return Response(context)


@api_view(['GET'])
def product_api(request):
    context = {
        'product': ProductOne(Product.objects.all(), many=True).data,
        'available': ProductOne(Product.objects.filter(available=True), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def about_api(request):
    context = {
        'news': NewOne(News.objects.all()).data
    }
    return Response(context)


@api_view(['GET'])
def single_product(request, pk):
    context = {
        'single': ProductOne(Product.objects.get(id=pk)).data,
        'related': ProductOne(Product.objects.filter(rating=5), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def single_news(request, pk):
    context = {
        'news': NewOne(News.objects.get(id=pk)).data,
    }
    return Response(context)


@api_view(['GET'])
def single_report(request, pk):
    context = {
        'singe': ReportOne(Report.objects.get(id=pk)).data,
    }
    return Response(context)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_wishlist(request, pk):
    user = request.user
    product = request.POST.get('product')
    Wishlist.objects.create(user=user, product_id=product)
    return Response(f'{product} added to wishlist')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_item_create(request, pk):
    product = Product.objects.get(id=pk)
    quantity = request.POST.get('quantity')
    OrderItem.objects.create(product=product, quantity=quantity)
    return Response(f'{product} added to order')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def order_create(request):
    order = request.POST.getlist('order')
    user = request.user
    users = User.objects.get(id=user.id)
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    phone_number = request.POST.get('number')
    address = request.POST.get('address')
    postal_code = request.POST.get('postal')
    email = request.POST.get('email')
    region = request.POST.get('region')
    city = request.POST.get('city')
    create = Order.objects.create(
        user=users, name=name, l_name=surname,
        number=phone_number, address=address,
        postal=postal_code, email=email,
        region_id=region, city=city)
    for i in order:
        create.order_item.add(OrderItem.objects.get(id=i))
    tg = Telegram.objects.last()
    for i in tg.chat_id.all():
        if i.type == 0:
            send_message(tg.bot_token, i.chat_id, create.name, create.l_name, create.number, create.address, create.postal, create.email, create.region.name, create.city)
        else:
            pass
    return Response('Done, Our admins will message to you')


# @api_view(['GET'])
# def game_view(request):
#     context = {
#         'game': GameSerializer(Game.objects.all(), many=True).data,
#     }
#     return Response(context)


@api_view(['GET'])
def game_chart(request):
    game = 0
    won = 0
    draw = 0
    lose = 0
    scored = 0
    conceded = 0
    point = 0
    game = Game.objects.all()
    for i in game:
        if i.guest_goal > i.host_goal:
            game += 1
            won += 1
            scored += i.guest_goal
            conceded += i.host_goal
            point += 3
        elif i.guest_goal == i.host_goal:
            game += 1
            draw += 1
            scored += i.guest_goal
            conceded += i.host_goal
            point += 1
        elif i.guest_goal < i.host_goal:
            game += 1
            lose += 1
            scored += i.guest_goal
            conceded += i.host_goal
        context = {
            'game': game,
            'won': won,
            'draw': draw,
            'lose': lose,
            'score': scored,
            'conceded': conceded,
            'point': point,
        }
    return Response(context)



