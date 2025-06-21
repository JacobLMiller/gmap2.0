from maps.models import Task
from lib.pipeline import call_graphviz, get_graphviz_map, call_graphviz_scale, set_status, call_hmds
from re import sub, search
import time
from datetime import datetime
from time import strftime

import logging
log = logging.getLogger('gmap_web')

def create_task(task_parameters, user_ip):
	log.debug(f"Creating new Task with parameters: and user_ip: {user_ip}")
	# set up new object

	task = Task()
	task.creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	task.creation_ip = user_ip

	task.input_dot = task_parameters['dotfile']
	task.vis_type = "Gmap"
	task.layout_algorithm = task_parameters['layout_algorithm']
	# task.iterations = task_parameters['iterations']
	# task.opt_alpha = task_parameters.get('opt_alpha', 'false')
	# task.hyperbolic_projection = task_parameters.get('hyperbolic','false')
	task.color_scheme = "blue" #task_parameters['color_scheme']
	# task.convergence = task_parameters.get('convergence', 'false')
	task.status = 'created'
	task.cluster_algorithm = 'k-means'
	task.save()
	log.debug(f"Task saved with ID: {task.id if hasattr(task, 'id') else 'unknown'}")

	return task

def create_map(task, *args):
	# set up new objects

	dot_out, svg_out = call_graphviz(task)
	log.debug(f"call_graphviz returned dot_out: {type(dot_out)}, svg_out: {type(svg_out)}")
	if dot_out is None or svg_out is None:
		log.error("call_graphviz returned None for dot_out or svg_out")
		return

	try:
		svg_rep, width, height = strip_dimensions(svg_out.decode())
	except Exception as e:
		log.error(f"Error decoding svg_out: {e}")
		svg_rep = ''
		width = 0
		height = 0

	task.dot_rep = dot_out
	task.svg_rep = svg_rep
	task.width = width
	task.height = height
	task.status = 'completed'
	log.debug(f"Task updated with dot_rep, svg_rep, width: {width}, height: {height}")

	# Save the same SVG for all zoom levels as a placeholder
	task.svg_rep0 = svg_rep
	task.svg_rep1 = svg_rep
	task.svg_rep2 = svg_rep
	task.svg_rep3 = svg_rep
	# TODO: Replace above with real zoomed SVG generation for each level

	task.save()

def get_formatted_map(task, format):
	return get_graphviz_map(task.dot_rep, format)

def strip_dimensions(svg):
    """having width and height attributes as well as a viewbox will cause openlayers to not display the svg propery, so we strip those attributes out"""
    svg = sub('<title>%3</title>', '', svg, count=1)

    match_re = '<svg width="(.*)pt" height="(.*)pt"'
    replacement = '<svg'
    try:
        width, height = map(float, search(match_re, svg).groups())
    except Exception:
        width, height = 0.0, 0.0
    return sub(match_re, replacement, svg, count=1), width, height
