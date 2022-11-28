from main.models import *
from rest_framework import authentication
from django.contrib.auth import login, logout, authenticate
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from bot.main import *

# login


@api_view(['POST'])
def register(request):
    try:
        username = request.data['username']
        password = request.data['password']
        number = request.data.get('number')
        email = request.data.get('email')
        users = User.objects.create_user(username=username, password=password, number=number, email=email, status=2)
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
def login_api(request):
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            usr = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
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


@api_view(['POST'])
def logout_api(request):
    logout(request)
    return Response('You logout!')

# Models Get


@api_view(['GET'])
def user_api(request):
    try:
        user = User.objects.all()
        usr = UserOne(user, many=True).data
        data = {
            'users': usr
        }
        return Response(data)
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['GET'])
def info_api(request):
    context = {
        'info': InfoOne(Info.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def ads_api(request):
    context = {
        'our advertisers': AdsOne(Ads.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def slider_api(request):
    context = {
        'slider': SliderOne(Slider.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def report_api(request):
    context = {
        'report': ReportOne(Report.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def video_api(request):
    video = Report.objects.filter(is_video=True)
    context = {
        'video': ReportOne(video, many=True).data
    }
    return Response(context)


@api_view(['GET'])
def news_api(request):
    context = {
        'news': NewOne(Report.objects.filter(is_news=True), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def league_api(request):
    context = {
        'league': LeagueOne(League.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def club_api(request):
    context = {
        'club': ClubOne(Club.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def player_api(request):
    context = {
        'player': PlayerOne(Player.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def staff_api(request):
    context = {
        'staff': StaffOne(Player.objects.filter(is_staff=True), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def game_api(request):
    context = {
        'game': GameOne(Game.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def subs_api(request):
    context = {
        'substitute': SubOne(Substitute.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def line_api(request):
    context = {
        'line': LineOne(Line.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def goal_api(request):
    context = {
        'goal': GoalOne(Goal.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def passes_api(request):
    context = {
        'passes': PassOne(Passes.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def statics_api(request):
    context = {
        'static': StaticOne(Statics.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def table_api(request):
    context = {
        'table': TableOne(Table.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def detail_api(request):
    context = {
        'detail': DetailOne(Detail.objects.all(), many=True).data
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
def wishlist_api(request):
    context = {
        'wishlist': WishlistOne(Wishlist.objects.all(), many=True).data
    }
    return Response(context)


@api_view(['GET'])
def order_item_api(request):
    context = {
        'order-item': OrderItemOne(OrderItem.objects.all()).data
    }
    return Response(context)


@api_view(['GET'])
def order_api(request):
    context = {
        'order': OrderOne(Order.objects.all()).data
    }
    return Response(context)


@api_view(['GET'])
def chat_api(request):
    context = {
        'chat': ChatOne(Chat.objects.all()).data
    }
    return Response(context)


@api_view(['GET'])
def telegram_api(request):
    context = {
        'telegram': TelegramOne(Telegram.objects.all()).data
    }
    return Response(context)

# single


@api_view(['GET'])
def single_user(request, pk):
    user = User.objects.get(id=pk)
    context = {
        'single': UserOne(user).data,
    }
    return Response(context)


@api_view(['GET'])
def single_report(request, pk):
    context = {
        'single': ReportOne(Report.objects.get(id=pk)).data,
    }
    return Response(context)


@api_view(['GET'])
def single_video(request, pk):
    context = {
        'single': ReportOne(Report.objects.get(id=pk, is_video=True)).data,
    }
    return Response(context)


@api_view(['GET'])
def single_news(request, pk):
    context = {
        'single': NewOne(Report.objects.get(id=pk)).data,
    }
    return Response(context)


@api_view(['GET'])
def single_table(request, pk):
    table = Table.objects.get(id=pk)
    statics = table.statics.all()
    tl = []
    try:
        league = {
            'name': table.league.name,
            'year': table.year,
        }
        print(league)
        for i in statics:
            context = {
                'club': i.club.name,
                'game': i.game,
                'win': i.win,
                'draw': i.draw,
                'lose': i.lose,
                'score': i.score,
                'conceded': i.conceded,
                'point': i.point
            }
            tl.append(context)
        data = {
            'table': league,
            'stats': tl
        }
        print(tl, data, context)
        return Response(data)
    except Exception as err:
        return Response(f'err: {err}')


@api_view(['GET'])
def single_player(request, pk):
    context = {
        'single': PlayerOne(Player.objects.get(id=pk)).data,
    }
    return Response(context)


@api_view(['GET'])
def single_game(request, pk):
    context = {
        'single': GameOne(Game.objects.get(id=pk)).data,
    }
    return Response(context)


@api_view(['GET'])
def single_product(request, pk):
    product = Product.objects.get(id=pk)
    context = {
        'single': ProductOne(product).data,
        'related': ProductOne(Product.objects.filter(rating=product.rating), many=True).data
    }
    return Response(context)

# add


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_wishlist(request):
    user = request.user
    product = request.POST.get('product')
    Wishlist.objects.create(user=user, product_id=product)
    return Response(f'{product} added to wishlist')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_order_item(request):
    product = request.POST.get('product')
    quantity = request.POST.get('quantity')
    OrderItem.objects.create(product_id=product, quantity=quantity)
    pro = Product.objects.get(id=product)
    return Response(f'{pro} added to order')


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_order(request):
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
