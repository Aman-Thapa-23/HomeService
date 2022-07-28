from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from service.models import Booking
from .models import ReviewWorker
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.models import WorkerCategory, Worker, CustomUser
from django.core.serializers import serialize
# Create your views here.



@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class MyBookedWorker(View):
    def get(self, request):
        my_booked_workers = Booking.objects.filter(customer=request.user).order_by('-booking_date')
        context = {
            'my_booked_workers': my_booked_workers,
        }
        return render(request, 'rating/my_booked_user.html', context)  


# @login_required
# def WorkerRatingView(request, pk):
#     worker = Worker.objects.get(user__pk=pk)
#     review = ReviewWorker.objects.filter(worker = worker)
   
#     serialized_data = serialize("json", review)
#     context = {
#         'reviews':  review,
#         'rating': serialized_data,
#         'pk': pk,
#         }

#     return render(request, 'rating/worker_rating.html', context)


# @login_required
# def PostWorkerReview(request):
#     data = request.POST
#     id = data['id']
#     worker = Worker.objects.get(id = id)

#     rating =  ReviewWorker.objects.create(
#         customer = request.user,
#         worker = worker,
#         rate = data['rating'],
#         comment = data['message']
#     )
#     rating.save()
#     return JsonResponse({'id': id}, safe=False )