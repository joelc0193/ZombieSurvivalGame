#aassasd
import pygame, sys, time, random, graph
import cPickle as pickle
from pygame.locals import *
from math import *
from copy import deepcopy
import sys
import numpy as np
import imghdr
import os

# Read all images
Images={}
SURFACEWIDTH=100
SURFACEHEIGHT=100
for dirpath, dirnames, filenames in os.walk('Characters/'):
    for filename in filenames:
    	if 'feet' in str(dirpath):
    		scale=(35,35)
    		location=(35,30)
    	elif 'Zombie1' in str(dirpath):
    		scale=(170,170)
    		location=(-43,-36)
    	else:
    		scale=(50,50)
    		location=(27,22)
        file_path = os.path.join(dirpath, filename)
        if imghdr.what(file_path):
        	if filename[-6]in['1','2','3','4','5','6','7','8','9','0,']:
        		surface =  pygame.Surface((SURFACEWIDTH, SURFACEHEIGHT), pygame.SRCALPHA, 32)
        		surface.blit(pygame.transform.scale(pygame.image.load(str(dirpath)+'/'+str(filename)), scale), location)
        		Images[str(dirpath)+filename[-6]+filename[-5]]=surface
    		else:
    			surface =  pygame.Surface((SURFACEWIDTH, SURFACEHEIGHT), pygame.SRCALPHA, 32)
    			surface.blit(pygame.transform.scale(pygame.image.load(str(dirpath)+'/'+str(filename)), scale), location)
    			Images[str(dirpath)+filename[-5]]=surface

for dirpath, dirnames, filenames in os.walk('Grenades/'):
    for filename in filenames:
        if imghdr.what(file_path):
        	if filename[-6]in['1','2','3','4','5','6','7','8','9','0,']:
        		Images[str(dirpath)+filename[-6]+filename[-5]]=pygame.image.load(str(dirpath)+'/'+str(filename))
    		else:
    			Images[str(dirpath)+filename[-5]]=pygame.image.load(str(dirpath)+'/'+str(filename))


# Used to pickle the map paths graph, map paths dictionary, Images dictionary
sys.setrecursionlimit(1000000000)

# frames per second setting
FPS = 30
fpsClock = pygame.time.Clock()

# Set up display area
WIDTH = 1300
HEIGHT = 720
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Zombie Survival')

# Define colors
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
LIME=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
CYAN=(0,255,255)
MAGENTA=(255,0,255)
SILVER=(192,192,192)
GRAY=(128,128,128)
MAROON=(128,0,0)
GREEN=(0,128,0)
PURPLE=(128,0,128)
TEAL=(0,128,128)
NAVY=(0,0,128)
OXFORDBLUE=(0,33,71)
COBALTBLUE=(0,28,67)
BARNRED=(124,10,2)
INDIGOBLUE=(0,70,150)
MEDALLION=(125,81,1)
FILIGREEYELLOW=(167, 126, 36)

def switched_rooms(thing): # Find if thing switched rooms or not
	if thing.switched_rooms:
		return False
	elif not (thing.current_room.rect.left<=thing.center_xcoord and thing.current_room.rect.right>=thing.center_xcoord and thing.current_room.rect.bottom>=thing.center_ycoord and thing.current_room.rect.top<=thing.center_ycoord):
		return True
	else:
		return False

def switched_areas(thing): # find if thing switched areas or not
	if thing.switched_areas:
		return False
	if thing.current_area!=None:
		if not (thing.current_area.rect.left<=thing.center_xcoord and thing.current_area.rect.right>=thing.center_xcoord and thing.current_area.rect.bottom>=thing.center_ycoord and thing.current_area.rect.top<=thing.center_ycoord):
			return True
		else:
			return False
	else:
		return False

def update_survivor_location():  # MOves the survivor
	for event in GameState['events']:
		# Check to see if a key was pressed or released and updates the state of that keypress
		if event.type==KEYUP or event.type==KEYDOWN:
			if event.key==273 or event.key==119:
				if event.type==KEYDOWN:
					survivor.move_up=True
				else:
					survivor.move_up=False
			if event.key==274 or event.key==115:
				if event.type==KEYDOWN:
					survivor.move_down=True
				else:
					survivor.move_down=False
			if event.key==275 or event.key==100:
				if event.type==KEYDOWN:
					survivor.move_right=True
				else:
					survivor.move_right=False
			if event.key==276 or event.key==97:
				if event.type==KEYDOWN:
					survivor.move_left=True
				else:
					survivor.move_left=False
			if event.key==114:
				if event.type==KEYDOWN:
					if survivor.body_motion!='reload':
						survivor.body_motion='reload'
						survivor.max_body_state_number=26
						survivor.current_body_state_number=0
						survivor.update_body_state_image_delay=.05
	# Updates survivor location based on state of corresponding keys
	move_x=survivor.center_xcoord
	move_y=survivor.center_ycoord
	if survivor.move_up==True:
		move_y-=5
	if survivor.move_down==True:
		move_y+=5
	if survivor.move_right==True:
		move_x+=5
	if survivor.move_left==True:
		move_x-=5

	WALKINGRECTWIDTH=15
	WALKINGRECTHEIGHT=15

	# If the survivor is not told to stay in place
	if not (move_x==survivor.center_xcoord and move_y==survivor.center_ycoord):
		# finds the direction where the survivor is headed
		survivor.angle_walk=angle_finder(survivor.center_xcoord, survivor.center_ycoord , move_x, move_y)
		# finds new x location based on speed of survivor and angle headed
		survivor.center_xcoord+=survivor.speed*cos(survivor.angle_walk)
		WALKINGRECTTOPLEFT=(survivor.center_xcoord-WALKINGRECTWIDTH/2, survivor.center_ycoord-WALKINGRECTHEIGHT/2)
		survivor.walking_rect=pygame.Rect(WALKINGRECTTOPLEFT[0], WALKINGRECTTOPLEFT[1], WALKINGRECTWIDTH, WALKINGRECTHEIGHT)
		# Checks to see if the survivor's new x location does not cause it to crash a wall
		for wall in current_map.walls:
			# If it crashes a wall, moves back
			if wall.rect.colliderect(survivor.walking_rect):
				survivor.center_xcoord-=survivor.speed*cos(survivor.angle_walk)
				WALKINGRECTTOPLEFT=(survivor.center_xcoord-WALKINGRECTWIDTH/2, survivor.center_ycoord-WALKINGRECTHEIGHT/2)
		survivor.walking_rect=pygame.Rect(WALKINGRECTTOPLEFT[0], WALKINGRECTTOPLEFT[1], WALKINGRECTWIDTH, WALKINGRECTHEIGHT)
		# finds new y location based on speed of survivor and angle headed
		survivor.center_ycoord+=survivor.speed*sin(survivor.angle_walk)
		WALKINGRECTTOPLEFT=(survivor.center_xcoord-WALKINGRECTWIDTH/2, survivor.center_ycoord-WALKINGRECTHEIGHT/2)
		survivor.walking_rect=pygame.Rect(WALKINGRECTTOPLEFT[0], WALKINGRECTTOPLEFT[1], WALKINGRECTWIDTH, WALKINGRECTHEIGHT)
		# checks to see if the survivor's new y location does not cause it to crash a wall
		for wall in current_map.walls:
			if wall.rect.colliderect(survivor.walking_rect):
				survivor.center_ycoord-=survivor.speed*sin(survivor.angle_walk)
				WALKINGRECTTOPLEFT=(survivor.center_xcoord-WALKINGRECTWIDTH/2, survivor.center_ycoord-WALKINGRECTHEIGHT/2)
		survivor.walking_rect=pygame.Rect(WALKINGRECTTOPLEFT[0], WALKINGRECTTOPLEFT[1], WALKINGRECTWIDTH, WALKINGRECTHEIGHT)
		# Draws the survivor
	survivor.center_coords=(survivor.center_xcoord, survivor.center_ycoord)

	# checks to see if survivor switched rooms
	survivor.switched_rooms=switched_rooms(survivor)
	# If survivor switched rooms, find new room
	if survivor.switched_rooms:
		survivor.current_room.entities_on.remove(survivor)
		survivor.current_room=find_current_location(survivor.center_coords, current_map.rooms)
		survivor.current_room.entities_on.add(survivor)
	# checks to see if survivor switches areas
	survivor.switched_areas=switched_areas(survivor)
	# if survivor switched area, finds new area
	if survivor.switched_areas:
		survivor.current_area.entities_on.remove(survivor)
		survivor.current_area=find_current_location(survivor.center_coords, current_map.areas)	
		survivor.current_area.entities_on.add(survivor)

	# finds new angle that survivor has to in order to be facing the cursor
	survivor.angle = angle_finder(survivor.center_xcoord, survivor.center_ycoord, GameState['xcoord_cursor'], GameState['ycoord_cursor'])

# updates the zombies's image as it walks
def update_zombie_state_image(zombie):
	now=time.time()
	if (zombie.time_of_last_generated_state==0) or (now-zombie.time_of_last_generated_state>=zombie.update_state_image_delay):
		zombie.time_of_last_generated_state = now # update the time of last zombie update to now
		zombie.current_state_number+=1
		zombie.current_state_number=zombie.current_state_number%zombie.max_number_of_states
		zombie.image=Images['Characters/Zombies/Zombie'+str(zombie.zombie_number)+'/'+zombie.body_motion+str(zombie.current_state_number)] # Find the image stored under the key generateed above
	return zombie.image

def move_zombies():
	# For each area that has at least one zombie on it, finds shortest path from that area to the survivor's area and gives it to each zombie that's on it
	if survivor.switched_areas:
		for zombie in GameState['zombies_collection']:
			generated_path=current_map.paths[(zombie.current_area.center_xcoord,zombie.current_area.center_ycoord),(survivor.current_area.center_xcoord, survivor.current_area.center_ycoord)][0]
			# If the len of the path is 1, that means that the zombie is on the survivor's area. else, the zombie goes to the second node because the first is the center of the zombie's current area
			if not len(generated_path)==1:
				zombie.path=generated_path[1::]
				zombie.distance=current_map.paths[(zombie.current_area.center_xcoord,zombie.current_area.center_ycoord),(survivor.current_area.center_xcoord, survivor.current_area.center_ycoord)][1]
			else:
				zombie.path=[(survivor.center_xcoord, survivor.center_ycoord)]
				zombie.distance=distance(zombie.center_xcoord, zombie.center_ycoord, survivor.center_xcoord, survivor.center_ycoord)
	# for each zombie...
	for zombie in GameState['zombies_collection']:
		# updates the zombie path so that tha last coordinate is the survivor's coordinates
		zombie.update_path()
		zombie.following_path=True
		# update direction that zombie should face
		zombie.angle=angle_finder(zombie.center_xcoord, zombie.center_ycoord , zombie.path[0][0], zombie.path[0][1])
		# draw the zombie
		zombie.prepare()
		zombie.draw()

		# If zombie has reached the node that he was walking towards, and that node is not the survivor's location, deletes that node and zombie keeps going with journey
		if zombie.center_coords==zombie.path[0]:
			if not len(zombie.path)==1:
				del zombie.path[0]
			if zombie.path[0]==survivor.center_coords:
				survivor.was_hit(zombie)

		# find future zombie location coordinates
		if zombie.body_motion!='attack':
			distanc=distance(zombie.center_xcoord+zombie.speed*cos(zombie.angle), zombie.center_ycoord+zombie.speed*sin(zombie.angle), zombie.path[0][0], zombie.path[0][1])
			if distanc<=zombie.speed:
				zombie.center_xcoord=zombie.path[0][0]
				zombie.center_ycoord=zombie.path[0][1]
			else:
				zombie.center_xcoord+=zombie.speed*cos(zombie.angle)
				zombie.center_ycoord+=zombie.speed*sin(zombie.angle)

			zombie.center_coords=(zombie.center_xcoord, zombie.center_ycoord)
			# rotate zombie so that he faces node that he is walking towards
			zombie.rotated_image = rotate_image(zombie, 'zombie')

			# find if zombie switched rooms and area
			zombie.switched_rooms=switched_rooms(zombie)
			zombie.switched_areas=switched_areas(zombie)
			# if zombie switched rooms, find new room
			if zombie.switched_rooms:
				zombie.current_room.entities_on.remove(zombie)
				zombie.current_room=find_current_location(zombie.center_coords, current_map.rooms)
				zombie.current_room.entities_on.add(zombie)
			# if zombie switched area, find new area
			if zombie.switched_areas:
				zombie.current_area.entities_on.remove(zombie)
				zombie.current_area=find_current_location(zombie.center_coords, current_map.areas)
				zombie.current_area.entities_on.add(zombie)
			# find the distance between the survivor and the zombie
			zombie.distance=distance(zombie.center_xcoord, zombie.center_ycoord, survivor.center_xcoord, survivor.center_ycoord)

def new_cursor_location():
	for event in GameState['events']:
		if event.type==MOUSEMOTION:  # If mouse was pressed, updates cursor's location
			GameState['xcoord_cursor'] = event.pos[0]
			GameState['ycoord_cursor'] = event.pos[1]
		# If mouse button was clicked, sets flag so that generate_function knows to keep generating bullets
		if event.type==MOUSEBUTTONDOWN:
			GameState['MouseButtonDown']=True
		elif event.type==MOUSEBUTTONUP: # If mouse button was released, sets flag so that no more projectiles are produced
			GameState['MouseButtonDown']=False
