from django.shortcuts import render, redirect
from settings.settings import CLOUDINARY
from apps.admin.utils.decorator import access_required
from apps.public.models import Commission


@access_required('admin')
def commissions(request):
  commissions = Commission.objects.order_by('-created_at')

  context = {'commissions': commissions}
  return render(request, 'commissions/commissions.html', context)

@access_required('admin')
def commission(request, commission_id):
  # try:
    commission = Commission.objects.get(id=commission_id)

    context = {'commission':  commission,
               'CLOUDINARY':  CLOUDINARY}
    return render(request, 'commissions/commission.html', context)
  # except Exception as e:
  #   print str(e)
  #   return redirect('admin:commissions')