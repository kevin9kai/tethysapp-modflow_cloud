from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse
from json import dump

from pyproj import Proj, transform #Remember to install this in tethys.byu.edu


import os

from xmltodict import parse

from hs_restclient import HydroShare

from tethys_sdk.gizmos import *

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    context = {}

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
    hs = HydroShare()
    res_info_list = []
    i =0

    for resource in hs.getResourceList(types=['MODFLOWModelInstanceResource']):
        xml = hs.getScienceMetadata(resource['resource_id'])
        print "iteration number"
        print i
        dict = parse(xml)
        #takes xml turns into string then json dictionary object ^
        try:
            box = dict['rdf:RDF']['rdf:Description'][0]['dc:coverage'][1]['dcterms:box']['rdf:value']
            #['rdf:Description'][0]['dc:coverage'][0]['dcterms:box']['rdf:value']
            # ^From the dictionary I pull out the values I need or the data from the "coverage" part of the model
            list_points = box.split('; ')
            # ^ splits up box to produce a list containing: northlimit, eastlimit, southlimit, westlimit, units
            #   and porjection.
            temp_dict = {} #creates an empty dictionary
            for l in list_points:
                temp_list = l.split('=') # splits up the list even further into name and value ex: northlimit, 40.5033
                # print temp_list
                temp_dict[temp_list[0]] = temp_list[1]
            res_info = {}
            res_info["resource_id"]=resource['resource_id']
            res_info["box"]=temp_dict
            res_info_list.append(res_info)
            print res_info


        except Exception, e:
            pass
        try:
            box = dict['rdf:RDF']['rdf:Description'][0]['dc:coverage'][0]['dcterms:box']['rdf:value']
            # ['rdf:Description'][0]['dc:coverage'][0]['dcterms:box']['rdf:value']
            # ^From the dictionary I pull out the values I need or the data from the "coverage" part of the model
            list_points = box.split('; ')
            # ^ splits up box to produce a list containing: northlimit, eastlimit, southlimit, westlimit, units
            #   and porjection.
            temp_dict = {}  # creates an empty dictionary
            for l in list_points:
                temp_list = l.split('=')  # splits up the list even further into name and value ex: northlimit, 40.5033
                # print temp_list
                temp_dict[temp_list[0]] = temp_list[1]
            res_info = {}
            res_info["resource_id"] = resource['resource_id']
            res_info["box"] = temp_dict
            res_info_list.append(res_info)
            print res_info

        except Exception, e:
            pass
        i += 1


    print "length of line"
    print len(res_info_list)
    print "These are the MODFLOW models"
    i=0
    while i< len(res_info_list):
        print res_info_list[i]["resource_id"]
        print res_info_list[i]["box"]["name"]
        print res_info_list[i]["box"]["projection"]
        print res_info_list[i]["box"]["northlimit"]
        print res_info_list[i]["box"]["southlimit"]
        print res_info_list[i]["box"]["eastlimit"]
        print res_info_list[i]["box"]["westlimit"]

    # print "This the entire list"
    # print res_info_list

    # Define GeoJSON layer
    ymax = float(res_info_list[0]["box"]["northlimit"])
    ymin = float(res_info_list[0]["box"]["southlimit"])
    xmax = float(res_info_list[0]["box"]["eastlimit"])
    xmin = float(res_info_list[0]["box"]["westlimit"])
    # Changing the projection for each value
    inProj = Proj(init='epsg:4326')
    outProj = Proj(init='epsg:3857')
    xmax, ymax = transform(inProj, outProj, xmax, ymax)
    xmin, ymin = transform(inProj, outProj, xmin, ymin)

    #gets the projection
    # projection = res_info_list[0]["box"]["projection"]  # returns 'WGS 84 EPSG:4326'
    # geojson_proj = projection.split(' ',2) # returns 'EPSG:4326'

    #Random point in Utah Lake
    ran_pt = [-111.80992, 40.19461]
    ran_pt = transform(inProj, outProj, ran_pt[0], ran_pt[1])

    #this is a list of all the coordinates and their values
    ymax_coor = []
    ymin_coor = []
    xmax_coor = []
    xmin_coor = []
    # this is a list of the shapes to be made
    # this loop will pull out all the coordiantes
    len_res_list = len(res_info_list)
    print "length of res_info_list: %d" % len_res_list


    features = []
    i=0
    print i
    while i < len_res_list:
        ymax_coor=(res_info_list[i]["box"]["northlimit"])
        ymin_coor=(res_info_list[i]["box"]["southlimit"])
        xmax_coor=(res_info_list[i]["box"]["eastlimit"])
        xmin_coor=(res_info_list[i]["box"]["westlimit"])
        top_right = transform(inProj, outProj, xmax_coor, ymax_coor)
        top_left = transform(inProj, outProj, xmax_coor, ymin_coor)
        bot_right = transform(inProj, outProj, xmin_coor, ymax_coor)
        bot_left = transform(inProj, outProj, xmin_coor, ymin_coor)
        features.append({
            'type': 'Feature',  # This produces the box
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[top_right, bot_right, bot_left, top_left]]
            }
        })
        i += 1

    #creates a random point for the map
    addpoint = {
        'type': 'Feature', # Just a test of a random point in Utah Lake
        'geometry': {
            'type': 'Point',
            'coordinates': ran_pt
        }
    }

    #adds the point to the list of features
    features.append(addpoint)

    # The correct shape
    geojson_object = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:3857'
                # 3857
            }
        },
        'features': features
    }

    #This one the first test and it works
    # shapes = {
    #     'type': 'FeatureCollection',
    #     'crs': {
    #         'type': 'name',
    #         'properties': {
    #             'name': 'EPSG:3857'
    #             #3857
    #         }
    #     },
    #     'features': [
    #         # for cooridnates in res_info_list[cooridnates]:
    #         {
    #             'type': 'Feature', # Just a test of a random point in Utah Lake
    #             'geometry': {
    #                 'type': 'Point',
    #                 'coordinates': ran_pt
    #             }
    #         },
    #         {
    #             'type': 'Feature',
    #             'geometry': {
    #                 'type': 'Point',
    #                 'coordinates': [xmax, ymax]
    #             }
    #         },
    #         {
    #             'type': 'Feature',# This produces the box
    #             'geometry': {
    #                 'type': 'Polygon',
    #                 'coordinates': [[[xmax, ymax], [xmin, ymax], [xmin, ymin], [xmax, ymin]]]
    #             }
    #         }
    #
    #     ]
    # }


    # geojson_object.append(features)

    #using gizmo configure the map
    viewoptions = MVView(
        projection = 'EPSG:4326', #webmercator proejction
        center = [-111.649, 40.247],
        zoom = '10',
        )
    geojson_layer = MVLayer(source='GeoJSON',
        options=geojson_object,
        legend_title='Test GeoJSON',
        legend_extent=[-300, -300, 200, 200],
        legend_classes=[
            MVLegendClass('polygon', 'Polygons', fill='rgba(255,255,255,0.8)', stroke='#3d9dcd'),
        ])
    map_view_options = MapView(
        height = '700px', #fix this one so it's conituingly growing
        width = '100%',
        controls = ['ZoomSlider', 'Rotate', 'FullScreen',
                  {'MousePosition': {'projection': 'EPSG:4326'}},
                  {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-130, 22, -65, 54]}}],
        layers=[geojson_layer],
        view = viewoptions,
        basemap='OpenStreetMap',
    )
