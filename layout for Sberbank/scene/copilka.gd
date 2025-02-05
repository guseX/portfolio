extends Control

var bank
var but
var bt 
var bth
var tbt
var tbth

func _ready():
	bank = $TextureRect/bank
	but = $TextureRect/TextureButton
	bt = $TextureRect/bank2
	bth = $TextureRect/bank3
	tbt = $TextureRect/tb_two
	tbth = $TextureRect/tb_three

func _on_texture_button_pressed():
	bank.visible = true
	but.visible = false

func _on_tb_three_pressed():
	bth.visible = true
	tbth.visible = false

func _on_tb_two_pressed():
	bt.visible = true
	tbt.visible = false
