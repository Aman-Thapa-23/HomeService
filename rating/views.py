from email import message
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from service.models import Booking
from .models import ReviewWorker
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.models import WorkerCategory, Worker, CustomUser
from django.core.serializers import serialize
from .forms import ReviewWorkerForm
from django.contrib import messages
# Create your views here.



@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class MyBookedWorker(View, LoginRequiredMixin):
    def get(self, request):
        my_booked_workers = Booking.objects.filter(customer=request.user).order_by('-booking_date')
        context = {
            'my_booked_workers': my_booked_workers,
        }
        return render(request, 'rating/my_booked_user.html', context)  


@method_decorator(login_required(login_url='/authentication/login'), name='dispatch')
class WorkerRatingView(View, LoginRequiredMixin):
    def get(self, request, pk):
        worker = Booking.objects.filter(worker__user__id=self.kwargs['pk']).first()
        form = ReviewWorkerForm(instance=worker)
        context = {
            'worker':worker,
            'form':form,
        }
        return render(request, 'rating/worker_rating_new.html', context)
        # return render(request, 'rating/worker_rating.html', context)

    def post(self, request, pk):
        worker = Booking.objects.filter(worker__user__id=self.kwargs['pk']).first()
        rate = request.POST['rating']
        comment = request.POST['review']
        print(rate)
        ReviewWorker.objects.create(worker=worker.worker, customer=request.user, rate=rate, comment=comment)
        print('redirect not working')
        messages.success(request, f'Successfully rated {rate} star')
        return redirect("dashboard")
# worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
#     customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     comment = models.TextField('Review',max_length=300)
#     rate = models.IntegerField(default=0, validators=[
#         MaxValueValidator(5),
#         MinValueValidator(0)
#     ])

        # form = ReviewWorkerForm(request.POST, instance=worker)
        # if form.is_valid():
        #     print("here")
        #     reviewform = form.save(commit=False)
        #     reviewform.customer=request.user
        #     reviewform.worker= worker
        #     reviewform.rate = rate
        #     reviewform.save()
        #     return JsonResponse({'success':'true', 'rate': rate}, safe=False)
        # return JsonResponse({'success':'false'})

# def RatingSave(self, request):
#         # worker = Booking.objects.filter(worker__user__id=self.kwargs['pk']).first()
#         # form = ReviewWorkerForm( request.POST, instance=worker)
#         # if form.is_valid():
#         #     comment= form.cleaned_data['comment']
#         #     rate= form.cleaned_data['rate']
#         #     form = ReviewWorker.objects.create(
#         #         customer=request.user,
#         #         worker=worker,
#         #         comment=comment,
#         #         rate=rate
#         #     )
#         #     data={
#         #         'user':request.user.name,
#         #         'review_text':request.POST['review_text'],
#         #         'review_rating':request.POST['review_rating']
#         #     }
#         #     return JsonResponse({'bool':True, 'data':data})
#     if request.method =="POST":
#         worker = Booking.objects.filter(worker__user__id=self.kwargs['pk']).first()
#         rate = request.POST.get('rate')
#         comment = request.POST.get('comment')
#         form = ReviewWorker.objects.create(
#             customer=request.user,
#             worker=worker,
#             comment = comment,
#             rate=rate
#         )
#         form.save()
#         return JsonResponse({'success':'true', 'rate': rate}, safe=False)
#     return JsonResponse({'success':'false'})



class CustomerRatingList(View):
    def get(self, request):
        review = ReviewWorker.objects.filter(customer=request.user)
        context = {
            'review':review
        }
        return render(request, 'rating/customer_rating_list.html', context)


class WorkerRatingList(View):
    def get(self, request, pk):
        worker = Worker.objects.get(user__pk=pk)
        review = ReviewWorker.objects.filter(worker=worker)
        context = {
            'review':review
        }
        return render(request, 'rating/worker_rating_list.html', context)