#
    context = {'map_view_options': map_view_options, "res_info_list": res_info_list}

    return render(request, 'modflow_cloud/map.html', context)

def data(request):
    """
    Controller for the app home page.
    """
    # html = 'base html string'
    table = '<table style="width:100%">' \
           '<tr>' \
           '    <th colspan="3">Title</th>' \
           '</tr>' \
           '<tr>' \
           '    <td>Author</td>' \
           '<tr style="border-bottom:1px solid black"><td colspan="100%"></td>' \
           '<td><br></td>' \
           '</table>' \

    hs = HydroShare()
    temp = []
    for resource in hs.getResourceList(types=['MODFLOWModelInstanceResource']):
        # for each resource, extract values you want and append them to your html

        temp.append(resource['resource_id'])

        table += '<table style = "width:100%">'\
                 '</tr>' \
                 '<tr:nth-child(even) {' \
                 '  background-color: #33ccff;}>' \
                 '  <th colspan="3">'+resource['resource_title']+'</th>' \
                 '</tr>' \
                 '<tr>' \
                 '  <td>'+resource['creator']+'</td>' \
                 '</tr>' \
                 '<tr>' \
                 '  <td>'+resource['resource_id']+'</td>' \
                 '<tr>' \
                 '  <th>Model Data:</th>' \
                 '  <th>Date Last updated:</th>'\
                 '</tr>' \
                 '<tr>' \
                 '  <td><button type="button" onclick="download_hs_res(' + "'" +resource['resource_id'] + "'" + ')">Download Files</button></td>' \
                 '  <td>'+resource['date_last_updated']+'</td>' \
                 '<tr style="border-bottom:1px solid black"><td colspan="100%"></td>' \
                 '<td><br></td>' \
        #html += '<tr>' \
         #       '   <th>creator</th>' \
          #      '   <th>creator'
        # string in the format they need to be
        # html += '<tr><td>' + resource['creator'] + '</td>

        '''
        # Button explained

        Explination for the button
        The button's attribute is onclick, and it's value is download_hs_res(...between " "
        The value in the attribute is a function: download_hs_res
        The parameters for the function are: ' + "'" +resource['resource_id'] + "'" + '
        So when button is clicked on it will go to data.js and use the function.
            This function in particular calls for a function in the download-hs-res url
            This goes to app.py and uses the download_hs_res which is in the
            controllers.py
        '''


        print resource['creator']
        table += '</tr>'
        # print(resource)
    # after your loop, make sure to append to the html string variable the closing html tags
    # i.e. html += '</table>'

    context = {
        #'html': '<div><b>Hello World, It works!</b></div>',
        'html': table,

        #'temp': temp
        #'test': 1,
    }

    return render(request, 'modflow_cloud/data.html', context)

def temp(request):
    print request, '22222222222222222222222222222222222222'
    #hs.getResource(, destination='/tmp', unzip=True)
    return render(request)

def download_hs_res(resquest):
    # get the value of para my_res_id from the url
    res_id = resquest.GET['my_res_id']

    # download the hydroshare res from hydroshare server to tethys server
    hs = HydroShare()
    hs.getResource(res_id, destination='/tmp')

    # return the res stored on tethys server to frontend/client
    response = HttpResponse(open("/tmp/{0}.zip".format(res_id), 'rb').read(), content_type='application/zip')
    #{0} is the place from the .format.
    #rb is readable binary
    response['Content-Disposition'] = "attachment; filename={0}.zip".format(res_id)
    #This tells you what type of files it is
    response['Content-Length'] = os.path.getsize('/tmp/{0}.zip'.format(res_id))
#   So this line helps the browser know how large the file is and calculate time.
    return response
