extends Control

# Called when the node enters the scene tree for the first time.
func _ready():
	pass

func _on_texture_button_pressed():
	get_tree().change_scene_to_file("res://scene/main.tscn")
