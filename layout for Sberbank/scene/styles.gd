extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	Gl.car = 0

func _on_guse_pressed():
	Gl.car = 1

func _on_cat_pressed():
	Gl.car = 3

func _on_rik_pressed():
	Gl.car = 2
