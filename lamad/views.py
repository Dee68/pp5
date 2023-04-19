from django.shortcuts import render


def page_not_found_view(request, exception):
    '''
        This function shows a customized 404 error page
    '''
    return render(request, 'errors/404.html', status=404)


def internal_server_error(request):
    '''
        This function shows a customized 500 error page
    '''
    return render(request, 'errors/500.html', status=500)
