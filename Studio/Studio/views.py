from django.http import JsonResponse
from Projet_Page.models import DataInfo
from Home_Page.models import ProjectInfo
from django.contrib.auth.models import User
def DataRead(request,Project):
    if request.user.is_authenticated:
        name = request.user.username
        user = User.objects.get(username=name)
        getproject = ProjectInfo.objects.get(user=user,project=Project)
        getValue = request.GET.get('q')
        AllData=getproject.Entrys.filter(name__istartswith=getValue)
        UniqueData=[]
        seen_name=set()
        for item in AllData:
            if item.name not in seen_name:
                UniqueData.append(item.name)
            seen_name.add(item.name)
        return JsonResponse(list(UniqueData),safe=False)
