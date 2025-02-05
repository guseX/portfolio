extends Control
var label

var base
var cat
var rik
var fun
var guse

func _ready():
	base = $base
	cat = $cat
	rik = $rik
	guse = $guse
	fun = $fun

func _on_timer_timeout():
	if Gl.car == 0:
		base.visible = true
		cat.visible = false
		rik.visible = false
		guse.visible = false
		fun.visible = false
	elif Gl.car ==  1:
		base.visible = true
		cat.visible = false
		rik.visible = false
		guse.visible = true
		fun.visible = false
	elif Gl.car == 2:
		base.visible = false
		cat.visible = false
		rik.visible = true
		guse.visible = false
		fun.visible = true
	elif Gl.car == 3:
		base.visible = false
		cat.visible = true
		rik.visible = false
		guse.visible = false
		fun.visible = true
		
