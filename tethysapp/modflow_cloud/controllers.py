from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hs_restclient import HydroShare, HydroShareAuthOAuth2


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    a = ["1","2","3"]
    print a, "888888888888888888888888888888888"
    context = {"a": a}

    return render(request, 'modflow_cloud/home.html', context)
def info(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'modflow_cloud/info.html', context)
def map(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'modflow_cloud/map.html', context)
def data(request):
    """
    Controller for the app home page.
    """
    # html = 'base html string'
    table = '<table style="width:100%">' \
           '<tr>' \
           '    <th>Title</th>' \
           '    <th>Author</th>' \

    hs = HydroShare()
    for resource in hs.getResourceList(types=['MODFLOWModelInstanceResource']):
        # for each resource, extract values you want and append them to your html
        add_title = resource['resource_title']
        add_author =resource['creator']
        table += '</tr>' \
                 '<tr>' \
                 '  <th>'+add_title+'</th>' \
                 '  <th>'+add_author+'</th>' \
        #html += '<tr>' \
         #       '   <th>creator</th>' \
          #      '   <th>creator'
        # string in the format they need to be
        # html += '<tr><td>' + resource['creator'] + '</td>
        print resource['creator']
        table += '</tr>'
        # print(resource)
    # after your loop, make sure to append to the html string variable the closing html tags
    # i.e. html += '</table>'

    context = {
        #'html': '<div><b>Hello World, It works!</b></div>',
        'html': table
        #'test': 1,
    }

    return render(request, 'modflow_cloud/data.html', context)