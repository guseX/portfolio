extends Control


func _ready():
	pass

func _on_texture_button_pressed():
	get_tree().change_scene_to_file("res://scene/reg_two.tscn") 
	
func _on_timer_timeout():
	if Gl.saw == 1:
		get_tree().change_scene_to_file("res://scene/main.tscn") 
