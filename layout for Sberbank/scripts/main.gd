extends Control

var ssc
var card
var money
var send
var label
var copilka
var score
var u
var m 
var n 
var p: String = ""
var info
var style
var exercise
var limits
var anys = 0
var back
var any

func _ready():
	label = $send_money/you/u
	ssc = $specsettingC
	money = $money
	send = $send_money
	copilka = $copilka
	score = $money/money
	u = $send_money/you/u
	n = $send_money/LineEdit2
	info = $info
	style = $styles
	exercise = $exercise
	limits = $limits
	any = $send_money/you/any
	back = $back
	
	score.text = str(Gl.money)
	u.text = str(Gl.money)
	
func _on_spec_setings_pressed():
	send.visible = false
	ssc.visible = true
	money.visible = false
	copilka.visible = false
	info.visible = false
	style.visible = false
	exercise.visible = false
	limits.visible = false
	back.visible = true
	
func _on_rubl_pressed():
	copilka.visible = true
	send.visible = false
	ssc.visible = false
	info.visible = false
	money.visible = false
	style.visible = false
	exercise.visible = false
	limits.visible = false
	back.visible = true
	
func _on_home_pressed():
	copilka.visible = false
	send.visible = false
	ssc.visible = false
	money.visible = true 
	info.visible = false
	style.visible = false
	exercise.visible = false
	limits.visible = false
	back.visible = false
	
func _on_exercise_pressed():
	copilka.visible = false
	send.visible = false
	ssc.visible = false
	money.visible = false
	info.visible = false
	style.visible = false
	exercise.visible = true
	limits.visible = false
	back.visible = true

func _on_plus_b_pressed():
	Gl.money += 1
	score.text = str(Gl.money)
	u.text = str(Gl.money)

func _on_send_b_pressed():
	send.visible = true
	money.visible = false

func _on_minus_b_pressed():
	Gl.money -= 1
	score.text = str(Gl.money)
	u.text = str(Gl.money)
	
func clear_line_edit():
	m.text = ""
	n.text = ""

func _on_texture_button_pressed():
	clear_line_edit()
	send.visible = false
	money.visible = true
	Gl.money -= anys
	u.text = str(Gl.money)
	score.text = str(Gl.money)

func _on_info_pressed():
	info.visible = true
	back.visible = true

func _on_sb_pressed():
	style.visible = true
	back.visible = true

func _on_lao_b_2_pressed():
	limits.visible = true
	back.visible = true

func _on_plus_pressed():
	anys += 1
	any.text = str(anys)

func _on_minus_pressed():
	anys -= 1
	any.text = str(anys)
	
func _on_color_timeout():
	if Gl.car == 0:
		score.modulate = Color(1, 1, 1, 1)
	elif Gl.car == 1 or 2 or 3:
		score.modulate = Color(0, 0, 0, 1)

func _on_back_pressed():
	copilka.visible = false
	send.visible = false
	ssc.visible = false
	money.visible = true
	info.visible = false
	style.visible = false
	exercise.visible = false
	limits.visible = false
	back.visible = false
