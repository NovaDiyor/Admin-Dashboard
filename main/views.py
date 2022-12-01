from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from django.core.mail import send_mail


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
    total = 0
    order = Order.objects.filter(status=3)
    for i in order:
        if i.bonus > 0:
            total += i.order_item.quantity * i.order_item.product.bonus
        elif i.bonus <= 0:
            total += i.order_item.quantity * i.order_item.product.price
    context = {
        'game': Game.objects.filter(status=3).order_by('-id')[:3],
        'playing': Game.objects.filter(status=2),
        'not': Game.objects.filter(status=1),
        'player': Player.objects.all().count(),
        'club': Club.objects.all().count(),
        'admin': User.objects.filter(status=2).count(),
        'product': Order.objects.filter(status=3).count(),
        'total': total
    }
    return render(request, 'dashboard.html', context)


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
        'club': Club.objects.all(),
        'league': League.objects.all()
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        league = request.POST.get('league')
        Club.objects.create(name=name, logo=logo, league_id=league)
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
        'table': Table.objects.all(),
        'statics': Statics.objects.all(),
        'league': League.objects.all()
    }
    if request.method == 'POST':
        league = request.POST.get('league')
        year = request.POST.get('year')
        statics = request.POST.getlist('statics')
        print(league, year, statics)
        t = Table.objects.create(league_id=league, year=year)
        for i in statics:
            t.statics.add(i)
        return redirect('table')
    return render(request, 'table.html', context)


@login_required(login_url='login')
def player_view(request):
    context = {
        'player': Player.objects.all(),
    }
    return render(request, 'player.html', context)


@login_required(login_url='login')
def game_view(request):
    context = {
        'game': Game.objects.all(),
    }
    return render(request, 'game.html', context)


@login_required(login_url='login')
def line_view(request):
    line = Line.objects.all()
    club = Club.objects.all()
    game = None
    players = None
    if request.method == 'POST':
        club_id = request.POST.get('club')
        game_id = request.POST.get('game_id')
        players_id = request.POST.getlist('players_id')
        if club is not None and club_id != '':
            club_post = Club.objects.get(id=club_id)
            players = Player.objects.filter(club=club_post, is_staff=False)
            game = Game.objects.filter(status=1, host=club_post)
            if game is None:
                game = Game.objects.filter(status=1, guest=club_post)
        if players_id is not None and players_id != '':
            if game_id is not None and game_id != '':
                t = Line.objects.create(club_id=club_id, game_id=game_id)
                for i in t:
                    t.team.add(i)
    context = {
        'line': line,
        'club': club,
        'game': game,
        'players': players
    }
    return render(request, 'line.html', context)


@login_required(login_url='login')
def passes_view(request):
    context = {
        'passes': Passes.objects.all()
    }
    return render(request, 'passes.html', context)


@login_required(login_url='login')
def subs_view(request):
    line = None
    game = None
    player = None
    club = Club.objects.all()
    if request.method == 'POST':
        line_id = request.POST.get('line')
        game_id = request.POST.get('game')
        player_id = request.POST.get('player')
        club_id = request.POST.get('club')
        minute = request.POST.get('minute')
        if club_id:
            club_p = Club.objects.get(id=club_id)
            player = Player.objects.filter(club_id=club_p, is_staff=False)
            game = Game.objects.filter(host_id=club_p, status=1)
            if game is None:
                game = Game.objects.filter(guest_id=club_p, status=1)
            ln = []
            for i in game:
                line = Line.objects.get(
                    club=club_p,
                    game=i
                )
                ln.append(line)
            # if line:
            #     ln = line.team.get(id=player_id)
            #     ln.team = player_id
            #     ln.save()
            # Substitute.objects.create(club=club_p, player=player, game_id=game_id, minute=minute, line_id=line_id)
    context = {
        'line': line,
        'game': game,
        'players': player,
        'club': club
    }
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
        img = request.FILES.get('img')
        is_img = request.POST.get('is-img')
        is_order = request.POST.get('is-order')
        if is_order is None:
            is_order = False
        if img is not None:
            Detail.objects.create(detail=detail, img=img, is_img=is_img, is_order=is_order)
        elif detail:
            if detail != ' ':
                Detail.objects.create(detail=detail, img=None, is_img=is_img, is_order=is_order)
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
        'telegram': Telegram.objects.all(),
        'chat': Chat.objects.all()
    }
    if request.method == 'POST':
        bot = request.POST.get('token')
        chat = request.POST.getlist('chat')
        t = Telegram.objects.create(bot_token=bot)
        for i in chat:
            t.chat.add(i)
        return redirect('telegram')
    return render(request, 'telegram.html', context)


