from . import views
from django .urls import path
app_name='shop'

urlpatterns=[
    # path('',views.index),
    path('',views.allproductcat,name='allproductcat'),
    path('<slug:c_slug>/',views.allproductcat,name='product_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/',views.prodetail,name='procatdetail')
]
