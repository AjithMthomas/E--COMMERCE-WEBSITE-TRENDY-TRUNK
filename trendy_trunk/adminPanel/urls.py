from django .urls import path
from . import views

# urls of adminPanel
urlpatterns = [
    # pages
    path('',views.adminPanel,name='adminPanel'),
    path('adminIndex',views.adminIndex,name='adminIndex'),
    path('adminUsers/',views.adminUsers,name='adminUsers'),
    path('adminProducts/',views.adminProducts,name='adminProducts'),


    # functions
    path('loginAdmin/',views.loginAdmin,name='loginAdmin'),
    path('logoutAdmin/',views.logoutAdmin,name='logoutAdmin'),
    path('deleteUser/<int:id>/',views.deleteUser,name='deleteUser' ),
    path('blockUser/<int:id>/<str:action>/',views.blockUser,name='blockUser'),
    path('list_unlistProduct/<int:id>/<str:action>/',views.list_unlistProduct,name='list_unlistProduct')
   

    

]
