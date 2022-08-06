from django.urls import path
from users import views

urlpatterns = [
    path('auth/signup/', views.UserSignUpView.as_view(), ),
    path('auth/email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('auth/login/',views.UserLoginView.as_view(),),

    path('auth/request-reset-email/', views.RequestPasswordResetEmail.as_view(),name="request-reset-email"), #Manda al email que quiere restablecer la contraseña
    path('auth/password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'), #A traves del link, se mandaran lque se ha validado las credenciales y se enviara el token
    path('auth/password-reset-complete/', views.SetNewPasswordAPIView.as_view(),name='password-reset-complete'), #Pide los datos proporcionados en la url anterior, como uidb64, token y password
     
    path('auth/password-change-confirm/', views.ChangeNewPasswordAPIView.as_view(), name="password-change-confirm"), 
]