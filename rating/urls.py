from django.urls import path
from .views import MyBookedWorker, WorkerRatingView, CustomerRatingList, WorkerRatingList


app_name='rating'

urlpatterns =[
    path('my-boooked-worker', MyBookedWorker.as_view(), name='my-boooked-worker'),
    path('worker-rating/<int:pk>', WorkerRatingView.as_view(), name='worker-rating'),
    path('customer-rating-list', CustomerRatingList.as_view(), name='customer-rating-list'),
    path('<int:pk>/worker-rating-list', WorkerRatingList.as_view(), name='worker-rating-list'),
    # path('worker-save', RatingSave, name='worker-save'),
    # path('post-worker-review', PostWorkerReview, name='post-worker-review'),
]