from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from lib.web_interface import create_task, create_map, get_formatted_map
from lib.interface import CallExternalException
from maps.models import Task
#import thread
import time
import json
import pygraphviz
from time import strftime
import networkx as nx
from networkx.readwrite import json_graph
from networkx.drawing import nx_agraph

def index(request):
	return render(request, 'maps/index.html')

def test(request):
	return render(request, 'maps/sphericalTest.html')

def description(request):
	return render(request, 'description.html')

def datasets(request):
	return render(request, 'datasets.html')

def about(request):
	return render(request, 'about.html')

def recent(request):
	map_list = []

	debug = request.GET.get('debug', 'false')
	page = int(request.GET.get('page', '0'))
	items_per_page = 30
	start = items_per_page*page
	end = start + items_per_page

	for task in Task.objects.order_by('-id')[start:end]:
		obj = {}
		obj['id'] = task.id
		obj['link'] = '/map/' + str(task.id)
		if len(task.input_dot) < 75:
			obj['dot'] = task.input_dot
		else:
			obj['dot'] = task.input_dot[:75] + '...'
		obj['dot_link'] = '/map/' + str(task.id) + '/input_dot'
		obj['date'] = task.creation_date
		obj['ip'] = task.creation_ip
		obj['status'] = task.status
		obj['status_link'] = '/map/' + str(task.id) + '/input_desc'
		obj['delete_link'] = '/delete_map/' + str(task.id)
		map_list.append(obj)
	return render(request, 'maps/recent.html', {'map_list': map_list, 'debug': debug})


def request_map(request):
	log.debug(f"request_map called with method: {request.method}")
	if request.method == 'POST':
		try:
			#log.debug(f"POST data: {dict(request.POST.items())}")
			task = create_task(dict(request.POST.items()), request.META.get('REMOTE_ADDR', ''))
			log.debug(f"Task created with ID: {task.id if hasattr(task, 'id') else 'unknown'}")
			try:
				import threading
				log.debug(f"Starting create_map thread for task ID: {task.id if hasattr(task, 'id') else 'unknown'}")
				threading.Thread(target=create_map,
				    args=(task,1),
				).start()
			except Exception as e:
				log.error(f"Thread start error: {str(e)}")
				print ('thread-error: ' + str(e))
			return redirect('/map/' + str(task.id) + '/')
		except CallExternalException as e:
			log.error(f"CallExternalException: {str(e)}")
			return render(request, 'maps/error.html', {'msg': str("<br />".join(str(e).split("\n")))})
		log.debug(f"Task creation and threading completed for task ID: {task.id if hasattr(task, 'id') else 'unknown'}")
		return redirect('/map/' + str(task.id) + '/')
	log.debug("request_map did not process POST request")
	return render(request, 'maps/error.html', {'msg': 'Invalid request method.'})

MIME_TYPES = {
    'pdf': 'application/pdf',
    'ps':  'application/postscript',
    'eps': 'application/postscript',
    'png': 'image/png',
    'gif': 'image/gif',
    'jpg': 'image/jpeg',
    'svg': 'image/svg+xml',
    'dot': 'text/plain',
    'gv':  'text/plain',
}

def display_map(request, task_id, format = ''):
	if request.method == 'GET':
		task = get_object_safe(task_id, 10)
		print("I am trying to display map")

		if format == '':
			# if task.layout_algorithm == 'SGD':
			# 	return render(request,'maps/SGD_display.html',{'task':task})
			# elif task.layout_algorithm == 'neato':
			# 	return render(request,'maps/hyperbolic.html',{'task':task})
			# return render(request, 'maps/hyperbolic.html',{'task': task});
			# if task.contiguous_algorithm == 'true':
			# 	return render(request, 'maps/spherical.html', {'task': task})
			# elif task.hyperbolic_projection == 'true':
			# 	return render(request, 'maps/hyperbolic.html',{'task': task})
			print("task is printed")
			print(task.json_metadata())
			return render(request, 'maps/map.html', {'task': task})
		else:
			if format in MIME_TYPES:
				content = get_formatted_map(task, format)
				return HttpResponse(content, content_type = MIME_TYPES[format])
			elif format == 'input_dot':
				return HttpResponse(task.input_dot, 'text/plain')
			elif format == 'input_desc':
				return HttpResponse(task.description(), 'text/plain')

def get_json(request, task_id):
	if request.method == 'GET':
		task = Task.objects.get(id = task_id)
		#print(task.description())
		dot_graph = nx_agraph.from_agraph(pygraphviz.AGraph(task.dot_rep))
		print(task.dot_rep)
		graph_json = json.dumps(json_graph.node_link_data(dot_graph))
		# graph_json = json.dumps(task.dot_rep)

		return HttpResponse(graph_json, content_type='application/json')

#def get_adjacency_matrix(request, task_id):
#	if request.method == 'POST':
#		task = Task.objects.get(id = task_id)
#		print dot_to_adjacency_matrix(pygraphviz.AGraph(task.dot_rep))

#def get_mds(request):
#	return HttpResponse(json.dumps(testMDS()), content_type='application/json')

def get_task_metadata(request, task_id):
	if request.method == "GET":
		task = Task.objects.get(id=task_id)
		print(task.json_metadata())
		return HttpResponse(task.json_metadata(), content_type='application/json')

def get_map(request, task_id):
	if request.method == 'GET':
		print(task_id)
		task = Task.objects.get(id = task_id)
		return HttpResponse(u'%s' % task.svg_rep, content_type="image/svg+xml")

import logging
log = logging.getLogger('gmap_web')

def get_map_zoomed(request, task_id):
    if request.method == 'GET':
        log.debug(f"get_map_zoomed called for task_id={task_id}")
        zoom = request.GET.get('zoom', '3')
        log.debug(f"Requested zoom level: {zoom}")
        task = get_object_safe(task_id, 10)
        svg = None
        if zoom == '0':
            svg = getattr(task, 'svg_rep0', None)
        elif zoom == '1':
            svg = getattr(task, 'svg_rep1', None)
        elif zoom == '2':
            svg = getattr(task, 'svg_rep2', None)
        elif zoom == '3':
            svg = getattr(task, 'svg_rep3', None)
        log.debug(f"SVG for zoom {zoom}: {'set' if svg else 'not set'}; length: {len(svg) if svg else 0}")
        if not svg:
            log.warning(f"No SVG found for zoom {zoom}, returning empty SVG.")
            # Return a minimal valid SVG if missing, to avoid XML parsing errors
            return HttpResponse('<svg xmlns="http://www.w3.org/2000/svg"></svg>', content_type="image/svg+xml")
        return HttpResponse(svg, content_type="image/svg+xml")

def get_object_safe(task_id, attempt):
	if attempt <= 0:
		return get_object_or_404(Task, id = task_id)

	try:
		task = get_object_or_404(Task, id = task_id)
		return task
	except Exception as e:
		if type(e).__name__ != 'OperationalError':
			raise e
		print (type(e).__name__ + ': ' + str(e))
		time.sleep(0.1)
		return get_object_safe(task_id, attempt - 1)

def delete_map(request, task_id):
	if request.method == 'GET':
		task = Task.objects.get(id = task_id)
		task.delete();
		return recent(request)
