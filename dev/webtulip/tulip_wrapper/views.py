from django.shortcuts import render
from django.conf import settings
import os
from django.http import HttpResponse
from tulip import tlp
from .tlp_json_converter import TlpJsonConverter

from documentation.models import Network

def loadGraph(request):

	# return list of all graphs the user can load
	if (request.method == "GET" and request.GET.get("name", None) != None):
		nameOfGraph = request.GET.get("name", None)
		networkFromDB = Network.objects.filter(name=nameOfGraph)[0]
		print (networkFromDB.network.name)
		currentNetwork = tlp.loadGraph(os.path.join(settings.MEDIA_ROOT,networkFromDB.network.name))

		graphInJson = TlpJsonConverter.tlp_to_json(nameOfGraph, currentNetwork)

		return HttpResponse(graphInJson, content_type="application/json")

# def saveGraph(request):

# 	# overwrites if no parameter, saves to new file if file name given
# 	print (request)
# 	return JsonResponse({'graph':'saved'})

# def importGraph(request):

# 	# user uploads / points to graph and gives it a name etc.
# 	print (request)
# 	return JsonResponse({'graph':'import'})

# def exportGraph(request):

# 	# export a graph to a file
# 	print (request)
# 	return JsonResponse({'graph':'export'})