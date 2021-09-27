


from video.models import *

from accounts.models import *

import datetime



def subscription_checker(request):
    if SubscriptionHistory.objects.filter(user = request.user , subscription_end_date__gte= datetime.datetime.today()).first():
        return True
    return False