from django.shortcuts import render
from django.conf import settings
import os
from django.http import JsonResponse
from tulip import tlp
from .tlp_json_converter import TlpJsonConverter

from documentation.models import Network

def loadGraph(request):
	# return list of all graphs the user can load
	if (request.method == "GET" and request.GET.get("network_name", None) != None):
		nameOfGraph = request.GET.get("network_name", None)
		networkFromDB = Network.objects.filter(network_name=nameOfGraph)[0]
		#print (networkFromDB.network_file.name)
		currentNetwork = tlp.loadGraph(os.path.join(settings.MEDIA_ROOT, networkFromDB.network_file.name))
		if currentNetwork is None:
			return JsonResponse({"success": False, "message": "File failed to load"})
		else:
			graphInJson = TlpJsonConverter.tlp_to_json(nameOfGraph, currentNetwork)
			return JsonResponse({"success": True, "data": graphInJson})
	return JsonResponse({"success": False, "message": "Define name and use GET"}) 

def deleteGraph(request):
	if (request.method == "POST" and request.POST.get("network_name", None) != None):
		nameOfGraph = request.POST.get("network_name", None)
		networkToDelete = Network.objects.filter(network_name=nameOfGraph)[0]

		if networkToDelete is None:
			return JsonResponse({"success": False, "message": "File failed to delete"})
		
		else:
			networkToDelete.network_file.delete()
			networkToDelete.delete()
			return JsonResponse({"success": True, "message": "File deleted"})

	return JsonResponse({"success": False, "message": "Define name and use POST"}) 



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