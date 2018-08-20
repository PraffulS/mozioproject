# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.http import *
from providers.models import providers, serviceAreas
import json
from shapely.geometry import shape, Point


@csrf_exempt
def deleteProvider(request):
	try:
		if request.GET.get('providerId'):
			providerId = request.GET.get('providerId')
			providerObj = providers.objects.filter(id=providerId)
			if providerObj:
				providerObj.delete()
				return HttpResponse('Deleted')
			else:
				return HttpResponse('Provider doesn\'t exists')
		else:
			return HttpResponse('Please provide provider Id')

	except Exception as e:
		return HttpResponse('Some problem occured - '+str(e))

@csrf_exempt
def updateProvider(request):
	try:
		providerId = request.GET.get('providerId')
		obj = json.loads(request.body)
		print providerId
		providerObj = providers.objects.get(id=providerId)
		if providerObj:
			if 'providerName' in obj:
				providerObj.providerName = obj['providerName']
			if 'providerEmail' in obj:
				providerObj.providerEmail = obj['providerEmail']
			if 'providerNo' in obj:
				providerObj.providerNo = obj['providerNo']
			if 'providerLanguage' in obj:
				providerObj.providerLanguage = obj['providerLanguage']
			if 'providerCurrency' in obj:
				providerObj.providerCurrency = obj['providerCurrency']
			providerObj.save()
			return HttpResponse('Updated successfully')

		else:
			return HttpResponse('Provider doesn\'t exists')
	except providers.DoesNotExist:
		return HttpResponse('Some problem occured ')

@csrf_exempt
def getProviders(request):
	try:
		if request.GET.get('providerId'):
			providerId = request.GET.get('providerId')
			providerObj = providers.objects.filter(id=providerId)
			if providerObj:
				return JsonResponse({'providerName':providerObj[0].providerName,'providerEmail':providerObj[0].providerEmail,'providerNo':providerObj[0].providerNo,'providerLanguage':providerObj[0].providerLanguage,'providerCurrency':providerObj[0].providerCurrency })
			else:
				return HttpResponse('Provider doesn\'t exists')
		else:
			providerObjs = providers.objects.all()
			obj = []
			for providerObj in providerObjs:
				dict1 = {'id':providerObj.id,'providerName':providerObj.providerName,'providerEmail':providerObj.providerEmail,'providerNo':providerObj.providerNo,'providerLanguage':providerObj.providerLanguage,'providerCurrency':providerObj.providerCurrency }
				obj.append(dict1)
			return JsonResponse({'result':obj})

	except Exception as e:
		return HttpResponse('Some problem occured '+str(e))


@csrf_exempt
def createProvider(request):
	try:
		obj = json.loads(request.body)
		providerObj = providers(providerName=obj['providerName'],
								providerEmail=obj['providerEmail'],
								providerNo=obj['providerNo'],
								providerLanguage=obj['providerLanguage'],
								providerCurrency=obj['providerCurrency'])
		providerObj.save()
		return HttpResponse('Provider added successfully with id '+str(providerObj.id))

	except Exception as e:
		print e
		return HttpResponse('Some problem occured '+str(e))



@csrf_exempt
def createServiceArea(request):
	try:
		obj = json.loads(request.body)
		providersObj = providers.objects.filter(id=obj['forProviderId'])
		if not providersObj:
			return HttpResponse('Please provider correct provider Id or create a new provider')
		else:
			flag=0
			if 'serviceArea' in obj:
				serviceArea = obj['serviceArea']
				flag=0
				if 'geometry' in serviceArea:
					if 'type' in serviceArea['geometry'] and 'coordinates' in serviceArea['geometry']:
						flag=1
					else:
						flag=0
						return HttpResponse('Please provide type and coordinates attributes')
				else:
					return HttpResponse('Please provide geomtery')
				if 'properties' in serviceArea:
					if 'Name' in serviceArea['properties'] and 'Price' in serviceArea['properties']:
						flag=1
					else:
						flag=0
						return HttpResponse('Please provide name and price attributes')
				else:
					return HttpResponse('Please provide properties attribute')
				if flag==1:
					serviceAreasObj = serviceAreas(forProviderId_id=obj['forProviderId'],
												   name=serviceArea['properties']['Name'],
												   price=serviceArea['properties']['Price'],
												   geometry=json.dumps(serviceArea['geometry']))
					serviceAreasObj.save()
					return HttpResponse('Added successfully')
				else:
					return HttpResponse('Please provide geometry attribute')
			else:
				return HttpResponse('There is no use of this API if you don\'t provider service area')
	except Exception as e:
		return HttpResponse('Some problem occured. '+str(e))


