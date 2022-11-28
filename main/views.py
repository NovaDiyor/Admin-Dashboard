from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *


def page_404(request):
    return render(request, 'page-404.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.count() > 0:
            usr = authenticate(username=username, password=password)
            if usr.status == 2:
                if usr is not None:
                    login(request, usr)
                    return redirect('dashboard')
                else:
                    return redirect('login')
            else:
                return redirect('login')
        else:
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def reset(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        new_password = request.POST.get('new-password')
        prove = request.POST.get('confirm-password')
        usr = authenticate(username=user.username, password=password)
        if new_password == prove:
            usr.username = username
            usr.set_password(new_password)
            usr.save()
            return redirect('dashboard')
        return redirect('reset')
    return render(request, 'reset-password.html', {'admin': user})


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html')


@login_required(login_url='login')
def info_view(request):
    context = {
        'info': Info.objects.all()
    }
    return render(request, 'info.html', context)


@login_required(login_url='login')
def report_view(request):
    context = {
        'report': Report.objects.all()
    }
    return render(request, 'report.html', context)


@login_required(login_url='login')
def ads_view(request):
    context = {
        'ads': Ads.objects.all()
    }
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        url = request.POST.get('url')
        Ads.objects.create(logo=logo, url=url)
        return redirect('ads')
    return render(request, 'ads.html', context)


@login_required(login_url='login')
def slider_view(request):
    context = {
        'slider': Slider.objects.all()
    }
    if request.method == 'POST':
        img = request.FILES.get('img')
        title = request.POST.get('title')
        text = request.POST.get('text')
        Slider.objects.create(img=img, title=title, text=text)
        return redirect('slider')
    return render(request, 'slider.html', context)


@login_required(login_url='login')
def league_view(request):
    context = {
        'league': League.objects.all()
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        League.objects.create(name=name, logo=logo)
        return redirect('league')
    return render(request, 'league.html', context)


@login_required(login_url='login')
def club_view(request):
    context = {
        'club': Club.objects.all()
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        league = request.POST.get('league')
        Club.objects.create(name=name, logo=logo, league=league)
        return redirect('club')
    return render(request, 'club.html', context)


@login_required(login_url='login')
def statics_view(request):
    context = {
        'statics': Statics.objects.all()
    }
    return render(request, 'statics.html', context)


@login_required(login_url='login')
def table_view(request):
    context = {
        'table': Table.objects.all()
    }
    if request.method == 'POST':
        league = request.POST.get('league')
        year = request.FILES.get('year')
        statics = request.POST.get('statics')
        Table.objects.create(league=league, year=year, statics=statics)
        return redirect('table')
    return render(request, 'table.html', context)


@login_required(login_url='login')
def player_view(request):
    context = {
        'player': Player.objects.alL(),
        'staff': Player.objects.filter(is_staff=True)
    }
    return render(request, 'player.html', context)


@login_required(login_url='login')
def game_view(request):
    context = {
        'game': Game.objects.alL(),
    }
    return render(request, 'player.html', context)


@login_required(login_url='login')
def line_view(request):
    context = {
        'line': Line.objects.all(),
        'club': Club.objects.all(),
        'team': Player.objects.all()
    }
    if request.method == 'POST':
        club = request.POST.get('club')
        team = request.POST.get('team')
        game = request.POST.get('game')
        w = Line.objects.create(club_id=club, game_id=game)
        for i in team:
            w.team.add(i)
        return redirect('line')
    return render(request, 'line.html', context)


@login_required(login_url='login')
def passes_view(request):
    context = {
        'passes': Passes.objects.all()
    }
    return render(request, 'passes.html', context)


@login_required(login_url='login')
def subs_view(request):
    context = {
        'squad': Player.objects.all(),
        'line': Line.objects.all()
    }
    if request.method == 'POST':
        request = request.POST.get
        squad = request('squad')
        line = request('line')
        game = request('game')
        minute = request('minute')
        Substitute.objects.create(squad_id=squad, game_id=game, line_id=line, minute=minute)
        return redirect('subs')
    return render(request, 'subs.html', context)


@login_required(login_url='login')
def goal_view(request):
    context = {
        'player': Player.objects.all(),
        'club': Club.objects.all(),
        'game': Game.objects.all(),
        'goal': Goal.objects.all()
    }
    if request.method == 'POST':
        request = request.POST.get
        minute = request('minute')
        club = request('club')
        player = request('player')
        game = request('game')
        pl = Player.objects.get(id=player)
        cl = Club.objects.get(id=club)
        gm = Game.objects.get(id=game)
        st = Statics.objects.get(club_id=club)
        if pl.club == cl:
            if cl == gm.host:
                pl.goal += 1
                st.score += 1
                gm.host += 1
            elif cl == gm.guest:
                pl.goal += 1
                st.score += 1
                gm.guest += 1
            else:
                return redirect('goal')
            Goal.objects.create(minute=minute, club_id=club, player_id=player, game_id=game)
            return redirect('goal')
        return redirect('goal')
    return render(request, 'goal.html', context)


@login_required(login_url='login')
def detail_view(request):
    context = {
        'detail': Detail.objects.all()
    }
    if request.method == 'POST':
        detail = request.POST.get('detail')
        img = request.POST.get('img')
        is_img = request.POST.get('is-img')
        Detail.objects.create(detail=detail, img=img, is_img=is_img)
        return redirect('detail')
    return render(request, 'detail.html', context)


@login_required(login_url='login')
def product_view(request):
    context = {
        'product': Product.objects.all()
    }
    return render(request, 'product.html', context)


@login_required(login_url='login')
def chat_view(request):
    context = {
        'chat': Chat.objects.all()
    }
    if request.method == 'POST':
        chat = request.POST.get('chat')
        Chat.objects.create(chat=chat)
        return redirect('chat')
    return render(request, 'chat.html', context)


@login_required(login_url='login')
def telegram_view(request):
    context = {
        'telegram': Telegram.objects.all()
    }
    if request.method == 'POST':
        bot = request.POST.get('token')
        chat = request.POST.getlist('chat')
        t = Telegram.objects.create(bot_token=bot)
        for i in chat:
            t.chat.add(i)
        return redirect('telegram')
    return render(request, 'telegram.html', context)

#  Koshish agar models di objectlari kop bosa koshishti ishlatdim


@login_required(login_url='login')
def add_info(request):
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        bio = request.POST.get('bio')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        insta = request.POST.get('insta')
        tg = request.POST.get('tg')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        Info.objects.create(
            logo=logo, bio=bio,
            phone=phone, email=email,
            insta=insta, tg=tg, fb=fb,
            yt=yt, tw=tw
        )
        return redirect('add-info')
    return render(request, 'add-info.html')


@login_required(login_url='login')
def add_report(request):
    if request.method == 'POST':
        img = request.FILES.get('img')
        video = request.FILES.get('video')
        is_video = request.POST.get('is-video')
        is_top = request.POST.get('is-top')
        is_news = request.POST.get('is-news')
        date = request.POST.get('date')
        bio = request.POST.get('bio')
        author = request.POST.get('author')
        Report.objects.create(img=img, video=video, is_video=is_video, is_top=is_top, is_news=is_news, date=date, bio=bio, author=author)
        return redirect('add-report')
    return render(request, 'add-report.html')


@login_required(login_url='login')
def add_statics(request):
    if request.method == 'POST':
        club = request.POST.get('club')
        game = request.POST.get('game')
        win = request.POST.get('win')
        draw = request.POST.get('draw')
        lose = request.POST.get('lose')
        score = request.POST.get('score')
        conceded = request.POST.get('conceded')
        point = request.POST.get('point')
        Statics.objects.create(
            club_id=club, game=game, win=win,
            draw=draw, lose=lose, score=score,
            conceded=conceded, point=point)
        return redirect('add-statics')
    return render(request, 'add-statics.html')


@login_required(login_url='login')
def add_player(request):
    if request.method == 'POST':
        club = request.POST.get('club')
        name = request.POST.get('name')
        l_name = request.POST.get('l-name')
        number = request.POST.get('number')
        position = request.POST.get('position')
        is_staff = request.POST.get('is-staff')
        birth = request.POST.get('birth')
        img = request.FILES.get('img')
        if is_staff is None:
            is_staff = False
        Player.objects.create(
            club=club, name=name, l_name=l_name,
            number=number, position=position,
            is_staff=is_staff, birth=birth, img=img
        )
        return redirect('add-player')
    return render(request, 'add-player.html')


@login_required(login_url='login')
def add_game(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        status = request.POST.get('status')
        guest = request.POST.get('h_goal')
        host = request.POST.get('passion')
        guest_goal = request.POST.get('kross')
        host_goal = request.POST.get('passes')
        mvp = request.POST.get('mvp')
        Game.objects.create(
            date=date,
            status=status,
            host_id=host,
            guest_id=guest,
            host_goal=host_goal,
            guest_goal=guest_goal,
            mvp_id=mvp
        )
        return redirect('add-game')
    return render(request, 'add-game.html')


@login_required(login_url='login')
def add_passes(request):
    context = {
        'club': Club.objects.all(),
        'game': Game.objects.all()
    }
    if request.method == 'POST':
        request = request.POST.get
        passes = request('pass')
        success = request('success')
        percent = request('percent')
        club = request('club')
        game = request('game')
        status = request('status')
        Passes.objects.create(
            all=passes, successful=success,
            percent=percent, club_id=club,
            game_id=game, status=status
        )
        return redirect('add-passes')
    return render(request, 'add-passes.html', context)


@login_required(login_url='login')
def add_product(request):
    context = {
        'detail': Detail.objects.all()
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        price = request.POST.get('price')
        bonus = request.POST.get('bonus')
        detail = request.POST.getlist('detail')
        available = request.POST.get('available')
        if available is None:
            available = False
        p = Product.objects.create(
            name=name, bio=bio,
            price=price, bonus=bonus,
            available=available
        )
        for i in detail:
            p.detail.add(i)
        return redirect('add-product')
    return render(request, 'add-product', context)

#  delete objects


def delete_info(request, pk):
    info = Info.objects.get(id=pk)
    info.delete()
    return redirect('info')


def delete_ads(request, pk):
    ads = Ads.objects.get(id=pk)
    ads.delete()
    return redirect('ads')


def delete_slider(request, pk):
    slider = Slider.objects.get(id=pk)
    slider.delete()
    return redirect('slider')


def delete_report(request, pk):
    report = Report.objects.get(id=pk)
    report.delete()
    return redirect('report')


def delete_league(request, pk):
    league = League.objects.get(id=pk)
    league.delete()
    return redirect('league')


def delete_club(request, pk):
    club = Club.objects.get(id=pk)
    club.delete()
    return redirect('club')


def delete_statics(request, pk):
    statics = Statics.objects.get(id=pk)
    statics.delete()
    return redirect('statics')


def delete_table(request, pk):
    table = Table.objects.get(id=pk)
    table.delete()
    return redirect('table')


def delete_player(request, pk):
    player = Player.objects.get(id=pk)
    player.delete()
    return redirect('player')


def delete_game(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    return redirect('game')


def delete_line(request, pk):
    line = Line.objects.get(id=pk)
    line.delete()
    return redirect('line')


def delete_passes(request, pk):
    passes = Passes.objects.get(id=pk)
    passes.delete()
    return redirect('passes')


def delete_subs(request, pk):
    subs = Substitute.objects.get(id=pk)
    subs.delete()
    return redirect('subs')


def delete_goal(request, pk):
    goal = Substitute.objects.get(id=pk)
    goal.delete()
    return redirect('goal')


def delete_detail(request, pk):
    detail = Substitute.objects.get(id=pk)
    detail.delete()
    return redirect('detail')


def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('product')


def delete_chat(request, pk):
    chat = Chat.objects.get(id=pk)
    chat.delete()
    return redirect('chat')


def delete_telegram(request, pk):
    telegram = Telegram.objects.get(id=pk)
    telegram.delete()
    return redirect('telegram')