def update_projectile_locations(): # updates the bullets
	for bullet in GameState['projectiles']: # For each projectile
		# If projectile is not out of bounds
		if (bullet.center_xcoord <= WIDTH and bullet.center_xcoord >=0) and (bullet.center_ycoord <= HEIGHT and bullet.center_ycoord >=0): 
			bullet.prepare()
			# check to see if it crashed into a wall and finds the speed at which the bullet should go so that it ends up at the first point of collision in the next frame
			walls_hit=pygame.sprite.spritecollide(bullet.wall_check, current_map.walls, False, pygame.sprite.collide_mask)
			if walls_hit:
				wall_hit_check=False
				x=bullet.center_xcoord
				y=bullet.center_ycoord
				brake=False
				while not wall_hit_check:
			 		for wall in current_map.walls:
			 			if wall.rect.collidepoint(x,y):
			 				wall_hit_check=True
			 				break
					x+=cos(bullet.angle)
					y+=sin(bullet.angle)
			 	bullet.speed=distance(bullet.center_xcoord, bullet.center_ycoord, x, y)
			 	bullet.remove_later=True
			 	if bullet.speed>1:
				 	bullet.prepare()
				else:
				 	bullet.remove=True
			bullet.draw()
			bullet.center_xcoord+=(bullet.speed*((bullet.bullet_number/bullet.total_number)))*cos(bullet.angle)
			bullet.center_ycoord+=(bullet.speed*((bullet.bullet_number/bullet.total_number)))*sin(bullet.angle)
			bullet.bullet_number=1
			bullet.total_number=1
			bullet.center_coords=(bullet.center_xcoord, bullet.center_ycoord)
			
			bullet.switched_areas=switched_areas(bullet)
			if bullet.switched_areas:
				bullet.current_area=find_current_location((bullet.center_xcoord, bullet.center_ycoord), current_map.areas)

			if not bullet.remove:
				# updates the new coordinates based on angle of direction and draws onto DISPLAYSURF
				zombies_hit=pygame.sprite.spritecollide(bullet.wall_check, GameState['zombies_collection'], False, pygame.sprite.collide_mask)
				zombies_hit.sort(key=lambda x: x.distance, reverse=False)
				for zombie in zombies_hit:
					zombie.was_hit(bullet)
					bullet.hit(zombie)
					if zombie.health<=0:
						zombie.kill()
						survivor.money+=1
					if bullet.penetration<=0:
						bullet.remove=True
						break
			if bullet.remove_later==True:
				bullet.remove=True
		else:
			bullet.remove=True

	GameState['projectiles'].update()

def rotate_image(thing,string): # rotates images
	if string=='zombie':
		location = thing.center_coords 
		rotated_sprite = pygame.transform.rotate(thing.image, -degrees(thing.angle))
		thing.rect=rotated_sprite.get_rect()
		thing.rect.center = thing.center_coords
		return rotated_sprite
	elif string=='bullet':
		loc = thing.image.get_rect().center  #rot_image is not defined 
		rot_sprite = pygame.transform.rotate(thing.image, -degrees(thing.angle))
		rot_sprite.get_rect().center = loc
		return rot_sprite
	elif string=='wall_check':
		loc = thing.image.get_rect().center  #rot_image is not defined 
		rot_sprite = pygame.transform.rotate(thing.image, -degrees(thing.angle+(3.14159/2)))
		return rot_sprite

def angle_finder(x1,y1,rotate_to_x2,rotate_to_y2): # finds angkes
	return atan2((rotate_to_y2-y1),(rotate_to_x2-x1))

def find_current_location(coords, locations): # finds current location
	for location in locations:
		if location.rect.collidepoint(coords[0], coords[1]):
			return location
 	closest_location=None
 	distanc=0
 	for location in locations:
 		d=distance(coords[0], coords[1], location.center_xcoord, location.center_ycoord)
 		if d<distance:
 			distanc=d
 			closest_location=location
 	return closest_location

def distance(x1, y1, x2, y2): # finds distance between two things
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)
    pass

def draw_game(args):
	DISPLAYSURF.fill(BLACK)
	DISPLAYSURF.blit(current_map.image, (current_map.xcoord,current_map.ycoord)) # Load map image
	if args[0]==1:
		for room in current_map.rooms:
			room.draw()
	if args[1]:
		for wall in current_map.walls:
			wall.draw()	
	if args[2]:
		for area in current_map.areas:
			area.draw()
	if args[3]:
	 	for node in current_map.nodes:
	 		pygame.draw.circle(DISPLAYSURF, GREEN, node, 4)

def menu_displayer():
	## Top middle menu with round number
	# New surface to allow for transparency
	MENUWIDTH=120
	MENUHEIGHT=65
	MENUTOPLEFT=((WIDTH/2)-(MENUWIDTH/2),0)

	surface = pygame.Surface((MENUWIDTH, MENUHEIGHT))  
	surface.set_alpha(128)
	surface.fill(INDIGOBLUE)
	DISPLAYSURF.blit(surface, MENUTOPLEFT)
 
 	# Menu outline
	menu_outline=pygame.Rect(MENUTOPLEFT[0], MENUTOPLEFT[1]-2, MENUWIDTH+2, MENUHEIGHT+4)
	pygame.draw.rect(DISPLAYSURF, BLACK, menu_outline, 2)


	# word: 'ROUND:'
	SPACEAWAYFROMLEFT=10
	SPACEAWAYFROMTOP=10
	health_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 35)
	health_text_surface_obj = health_text_obj.render('ROUND:', True, BLACK)
	DISPLAYSURF.blit(health_text_surface_obj, (MENUTOPLEFT[0]+SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))
	# word: round number
	SPACEAWAYFROMLEFT=90
	SPACEAWAYFROMTOP=10
	health_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 35)
	health_text_surface_obj = health_text_obj.render('1', True, MEDALLION)
	DISPLAYSURF.blit(health_text_surface_obj, (MENUTOPLEFT[0]+SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))

	## Top right menu with health and armor
	# New surface to allow for transparency
	MENUWIDTH=280
	MENUHEIGHT=65
	MENUTOPLEFT=(WIDTH-MENUWIDTH,0)

	surface = pygame.Surface((MENUWIDTH, MENUHEIGHT))  
	surface.set_alpha(128) 
	surface.fill(INDIGOBLUE)
	DISPLAYSURF.blit(surface, MENUTOPLEFT)

 	# Menu outline
	menu_outline=pygame.Rect(MENUTOPLEFT[0], MENUTOPLEFT[1]-2, MENUWIDTH+2, MENUHEIGHT+3)
	pygame.draw.rect(DISPLAYSURF, BLACK, menu_outline, 2)

	
	# word: 'Armor'
	SPACEAWAYFROMLEFT=10
	SPACEAWAYFROMTOP=10
	health_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 16)
	health_text_surface_obj = health_text_obj.render('Armor:', True, BLACK)
	DISPLAYSURF.blit(health_text_surface_obj, (MENUTOPLEFT[0]+SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))
	# word: 'Armor'
	SPACEAWAYFROMLEFT=8
	SPACEAWAYFROMTOP=35
	health_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 16)
	health_text_surface_obj = health_text_obj.render('Armor:', True, BLACK)
	DISPLAYSURF.blit(health_text_surface_obj, (MENUTOPLEFT[0]+SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))
	
	# Armor Bar Outline
	BARWIDTH=200
	BARHEIGHT=13
	SPACEAWAYFROMLEFT=50
	SPACEAWAYFROMTOP=15
	health_bar=pygame.Rect(MENUTOPLEFT[0]+SPACEAWAYFROMLEFT,SPACEAWAYFROMTOP,BARWIDTH, BARHEIGHT)
	pygame.draw.rect(DISPLAYSURF, BLACK, health_bar,2)

	# Armor Bar Outline
	BARWIDTH=200
	BARHEIGHT=13
	SPACEAWAYFROMLEFT=50
	SPACEAWAYFROMTOP=40
	armor_bar=pygame.Rect(MENUTOPLEFT[0]+SPACEAWAYFROMLEFT,SPACEAWAYFROMTOP,BARWIDTH, BARHEIGHT)
	pygame.draw.rect(DISPLAYSURF, BLACK, armor_bar,2)

	# Armor Bar
	BARMAXWIDTH=197
	if not survivor.current_health<=0:
		BARWIDTH=(float(survivor.current_health)/survivor.max_health)*BARMAXWIDTH
	else:
		BARWIDTH=0
	BARHEIGHT=10
	SPACEAWAYFROMLEFT=52
	SPACEAWAYFROMTOP=17
	if not BARWIDTH==0:
		health_bar=pygame.Rect(MENUTOPLEFT[0]+SPACEAWAYFROMLEFT,SPACEAWAYFROMTOP,BARWIDTH, BARHEIGHT)
		pygame.draw.rect(DISPLAYSURF, BARNRED, health_bar)
	# Armor Bar
	BARMAXWIDTH=197
	if not survivor.current_armor<=0:
		BARWIDTH=(float(survivor.current_armor)/survivor.max_armor)*BARMAXWIDTH
	else:
		BARWIDTH=0
	BARHEIGHT=10
	SPACEAWAYFROMLEFT=52
	SPACEAWAYFROMTOP=42
	if not BARWIDTH==0:
		armor_bar=pygame.Rect(MENUTOPLEFT[0]+SPACEAWAYFROMLEFT,SPACEAWAYFROMTOP, BARWIDTH, BARHEIGHT)
		pygame.draw.rect(DISPLAYSURF, OXFORDBLUE, armor_bar)

	
	# Armor Fraction
	health_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 14)
	if survivor.current_health>=0:
		health_text_surface_obj = health_text_obj.render(str(survivor.current_health)+'/'+str(survivor.max_health), True, BLACK)
		health_text_surface_obj_rect=health_text_surface_obj.get_rect(center=health_bar.center)
	else:
		health_text_surface_obj = health_text_obj.render('0/0', True, BLACK)
		health_text_surface_obj_rect=health_text_surface_obj.get_rect(center=health_bar.center)
	DISPLAYSURF.blit(health_text_surface_obj, health_text_surface_obj_rect)
	# Armor Fraction
	armor_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 14)
	if survivor.current_armor>=0:
		armor_text_surface_obj = armor_text_obj.render(str(survivor.current_armor)+'/'+str(survivor.max_armor), True, BLACK)
		armor_text_surface_obj_rect=armor_text_surface_obj.get_rect(center=armor_bar.center)
	else:
		armor_text_surface_obj = armor_text_obj.render('0/0', True, BLACK)
		armor_text_surface_obj_rect=armor_text_surface_obj.get_rect(center=armor_bar.center)
	DISPLAYSURF.blit(armor_text_surface_obj, armor_text_surface_obj_rect)

	# Money counter
	MENUWIDTH=100
	MENUHEIGHT=30
	MENUTOPLEFT=(WIDTH-MENUWIDTH,65)

	surface = pygame.Surface((MENUWIDTH, MENUHEIGHT))  
	surface.set_alpha(128) 
	surface.fill(INDIGOBLUE)
	DISPLAYSURF.blit(surface, MENUTOPLEFT)
	
 	# Menu outline
	menu_outline=pygame.Rect(MENUTOPLEFT[0], MENUTOPLEFT[1], MENUWIDTH+2, MENUHEIGHT+2)
	pygame.draw.rect(DISPLAYSURF, BLACK, menu_outline, 2)

	# money text
	money_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 25)
	money_text_surface_obj = money_text_obj.render('$'+str(survivor.money), True, BLACK)
	money_text_surface_obj_rect=money_text_surface_obj.get_rect(centerx=menu_outline.centerx,centery=menu_outline.centery-2)
	DISPLAYSURF.blit(money_text_surface_obj, money_text_surface_obj_rect)

	## Bottom right
	# Rectangular menu
	# New surface to allow for transparency
	SURFACEWIDTH=500
	SURFACEHEIGHT=120
	SURFACETOPLEFT=(WIDTH-SURFACEWIDTH,HEIGHT-SURFACEHEIGHT)
	surface =  pygame.Surface((SURFACEWIDTH, SURFACEHEIGHT), pygame.SRCALPHA, 32)
	
	# Rectangle
	MENUWIDTH=SURFACEWIDTH-100
	MENUHEIGHT=SURFACEHEIGHT-30
	MENUTOPLEFT=(SURFACEWIDTH-MENUWIDTH, SURFACEHEIGHT-MENUHEIGHT)
	pygame.draw.rect(surface, (0,70,150,128), (MENUTOPLEFT[0], MENUTOPLEFT[1], MENUWIDTH, MENUHEIGHT))
	# Rectangle outline
	pygame.draw.rect(surface, BLACK, (MENUTOPLEFT[0], MENUTOPLEFT[1], MENUWIDTH, MENUHEIGHT),2)

	# Circle with weapon on it
	RADIUS=100
	Y_OFFSET=RADIUS/5
	pygame.draw.circle(surface, (0,70,150,128), (RADIUS,RADIUS), RADIUS)
	# Circle outline
	RADIUS=100
	Y_OFFSET=RADIUS/5
	pygame.draw.circle(surface, BLACK, (RADIUS,RADIUS), RADIUS, 2)

	# Word: 'Mag:'
	SPACEAWAYFROMLEFT=220
	SPACEAWAYFROMTOP=43
	mag_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 25)
	mag_text_surface_obj = mag_text_obj.render('MAG:', True, BLACK)
	surface.blit(mag_text_surface_obj, (SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))

	# Mag Display
	SPACEAWAYFROMLEFT=265
	SPACEAWAYFROMTOP=43
	mag_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 25)
	mag_text_surface_obj = mag_text_obj.render(str(survivor.weapon.current_mag_ammo)+'/'+str(survivor.weapon.max_mag_ammo), True, BLACK)
	surface.blit(mag_text_surface_obj, (SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))

	# Word 'Ammo'
	SPACEAWAYFROMLEFT=220
	SPACEAWAYFROMTOP=75
	mag_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 25)
	mag_text_surface_obj = mag_text_obj.render('STOCK:', True, BLACK)
	surface.blit(mag_text_surface_obj, (SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))

	# Ammo Display
	SPACEAWAYFROMLEFT=275
	SPACEAWAYFROMTOP=75
	mag_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 25)
	mag_text_surface_obj = mag_text_obj.render(str(survivor.weapon.current_weapon_ammo)+'/'+str(survivor.weapon.max_weapon_ammo), True, BLACK)
	surface.blit(mag_text_surface_obj, (SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))

	if survivor.body_motion=='reload':
		# Reloading Bar Outline
		BARWIDTH=140
		BARHEIGHT=13
		SPACEAWAYFROMLEFT=30
		SPACEAWAYFROMTOP=100
		armor_bar=pygame.Rect(SPACEAWAYFROMLEFT,SPACEAWAYFROMTOP,BARWIDTH, BARHEIGHT)
		pygame.draw.rect(surface, BLACK, armor_bar,2)

		# Reloading Bar
		BARMAXWIDTH=137
		BARHEIGHT=10
		SPACEAWAYFROMLEFT=32
		SPACEAWAYFROMTOP=102
		if not survivor.current_body_state_number==0:
			BARWIDTH=(float(survivor.current_body_state_number)/survivor.max_body_state_number)*BARMAXWIDTH
		if not BARWIDTH==0:
			reload_bar=pygame.Rect(SPACEAWAYFROMLEFT,SPACEAWAYFROMTOP, BARWIDTH, BARHEIGHT)
			pygame.draw.rect(surface, FILIGREEYELLOW, reload_bar)

		# Word: 'Reloading'
		SPACEAWAYFROMLEFT=77
		SPACEAWAYFROMTOP=99
		reload_text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 12)
		reload_text_surface_obj = reload_text_obj.render('Reloading...', True, BLACK)
		surface.blit(reload_text_surface_obj, (SPACEAWAYFROMLEFT, SPACEAWAYFROMTOP))

	DISPLAYSURF.blit(surface, SURFACETOPLEFT)

	# Image of current weapon
	DISPLAYSURF.blit(survivor.weapon.weapon_image, (850,610))