@login_required(login_url='login')
def get_table(request, pk):
    table = Table.objects.get(id=pk)
    context = {
        'table': table.statics.all()
    }
    return render(request, 'get-table.html', context)


@login_required(login_url='login')
def get_line(request, pk):
    line = Line.objects.get(id=pk)
    context = {
        'line': line.team.all()
    }
    return render(request, 'get-line.html', context)


@login_required(login_url='login')
def get_detail(request, pk):
    detail = Product.objects.get(id=pk)
    context = {
        'detail': detail.info.all(),
    }
    return render(request, 'get-detail.html', context)


@login_required(login_url='login')
def get_image(request, pk):
    detail = Product.objects.get(id=pk)
    context = {
        'image': detail.image.all(),
    }
    return render(request, 'get-detail.html', context)


@login_required(login_url='login')
def get_chat(request, pk):
    chat = Telegram.objects.get(id=pk)
    context = {
        'chat': chat.chat.all(),
    }
    return render(request, 'get-chat.html', context)

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
        if is_video is None:
            is_video = False
        if is_news is None:
            is_news = False
        if is_top is None:
            is_top = False
        Report.objects.create(img=img, video=video, is_video=is_video, is_top=is_top, is_news=is_news, date=date, bio=bio, author=author)
        return redirect('add-report')
    return render(request, 'add-report.html')


@login_required(login_url='login')
def add_statics(request):
    context = {
        'club': Club.objects.all()
    }
    if request.method == 'POST':
        cb = request.POST.get('club')
        gm = request.POST.get('game')
        win = request.POST.get('win')
        draw = request.POST.get('draw')
        lose = request.POST.get('lose')
        score = request.POST.get('score')
        conceded = request.POST.get('conceded')
        point = 0
        club = Club.objects.get(id=cb)
        game = Game.objects.filter(status=3)
        if game:
            for i in game:
                if i.host == club:
                    if i.host_goal > i.guest_goal:
                        score += i.host_goal
                        conceded += i.guest_goal
                        point += 3
                    elif i.host_goal == i.guest_goal:
                        score += i.host_goal
                        conceded += i.guest_goal
                        point += 1
                    elif i.host_goal < i.guest_goal:
                        score += i.host_goal
                        conceded += i.guest_goal
                    else:
                        pass
                elif i.guest == club:
                    if i.guest_goal > i.host_goal:
                        score += i.guest_goal
                        conceded += i.host_goal
                        point += 3
                    elif i.host_goal == i.guest_goal:
                        score += i.guest_goal
                        conceded += i.host_goal
                        point += 1
                    elif i.guest_goal < i.host_goal:
                        score += i.guest_goal
                        conceded += i.host_goal
                    else:
                        pass
                else:
                    pass
        else:
            pass
        if int(win) > 0:
            for i in range(int(win)):
                point += 3
        if int(draw) > 0:
            for i in range(int(draw)):
                point += 1
        overall = int(win) + int(draw) + int(lose)
        print(gm, overall)
        if gm == str(overall):
            print(gm)
            Statics.objects.create(
                club_id=cb, game=gm, win=win,
                draw=draw, lose=lose, score=score,
                conceded=conceded, point=point)
            return redirect('add-statics')
        else:
            return redirect('statics')
    return render(request, 'add-statics.html', context)


@login_required(login_url='login')
def add_player(request):
    context = {
        'club': Club.objects.all()
    }
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
        if int(number) > 100:
            number = '99'
        Player.objects.create(
            club_id=club, name=name, l_name=l_name,
            number=number, position=position,
            is_staff=is_staff, birth=birth, img=img
        )
        return redirect('add-player')
    return render(request, 'add-player.html', context)


@login_required(login_url='login')
def add_game(request):
    context = {
        'club': Club.objects.all(),
    }
    if request.method == 'POST':
        date = request.POST.get('date')
        status = request.POST.get('status')
        guest = request.POST.get('guest')
        host = request.POST.get('host')
        if guest == host:
            pass
        else:
            Game.objects.create(
                date=date,
                status=status,
                host_id=host,
                guest_id=guest,
                host_goal=0,
                guest_goal=0,
            )
        return redirect('add-game')
    return render(request, 'add-game.html', context)


@login_required(login_url='login')
def add_passes(request):
    if request.method == 'POST':
        request = request.POST.get
        name = request('name')
        passes = request('pass')
        success = request('success')
        player = request('player')
        Passes.objects.create(
            all=passes, successful=success,
            name=name, player_id=player)
        return redirect('add-passes')
    context = {
        'player': Player.objects.all(),
    }
    return render(request, 'add-passes.html', context)


