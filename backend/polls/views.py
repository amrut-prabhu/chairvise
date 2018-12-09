# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

import json

from utils import returnTestChartData
from insightMaker import getSingleFileInsights, getMultipleFileInsights

# Create your views here.
# Note: a view is a func taking the HTTP request and returns something accordingly


def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")


def test(request):
	return HttpResponse("<h1>This is the very first HTTP request!</h1>")


# Note: csr: cross site request, adding this to enable request from localhost
@csrf_exempt
def uploadCSV(request):
	print "Inside the upload function"
	mappings = json.loads(request.POST['mappings'])

	if request.FILES:
		csvFiles = request.FILES.getlist('file')
		insights = []

		if len(csvFiles) == 1:  # Single file insights
			try:
				insights = getSingleFileInsights(csvFiles[0], mappings)
			except Exception as inst:
				print "Exception: ", inst.args
				HttpResponseNotFound(inst.args)
				pass
		elif len(csvFiles) > 1:  # Multiple files insights
			try:
				insights = getMultipleFileInsights(csvFiles, mappings)
			except Exception as inst:
				print "Exception: ", inst.args
				HttpResponseNotFound(inst.args)
				pass
		else:
			print "No files uploaded"
			return HttpResponseNotFound('Cannot generate insights as no files were uploaded')
		
		if request.POST:
			# current problem: request from axios not recognized as POST
			print "Now we got the csv file"
		return HttpResponse(json.dumps(insights))
	else:
		print "Did not find the file(s)!"
		return HttpResponseNotFound('Page not found for CSV')
