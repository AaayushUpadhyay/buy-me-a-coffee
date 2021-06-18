from django.shortcuts import render
import razorpay
from .models import Coffee
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    if request.method=="POST":
        name=request.POST.get("name")
        price=int(request.POST.get("price"))*100
        client=razorpay.Client(auth=("rzp_test_daHPr4QhX1TJ4V","xyxpeNlfNMDktLHfBkpGx75W"))
        payment=client.order.create({'amount':price, 'currency':"INR",'payment_capture':'1'})
        print(payment)
        coffee=Coffee(name=name,amount=price,payment_id=payment['id'])
        coffee.save()
        return render(request,'bmac/home.html',{'payment':payment})
    return render(request,'bmac/home.html')
@csrf_exempt
def success(request):
    data=dict()
    if request.method=="POST":
        a=request.POST.get('razorpay_order_id')
        data['razorpay_order_id']=a
        data['razorpay_payment_id']=request.POST.get('razorpay_payment_id')
        data['razorpay_signature']=request.POST.get('razorpay_signature')
        user=Coffee.objects.filter(payment_id=a).first()
        client=razorpay.Client(auth=("rzp_test_daHPr4QhX1TJ4V","xyxpeNlfNMDktLHfBkpGx75W"))
        check=client.utility.verify_payment_signature(data)
        if check:
            return render(request,'bmac/error.html')

        user.paid=True
        user.save()
    return render(request,'bmac/success.html')