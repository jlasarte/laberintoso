import pygame as pg
pg.init()

class jmenu:
	''
	coef = 1.5
	default_font = pg.font.get_default_font()
	bip = pg.mixer.Sound('data/sonido/Opcion.wav')
	select = pg.mixer.Sound('data/sonido/Opcion.wav')

def run(menu,color,size,COLOR=None,font=None,interline=0,SIZE=None,light=5,justify=True,pos=('center','center')):
	"jmenu.run(menu=list,color=(r,g,b),size=int[[[[[[[COLOR=(r,g,b)],font=font_path],interline=real],SIZE=int],light=int],justify=bool],pos]) : return str\n\
	 menu = liste de str, ex: ['choix1','choix2','choix3']\n\
	 light est un reel dans l'intreval -10/+10\n\
	 si COLOR est defini, light est ignore\n\
	 pos=('left'|'cenetr'|'right'|int,'top'|'center'|'bottom'|int)\n\
	 return str de menu"

	screen = pg.display.get_surface()
	bg = screen.copy()
	mouse_rect = pg.Rect((0,0),(1,1))
	if font==None : font = jmenu.default_font
	font1 = pg.font.Font(font,size)
	size = font1.get_height()
	font2 = pg.font.Font(font,SIZE if SIZE!=None else int(size*jmenu.coef))
	SIZE = font2.get_height()
	scr_w,scr_h = screen.get_size()
	H = font1.get_height()+interline
	if COLOR==None : COLOR = map(lambda x:x+((255-x if light>0 else x)*light/10),color)
	surfs = []
	rects = []
	RECTS = []
	for c in range(len(menu)):
		surfs.append((font1.render(menu[c],1,color),font2.render(menu[c],1,COLOR)))
		(w0,h0),(w1,h1) = surfs[c][0].get_size(),surfs[c][1].get_size()
		rects.append(surfs[c][0].get_rect().move(-w0/2 if justify else 0,c*H))
		RECTS.append(rects[c].inflate(w1-w0,h1-h0)) if justify else RECTS.append(rects[c].inflate(w1-w0,h1-h0).move((w1-w0)/2,0))
	menu_rect = RECTS[0].unionall(RECTS) if SIZE > size else rects[0].unionall(rects)
	X = {'left':0,'center':(scr_w-menu_rect.width)/2,'right':scr_w-menu_rect.width}
	Y = {'top':0,'center':(scr_h-menu_rect.height)/2,'bottom':scr_h-menu_rect.height}
	x = (X[pos[0]] if type(pos[0])==str else pos[0])-menu_rect.x
	y = (Y[pos[1]] if type(pos[1])==str else pos[1])-menu_rect.y
	for c in rects+RECTS: c.move_ip(x,y)
	item = 0

	def update():
		screen.blit(bg,(0,0))
		for c in range(len(menu)):
			if c!=item :
				screen.blit(surfs[c][0],rects[c].topleft)
				#pg.draw.rect(screen,(255,0,0),rects[c],1)#decommenter pour reglage
			screen.blit(surfs[item][1],RECTS[item].topleft)
			#pg.draw.rect(screen,(0,0,255),RECTS[item],1)#decommenter pour reglage
		pg.display.flip()
	
	update()
	while True:
		e = pg.event.wait()
		mouse = mouse_rect.move(pg.mouse.get_pos())
		key = pg.key.get_pressed()
		xx = [RECTS[item]]+rects
		if e.type == pg.MOUSEMOTION or (e.type == pg.MOUSEBUTTONDOWN and e.button == 1):
			j = mouse.collidelist(xx)
			if j>0:
				item = j-1
				jmenu.bip.play()
				update()
		elif e.type == pg.MOUSEBUTTONUP and e.button == 1 and mouse.collidelist(xx)==0: break
		elif (key[pg.K_RETURN] or key[pg.K_KP_ENTER]) and item>-1 : break
		elif key[pg.K_DOWN]:
			item+=1;item=item%len(menu)
			update()
		elif  key[pg.K_UP]:
			item = len(menu)-1 if not item else item-1
			update()
		elif e.type == pg.QUIT or key[pg.K_ESCAPE]:
			pg.event.post(pg.event.Event(pg.QUIT,{}))
			screen.blit(bg,(0,0))
			pg.display.flip()
			return None
	screen.blit(bg,(0,0))
	jmenu.select.play()
	pg.display.flip()
	return menu[item]