@csrf_exempt
def getServiceAreas(request):
	try:
		if request.GET.get('providerId'):
			providerId = request.GET.get('providerId')
			providerObj = providers.objects.filter(id=providerId)
			if providerObj:
				serviceAreasObj = serviceAreas.objects.filter(forProviderId_id=providerId)
				if serviceAreasObj:
					obj = []
					for serviceArea in serviceAreasObj:
						dict1 = {'name':serviceArea.name, 'price':serviceArea.price, 'geometry':serviceArea.geometry}
						obj.append(dict1)
					return JsonResponse({'result':obj})
				else:
					return HttpResponse('No service areas defined for given provider')

			else:
				return HttpResponse('Provider doesn\'t exists')
		else:
			return HttpResponse('Please provide provider Id')

	except Exception as e:
		return HttpResponse('Some problem occured '+str(e))

@csrf_exempt
def deleteServiceArea(request):
	try:
		if request.GET.get('serviceAreaId'):
			serviceAreaId = request.GET.get('serviceAreaId')
			serviceAreasObj = serviceAreas.objects.filter(id=serviceAreaId)
			if serviceAreasObj:
				serviceAreasObj.delete()
				return HttpResponse('Deleted')
			else:
				return HttpResponse('Service Area doesn\'t exists')
		else:
			return HttpResponse('Please provide Service Area Id')

	except Exception as e:
		return HttpResponse('Some problem occured - '+str(e))

@csrf_exempt
def updateServiceArea(request):
	try:
		serviceAreaId = request.GET.get('serviceAreaId')
		obj = json.loads(request.body)
		serviceAreaObj = serviceAreas.objects.get(id=serviceAreaId)
		if serviceAreaObj:
			if 'name' in obj:
				serviceAreaObj.name = obj["name"]
			if 'price' in obj:
				serviceAreaObj.price = obj["price"]
			if 'geometry' in obj:
				geometry = {}
				if obj["geometry"]["coordinates"]:
					geometry["coordinates"] = obj["geometry"]["coordinates"]
				if obj["geometry"]["type"]:
					geometry["type"] = obj["geometry"]["type"]
				serviceAreaObj.geometry = json.dumps(geometry)
			serviceAreaObj.save()
			return HttpResponse('Updated successfully')
		else:
			return HttpResponse('Service Area doesn\'t exists')
	except serviceAreas.DoesNotExist:
		return HttpResponse('Service Area doesn\'t exists')
	except Exception as e:
		return HttpResponse('Some problem occured '+str(e))


@csrf_exempt
def findServiceAreas(request):
	try:
		obj = json.loads(request.body)
		latitude = obj['latitude']
		longitude = obj['longitude']
		point = Point(latitude,longitude)
		geometryObjs = serviceAreas.objects.all().order_by('forProviderId').prefetch_related('forProviderId')
		result = []
		for i in  geometryObjs:
			print i.geometry
			polygon = shape(json.loads(i.geometry))
			print polygon
			if polygon.contains(point):
				dict1 = {'serviceAreaName': i.name, 'serviceAreaPrice': i.price, 'ProviderName': i.forProviderId.providerName}
				result.append(dict1)
		return JsonResponse({'result':result})
	except Exception as e:
		return HttpResponse('Some problem occured '+str(e))

