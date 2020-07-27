from management.models import Doctors, verifycode

def add_variable_to_context(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:

            request.session.clear_expired()
            context = { 

                'verify': True

            }
            return context
        else:
            test = verifycode.objects.get(user_id=request.user.id)

            request.session.clear_expired()
            if Doctors.objects.filter(username=request.user.username).exists():

                ab = Doctors.objects.get(username= request.user.username)
                context = { 
                    'image': ab,
                    'verify': test.verified

                }
            else:
                context = { 

                    'verify': test.verified

                }

            return context
    else:
        return {}