@login_required(login_url='login')
def add_product(request):
    context = {
        'detail': Detail.objects.filter(is_img=False),
        'img': Detail.objects.filter(is_img=True)
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        price = request.POST.get('price')
        bonus = request.POST.get('bonus')
        detail = request.POST.getlist('detail')
        img = request.POST.getlist('img')
        available = request.POST.get('available')
        if available is None:
            available = False
        p = Product.objects.create(
            name=name, bio=bio,
            price=price, bonus=bonus,
            available=available
        )
        for i in detail:
            p.info.add(i)
        for i in img:
            p.image.add(i)
        return redirect('add-product')
    return render(request, 'add-product.html', context)

# update objects


@login_required(login_url='login')
def update_info(request, pk):
    info = Info.objects.get(id=pk)
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        bio = request.POST.get('bio')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        insta = request.POST.get('insta')
        tg = request.POST.get('tg')
        fb = request.POST.get('fb')
        yt = request.POST.get('yt')
        tw = request.POST.get('tw')
        info.logo = logo
        info.bio = bio
        info.phone = phone
        info.email = email
        info.insta = insta
        info.tg = tg
        info.fb = fb
        info.yt = yt
        info.tw = tw
        info.save()
        return redirect('info')
    return render(request, 'update-info.html', {'info': Info.objects.get(id=pk)})


@login_required(login_url='login')
def update_ads(request, pk):
    context = {
        'ads': Ads.objects.get(id=pk)
    }
    ads = Ads.objects.get(id=pk)
    if request.method == 'POST':
        logo = request.FILES.get('logo')
        url = request.POST.get('url')
        ads.logo = logo
        ads.url = url
        ads.save()
        return redirect('ads')
    return render(request, 'update-ads.html', context)


@login_required(login_url='login')
def update_slider(request, pk):
    slider = Slider.objects.get(id=pk)
    if request.method == 'POST':
        img = request.FILES.get('img')
        title = request.POST.get('title')
        text = request.POST.get('text')
        slider.img = img
        slider.title = title
        slider.text = text
        slider.save()
        return redirect('slider')
    return render(request, 'update-slider.html', {'slider': Slider.objects.get(id=pk)})


@login_required(login_url='login')
def update_report(request, pk):
    report = Report.objects.get(id=pk)
    if request.method == 'POST':
        img = request.FILES.get('img')
        video = request.POST.get('video')
        is_video = request.POST.get('is-video')
        is_top = request.POST.get('is-top')
        is_news = request.POST.get('is-news')
        date = request.POST.get('date')
        bio = request.POST.get('bio')
        author = request.POST.get('author')
        report.video = video
        report.bio = bio
        report.author = author
        if is_video is None:
            is_video = False
        if is_top is None:
            is_top = False
        if is_news is None:
            is_news = False
        if date:
            report.date = date
        else:
            report.date = report.date
        if img:
            report.img = img
        else:
            report.img = report.img
        report.is_video = is_video
        report.is_top = is_top
        report.is_news = is_news
        report.save()
        return redirect('report')
    return render(request, 'update-report.html', {'report': Report.objects.get(id=pk)})


@login_required(login_url='login')
def update_league(request, pk):
    context = {
        'league': League.objects.get(id=pk)
    }
    league = League.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        league.name = name
        if logo:
            league.logo = logo
        else:
            league.logo = league.logo
        league.save()
        return redirect('league')
    return render(request, 'update-league.html', context)


@login_required(login_url='login')
def update_club(request, pk):
    context = {
        'club': Club.objects.get(id=pk),
        'league': League.objects.all(),
    }
    club = Club.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.POST.get('logo')
        league = request.POST.get('league')
        club.name = name
        if logo:
            club.logo = logo
        else:
            club.logo = club.logo
        club.league = league
        club.save()
        return redirect('club')
    return render(request, 'update-club.html', context)


@login_required(login_url='login')
def update_statics(request, pk):
    context = {
        'club': Club.objects.all(),
        'statics': Statics.objects.get(id=pk)
    }
    statics = Statics.objects.get(id=pk)
    if request.method == 'POST':
        request = request.POST.get
        club = request('club')
        game = request('game')
        win = request('win')
        draw = request('draw')
        lose = request('lose')
        score = request('score')
        conceded = request('conceded')
        point = request('point')
        print(win, draw, lose)
        print(int(win) + int(draw) + int(lose))
        overall = int(win) + int(draw) + int(lose)
        print(game, overall)
        if game == str(overall):
            statics.club_id = club
            statics.game = game
            statics.win = win
            statics.draw = draw
            statics.lose = lose
            statics.score = score
            statics.conceded = conceded
            point = 0
            if int(win) > 0:
                for i in range(int(win)):
                    point += 3
            if int(draw) > 0:
                for i in range(int(draw)):
                    point += 1
            statics.point = point
            statics.save()
            return redirect('statics')
    return render(request, 'update-statics.html', context)


@login_required(login_url='login')
def update_table(request, pk):
    context = {
        'league': League.objects.all(),
        'statics': Statics.objects.all(),
        'table': Table.objects.get(id=pk)
    }
    table = Table.objects.get(id=pk)
    if request.method == 'POST':
        league = request.POST.get('league')
        year = request.POST.get('year')
        statics = request.POST.getlist('statics')
        table.league_id = league
        table.year = year
        try:
            if statics == True:
                table.statics = table.statics
            else:
                for x in statics:
                    st = Statics.objects.get(id=x)
                    if st:
                        table.statics.add(st)
        except Exception as err:
            print(err)
        table.save()
        return redirect('table')
    return render(request, 'update-table.html', context)


@login_required(login_url='login')
def update_player(request, pk):
    player = Player.objects.get(id=pk)
    if request.method == 'POST':
        club = request.POST.get('club')
        name = request.POST.get('name')
        l_name = request.POST.get('l_name')
        number = request.POST.get('number')
        position = request.POST.get('position')
        is_staff = request.POST.get('is_staff')
        birth = request.POST.get('birth')
        img = request.POST.get('img')
        goals = request.POST.get('goals')
        player.club = club
        player.name = name
        player.l_name = l_name
        player.number = number
        player.position = position
        if is_staff is None:
            is_staff = False
        player.is_staff = is_staff
        player.birth = birth
        if img is None:
            player.img = player.img
        else:
            player.img = img
        if goals is None:
            goals = 0
        player.goals = goals
        player.save()
        return redirect('player')
    return render(request, 'update-player.html', {'player': Player.objects.get(id=pk)})


@login_required(login_url='login')
def update_game(request, pk):
    context = {
        'game': Game.objects.get(id=pk),
        'player': Player.objects.all()
    }
    game = Game.objects.get(id=pk)
    if request.method == 'POST':
        request = request.POST.get
        date = request('date')
        status = request('status')
        host = request('host')
        guest = request('guest')
        host_g = request('host-g')
        guest_g = request('guest-g')
        mvp = request('mvp')
        game.date = date
        game.status = status
        game.host_id = host
        game.guest_id = guest
        game.host_goal = host_g
        game.guest_goal = guest_g
        game.mvp = mvp
        game.save()
        if status == 3:
            line = Line.objects.filter(game_id=game)
            pl = line.team.all()
            for i in pl:
                i.minute += 90
                i.save()
        return redirect('game')
    return render(request, 'update-game.html', context)


@login_required(login_url='login')
def update_line(request, pk):
    line = Line.objects.get(id=pk)
    club = Club.objects.all()
    game = None
    players = None
    if request.method == 'POST':
        club_id = request.POST.get('club')
        game_id = request.POST.get('game')
        players_id = request.POST.getlist('players')
        if club is not None and club_id != '':
            club_post = Club.objects.get(id=club_id)
            players = Player.objects.filter(club=club_post, is_staff=False)
            game = Game.objects.filter(status=1, host=club_post)
            if game is None:
                game = Game.objects.filter(status=1, guest=club_post)
        if players_id is not None and players_id != '':
            if game_id is not None and game_id != '':
                line.club = club_id
                line.game = game_id
                for i in players_id:
                    o = Player.objects.get(id=i)
                    line.team.add(o)
                    return redirect('line')
    context = {
        'line': line,
        'club': club,
        'game': game,
        'players': players
    }
    return render(request, 'update-line.html', context)


@login_required(login_url='login')
def update_passes(request, pk):
    passes = Passes.objects.get(id=pk)
    if request.method == 'POST':
        all = request.POST.get('all')
        successful = request.POST.getlist('successful')
        percent = request.POST.get('percent')
        club = request.POST.get('club')
        game = request.POST.getlist('game')
        status = request.POST.getlist('status')
        passes.all = all
        passes.successful = successful
        passes.percent = percent
        passes.club = Club.objects.all(id=club)
        passes.game = Game.objects.all(id=game)
        passes.status = status
        passes.save()
        return redirect('passes')
    return render(request, 'update-passes.html', {'passes': Passes.objects.get(id=pk)})


@login_required(login_url='login')
def update_subs(request, pk):
    context = {
        'squad': Player.objects.all(),
        'game': Game.objects.all(),
        'line': Player.objects.all(),
        'subs': Substitute.objects.get(id=pk)
    }
    subs = Substitute.objects.get(id=pk)
    if request.method == 'POST':
        squad = request.POST.get('squad')
        game = request.POST.get('game')
        line = request.POST.get('line')
        minute = request.POST.get('minute')
        subs.squad = squad
        subs.game = game
        subs.line = line
        subs.minute = minute
        return redirect('subs')
    return render(request, 'update-subs.html', context)


@login_required(login_url='login')
def update_goal(request, pk):
    context = {
        'player': Player.objects.all(),
        'club': Club.objects.all(),
        'game': Game.objects.all(),
        'goal': Goal.objects.get(id=pk)
    }
    goal = Goal.objects.get(id=pk)
    if request.method == 'POST':
        minute = request.POST.get('minute')
        player = request.POST.get('player')
        club = request.POST.get('club')
        game = request.POST.get('game')
        goals = request.POST.get('goal')
        goal.minute = minute
        goal.player = player
        goal.club = club
        goal.game = game
        pl = Player.objects.get(id=player)
        cl = Club.objects.get(id=club)
        gm = Game.objects.get(id=game)
        st = Statics.objects.get(club_id=club)
        if pl.club == cl:
            if cl == gm.host:
                if goals == 'Fair':
                    goal.save()
                elif goals == 'Unfair':
                    pl.goal -= 1
                    st.score -= 1
                    gm.host_goal -= 1
                    goal.save()
                else:
                    return redirect('update-goal')
            elif cl == gm.guest:
                if goals == 'Fair':
                    goal.save()
                elif goals == 'Unfair':
                    pl.goal -= 1
                    st.score -= 1
                    gm.guest_goal -= 1
                    goal.save()
                else:
                    return redirect('update-goal')
            else:
                return redirect('update-goal')
        return redirect('goal')
    return render(request, 'update-goal.html', context)


@login_required(login_url='login')
def update_detail(request, pk):
    context = {
        'detail': Detail.objects.get(id=pk)
    }
    detail = Detail.objects.get(id=pk)
    if request.method == 'POST':
        details = request.POST.get('detail')
        img = request.FILES.get('img')
        is_img = request.POST.get('is_img')
        is_order = request.POST.get('is_order')
        detail.details = details
        if img is None:
            detail.img = detail.img
        else:
            detail.img = img
        if is_img is None:
            is_img = False
        if is_order is None:
            is_order = False
        detail.is_img = is_img
        detail.is_order = is_order
        detail.save()
        return redirect('detail')
    return render(request, 'update-detail.html', context)


@login_required(login_url='login')
def update_product(request, pk):
    pro = Product.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.getlist('bio')
        price = request.POST.get('price')
        bonus = request.POST.get('bonus')
        info = request.POST.getlist('detail')
        img = request.POST.getlist('img')
        available = request.POST.get('available')
        rating = request.POST.get('rating')
        pro.name = name
        pro.bio = bio
        pro.price = price
        pro.bonus = bonus
        if available is None:
            available = False
        pro.available = available
        pro.rating = rating
        pro.info.clear()
        for i in info:
            o = Detail.objects.get(id=i)
            pro.info.add(o)
        pro.image.clear()
        for i in img:
            o = Detail.objects.get(id=i)
            pro.image.add(o)
        pro.save()
        return redirect('product')
    context = {
        'product': pro,
        'detail': Detail.objects.filter(is_img=False),
        'img': Detail.objects.filter(is_img=True)
    }
    return render(request, 'update-product.html', context)


@login_required(login_url='login')
def update_chat(request, pk):
    context = {
        'chat': Chat.objects.get(id=pk)
    }
    chats = Chat.objects.get(id=pk)
    if request.method == 'POST':
        chat = request.POST.get('chat')
        chats.chat = chat
        chats.save()
        return redirect('chat')
    return render(request, 'update-chat.html', context)


@login_required(login_url='login')
def update_telegram(request, pk):
    context = {
        'telegram': Telegram.objects.get(id=pk),
        'chat': Chat.objects.all()
    }
    telegrams = Telegram.objects.get(id=pk)
    if request.method == 'POST':
        bot_token = request.POST.get('bot_token')
        chat = request.POST.getlist('chat')
        telegrams.bot_token = bot_token
        for i in chat:
            chats = Chat.objects.get(id=i)
            telegrams.chat.add(chats)
        telegrams.save()
        return redirect('telegram')
    return render(request, 'update-telegram.html', context)

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
    goal = Goal.objects.get(id=pk)
    goal.delete()
    return redirect('goal')


def delete_detail(request, pk):
    detail = Detail.objects.get(id=pk)
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

