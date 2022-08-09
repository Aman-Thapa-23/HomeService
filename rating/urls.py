from django.urls import path
from .views import MyBookedWorker, WorkerRatingView


app_name='rating'

urlpatterns =[
    path('my-boooked-worker', MyBookedWorker.as_view(), name='my-boooked-worker'),
    path('worker-rating/<int:pk>', WorkerRatingView.as_view(), name='worker-rating'),
    # path('worker-save', RatingSave, name='worker-save'),
    # path('post-worker-review', PostWorkerReview, name='post-worker-review'),
]