def pause_menu():
	for event in GameState['events']:
			if event.type==MOUSEBUTTONDOWN:
				point=(GameState['xcoord_cursor'], GameState['ycoord_cursor'])
				GameState['active_tab'].color=INDIGOBLUE
				if player_tab.rect.collidepoint(point):
					GameState['active_tab']=player_tab
				elif weapons_tab.rect.collidepoint(point):
					GameState['active_tab']=weapons_tab
				elif explosives_tab.rect.collidepoint(point):
					GameState['active_tab']=explosives_tab
				elif turrets_tab.rect.collidepoint(point):
					GameState['active_tab']=turrets_tab
				GameState['active_tab'].color=OXFORDBLUE

	# Main Menu
	rect=pygame.Rect(300,100,700,500)
	pygame.draw.rect(DISPLAYSURF, OXFORDBLUE, rect)
	
	# Money background
	rect=pygame.Rect(900,100,100,40)
	pygame.draw.rect(DISPLAYSURF, BLACK, rect)
	# Money Text
	text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
	text_surface_obj = text_obj.render('$'+str(survivor.money), True, WHITE)
	text_rect=text_surface_obj.get_rect(center=rect.center)
	DISPLAYSURF.blit(text_surface_obj, text_rect)

	# Line under tabs
	rect=pygame.Rect(350,200,600,10)
	pygame.draw.rect(DISPLAYSURF, BLACK, rect)
	rect=pygame.Rect(350,200,600,10)
	pygame.draw.rect(DISPLAYSURF, BLACK, rect, 2)

	# Blue square behind items
	rect=pygame.Rect(350,210,600,350)
	pygame.draw.rect(DISPLAYSURF, INDIGOBLUE, rect)

	# Blue square behind items outine
	rect=pygame.Rect(350,210,600,350)
	pygame.draw.rect(DISPLAYSURF, BLACK, rect, 2)

	player_tab.draw_tab()
	weapons_tab.draw_tab()
	explosives_tab.draw_tab()
	turrets_tab.draw_tab()

	GameState['active_tab'].draw_contents()
	GameState['active_tab'].tab_handler()

class Player_Tab:
	def __init__(self):
		self.text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 40)
		self.text_surface_obj = self.text_obj.render('Player', True, BLACK)
		self.rect= pygame.Rect(350,150,150,50)
		self.color=INDIGOBLUE
	def draw_tab(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
		pygame.draw.rect(DISPLAYSURF, BLACK, self.rect, 2)
		DISPLAYSURF.blit(self.text_surface_obj, (385, 150))
	def draw_contents(self):
		## Displaying upgrades
		LEFT=350
		TOP=260
		WIDTH=600
		HEIGHT=100
		# Max Armor Container
		item = Menu_Item(LEFT+50, TOP+10, 235, 40, 'max_health', INDIGOBLUE, BLACK)
		item.draw()
		# Max Armor Text
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
		text_surface_obj = text_obj.render('Max Armor: '+str(survivor.max_health), True, BLACK)
		text_surface_obj_rect=text_surface_obj.get_rect(topleft=((LEFT+70, TOP+10)))
		DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
		# Next Upgrade
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
		if not len(survivor.max_health_upgrades)==0:
			text_surface_obj = text_obj.render('+'+str(survivor.max_health_upgrades[0]), True, GREEN)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(text_surface_obj_rect.right,text_surface_obj_rect.top+10))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Upgrade Damage Box
			button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, survivor, 'max_health', survivor.upgrade_max_health_cost, survivor.max_health_upgrades)
			button.draw()
			# Upgrade Damage Cost
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
			text_surface_obj = text_obj.render('$'+str(survivor.upgrade_max_health_cost[0]), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)

		# Armor Upgrade
		LEFT=620
		TOP=260
		WIDTH=600
		HEIGHT=100
		# Max Armor Container
		item = Menu_Item(LEFT+50, TOP+10, 235, 40, 'max_armor', INDIGOBLUE, BLACK)
		item.draw()
		# Max Armor Text
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
		text_surface_obj = text_obj.render('Max Armor: '+str(survivor.max_armor), True, BLACK)
		text_surface_obj_rect=text_surface_obj.get_rect(topleft=((LEFT+70, TOP+10)))
		DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
		# Next Upgrade
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
		if not len(survivor.max_armor_upgrades)==0:
			text_surface_obj = text_obj.render('+'+str(survivor.max_armor_upgrades[0]), True, GREEN)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(text_surface_obj_rect.right,text_surface_obj_rect.top+10))	
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Upgrade Damage Box
			button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, survivor, 'max_armor', survivor.upgrade_max_armor_cost, survivor.max_armor_upgrades)
			button.draw()
			# Upgrade Damage Cost
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
			text_surface_obj = text_obj.render('$'+str(survivor.upgrade_max_armor_cost[0]), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)

		# Upgrade Speed
		LEFT=350
		TOP=350
		WIDTH=600
		HEIGHT=100
		# Max Speed Container
		item = Menu_Item(LEFT+50, TOP+10, 190, 40, 'walk_speed', INDIGOBLUE, BLACK)
		item.draw()
		# Max Speed Text
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
		text_surface_obj = text_obj.render('Speed: '+str(survivor.walk_speed), True, BLACK)
		text_surface_obj_rect=text_surface_obj.get_rect(topleft=((LEFT+70, TOP+10)))
		DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
		# Next Upgrade
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
		if not len(survivor.walk_speed_upgrades)==0:
			text_surface_obj = text_obj.render('+'+str(survivor.walk_speed_upgrades[0]), True, GREEN)	
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(text_surface_obj_rect.right,text_surface_obj_rect.top+10))	
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Upgrade Damage Box
			button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, survivor, 'walk_speed', survivor.upgrade_walk_speed_cost, survivor.walk_speed_upgrades)
			button.draw()
			# Upgrade Damage Cost
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
			text_surface_obj = text_obj.render('$'+str(survivor.upgrade_walk_speed_cost[0]), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)

		# Bullet Speed Upgrade
		LEFT=575
		TOP=350
		WIDTH=645
		HEIGHT=100
		# Max Bullet Speed Container
		item = Menu_Item(LEFT+50, TOP+10, 280, 40, 'bullet_speed', INDIGOBLUE, BLACK)
		item.draw()
		# Max Bullet Speed Text
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
		text_surface_obj = text_obj.render('Bullet Speed: '+str(survivor.bullet_speed), True, BLACK)
		text_surface_obj_rect=text_surface_obj.get_rect(topleft=((LEFT+70, TOP+10)))
		DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
		# Next Upgrade
		text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
		if not len(survivor.bullet_speed_upgrades)==0:
			text_surface_obj = text_obj.render('+'+str(survivor.bullet_speed_upgrades[0]), True, GREEN)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(text_surface_obj_rect.right,text_surface_obj_rect.top+10))	
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Upgrade Damage Box
			button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, survivor, 'bullet_speed', survivor.upgrade_bullet_speed_cost, survivor.bullet_speed_upgrades)
			button.draw()
			# Upgrade Damage Cost
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
			text_surface_obj = text_obj.render('$'+str(survivor.upgrade_bullet_speed_cost[0]), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)

	def tab_handler(self):
		i=0
		rects=[]
		for event in GameState['events']:
			if event.type==MOUSEBUTTONDOWN:
				point=(GameState['xcoord_cursor'], GameState['ycoord_cursor'])
				for item in GameState['menu_items']:
					i+=1
					i=i%len(GameState['colors'])
					if item.rect.collidepoint(point):
						if isinstance(item, Upgrade_Button):
							if not survivor.money-item.field_upgrade_cost[0]<0:
								survivor.money-=item.field_upgrade_cost[0]
								field_upgrade_cost=item.field_upgrade_cost[0]
								field_upgrade=item.field_upgrades
								x = getattr(survivor, item.weapon_field)
								setattr(survivor, item.weapon_field, x+field_upgrade[0])
								del field_upgrade[0]

		pygame.sprite.Group.empty(GameState['menu_items'])


