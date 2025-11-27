from django.urls import path
from journalist import views, update_profile, post_management

urlpatterns = [
    path('sign-up/', views.Journalist_Sign_Up, name='sign-up'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('get-states/', views.get_states, name='get_states'),
    path('check-email-exists/', views.check_email_exists, name='check-email-exists'),
    path("send-otp-signup", views.Send_OTP_Signup, name="send-otp-signup"),
    path("verify-otp-signup/", views.Verify_OTP_Signup, name="verify-otp-signup"),
    path('sign-in', views.Journalist_SignIn, name='sign-in'),
    path('forgot-password', views.Journalist_Forgot_Password, name='forgot-password'),
    path('reset-password/<str:token>/', views.Journalist_Reset_Password, name='Journalist-reset-password'),
    
    path('dashboard', views.Journalist_Dashboard, name='dashboard'),
    path('profile', views.Journalist_Profile, name='profile'),

    path('logout-user', views.logout_view, name='logout-user'),

    path('update/profile', update_profile.UpdateProfile, name='update_profile'),
    path('update/profile/pic', update_profile.UpdateProfilePic, name='update_profile_pic'),
    path('update/banner/pic', update_profile.UpdateBannerPic, name='update_banner_pic'),
    path('update/address', update_profile.UpdateAddress, name='update_address'),
    path('update/strength', update_profile.UpdateStrength, name='update_strength'),
    path('update/equipment', update_profile.UpdateEquipment, name='update_equipment'),
    path('update/social_media', update_profile.UpdateSocialMedia, name='update_social_media'),

    path('news-post', post_management.Journalist_News_Post, name='news-post'),
    path('manage-post', post_management.Journalist_Manage_Post, name='manage-post'),
    path('edit-post/<int:post_id>', post_management.Journalist_Edit_News_Post, name='edit-post'),
    path('journalist-update-post', post_management.JournalistUpdatePost, name="journalist-update-post"),
    path('gallery-post/', post_management.GalleryPost, name='gallery_post'),
    path('delete-gallery/<int:pk>/', post_management.delete_gallery_image, name='delete_gallery'),

    path('add-artist', post_management.AddArtist, name="add_artist"),

    path('video-post', post_management.Journalist_video_Post, name='video-post'),
    path('manage-video-post', post_management.Journalist_Manage_Video_Post, name='manage-video-post'),
    path('edit-video-post/<int:post_id>', post_management.Journalist_Edit_Video_Post, name='edit-video-post'),
    path('journalist-update-video-post', post_management.JournalistUpdateVideoPost, name="journalist-update-video-post"),
]