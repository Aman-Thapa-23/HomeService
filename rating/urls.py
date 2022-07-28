from django.urls import path
from .views import MyBookedWorker


app_name='rating'

urlpatterns =[
    path('my-boooked-worker', MyBookedWorker.as_view(), name='my-boooked-worker'),
    # path('<int:pk>/worker-rating', WorkerRatingView, name='worker-rating'),
    # path('post-worker-review', PostWorkerReview, name='post-worker-review'),
]