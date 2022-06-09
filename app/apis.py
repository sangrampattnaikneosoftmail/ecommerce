from .models import Coupon
from django.http import JsonResponse

def apply_coupon(request,code):
    cpn = Coupon.objects.filter(code=code).first()
    if not cpn:
        return JsonResponse({"status": "success","msg": "coupon not found"}, status=400)
    if not cpn.is_active:
        return JsonResponse({"status": "success","msg": "coupon is not active"},status=400)

    return JsonResponse(
        {
            "status": 'success',
            "msg": "coupon applied",
            "amount": cpn.discount_amount
        }
    )
        

