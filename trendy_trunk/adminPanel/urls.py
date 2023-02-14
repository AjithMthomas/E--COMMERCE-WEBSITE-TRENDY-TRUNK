from django .urls import path
from . import views

# urls of adminPanel
urlpatterns = [
    # pages
    path('',views.adminPanel,name='adminPanel'),
    path('adminIndex',views.adminIndex,name='adminIndex'),
    path('adminUsers/',views.adminUsers,name='adminUsers'),
    path('adminProducts/',views.adminProducts,name='adminProducts'),
    path('adminSingleProduct/<int:id>/',views.adminSingleProduct,name='adminSingleProduct'),
    path('adminCategory/',views.adminCategory,name='adminCategory'),
    path('addProductPage/',views.addProductPage,name='addProductPage'),
    path('addCategoryPage/',views.addCategoryPage,name='addCategoryPage'),
    path('upadateCategory/<int:id>/',views.upadateCategory,name='upadateCategory'),
    path('updateProduct/<int:id>/',views.updateProduct,name='updateProduct'),
    path('adminOrders/',views.adminOrders,name='adminOrders'),
    path('invoice/<int:id>/',views.invoice,name='invoice'),
    

    

    # functions
    path('loginAdmin/',views.loginAdmin,name='loginAdmin'),
    path('logoutAdmin/',views.logoutAdmin,name='logoutAdmin'),
    path('deleteUser/<int:id>/',views.deleteUser,name='deleteUser' ),
    path('blockUser/<int:id>/<str:action>/',views.blockUser,name='blockUser'),
    path('list_unlistProduct/<int:id>/<str:action>/',views.list_unlistProduct,name='list_unlistProduct'),
    path('deleteSingleProdudct/<int:id>/',views.deleteSingleProdudct,name='deleteSingleProdudct'),
    path('deleteCategory/<int:id>/',views.deleteCategory,name='deleteCategory'),
    path('addProduct/',views.addProduct,name='addProduct'),
    path('addCategory/',views.addCategory,name='addCategory'),
    path('orderSearch/',views.orderSearch,name='orderSearch')

]
