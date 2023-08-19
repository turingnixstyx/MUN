from django.shortcuts import render,redirect
from django.http import HttpResponseServerError

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            print(type(response.status_code))

            if response.status_code == 403:
                return redirect("login")
            
            elif response.status_code // 100 in [4, 5]:
                print(response)
                return render(request, 'error.html', status=500)

        except Exception as e:
            return render(request, 'error.html', status=500)
        return response
    
    def process_exception(self, request, exception):
        print("Inside process_exception!")
        print (exception.__class__.__name__)
        print (exception.message)
        return render(request, 'error.html', status=500)