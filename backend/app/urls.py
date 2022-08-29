from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),


    path('', views.IndexView.as_view()),
    path('test-list/', views.TestListAPI.as_view()),
    path('inventory/', views.InventoryAPI.as_view()),
    path('categories/', views.CategoriesAPI.as_view()),
    path('inventory/<int:pk>/', views.InventoryDetailAPI.as_view()),
    path('category/<int:pk>/', views.CategoryDetailAPI.as_view()),

    path('import-items-excel/', views.ImportItemsExcelAPI.as_view()),


    path('users/', views.UsersAPI.as_view()),
    path('users/<int:pk>/', views.UserDetailsAPI.as_view()),


    path('latest-rr-code/', views.LatestRRCodeAPI.as_view()),
    path('latest-adj-code/', views.LatestADCodeAPI.as_view()),
    path('latest-sales-code/', views.LatestSalesCodeAPI.as_view()),


    path('customers/', views.CustomersAPI.as_view()),
    path('customers/<int:pk>/', views.CustomerDetailsAPI.as_view()),
    path('import-customer-excel/', views.ImportCustomerExcelAPI.as_view()),
    path('suppliers/', views.SuppliersAPI.as_view()),
    path('suppliers/<int:pk>/', views.SupplierDetailsAPI.as_view()),
    path('import-supplier-excel/', views.ImportSupplierExcelAPI.as_view()),


    path('receiving-report/', views.ReceivingReportAPI.as_view()),
    path('adjustment/', views.AdjustmentAPI.as_view()),


    path('me/', views.MeAPI.as_view()),
    path('update-my-name/', views.UpdateMyNameAPI.as_view()),
    path('update-my-email/', views.UpdateMyEmailAPI.as_view()),
    path('update-my-password/', views.UpdateMyPasswordAPI.as_view()),

    path('sales/', views.SalesAPI.as_view()),
    path('sales/<int:pk>/', views.SalesDetailsAPI.as_view()),
    path('void-sales/<int:pk>/', views.VoidSalesAPI.as_view()),
    path('sales-for-the-month/', views.SalesForTheMonthAPI.as_view()),
    path('sales-for-the-day/', views.SalesForTheDayAPI.as_view()),
    path('low-quantity-products/', views.LowQuantityProductsAPI.as_view()),
    path('top-products/', views.TopProductsAPI.as_view()),
    path('sales-graph/', views.SalesGraphAPI.as_view()),
    path('sales-graph-void/', views.SalesGraphVoidedAPI.as_view()),
    path('business-profile/', views.BusinessAPI.as_view()),

    path('add-user/', views.AddUserAPI.as_view()),
    path('update-my-username/', views.ChangeUsernameAPI.as_view()),
]