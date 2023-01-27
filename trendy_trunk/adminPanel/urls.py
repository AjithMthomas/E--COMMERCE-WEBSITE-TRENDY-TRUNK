from django .urls import path
from . import views

# urls of adminPanel
urlpatterns = [
    path('',views.adminPanel,name='adminPanel'),
    path('loginAdmin/',views.loginAdmin,name='loginAdmin'),
    path('adminIndex',views.adminIndex,name='adminIndex'),
    path('logoutAdmin/',views.logoutAdmin,name='logoutAdmin'),
    path('adminUsers/',views.adminUsers,name='adminUsers'),
    path('deleteUser/<int:id>/',views.deleteUser,name='deleteUser' ),
    path('blockUser/<int:id>/<str:action>/',views.blockUser,name='blockUser')
    

]
