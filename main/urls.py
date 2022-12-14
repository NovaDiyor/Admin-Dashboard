from django.urls import path
from .views import *

urlpatterns = [
    path('', page_404, name='page-404'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset-password/', reset, name='reset'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('info/', info_view, name='info'),
    path('ads/', ads_view, name='ads'),
    path('slider/', slider_view, name='slider'),
    path('report/', report_view, name='report'),
    path('league/', league_view, name='league'),
    path('club/', club_view, name='club'),
    path('statics/', statics_view, name='statics'),
    path('table/', table_view, name='table'),
    path('player/', player_view, name='player'),
    path('game/', game_view, name='game'),
    path('line/', line_view, name='line'),
    path('passes/', passes_view, name='passes'),
    path('subs/', subs_view, name='subs'),
    path('goal/', goal_view, name='goal'),
    path('detail/', detail_view, name='detail'),
    path('product/', product_view, name='product'),
    path('chat/', chat_view, name='chat'),
    path('telegram/', telegram_view, name='telegram'),
    path('info/add/', add_info, name='add-info'),
    path('report/add/', add_report, name='add-report'),
    path('statics/add/', add_statics, name='add-statics'),
    path('player/add/', add_player, name='add-player'),
    path('game/add/', add_game, name='add-game'),
    path('subs/add/', add_subs, name='add-subs'),
    path('passes/add/', add_passes, name='add-passes'),
    path('product/add/', add_product, name='add-product'),
    path('table/get/<int:pk>/', get_table, name='get-table'),
    path('line/get/<int:pk>/', get_line, name='get-line'),
    path('detail/get/<int:pk>/', get_detail, name='get-detail'),
    path('image/get/<int:pk>/', get_image, name='get-image'),
    path('chat/get/<int:pk>/', get_chat, name='get-chat'),
    path('info/update/<int:pk>/', update_info, name='update-info'),
    path('ads/update/<int:pk>/', update_ads, name='update-ads'),
    path('slider/update/<int:pk>/', update_slider, name='update-slider'),
    path('report/update/<int:pk>/', update_report, name='update-report'),
    path('league/update/<int:pk>/', update_league, name='update-league'),
    path('club/update/<int:pk>/', update_club, name='update-club'),
    path('statics/update/<int:pk>/', update_statics, name='update-statics'),
    path('table/update/<int:pk>/', update_table, name='update-table'),
    path('player/update/<int:pk>/', update_player, name='update-player'),
    path('game/update/<int:pk>/', update_game, name='update-game'),
    path('line/update/<int:pk>/', update_line, name='update-line'),
    path('passes/update/<int:pk>/', update_passes, name='update-passes'),
    path('substitute/update/<int:pk>/', update_subs, name='update-subs'),
    path('goal/update/<int:pk>/', update_goal, name='update-goal'),
    path('detail/update/<int:pk>/', update_detail, name='update-detail'),
    path('product/update/<int:pk>/', update_product, name='update-product'),
    path('chat/update/<int:pk>/', update_chat, name='update-chat'),
    path('telegram/update/<int:pk>/', update_telegram, name='update-telegram'),
    path('info/delete/<int:pk>/', delete_info, name='delete-info'),
    path('ads/delete/<int:pk>/', delete_ads, name='delete-ads'),
    path('slider/delete/<int:pk>/', delete_slider, name='delete-slider'),
    path('report/delete/<int:pk>/', delete_report, name='delete-report'),
    path('league/delete/<int:pk>/', delete_league, name='delete-league'),
    path('club/delete/<int:pk>/', delete_club, name='delete-club'),
    path('statics/delete/<int:pk>/', delete_statics, name='delete-statics'),
    path('table/delete/<int:pk>/', delete_table, name='delete-table'),
    path('player/delete/<int:pk>/', delete_player, name='delete-player'),
    path('passes/delete/<int:pk>/', delete_passes, name='delete-passes'),
    path('game/delete/<int:pk>/', delete_game, name='delete-game'),
    path('line/delete/<int:pk>/', delete_line, name='delete-line'),
    path('subs/delete/<int:pk>/', delete_subs, name='delete-subs'),
    path('goal/delete/<int:pk>/', delete_goal, name='delete-goal'),
    path('detail/delete/<int:pk>/', delete_detail, name='delete-detail'),
    path('product/delete/<int:pk>/', delete_product, name='delete-product'),
    path('chat/delete/<int:pk>/', delete_chat, name='delete-chat'),
    path('telegram/delete/<int:pk>/', delete_telegram, name='delete-telegram'),
]