class Weapons_Tab:
	def __init__(self):
		# Text Second Tab
		self.text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 40)
		self.text_surface_obj = self.text_obj.render('Weapons', True, BLACK)
		self.rect= pygame.Rect(500,150,150,50)
		self.color=INDIGOBLUE
	def draw_tab(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
		pygame.draw.rect(DISPLAYSURF, BLACK, self.rect, 2)
		DISPLAYSURF.blit(self.text_surface_obj, (520, 150))
	def draw_contents(self):
		## Displaying items
		LEFT=350
		TOP=210
		WIDTH=600
		HEIGHT=100
		for weapon in survivor.weapons:
			# Big Tab
			item = Menu_Item(LEFT, TOP, WIDTH, HEIGHT, weapon.weapon_name, INDIGOBLUE, BLACK)
			item.draw()
			# Picture
			DISPLAYSURF.blit(pygame.transform.scale(survivor.weapon.weapon_image1, (80,80)), (LEFT+20, TOP+10))
			# Damage Container
			item = Menu_Item(LEFT+110, TOP+10, 190, 40, 'damage', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Damage Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Damage: '+str(weapon.damage), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(470, TOP+10))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Next Upgrade
			if not len(weapon.damage_upgrades)==0:
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(weapon.damage_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Damage Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, weapon, 'damage', weapon.upgrade_damage_cost, weapon.damage_upgrades)
				button.draw()
				# Upgrade Damage Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(weapon.upgrade_damage_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Penetration Container
			item = Menu_Item(LEFT+110, TOP+50, 210, 40, 'penetration', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Penetration Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Penetration: '+str(weapon.penetration), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(470, TOP+50))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			if not len(weapon.penetration_upgrades)==0:
				# Next Upgrade
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(weapon.penetration_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Penetration Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, weapon, 'penetration', weapon.upgrade_penetration_cost, weapon.penetration_upgrades)
				button.draw()
				# Upgrade Penetration Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(weapon.upgrade_penetration_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Mag Ammo Container
			item = Menu_Item(LEFT+340, TOP+50, 190, 40, 'max_mag_ammo', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Mag Ammo Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Mag Ammo: '+str(weapon.max_mag_ammo), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(700, TOP+50))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			if not len(weapon.max_mag_ammo_upgrades)==0:
				# Next Upgrade
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(weapon.max_mag_ammo_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Mag Ammo Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, weapon, 'max_mag_ammo', weapon.upgrade_max_mag_ammo_cost, weapon.max_mag_ammo_upgrades)
				button.draw()
				# Upgrade Mag Ammo Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(weapon.upgrade_penetration_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Weapon Ammo Container
			item = Menu_Item(LEFT+340, TOP+10, 240, 40, 'max_weapon_ammo', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Weapon Ammo Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Weapon ammo: '+str(weapon.max_weapon_ammo), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(693, TOP+10))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			if not len(weapon.max_weapon_ammo_upgrades)==0:
				# Next Upgrade
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(weapon.max_weapon_ammo_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Weapon Ammo Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, weapon, 'max_weapon_ammo', weapon.upgrade_max_weapon_ammo_cost, weapon.max_weapon_ammo_upgrades)
				button.draw()
				# Upgrade Weapon Ammo Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(weapon.upgrade_max_weapon_ammo_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			TOP+=HEIGHT

	def tab_handler(self):
		i=0
		rects=[]
		for event in GameState['events']:
			if event.type==MOUSEBUTTONDOWN:
				point=(GameState['xcoord_cursor'], GameState['ycoord_cursor'])
				for item in GameState['menu_items']:
					i+=1
					i=i%len(GameState['colors'])
					if item.rect.collidepoint(point):
						if isinstance(item, Upgrade_Button):
							if not survivor.money-item.field_upgrade_cost<0:
								survivor.money-=item.field_upgrade_cost
								weapon=item.weapon
								field_upgrade_cost=item.field_upgrade_cost
								field_upgrades=item.field_upgrades
								x = getattr(weapon, item.weapon_field)
								setattr(weapon, item.weapon_field, x+field_upgrades[0])
								del field_upgrades[0]

		pygame.sprite.Group.empty(GameState['menu_items'])

class Explosives_Tab:
	def __init__(self):
		self.text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 40)
		self.text_surface_obj = self.text_obj.render('Explosives', True, BLACK)
		self.rect= pygame.Rect(650,150,150,50)
		self.color=INDIGOBLUE
	def draw_tab(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
		pygame.draw.rect(DISPLAYSURF, BLACK, self.rect, 2)
		DISPLAYSURF.blit(self.text_surface_obj, (660, 150))
	def draw_contents(self):
		## Displaying items
		LEFT=350
		TOP=210
		WIDTH=600
		HEIGHT=100
		for grenade in GameState['grenades']:
		# Big Tab
			item = Menu_Item(LEFT, TOP, WIDTH, HEIGHT, None, INDIGOBLUE, BLACK)
			item.draw()
			# Picture
			DISPLAYSURF.blit(pygame.transform.scale(grenade.image1, (70,90)), (LEFT+20, TOP+5))
			# Damage Container
			item = Menu_Item(LEFT+110, TOP+10, 190, 40, 'damage', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Damage Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Damage: '+str(grenade.damage), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(470, TOP+10))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Next Upgrade
			if not len(grenade.damage_upgrades)==0:
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(grenade.damage_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Damage Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, grenade, 'damage', grenade.upgrade_damage_cost, grenade.damage_upgrades)
				button.draw()
				# Upgrade Damage Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(grenade.upgrade_damage_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Penetration Container
			item = Menu_Item(LEFT+110, TOP+50, 210, 40, 'penetration', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Penetration Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Penetration: '+str(grenade.penetration), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(470, TOP+50))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			if not len(grenade.penetration_upgrades)==0:
				# Next Upgrade
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(grenade.penetration_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Penetration Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, grenade, 'penetration', grenade.upgrade_penetration_cost, grenade.penetration_upgrades)
				button.draw()
				# Upgrade Penetration Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(grenade.upgrade_penetration_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Mag Ammo Container
			item = Menu_Item(LEFT+340, TOP+50, 190, 40, 'max_mag_ammo', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Mag Ammo Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Mag Ammo: '+str(grenade.max_grenade_ammo), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(700, TOP+50))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			if not len(grenade.max_grenade_ammo_upgrades)==0:
				# Next Upgrade
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(grenade.max_grenade_ammo_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Mag Ammo Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, grenade, 'max_grenade_ammo', grenade.upgrade_max_grenade_ammo_cost, grenade.max_grenade_ammo_upgrades)
				button.draw()
				# Upgrade Mag Ammo Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(grenade.upgrade_penetration_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			# Weapon Ammo Container
			item = Menu_Item(LEFT+340, TOP+10, 240, 40, 'max_grenade_ammo', INDIGOBLUE, INDIGOBLUE)
			item.draw()
			# Weapon Ammo Text
			text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 30)
			text_surface_obj = text_obj.render('Weapon ammo: '+str(grenade.max_grenade_ammo), True, BLACK)
			text_surface_obj_rect=text_surface_obj.get_rect(topleft=(693, TOP+10))
			DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			if not len(grenade.max_grenade_ammo_upgrades)==0:
				# Next Upgrade
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('+'+str(grenade.max_grenade_ammo_upgrades[0]), True, GREEN)
				text_surface_obj_rect=text_surface_obj.get_rect(left=text_surface_obj_rect.right, top=text_surface_obj_rect.top+10)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
				# Upgrade Weapon Ammo Box
				button = Upgrade_Button(text_surface_obj_rect.right+10, text_surface_obj_rect.top, 30, 20, 'upgrade', RED, BLACK, grenade, 'max_grenade_ammo', grenade.upgrade_max_grenade_ammo_cost, grenade.max_grenade_ammo_upgrades)
				button.draw()
				# Upgrade Weapon Ammo Cost
				text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 15)
				text_surface_obj = text_obj.render('$'+str(grenade.upgrade_max_grenade_ammo_cost), True, BLACK)
				text_surface_obj_rect=text_surface_obj.get_rect(center=button.rect.center)
				DISPLAYSURF.blit(text_surface_obj, text_surface_obj_rect)
			TOP+=HEIGHT
	def tab_handler(self):
		pass

class Turrets_Tab:
	def __init__(self):
		self.text_obj = pygame.font.Font('Fonts/PopulationZeroBB.otf', 40)
		self.text_surface_obj = self.text_obj.render('Turrets', True, BLACK)
		self.rect= pygame.Rect(800,150,150,50)
		self.color=INDIGOBLUE
	def draw_tab(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
		pygame.draw.rect(DISPLAYSURF, BLACK, self.rect, 2)
		DISPLAYSURF.blit(self.text_surface_obj, (825, 150))
	def draw_contents(self):
		pass
	def tab_handler(self):
		pass



def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

GameState={
'zombies_collection':pygame.sprite.Group(),
'weapons_collection':pygame.sprite.Group(),
# All nodes locations
'survivor_switched_rooms':True,
# Initial directions to move survivor in
'Up':False,
'Down':False,
'Left':False,
'Right':False,
# Keep track of direction of bullet
'xcoord_cursor':0,
'ycoord_cursor':0,
'MouseButtonDown':False,
# Projectiles to keep track of
'projectiles':pygame.sprite.Group(),
# Angle between cursor and survivor
'angle':0,
'x_image_center':0,
'y_image_center':0,
'colors':[BLACK, WHITE, RED, LIME, BLUE, YELLOW, CYAN, MAGENTA, MAROON, GREEN, PURPLE, TEAL, NAVY],
'menu_items':pygame.sprite.Group(),
'active_tab':None,
}

class Map:
	def __init__(self, image, zombie_spawns_coordinates, rooms, areas, coords, walls, nodes):
		self.image=image.convert_alpha()
		self.walls=walls
		self.zombie_spawns=zombie_spawns_coordinates
		self.xcoord=coords[0]
		self.ycoord=coords[1]
		self.nodes=nodes
		for index, spawn_coordinates in enumerate(zombie_spawns_coordinates):
			self.zombie_spawns[index]=Zombie_Spawn(self.zombie_spawns[index][0], self.zombie_spawns[index][1])
		self.areas=areas
		for index, area in enumerate(self.areas):
			index_colors=index%len(GameState['colors'])
			self.areas[index]=Area(GameState['colors'][index_colors], area[0][0], area[0][1], area[1][0], area[1][1])
			self.areas[index].prepare()
			self.areas[index].draw()
		self.rooms=rooms
		for index, room in enumerate(self.rooms):
			index_colors=index%len(GameState['colors'])
			self.rooms[index]=Room(GameState['colors'][index_colors], room[0][0], room[0][1], room[1][0], room[1][1], nodes)
			self.rooms[index].prepare()
			self.rooms[index].draw()
		self.obstacles=pygame.sprite.Group()
		for index, wall in enumerate(self.walls):
			index_colors=index%len(GameState['colors'])
			self.walls[index]=Wall(GameState['colors'][index_colors], wall[0][0], wall[0][1], wall[1][0], wall[1][1], self.obstacles)
			self.walls[index].draw()
		self.original_graph=graph.Graph()
		for node in self.nodes:
			self.original_graph.add_vertex(node)
		self.nodes_copy=self.nodes
		## This is used in part to make the graph of the nodes. Uncomment in when working on a new map
		# for index1, node1 in enumerate(self.nodes_copy):
		# 	for index2, node2 in enumerate(self.nodes_copy):
		# 		if node1!=node2:
		# 			DISPLAYSURF.fill(BLACK)
		# 			DISPLAYSURF.blit(self.image, (self.xcoord,self.ycoord))
		# 			for wall in self.walls:
		# 				wall.draw()
		# 			wall_check=Wall_Check(node1, node2, 1)
		#			wall_check.prepare()
		# 			wall_check.draw()
		# 			walls_hit = pygame.sprite.spritecollide(wall_check, self.walls, False, pygame.sprite.collide_mask)
		# 			if not walls_hit:
		# 				distanc=distance(node1[0], node1[1], node2[0], node2[1])
		# 				self.original_graph.add_edge(node1, node2, distanc)

class Menu_Item(pygame.sprite.Sprite):
	def __init__(self, left, top, width, height, name, color, color2):
		pygame.sprite.Sprite.__init__(self, GameState['menu_items'])
		self.rect=pygame.Rect(left, top, width, height)
		self.name=name
		self.color=color
		self.color2=color2
	def draw(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
		pygame.draw.rect(DISPLAYSURF, self.color2, self.rect, 2)

class Upgrade_Button(pygame.sprite.Sprite):
	def __init__(self, left, top, width, height, name, color, color2, weapon, weapon_field, field_upgrade_cost, field_upgrades):
		pygame.sprite.Sprite.__init__(self, GameState['menu_items'])
		self.rect=pygame.Rect(left, top, width, height)
		self.name=name
		self.color=color
		self.color2=color2
		self.weapon=weapon
		self.weapon_field=weapon_field
		self.field_upgrade_cost=field_upgrade_cost
		self.field_upgrades=field_upgrades
	def draw(self):
		pygame.draw.rect(DISPLAYSURF, self.color, self.rect)
		pygame.draw.rect(DISPLAYSURF, self.color2, self.rect, 2)

GameState['menu_items'].add(Menu_Item(350,150,150,50,'Player', INDIGOBLUE, BLACK))
GameState['menu_items'].add(Menu_Item(500,150,150,50, 'Weapons', INDIGOBLUE, BLACK))
GameState['menu_items'].add(Menu_Item(650,150,150,50, 'Explosives', INDIGOBLUE, BLACK))
GameState['menu_items'].add(Menu_Item(800,150,150,50, 'Turrets', INDIGOBLUE, BLACK))

class Wall(pygame.sprite.Sprite):
	def __init__(self, color, x1coord, y1coord, x2coord, y2coord, group):
		pygame.sprite.Sprite.__init__(self, group)
		self.image=pygame.image.load('black_image.png').convert_alpha()
		self.image=pygame.transform.scale(self.image, (x2coord-x1coord,y2coord-y1coord))
		self.x1coord = x1coord
		self.y1coord = y1coord
		self.x2coord = x2coord
		self.y2coord = y2coord
		self.color=color
		self.rect = pygame.Rect(x1coord, y1coord, x2coord-x1coord, y2coord-y1coord)
	def prepare(self):
		self.surface=pygame.Surface((self.x2coord-self.x1coord,self.y2coord-self.y1coord))
		self.mask=pygame.mask.from_surface(self.image)
	def draw(self):
		DISPLAYSURF.blit(self.image, (self.x1coord,self.y1coord))
	def was_hit(self, bullet):
		bullet.penetration=0

class Room:
	def __init__(self, color, x1coord, y1coord, x2coord, y2coord, nodes):
		self.color = color
		self.x1coord = x1coord
		self.y1coord = y1coord
		self.x2coord = x2coord
		self.y2coord = y2coord
		self.color=color
		self.entities_on=pygame.sprite.Group()
		self.rect = pygame.Rect(x1coord, y1coord, x2coord-x1coord, y2coord-y1coord)
		self.entities_on=pygame.sprite.Group()
		self.nodes=[]
		for node in nodes:
			if self.rect.collidepoint(node):
				self.nodes.append(node)
	def prepare(self):
		self.surface=pygame.Surface((abs(self.x2coord-self.x1coord),abs(self.y2coord-self.y1coord)))  # the size of the rect
		self.surface.set_alpha(128)               # alpha map
		self.surface.fill((self.color))           # this fills the entire surface
	def draw(self):
		DISPLAYSURF.blit(self.surface, (self.x1coord,self.y1coord))

class Area:
	def __init__(self, color, x1coord, y1coord, x2coord, y2coord):
		self.color = color
		self.x1coord = x1coord
		self.y1coord = y1coord
		self.x2coord = x2coord
		self.y2coord = y2coord
		self.rect = pygame.Rect(x1coord, y1coord, x2coord-x1coord, y2coord-y1coord)
		self.entities_on=pygame.sprite.Group()
		self.center_xcoord=(self.x1coord+self.x2coord)/2
		self.center_ycoord=(self.y1coord+self.y2coord)/2
		self.path=None
	def prepare(self):
		self.surface=pygame.Surface((abs(self.x2coord-self.x1coord),abs(self.y2coord-self.y1coord)))  # the size of the rect
		self.surface.set_alpha(128)                # alpha map
		self.surface.fill((self.color))           # this fills the entire surface
	def draw(self):
		DISPLAYSURF.blit(self.surface, (self.x1coord,self.y1coord))
	def shortest_path(self, thing):
		self.starting_node=(self.center_xcoord, self.center_ycoord)
		self.ending_node=(thing.current_area.center_xcoord,thing.current_area.center_ycoord)
		self.path=current_map.paths[self.starting_node, self.ending_node]
		
class Survivor(pygame.sprite.Sprite):
	def __init__(self, xcoord, ycoord, speed):
		pygame.sprite.Sprite.__init__(self)
		self.current_health=30
		self.max_health=30
		self.max_health_upgrades=[20,10,5]
		self.upgrade_max_health_cost=[50,25,12]
		self.current_armor=30
		self.max_armor=30
		self.max_armor_upgrades=[999,10,5]
		self.upgrade_max_armor_cost=[9999,25,12]
		self.money=9999
		self.walk_speed=4.5
		self.walk_speed_upgrades=[20,10,5]
		self.upgrade_walk_speed_cost=[50,25,12]
		self.speed=self.walk_speed
		self.strafe_percent=.75
		self.backwards_percent=.5
		self.angle_walk=0
		self.switched_rooms=True
		self.bullet_speed=10
		self.bullet_speed_upgrades=[20,10,900]
		self.upgrade_bullet_speed_cost=[50,25,12]
		self.move_up=False
		self.move_down=False
		self.move_left=False
		self.move_right=False
		self.feet_motion='walk'
		self.body_motion='idle'
		self.center_xcoord=xcoord
		self.center_ycoord=ycoord
		self.time_of_last_generated_body_state=0
		self.time_of_last_generated_feet_state=0
		self.current_body_state_number=0
		self.current_feet_state_number=0
		self.max_body_state_number=19
		self.max_feet_state_number=0
		self.body_image=Images['Characters/Survivor/handgun/idle0']
		self.feet_image=Images['Characters/Survivor/feet/idle0']
		self.current_room=None
		self.rotated_body_image=None
		self.angle=0
		self.update_body_state_image_delay=.02
		self.update_feet_state_image_delay=.02
		self.body_rect=self.body_image.get_rect(centerx=self.center_xcoord, centery=self.center_ycoord)
		self.feet_rect=self.feet_image.get_rect(centerx=self.center_xcoord, centery=self.center_ycoord)
		self.current_area=None
		self.switched_areas=True
		self.center_coords=(self.center_xcoord, self.center_ycoord)
		self.walking_rect=pygame.Rect(self.center_coords[0]-7.5, self.center_coords[1]-7.5, 15, 15)
		self.weapon=[weapon for weapon in GameState['weapons_collection'] if weapon.weapon_name=='handgun'][0]
		self.weapons=[weapon for weapon in GameState['weapons_collection']]
		self.images=Images
		self.current_survivor_body_state_number=0
		self.current_survivor_feet_state_number=0
	def rotate_survivor(self):
		# Rotate Body
		location = self.center_coords
		rotated_body_sprite = pygame.transform.rotate(self.body_image, -degrees(self.angle))
		self.body_rect=rotated_body_sprite.get_rect()
		self.body_rect.center = self.center_coords
		self.rect=self.body_rect

		#Rotate Feet and find feet update delay
		angle=(survivor.angle-survivor.angle_walk)%(2*pi)
		angle_to_rotate_survivor_feet=survivor.angle_walk
		if self.move_up == False and self.move_down == False and self.move_left == False and self.move_right == False:
			survivor.feet_motion='idle'
			survivor.max_feet_state_number=0
			angle_to_rotate_survivor_feet=survivor.angle
			survivor.update_feet_state_image_delay=.02
			update_body_state_image_delay=.02
		elif angle>=7*pi/4 or angle<=pi/4:
			survivor.feet_motion='walk'
			survivor.max_feet_state_number=19
			survivor.speed=self.walk_speed
			survivor.update_feet_state_image_delay=.05
			update_body_state_image_delay=.05
		elif angle>=5*pi/4 and angle<=7*pi/4:
			survivor.feet_motion='strafe_right'
			survivor.max_feet_state_number=19
			angle_to_rotate_survivor_feet=pi/2
			survivor.speed=self.walk_speed*self.strafe_percent
			survivor.update_feet_state_image_delay=.03
			update_body_state_image_delay=.03
		elif angle>=pi/4 and angle<=3*pi/4:
			angle_to_rotate_survivor_feet=3*pi/2
			survivor.feet_motion='strafe_left'
			survivor.max_feet_state_number=19
			angle_to_rotate_survivor_feet=pi/2
			survivor.speed=self.walk_speed*self.strafe_percent
			survivor.update_feet_state_image_delay=.03
			update_body_state_image_delay=.03
		elif angle>=3*pi/4 or angle<=5*pi/4:
			survivor.feet_motion='walk'
			survivor.max_feet_state_number=19
			survivor.speed=self.walk_speed*self.backwards_percent
			survivor.update_feet_state_image_delay=.03
			update_body_state_image_delay=.03
		
		# Reloading has a different update delay time
		if survivor.body_motion!='reload':
			survivor.update_body_state_image_delay=update_body_state_image_delay

		rotated_feet_sprite = pygame.transform.rotate(self.feet_image, -degrees(angle_to_rotate_survivor_feet))
		self.feet_rect=rotated_feet_sprite.get_rect()
		self.feet_rect.center=self.center_coords
		return rotated_body_sprite, rotated_feet_sprite
	def update_state(self): # updates the self state image and rotates it
		now=time.time()
		self.find_body_motion()
		if (self.time_of_last_generated_body_state==0) or (now-self.time_of_last_generated_body_state>=self.update_body_state_image_delay):
			self.time_of_last_generated_body_state = now # update the time of last self update to now
			self.current_body_state_number+=1
			self.current_body_state_number=self.current_body_state_number%(survivor.max_body_state_number+1)
			self.body_image=Images['Characters/Survivor/handgun/'+str(survivor.body_motion)+str(survivor.current_body_state_number)] # Find the image stored under the key generateed above

		if (self.time_of_last_generated_feet_state==0) or (now-self.time_of_last_generated_feet_state>=self.update_feet_state_image_delay):
			self.time_of_last_generated_feet_state = now # update the time of last self update to now
			self.current_feet_state_number+=1
			self.current_feet_state_number=self.current_feet_state_number%(survivor.max_feet_state_number+1)
			self.feet_image=Images['Characters/Survivor/feet/'+str(survivor.feet_motion)+str(survivor.current_feet_state_number)]

	def find_body_motion(self):
		if survivor.body_motion=='reload':
			if survivor.current_body_state_number==survivor.max_body_state_number and (survivor.weapon.current_mag_ammo==survivor.weapon.max_mag_ammo or survivor.weapon.current_weapon_ammo==0):
				survivor.body_motion=None
			elif survivor.current_body_state_number==survivor.max_body_state_number and survivor.weapon.current_mag_ammo!=survivor.weapon.max_mag_ammo:
				bullets_to_add=survivor.weapon.max_mag_ammo-survivor.weapon.current_mag_ammo
				if bullets_to_add>survivor.weapon.current_weapon_ammo:
					bullets_to_add=survivor.weapon.current_weapon_ammo
				survivor.weapon.current_mag_ammo+=bullets_to_add
				survivor.weapon.current_weapon_ammo-=bullets_to_add

		if survivor.body_motion==None:
			if not (self.move_up == False and self.move_down == False and self.move_left == False and self.move_right == False):
				survivor.body_motion='move'
				survivor.max_body_state_number=19
				survivor.current_body_state_number=0
			else:
				if GameState['MouseButtonDown']:
						survivor.body_motion='shoot'
						survivor.current_body_state_number=0
						survivor.max_body_state_number=2
						survivor.update_feet_state_image_delay=.1
				else:				
					survivor.body_motion='idle'
					survivor.update_body_state_image_delay=0.02
					survivor.max_body_state_number=0
					survivor.current_body_state_number=0
	def prepare(self):
		self.update_state()
		self.rotated_body_image, self.rotated_feet_image=self.rotate_survivor()
		self.mask = pygame.mask.from_surface(self.rotated_body_image,0)
		pygame.draw.rect(DISPLAYSURF, BLACK, self.walking_rect)
	def draw(self):
		DISPLAYSURF.blit(self.rotated_feet_image, self.feet_rect)
		DISPLAYSURF.blit(self.rotated_body_image, self.body_rect)
	def was_hit(self, zombie):
		damage_dealt=zombie.damage
		if self.current_armor>0:
			if self.current_armor>damage_dealt:
				self.current_armor-=damage_dealt
			else:
				damage_dealt-=self.current_armor
				self.current_armor=0
				self.current_health-=damage_dealt
		else:
			self.current_health-=damage_dealt
		if self.current_health<=0:
			pass

class Projectile(pygame.sprite.Sprite):
	def __init__(self, center_xcoord, center_ycoord, angle, ProjSpeed, bullet_number, total_number, weapon):
		pygame.sprite.Sprite.__init__(self, GameState['projectiles'])
		self.weapon_originated=weapon
		self.image=pygame.image.load('Bullets/bullet.png')
		self.width=5
		self.height=5
		self.remove_later=False
		self.image=pygame.transform.scale(self.image, (self.width, self.height))
		self.color = color
		self.center_xcoord = center_xcoord
		self.center_ycoord = center_ycoord
		self.rect=self.image.get_rect(centerx=self.center_xcoord, centery=self.center_ycoord)
		self.color = color
		self.angle = angle
		self.speed = ProjSpeed
		self.penetration = weapon.penetration
		self.rect = DISPLAYSURF.blit(self.image, self.rect)
		self.bullet_number=float(bullet_number)
		self.total_number=float(total_number)
		self.current_area=survivor.current_area
		self.switched_areas=True
		self.image=rotate_image(self, 'bullet')
		self.remove=False
		self.wall_check=None
		self.center_coords=(self.center_xcoord, self.center_ycoord)
	def prepare(self):
		self.wall_check=Wall_Check((self.center_xcoord, self.center_ycoord), (self.center_xcoord+cos(self.angle)*self.speed, self.center_ycoord+sin(self.angle)*self.speed), self.width)
		self.mask = pygame.mask.from_surface(self.image,0)
		self.rect.center=(self.center_xcoord, self.center_ycoord)
		self.wall_check.prepare()
	def draw(self):
		DISPLAYSURF.blit(self.image, self.rect)
	def hit(self, zombie):
		self.penetration-=zombie.penetration
	def update(self):
		if self.remove==True:
			self.kill()

class Zombie_Spawn:
	def __init__(self, xcoord, ycoord):
		self.xcoord=xcoord
		self.ycoord=ycoord
		self.area=None
	def find_area(self):
		# Finds the area that the spawn is in
		for area in current_map.areas:
			if self.xcoord>area.x1coord and self.xcoord<area.x2coord and self.ycoord>area.y1coord and self.ycoord<area.y2coord:
				self.area=area
				break

class Zombie(pygame.sprite.Sprite):
	def __init__(self, xcoord, ycoord, speed, area, max_number_of_walking_states, zombie_number, max_number_of_attacking_states, attack_state_number, attack_distance):
		pygame.sprite.Sprite.__init__(self, GameState['zombies_collection'])
		self.attack_distance=attack_distance
		self.attack_state_number=attack_state_number
		self.zombie_number=zombie_number
		self.current_state_number=0
		self.speed=speed
		self.damage=1
		self.center_xcoord = xcoord
		self.center_ycoord = ycoord
		self.image = Images['Characters/Zombies/Zombie'+str(zombie_number)+'/walk'+str(self.current_state_number)]
		self.rect=self.image.get_rect()
		self.body_motion='walk'
		self.bullets_in=pygame.sprite.Group()
		self.health=100
		self.penetration=5
		self.switched_rooms=True
		self.current_room=None
		self.angle=None
		self.rotated_image=None
		self.time_of_last_generated_state=0
		self.update_state_image_delay=.02
		self.current_survivor_state_number=2
		self.survivor_states_images={}
		self.max_number_of_walking_states=max_number_of_walking_states
		self.max_number_of_states=self.max_number_of_walking_states
		self.max_number_of_attacking_states=max_number_of_attacking_states
		self.current_area=area
		self.switched_areas=True
		self.following_path=False
		self.center_coords=(self.center_xcoord, self.center_ycoord)
		self.distance=distance(self.center_xcoord, self.center_ycoord, survivor.center_xcoord, survivor.center_ycoord)
	def prepare(self):
		self.image=update_zombie_state_image(self)
		self.angle=angle_finder(self.center_xcoord, self.center_ycoord , self.path[0][0], self.path[0][1])
		self.rotated_image = rotate_image(self, 'zombie')
		self.rect = self.rotated_image.get_rect(centerx=self.center_xcoord, centery=self.center_ycoord)
		self.mask = pygame.mask.from_surface(self.rotated_image,0)
		if self.body_motion=='attack' and self.current_state_number==self.attack_state_number:
			if pygame.sprite.collide_mask(self, survivor):
				survivor.was_hit(self)

	def draw(self):
		DISPLAYSURF.blit(self.rotated_image, (self.rect.left, self.rect.top))		
	def was_hit(self, bullet):
		if not self.bullets_in.has(bullet):
			self.bullets_in.add(bullet)
			self.health-=bullet.weapon_originated.damage
	def update_path(self):
		if (self.center_xcoord-self.attack_distance)<=survivor.center_xcoord and (self.center_xcoord+self.attack_distance)>=survivor.center_xcoord and (self.center_ycoord-self.attack_distance)<=survivor.center_ycoord and (self.center_ycoord+self.attack_distance)>=survivor.center_ycoord:
			if self.body_motion!='attack':
				self.body_motion='attack'
				self.current_state_number=0
				self.max_number_of_states=self.max_number_of_attacking_states
		elif self.body_motion=='attack' and self.current_state_number==self.max_number_of_states-1:
			self.body_motion='walk'
			self.current_state_number=0
			self.max_number_of_states=self.max_number_of_walking_states
		if len(self.path)==1:
			self.path=[(survivor.center_xcoord,survivor.center_ycoord)]

class Wall_Check:
	def __init__(self, node1, node2, width):
		self.image=pygame.image.load('black_image.png').convert_alpha()
		self.node1=node1
		self.node2=node2
		self.distanc=distance(self.node1[0], self.node1[1], self.node2[0], self.node2[1])
		self.angle=angle=angle_finder(self.node1[0], self.node1[1], self.node2[0], self.node2[1])
		self.width=width
		self.height=abs(node2[1]-node2[1])
		self.image=pygame.transform.scale(self.image, (self.width,int(self.distanc)))
		self.centerx=abs(node1[0]-node2[0])
		self.centery=abs(node1[1]-node2[1])
		self.image=rotate_image(self, 'wall_check')
		self.rect=self.image.get_rect()
		self.xcoord=min([self.node1[0], self.node2[0]])
		self.ycoord=min([self.node1[1], self.node2[1]])
		self.rect=self.image.get_rect(left=self.xcoord, top=self.ycoord)
	def prepare(self):
		self.mask=pygame.mask.from_surface(self.image)
	def draw(self):
		DISPLAYSURF.blit(self.image, (self.rect))

class Weapon(pygame.sprite.Sprite):
	def __init__(self, weapon_name, shooting_type, weapon_image, price, price_per_mag, fire_rate, bullet_image, weapon_size, damage, max_mag_ammo, max_weapon_ammo, weapon_scale, penetration, upgrade_damage_cost, upgrade_penetration_cost, upgrade_max_mag_ammo_cost, upgrade_max_weapon_ammo_cost):
		pygame.sprite.Sprite.__init__(self, GameState['weapons_collection'])
		self.upgrade_damage_cost=upgrade_damage_cost
		self.upgrade_penetration_cost=upgrade_penetration_cost
		self.upgrade_max_mag_ammo_cost=upgrade_max_mag_ammo_cost
		self.upgrade_max_weapon_ammo_cost=upgrade_max_weapon_ammo_cost		
		self.damage_upgrades=[15,14,13,12,11]
		self.penetration_upgrades=[5,4,3,2,1]
		self.max_mag_ammo_upgrades=[2,2,2,2]
		self.max_weapon_ammo_upgrades=[20,20,20,20]
		self.weapon_name=weapon_name
		self.penetration=penetration
		self.shooting_type=shooting_type
		self.weapon_image1=pygame.image.load(weapon_image)
		self.weapon_image=pygame.transform.scale(pygame.image.load(weapon_image),weapon_scale)
		self.bullet_image=None
		self.weapon_size=weapon_size
		self.damage=damage
		self.price=price
		self.price_per_mag=price_per_mag
		self.fire_rate=fire_rate
		self.bullet_delay=1./self.fire_rate
		self.DPS=self.damage*self.fire_rate
		self.bullets=pygame.sprite.Group()
		self.last_time_bullet_shot=0
		self.bullet_shot=False
		self.current_mag_ammo=12
		self.max_mag_ammo=max_mag_ammo
		self.current_weapon_ammo=80
		self.max_weapon_ammo=max_weapon_ammo
	def bullet_handler(self):
		if self.shooting_type=='automatic':
			if survivor.body_motion=='shoot' and survivor.current_body_state_number==0:
				survivor.body_motion=None
			self.x_distance=pol2cart(self.distance_from_survivor_to_tip_of_weapon, self.angle_from_survivor_to_tip_of_weapon+survivor.angle)[0] # from survivor head to top of weapon
			self.y_distance=pol2cart(self.distance_from_survivor_to_tip_of_weapon, self.angle_from_survivor_to_tip_of_weapon+survivor.angle)[1] # from survivor head to tip of weapon
			self.new_projectile_coords=(self.x_distance+survivor.center_xcoord, self.y_distance+survivor.center_ycoord)
			now=time.time()
			if (now-self.last_time_bullet_shot>=self.bullet_delay):
				if GameState['MouseButtonDown']:
					self.last_time_bullet_shot=now-self.bullet_delay
					total_number=int(round((now-self.last_time_bullet_shot)/self.bullet_delay))
					bullets_fired=0
					for bullet_number in range(1,total_number+1):
						if self.current_mag_ammo!=0 and survivor.body_motion!='reload':
							survivor.body_motion='shoot'
							survivor.current_body_state_number=0
							survivor.max_body_state_number=2
							survivor.update_feet_state_image_delay=.1
							bullet = Projectile(self.new_projectile_coords[0], self.new_projectile_coords[1],survivor.angle, survivor.bullet_speed, bullet_number, total_number, self)
							bullet.current_area=find_current_location(bullet.center_coords, current_map.areas)
							bullet.current_area.entities_on.add(bullet)
							self.current_mag_ammo-=1
							bullets_fired+=1
						else:
							break
				if survivor.weapon.current_weapon_ammo>0 and survivor.weapon.current_mag_ammo==0 and survivor.body_motion!='reload':
					survivor.body_motion='reload'
					survivor.max_body_state_number=26
					survivor.current_body_state_number=0
					survivor.update_body_state_image_delay=.05
				self.last_time_bullet_shot=now
				self.bullet_shot=True
			if GameState['MouseButtonDown']==False and self.bullet_shot:
				self.last_time_bullet_shot=now
				self.bullet_shot=False

		elif self.shooting_type=='semi automatic':
			if survivor.body_motion=='shoot' and survivor.current_body_state_number==0:
				survivor.body_motion=None
			self.x_distance=pol2cart(self.distance_from_survivor_to_tip_of_weapon, self.angle_from_survivor_to_tip_of_weapon+survivor.angle)[0] # from survivor head to top of weapon
			self.y_distance=pol2cart(self.distance_from_survivor_to_tip_of_weapon, self.angle_from_survivor_to_tip_of_weapon+survivor.angle)[1] # from survivor head to tip of weapon
			self.new_projectile_coords=(self.x_distance+survivor.center_xcoord, self.y_distance+survivor.center_ycoord)
			if GameState['MouseButtonDown']:
				total_number=1
				bullets_fired=0
				for bullet_number in range(1,total_number+1):
					if self.current_mag_ammo!=0 and survivor.body_motion!='reload':
						survivor.body_motion='shoot'
						survivor.current_body_state_number=0
						survivor.max_body_state_number=2
						survivor.update_feet_state_image_delay=.1
						bullet = Projectile(self.new_projectile_coords[0], self.new_projectile_coords[1], survivor.angle, survivor.bullet_speed, bullet_number, total_number, self)
						bullet.current_area=find_current_location(bullet.center_coords, current_map.areas)
						bullet.current_area.entities_on.add(bullet)
						self.current_mag_ammo-=1
						bullets_fired+=1
						GameState['MouseButtonDown']=False
					else:
						break
			if survivor.weapon.current_weapon_ammo>0 and survivor.weapon.current_mag_ammo==0 and survivor.body_motion!='reload':
				survivor.body_motion='reload'
				survivor.max_body_state_number=26
				survivor.current_body_state_number=0
				survivor.update_body_state_image_delay=.05
			self.bullet_shot=True
			if GameState['MouseButtonDown']==False and self.bullet_shot:
				self.bullet_shot=False	

name='handgun'
shooting='semi automatic'
filename='Guns/CartoonGlock.png'
price=10
price_per_mag=2
fire_rate=1
bullet_image='bullet.png'
weapon_size=(15,10)
damage=100
max_mag_ammo=12
max_weapon_ammo=80
weapon_scale=100,100
penetration=10
upgrade_damage_cost=10
upgrade_penetration_cost=5
upgrade_max_mag_ammo_cost=5
upgrade_max_weapon_ammo_cost=3
Weapon(name, shooting, filename, price,price_per_mag, fire_rate, bullet_image, weapon_size, damage, max_mag_ammo, max_weapon_ammo, weapon_scale, penetration, upgrade_damage_cost, upgrade_penetration_cost, upgrade_max_mag_ammo_cost, upgrade_max_weapon_ammo_cost)

name='ak-47'
shooting='semi automatic'
filename='Guns/CartoonGlock.png'
price=10
price_per_mag=2
fire_rate=1
bullet_image='bullet.png'
weapon_size=(0,10)
damage=100
max_mag_ammo=12
max_weapon_ammo=80
weapon_scale=100,100
penetration=1
upgrade_damage_cost=10
upgrade_penetration_cost=5
upgrade_max_mag_ammo_cost=5
upgrade_max_weapon_ammo_cost=3
Weapon(name, shooting, filename, price,price_per_mag, fire_rate, bullet_image, weapon_size, damage, max_mag_ammo, max_weapon_ammo, weapon_scale, penetration, upgrade_damage_cost, upgrade_penetration_cost, upgrade_max_mag_ammo_cost, upgrade_max_weapon_ammo_cost)

GameState['grenades']=pygame.sprite.Group()

class Grenade(pygame.sprite.Sprite):
	def __init__(self, image, ProjSpeed, damage, scale):
		pygame.sprite.Sprite.__init__(self, GameState['grenades'])
		self.image1=pygame.image.load(image)
		self.image=pygame.transform.scale(pygame.image.load(image), scale)
		self.center_xcoord=None
		self.center_ycoord=None
		self.angle=None
		self.speed=ProjSpeed
		self.damage=damage
		self.damage_upgrades=[1,2,3,4]
		self.upgrade_damage_cost=3
		self.penetration=penetration
		self.penetration_upgrades=[1,2,3,4]
		self.upgrade_penetration_cost=3
		self.max_grenade_ammo=max_mag_ammo
		self.max_grenade_ammo_upgrades=[1,2,3,4]
		self.upgrade_max_grenade_ammo_cost=3
	def draw(self):
		DISPLAYSURF.blit(self.image, (self.center_xcoord,self.center_ycoord))

Grenade('Grenades/Grenade1/grenade1.png', 2, 2, (15,30))

class Round:
	def __init__(self, cap):
		self.zombie_cap=5
		self.zombie_quantities=[0,0,0,0]
		self.zombie_delays=[1,1,0,0]
		self.zombie_last_times=[0,0,0,0]
		self.delays_doubled=False
	def zombie_handler(self):
		# Generates zombies
		now=time.time()
		for i, zombie_quantity in enumerate(self.zombie_quantities):
			if zombie_quantity>0 and ((self.zombie_last_times[i]==0) or ((now-self.zombie_last_times[i]>self.zombie_delays[i]))):
				generated_zombie=self.zombie_generater(i)
				generated_zombie.current_room=find_current_location((generated_zombie.center_xcoord, generated_zombie.center_ycoord), current_map.rooms)
				generated_zombie.current_room.entities_on.add(generated_zombie)
				generated_zombie.current_area=find_current_location((generated_zombie.center_xcoord, generated_zombie.center_ycoord), current_map.areas)
				generated_zombie.path=deepcopy(current_map.paths[(generated_zombie.current_area.center_xcoord,generated_zombie.current_area.center_ycoord),(survivor.current_area.center_xcoord, survivor.current_area.center_ycoord)][0])
				generated_zombie.distance=current_map.paths[(generated_zombie.current_area.center_xcoord,generated_zombie.current_area.center_ycoord),(survivor.current_area.center_xcoord, survivor.current_area.center_ycoord)][1]
				self.zombie_last_times[i]=now
				self.zombie_quantities[i]-=1
		if len(GameState['zombies_collection'])>=current_round.zombie_cap and not self.delays_doubled:
			self.zombie_delays=[i*3 for i in self.zombie_delays]
			self.delays_doubled=True
		elif len(GameState['zombies_collection'])<current_round.zombie_cap and self.delays_doubled:
			self.zombie_delays=[i/3 for i in self.zombie_delays]
			self.delays_doubled=False
	def zombie_generater(self, number):
		rand_number=int(random.random()*len(current_map.zombie_spawns))
		if number==0:
			generated_zombie=Zombie(current_map.zombie_spawns[rand_number].xcoord, current_map.zombie_spawns[rand_number].ycoord, 2.5, current_map.zombie_spawns[rand_number], 16, number, 8, 6, 20)
		if number==1:
			generated_zombie=Zombie(current_map.zombie_spawns[rand_number].xcoord, current_map.zombie_spawns[rand_number].ycoord, 4, current_map.zombie_spawns[rand_number], 32, number, 20, 12, 23)		
		return generated_zombie

GameState['maps']=[]
rooms=[[(184,98),(620,314)], [(184,314),(620,410)], [(184,410),(430,590)], [(430,410),(557,590)], [(557,410),(814,590)], [(814,410),(975,590)], [(975,345),(1157,590)], [(620,218),(1157,345)], [(620,98),(1157,218)], [(620,345),(975,410)]]
walls=[[(164, 98),(184, 590)], [(164, 590), (568,609)], [(164,78),(1175,98)], [(1155,98),(1175, 609)], [(804,590),(1155,609)], [(965, 335),(1111,353)], [(965,353),(984,545)], [(617,98),(627,317)],[(681,211),(1107,222)], [(235,307),(562,318)],[(184,404),(370,413)],[(425,404),(435,590)],[(549,398),(568,547)],[(568,398),(804,418)],[(804,398),(824,547)], [(558,570),(813,595)]]
nodes=[(231,325),(231,302), (568,325), (568,301),(375,396), (375,420), (441,397), (420,396), (542, 389), (543, 555), (573, 556), (831, 392), (611, 324), (632, 326), (673, 230), (672, 206), (1115, 206), (1114, 228), (959, 327), (796, 557), (827, 560),(959, 551),(1120, 330),(1120, 362), (989,553)]
areas=[[(806, 546), (814, 571)], [(549, 546), (559, 590)], [(559, 546), (568, 570)], [(813, 546), (822, 590)], [(164, 98), (278, 152)], [(278, 98), (392, 152)], [(164, 152), (278, 206)], [(278, 152), (392, 206)], [(392, 98), (506, 152)], [(506, 98), (620, 152)], [(392, 152), (506, 206)], [(506, 152), (620, 206)], [(164, 206), (278, 260)], [(278, 206), (392, 260)], [(164, 260), (278, 314)], [(278, 260), (392, 314)], [(392, 206), (506, 260)], [(506, 206), (620, 260)], [(392, 260), (506, 314)], [(506, 260), (620, 314)], [(184, 314), (238, 337)], [(238, 314), (293, 337)], [(184, 337), (238, 360)], [(238, 337), (293, 360)], [(293, 314), (347, 337)], [(347, 314), (402, 337)], [(293, 337), (347, 360)], [(347, 337), (402, 360)], [(184, 360), (238, 383)], [(238, 360), (293, 383)], [(184, 383), (238, 407)], [(238, 383), (293, 407)], [(293, 360), (347, 383)], [(347, 360), (402, 383)], [(293, 383), (347, 407)], [(347, 383), (402, 407)], [(402, 314), (439, 337)], [(439, 314), (476, 337)], [(402, 337), (439, 360)], [(439, 337), (476, 360)], [(476, 314), (513, 337)], [(513, 314), (551, 337)], [(476, 337), (513, 360)], [(513, 337), (551, 360)], [(402, 360), (439, 383)], [(439, 360), (476, 383)], [(402, 383), (439, 407)], [(439, 383), (476, 407)], [(476, 360), (513, 383)], [(513, 360), (551, 383)], [(476, 383), (513, 407)], [(513, 383), (551, 407)], [(551, 314), (568, 335)], [(568, 314), (585, 335)], [(551, 335), (568, 356)], [(568, 335), (585, 356)], [(585, 314), (602, 335)], [(602, 314), (620, 335)], [(585, 335), (602, 356)], [(602, 335), (620, 356)], [(551, 356), (568, 377)], [(568, 356), (585, 377)], [(551, 377), (568, 399)], [(568, 377), (585, 399)], [(585, 356), (602, 377)], [(602, 356), (620, 377)], [(585, 377), (602, 399)], [(602, 377), (620, 399)], [(184, 411), (245, 455)], [(245, 411), (307, 455)], [(184, 455), (245, 500)], [(245, 455), (307, 500)], [(307, 411), (368, 455)], [(368, 411), (430, 455)], [(307, 455), (368, 500)], [(368, 455), (430, 500)], [(184, 500), (245, 545)], [(245, 500), (307, 545)], [(184, 545), (245, 590)], [(245, 545), (307, 590)], [(307, 500), (368, 545)], [(368, 500), (430, 545)], [(307, 545), (368, 590)], [(368, 545), (430, 590)], [(430, 407), (446, 430)], [(446, 407), (462, 430)], [(430, 430), (446, 453)], [(446, 430), (462, 453)], [(462, 407), (478, 430)], [(478, 407), (494, 430)], [(462, 430), (478, 453)], [(478, 430), (494, 453)], [(430, 453), (446, 476)], [(446, 453), (462, 476)], [(430, 476), (446, 500)], [(446, 476), (462, 500)], [(462, 453), (478, 476)], [(478, 453), (494, 476)], [(462, 476), (478, 500)], [(478, 476), (494, 500)], [(430, 500), (446, 522)], [(446, 500), (462, 522)], [(430, 522), (446, 545)], [(446, 522), (462, 545)], [(462, 500), (478, 522)], [(478, 500), (494, 522)], [(462, 522), (478, 545)], [(478, 522), (494, 545)], [(430, 545), (446, 567)], [(446, 545), (462, 567)], [(430, 567), (446, 590)], [(446, 567), (462, 590)], [(462, 545), (478, 567)], [(478, 545), (494, 567)], [(462, 567), (478, 590)], [(478, 567), (494, 590)], [(494, 407), (508, 430)], [(508, 407), (522, 430)], [(494, 430), (508, 453)], [(508, 430), (522, 453)], [(522, 407), (536, 430)], [(536, 407), (550, 430)], [(522, 430), (536, 453)], [(536, 430), (550, 453)], [(494, 453), (508, 476)], [(508, 453), (522, 476)], [(494, 476), (508, 500)], [(508, 476), (522, 500)], [(522, 453), (536, 476)], [(536, 453), (550, 476)], [(522, 476), (536, 500)], [(536, 476), (550, 500)], [(494, 500), (508, 522)], [(508, 500), (522, 522)], [(494, 522), (508, 545)], [(508, 522), (522, 545)], [(522, 500), (536, 522)], [(536, 500), (550, 522)], [(522, 522), (536, 545)], [(536, 522), (550, 545)], [(494, 545), (508, 567)], [(508, 545), (522, 567)], [(494, 567), (508, 590)], [(508, 567), (522, 590)], [(522, 545), (536, 567)], [(536, 545), (550, 567)], [(522, 567), (536, 590)], [(536, 567), (550, 590)], [(568, 417), (597, 437)], [(597, 417), (627, 437)], [(568, 437), (597, 458)], [(597, 437), (627, 458)], [(627, 417), (656, 437)], [(656, 417), (686, 437)], [(627, 437), (656, 458)], [(656, 437), (686, 458)], [(568, 458), (597, 479)], [(597, 458), (627, 479)], [(568, 479), (597, 500)], [(597, 479), (627, 500)], [(627, 458), (656, 479)], [(656, 458), (686, 479)], [(627, 479), (656, 500)], [(656, 479), (686, 500)], [(686, 417), (716, 437)], [(716, 417), (746, 437)], [(686, 437), (716, 458)], [(716, 437), (746, 458)], [(746, 417), (776, 437)], [(776, 417), (806, 437)], [(746, 437), (776, 458)], [(776, 437), (806, 458)], [(686, 458), (716, 479)], [(716, 458), (746, 479)], [(686, 479), (716, 500)], [(716, 479), (746, 500)], [(746, 458), (776, 479)], [(776, 458), (806, 479)], [(746, 479), (776, 500)], [(776, 479), (806, 500)], [(568, 500), (597, 517)], [(597, 500), (627, 517)], [(568, 517), (597, 535)], [(597, 517), (627, 535)], [(627, 500), (656, 517)], [(656, 500), (686, 517)], [(627, 517), (656, 535)], [(656, 517), (686, 535)], [(568, 535), (597, 553)], [(597, 535), (627, 553)], [(568, 553), (597, 571)], [(597, 553), (627, 571)], [(627, 535), (656, 553)], [(656, 535), (686, 553)], [(627, 553), (656, 571)], [(656, 553), (686, 571)], [(686, 500), (716, 517)], [(716, 500), (746, 517)], [(686, 517), (716, 535)], [(716, 517), (746, 535)], [(746, 500), (776, 517)], [(776, 500), (806, 517)], [(746, 517), (776, 535)], [(776, 517), (806, 535)], [(686, 535), (716, 553)], [(716, 535), (746, 553)], [(686, 553), (716, 571)], [(716, 553), (746, 571)], [(746, 535), (776, 553)], [(776, 535), (806, 553)], [(746, 553), (776, 571)], [(776, 553), (806, 571)], [(369, 407), (383, 408)], [(383, 407), (397, 408)], [(369, 408), (383, 410)], [(383, 408), (397, 410)], [(397, 407), (411, 408)], [(411, 407), (426, 408)], [(397, 408), (411, 410)], [(411, 408), (426, 410)], [(369, 410), (383, 412)], [(383, 410), (397, 412)], [(369, 412), (383, 414)], [(383, 412), (397, 414)], [(397, 410), (411, 412)], [(411, 410), (426, 412)], [(397, 412), (411, 414)], [(411, 412), (426, 414)], [(822, 400), (858, 447)], [(858, 400), (894, 447)], [(822, 447), (858, 495)], [(858, 447), (894, 495)], [(894, 400), (930, 447)], [(930, 400), (966, 447)], [(894, 447), (930, 495)], [(930, 447), (966, 495)], [(822, 495), (858, 542)], [(858, 495), (894, 542)], [(822, 542), (858, 590)], [(858, 542), (894, 590)], [(894, 495), (930, 542)], [(930, 495), (966, 542)], [(894, 542), (930, 590)], [(930, 542), (966, 590)], [(966, 544), (969, 555)], [(969, 544), (973, 555)], [(966, 555), (969, 567)], [(969, 555), (973, 567)], [(973, 544), (977, 555)], [(977, 544), (981, 555)], [(973, 555), (977, 567)], [(977, 555), (981, 567)], [(966, 567), (969, 578)], [(969, 567), (973, 578)], [(966, 578), (969, 590)], [(969, 578), (973, 590)], [(973, 567), (977, 578)], [(977, 567), (981, 578)], [(973, 578), (977, 590)], [(977, 578), (981, 590)], [(981, 353), (1002, 381)], [(1002, 353), (1023, 381)], [(981, 381), (1002, 410)], [(1002, 381), (1023, 410)], [(1023, 353), (1044, 381)], [(1044, 353), (1066, 381)], [(1023, 381), (1044, 410)], [(1044, 381), (1066, 410)], [(981, 410), (1002, 439)], [(1002, 410), (1023, 439)], [(981, 439), (1002, 468)], [(1002, 439), (1023, 468)], [(1023, 410), (1044, 439)], [(1044, 410), (1066, 439)], [(1023, 439), (1044, 468)], [(1044, 439), (1066, 468)], [(1066, 353), (1088, 381)], [(1088, 353), (1111, 381)], [(1066, 381), (1088, 410)], [(1088, 381), (1111, 410)], [(1111, 353), (1134, 381)], [(1134, 353), (1157, 381)], [(1111, 381), (1134, 410)], [(1134, 381), (1157, 410)], [(1066, 410), (1088, 439)], [(1088, 410), (1111, 439)], [(1066, 439), (1088, 468)], [(1088, 439), (1111, 468)], [(1111, 410), (1134, 439)], [(1134, 410), (1157, 439)], [(1111, 439), (1134, 468)], [(1134, 439), (1157, 468)], [(981, 468), (1002, 498)], [(1002, 468), (1023, 498)], [(981, 498), (1002, 529)], [(1002, 498), (1023, 529)], [(1023, 468), (1044, 498)], [(1044, 468), (1066, 498)], [(1023, 498), (1044, 529)], [(1044, 498), (1066, 529)], [(981, 529), (1002, 559)], [(1002, 529), (1023, 559)], [(981, 559), (1002, 590)], [(1002, 559), (1023, 590)], [(1023, 529), (1044, 559)], [(1044, 529), (1066, 559)], [(1023, 559), (1044, 590)], [(1044, 559), (1066, 590)], [(1066, 468), (1088, 498)], [(1088, 468), (1111, 498)], [(1066, 498), (1088, 529)], [(1088, 498), (1111, 529)], [(1111, 468), (1134, 498)], [(1134, 468), (1157, 498)], [(1111, 498), (1134, 529)], [(1134, 498), (1157, 529)], [(1066, 529), (1088, 559)], [(1088, 529), (1111, 559)], [(1066, 559), (1088, 590)], [(1088, 559), (1111, 590)], [(1111, 529), (1134, 559)], [(1134, 529), (1157, 559)], [(1111, 559), (1134, 590)], [(1134, 559), (1157, 590)], [(620, 218), (664, 249)], [(664, 218), (709, 249)], [(620, 249), (664, 281)], [(664, 249), (709, 281)], [(709, 218), (754, 249)], [(754, 218), (799, 249)], [(709, 249), (754, 281)], [(754, 249), (799, 281)], [(620, 281), (664, 313)], [(664, 281), (709, 313)], [(620, 313), (664, 345)], [(664, 313), (709, 345)], [(709, 281), (754, 313)], [(754, 281), (799, 313)], [(709, 313), (754, 345)], [(754, 313), (799, 345)], [(799, 218), (843, 247)], [(843, 218), (888, 247)], [(799, 247), (843, 277)], [(843, 247), (888, 277)], [(888, 218), (933, 247)], [(933, 218), (978, 247)], [(888, 247), (933, 277)], [(933, 247), (978, 277)], [(799, 277), (843, 307)], [(843, 277), (888, 307)], [(799, 307), (843, 337)], [(843, 307), (888, 337)], [(888, 277), (933, 307)], [(933, 277), (978, 307)], [(888, 307), (933, 337)], [(933, 307), (978, 337)], [(799, 337), (840, 339)], [(840, 337), (882, 339)], [(799, 339), (840, 341)], [(840, 339), (882, 341)], [(882, 337), (924, 339)], [(924, 337), (966, 339)], [(882, 339), (924, 341)], [(924, 339), (966, 341)], [(799, 341), (840, 343)], [(840, 341), (882, 343)], [(799, 343), (840, 345)], [(840, 343), (882, 345)], [(882, 341), (924, 343)], [(924, 341), (966, 343)], [(882, 343), (924, 345)], [(924, 343), (966, 345)], [(978, 218), (1022, 247)], [(1022, 218), (1067, 247)], [(978, 247), (1022, 277)], [(1022, 247), (1067, 277)], [(1067, 218), (1112, 247)], [(1112, 218), (1157, 247)], [(1067, 247), (1112, 277)], [(1112, 247), (1157, 277)], [(978, 277), (1022, 307)], [(1022, 277), (1067, 307)], [(978, 307), (1022, 337)], [(1022, 307), (1067, 337)], [(1067, 277), (1112, 307)], [(1112, 277), (1157, 307)], [(1067, 307), (1112, 337)], [(1112, 307), (1157, 337)], [(1108, 337), (1120, 341)], [(1120, 337), (1132, 341)], [(1108, 341), (1120, 345)], [(1120, 341), (1132, 345)], [(1132, 337), (1144, 341)], [(1144, 337), (1157, 341)], [(1132, 341), (1144, 345)], [(1144, 341), (1157, 345)], [(1108, 345), (1120, 349)], [(1120, 345), (1132, 349)], [(1108, 349), (1120, 353)], [(1120, 349), (1132, 353)], [(1132, 345), (1144, 349)], [(1144, 345), (1157, 349)], [(1132, 349), (1144, 353)], [(1144, 349), (1157, 353)], [(620, 98), (664, 128)], [(664, 98), (709, 128)], [(620, 128), (664, 158)], [(664, 128), (709, 158)], [(709, 98), (754, 128)], [(754, 98), (799, 128)], [(709, 128), (754, 158)], [(754, 128), (799, 158)], [(620, 158), (664, 188)], [(664, 158), (709, 188)], [(620, 188), (664, 218)], [(664, 188), (709, 218)], [(709, 158), (754, 188)], [(754, 158), (799, 188)], [(709, 188), (754, 218)], [(754, 188), (799, 218)], [(799, 98), (843, 128)], [(843, 98), (888, 128)], [(799, 128), (843, 158)], [(843, 128), (888, 158)], [(888, 98), (933, 128)], [(933, 98), (978, 128)], [(888, 128), (933, 158)], [(933, 128), (978, 158)], [(799, 158), (843, 188)], [(843, 158), (888, 188)], [(799, 188), (843, 218)], [(843, 188), (888, 218)], [(888, 158), (933, 188)], [(933, 158), (978, 188)], [(888, 188), (933, 218)], [(933, 188), (978, 218)], [(978, 98), (1022, 128)], [(1022, 98), (1067, 128)], [(978, 128), (1022, 158)], [(1022, 128), (1067, 158)], [(1067, 98), (1112, 128)], [(1112, 98), (1157, 128)], [(1067, 128), (1112, 158)], [(1112, 128), (1157, 158)], [(978, 158), (1022, 188)], [(1022, 158), (1067, 188)], [(978, 188), (1022, 218)], [(1022, 188), (1067, 218)], [(1067, 158), (1112, 188)], [(1112, 158), (1157, 188)], [(1067, 188), (1112, 218)], [(1112, 188), (1157, 218)], [(620, 345), (664, 358)], [(664, 345), (709, 358)], [(620, 358), (664, 372)], [(664, 358), (709, 372)], [(709, 345), (753, 358)], [(753, 345), (798, 358)], [(709, 358), (753, 372)], [(753, 358), (798, 372)], [(620, 372), (664, 386)], [(664, 372), (709, 386)], [(620, 386), (664, 400)], [(664, 386), (709, 400)], [(709, 372), (753, 386)], [(753, 372), (798, 386)], [(709, 386), (753, 400)], [(753, 386), (798, 400)], [(798, 345), (840, 358)], [(840, 345), (882, 358)], [(798, 358), (840, 372)], [(840, 358), (882, 372)], [(882, 345), (924, 358)], [(924, 345), (966, 358)], [(882, 358), (924, 372)], [(924, 358), (966, 372)], [(798, 372), (840, 386)], [(840, 372), (882, 386)], [(798, 386), (840, 400)], [(840, 386), (882, 400)], [(882, 372), (924, 386)], [(924, 372), (966, 386)], [(882, 386), (924, 400)], [(924, 386), (966, 400)]]

map_1=Map(pygame.image.load('Maps/map1.png'), [(200,200),(300,300)], rooms, areas, (-370,-200), walls, nodes)
GameState['maps'].append(map_1)

GameState['rounds']=[]
round_1=Round(1)
GameState['rounds'].append(round_1)

current_map=GameState['maps'][0]
current_round=GameState['rounds'][0]
for zombie_spawn in current_map.zombie_spawns:
	zombie_spawn.find_area()

survivor = Survivor(250, 350, 3)
survivor.current_room=find_current_location((survivor.center_xcoord, survivor.center_ycoord), current_map.rooms)
survivor.current_area=find_current_location((survivor.center_xcoord, survivor.center_ycoord), current_map.areas)

survivor.weapon.distance_from_survivor_to_tip_of_weapon=distance(survivor.center_xcoord, survivor.center_ycoord, survivor.center_xcoord+survivor.weapon.weapon_size[0], survivor.center_ycoord+survivor.weapon.weapon_size[1])
survivor.weapon.angle_from_survivor_to_tip_of_weapon=angle_finder(survivor.center_xcoord, survivor.center_ycoord, survivor.center_xcoord+survivor.weapon.weapon_size[0], survivor.center_ycoord+survivor.weapon.weapon_size[1])


# g=deepcopy(current_map.original_graph)

# for area in current_map.areas:
# 	node=(area.center_xcoord,area.center_ycoord)
# 	g.add_vertex((area.center_xcoord,area.center_ycoord))

# a=0
# b=g.num_vertices**2
# for node1 in g:
# 	for node2 in g:
# 		starting_node=node1.id
# 		ending_node=node2.id
# 		if not (round(ending_node[0]),round(ending_node[1]))==(round(starting_node[0]), round(starting_node[1])):
# 			wall_check=Wall_Check((round(starting_node[0]), round(starting_node[1])), (round(ending_node[0]),round(ending_node[1])), 1)
# 			walls_hit = pygame.sprite.spritecollide(wall_check, current_map.walls, False, pygame.sprite.collide_mask)
# 			if not walls_hit:
# 				distanc=distance(starting_node[0], starting_node[1], ending_node[0], ending_node[1])
# 				g.add_edge(starting_node, ending_node, distanc)
# 		print a,b
# 		a+=1

# current_map.graph=g
# current_map.original_graph=g

# with open('map_1_graph.pkl', 'wb') as output:
#     pickle.dump(g, output, pickle.HIGHEST_PROTOCOL)

with open('map_1_graph.pkl', 'rb') as input:
    current_map.graph = pickle.load(input)

with open('map_1_graph.pkl', 'rb') as input:
    current_map.original_graph = pickle.load(input)

# paths={}

# i=0
# a=0
# b=current_map.graph.num_vertices**2
# for node1 in current_map.graph:
# 	current_map.graph=deepcopy(current_map.original_graph)
# 	for node2 in current_map.graph:
# 		starting_node=node1.id
# 		ending_node=node2.id
# 		graph.dijkstra(current_map.graph, current_map.graph.get_vertex(starting_node), current_map.graph.get_vertex(ending_node))
# 		target = current_map.graph.get_vertex(ending_node)
# 		path = [target.get_id()]
# 		graph.shortest(target, path)
# 		path = path[::-1]
# 		paths[starting_node, ending_node]=path
# 		a+=1
# 		print a, b

# with open('map_1_paths.pkl', 'wb') as output:
#     pickle.dump(paths, output, pickle.HIGHEST_PROTOCOL)

# with open('map_1_paths.pkl', 'rb') as input:
#     current_map.paths = pickle.load(input)

# for key in current_map.paths:
# 	total_d=0
# 	for i in range(0, len(current_map.paths[key])-1):
# 		total_d+=distance(current_map.paths[key][i][0], current_map.paths[key][i][1], current_map.paths[key][i+1][0], current_map.paths[key][i+1][1])
# 	current_map.paths[key]=[current_map.paths[key], total_d]

# with open('map_1_paths.pkl', 'wb') as output:
#     pickle.dump(current_map.paths, output, pickle.HIGHEST_PROTOCOL)

with open('map_1_paths.pkl', 'rb') as input:
    current_map.paths = pickle.load(input)

# i=0
# for area in current_map.areas:
# 	area.shortest_path(survivor)
# 	i, len(current_map.areas)
# 	i+=1

# for area in current_map.areas:
# 	area.surface=None
# 	area.mask=None

# with open('map_1_areas.pkl', 'wb') as output:
#     pickle.dump(current_map.areas, output, pickle.HIGHEST_PROTOCOL)

with open('map_1_areas.pkl', 'rb') as input:
    current_map.areas = pickle.load(input)

current_map=GameState['maps'][0]

for area in current_map.areas:
	area.prepare()
for room in current_map.rooms:
	room.prepare()
for wall in current_map.rooms:
	room.prepare()

for index in range(0,len(current_map.areas)):
	current_map.nodes.append((current_map.areas[index].center_xcoord,current_map.areas[index].center_ycoord))

def main():
	pygame.init()
	global fpsClock, DISPLAYSURF, GameState, survivor, current_map, player_tab, weapons_tab, explosives_tab, turrets_tab
	# Game
	player_tab=Player_Tab()
	weapons_tab=Weapons_Tab()
	explosives_tab=Explosives_Tab()
	turrets_tab=Turrets_Tab()
	GameState['active_tab']=player_tab
	GameState['active_tab'].color=OXFORDBLUE
	pause=False
	while True:
		GameState['events']=pygame.event.get()
		# Look for pause or quit
		for event in GameState['events']:
			if event.type==MOUSEMOTION:  # If mouse was pressed, updates cursor's location
				GameState['xcoord_cursor'] = event.pos[0]
				GameState['ycoord_cursor'] = event.pos[1]
			if event.type==KEYDOWN:
				if event.key==112 and pause==False:
					pause=True
				elif event.key==112 and pause==True:
					pause=False
			if event.type==QUIT or (event.type==KEYDOWN and event.key==27):  # If close window or esc button was pressed, stops game
				pygame.quit()
				sys.exit()
		# If pause, open pause menu
		if pause:
			pause_menu()
		# If not pause, continue game
		if not pause:
			# Draws the game. (rooms, walls, areas, nodes)
			draw_game([0, 0, 0,0])
			# Gets all the events
			# Moves and draws survivor
			update_survivor_location()
			# Makes bullets based on time of click and time elapsed between last time click was checked and now
			survivor.weapon.bullet_handler()
			# Updates each bullet's location and draws it on DISPLAYSURF
			update_projectile_locations()
			# Calls the generate function of each spawn location
			current_round.zombie_handler()
			# Moves Zombies
			move_zombies()
			# Determines the location of cursor and if quit game
			new_cursor_location()
			# Updates and displays all game bars onto the screen
			menu_displayer()
			# Draw survivor
			survivor.prepare()
			survivor.draw()
		# updates game window with final DISPLAYSURF
		pygame.display.update()
		# Waits a certin amount of time before starting loop again
		fpsClock.tick(FPS)

if __name__ =="__main__":
	main()
