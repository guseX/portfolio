extends Control

var nc 
var date 
var nam 

func _ready():
	pass

func _on_nc_text_changed(new_text):
	nc = new_text

func _on_date_text_changed(new_text):
	date = new_text

func _on_nam_text_changed(new_text):
	nam = new_text
