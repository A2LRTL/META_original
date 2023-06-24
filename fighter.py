import pygame
from pygame.sprite import Sprite
import json
import time
import random  


class Fighter(pygame.sprite.Sprite):
  def __init__(self, player, x, y, flip, fighter_def_file):
    with open(fighter_def_file, 'r') as f:
            fighter_def = json.load(f)

        # Set variables from the fighter definition file
    sprite_sheet = pygame.image.load(fighter_def['sprite_sheet']).convert_alpha() #load l'image
    animation_steps = fighter_def['animation_steps']  #load animation
    sound = pygame.mixer.Sound(fighter_def['sound'])
    super().__init__()
    self.player = player
    self.size = fighter_def['size']
    self.image_scale = fighter_def['scale']
    self.offset = fighter_def['offset']
    self.flip = flip
    self.animation_list = self.load_images(sprite_sheet, animation_steps)
    self.action = 0
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.vel_y = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True
    self.mask = pygame.mask.from_surface(self.image)
    self.load_config(fighter_def_file)
    self.combo_keys = []
    self.combo_timer = 0
    self.state = "Combat"
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0
    
    



        
  def load_config(self, config_file):
    with open(config_file, "r") as f:
          self.config = json.load(f)
      
    self.move_left = self.config["move_left"]
    self.move_right = self.config["move_right"]
    self.move_up = self.config["move_up"]
    self.attack_1 = self.config["attack_1"]
    self.attack_2 = self.config["attack_2"]
    self.combo_1 = self.config["combo_1"]
    self.combo_2 = self.config["combo_2"]
    self.combo_3 = self.config["combo_3"]
    
    
  def reset(self):
    self.health = 100
    self.alive = True
    self.attacking = False
    self.attack_type = 0
    self.attack_cooldown = 0
    self.jump = False
    self.running = False
    self.hit = False
    self.action = 0  # Set action to idle
    self.frame_index = 0
    self.image = self.animation_list[self.action][self.frame_index]
    self.vel_y = 0
    
  def load_images(self, sprite_sheet, animation_steps):
    #extract images from spritesheet
    animation_list = []
    for y, animation in enumerate(animation_steps):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
      animation_list.append(temp_img_list)
    return animation_list
  


  def move(self, screen_width, screen_height, target, round_over):
    # Initialize constants for speed, gravity, and character states
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    # Get the current state of keyboard keys
    key = pygame.key.get_pressed()

    # Check if the character is alive and the round is not over
    if self.alive and not round_over:
        # Player controls
        if self.player == 1: 
          player_keys = self.config
          
          # Movement
          if key[self.move_left]:
              print("moveleft")
              dx = -SPEED
              self.running = True
          if key[self.move_right]:
              print("moveright")
              dx = SPEED
              self.running = True
          if key[self.move_up] and not self.jump:
            self.vel_y = -30  # needs to be negative because of the origin in the upper left
            self.jump = True
        


        elif self.player == 2:  # Added this elif block
          if self.state == "Combat":
              self.combat_behaviour(target)
          elif self.state == "Defense":
              self.defend(target)
          elif self.state == "Retreat":
              self.retreat(target)
          else: # AI starts in Combat mode
              self.state = "Combat"
    

          

        # Handle attacks and combos
        self.handle_attacks_and_combos(target, key)

    # Apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    # Ensure player stays on screen
    dx, dy = self.ensure_on_screen(dx, dy, screen_width, screen_height)

    # Ensure players face each other
    self.face_opponent(target)

    # Apply attack cooldown (prevents switching attacks during an ongoing attack)
    if self.attack_cooldown > 0:
        self.attack_cooldown -= 1

    # Update player position
    self.rect.x += dx
    self.rect.y += dy

  def calculate_distance(self, target):
      # Calculate the distance between the AI and the target
      return abs(self.rect.x - target.rect.x)
  
  def targets_direction(self, target):
    # Calculate the direction to the target
    return 1 if target.rect.x > self.rect.x else -1
  
  def approach_target(self, target):
    SPEED = 10
    dx = SPEED * self.targets_direction(target)
    self.running = True
    return dx
  
  def combat_behaviour(self, target):
# Constant speed
    SPEED = 10
    GRAVITY = 2

    # Distance thresholds
    long_distance = 400
    medium_distance = 150
    close_distance = 50

    # Health thresholds
    high_health = 80
    medium_health = 40

    dx = 0
    dy = 0
    self.running = False
    self.jump = False
    self.attacking = False
    self.defending = False
    self.retreating = False
    self.attack_type = 0  # default to ranged attack

    # Get the distance to the target
    distance = self.calculate_distance(target)

    # Apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    # Action decision-making based on distance to target and own health
    if self.health > high_health:
        if distance > long_distance:
            dx = self.approach_target(target)
        elif medium_distance < distance <= long_distance:
            self.attack_type = 1  # ranged attack
            self.attacking = True
            self.attack(target)
        elif distance <= medium_distance:
            self.attack_type = 1  # melee attack
            self.attacking = True
            self.attack(target)

    elif medium_health < self.health <= high_health:
        pass
    elif self.health <= medium_health:
        pass

  # Apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y
    
    if self.attack_cooldown > 0:
        self.attack_cooldown -= 1
    # Update player position
    self.rect.x += dx
    self.rect.y += dy
   
    self.execute_action(target)



  def execute_action(self, target):
    SPEED = 10
    dx = 0
    dy = 0
    self.running = False

    if self.action == 1 :
        dx = -SPEED
        self.running = True  
        print("AI moves left")
    elif self.action == 1 :
        dx = SPEED
        self.running = True
        print("AI moves right")
    elif self.action == 2:
        if not self.jump:  # Ensure the character is not already in a jump state
            self.vel_y = -30  # needs to be negative because of the origin in the upper left
            self.jump = True
        print("AI jumps")
    elif self.action == 3 :
        self.attack(target)
        self.attack_cooldown = 50 #beug : attack pas si mvt en x

        print("AI attacks")

    #elif action == 'retreat':
     #   self.retreat(target)
      #  print("AI retreats")
    #elif action == 'defend':
    #    self.defend(target)
     #   print("AI defends")

    self.rect.x += dx
    self.rect.y += dy      


  def retreat(self, target):
    SPEED = 10
    dx = 0
    dx = SPEED  # Move right
    self.rect.x += dx
    self.running = True
    print("AI retreats")
    
  def defend(self, target):
    self.vel_y = -3
    self.jump = True  # makes the character jump to simulate a defense posture
    print("AI defends")
    self.state = "Combat"

  def ensure_on_screen(self, dx, dy, screen_width, screen_height):
      # Keep the player on screen and adjust dx, dy accordingly

      # Ensure player stays on screen (horizontal)
      if self.rect.left + dx < 0:
          dx = 0 - self.rect.left
      if self.rect.right + dx > screen_width:
          dx = screen_width - self.rect.right

      # Ensure player stays on screen (vertical)
      if self.rect.bottom + dy > screen_height - 110:  # 110 px is the floor height in this background
          self.vel_y = 0
          self.jump = False
          dy = screen_height - 110 - self.rect.bottom

      return dx, dy

  def face_opponent(self, target):
      # Make the player face their opponent
      if target.rect.centerx > self.rect.centerx:
          self.flip = False
      else:
          self.flip = True

  def handle_attacks_and_combos(self, target, key):
    # Attack
    if (key[self.attack_1] or key[self.attack_2]) and not self.attacking:
        self.attack(target)
        if key[self.attack_1]:
            self.attack_type = 1
        if key[self.attack_2]:
            self.attack_type = 2



    # Combo attacks
    if (key[self.combo_1] or key[self.combo_2]) or key[self.combo_3]:

        # Add the keypress and its timestamp to the combo_keys list
        self.combo_keys.append((pygame.key.name(key.index(1)), time.time()))
        # Update the combo timer
        self.combo_timer = time.time()

        # 2-key combos
        if len(self.combo_keys) >= 2 and not self.attacking:
            key_sequence1 = ['r', 'f']
            key_sequence2 = ['t', 'g']
            pressed_keys = [k[0] for k in self.combo_keys[-2:]]
            if pressed_keys == key_sequence1:
                self.attack_type = 3
                self.attack(target)
            elif pressed_keys == key_sequence2:
                self.attack_type = 4
                self.attack(target)

        # 3-key combos
        if len(self.combo_keys) >= 3 and not self.attacking:
            key_sequence1 = ['r', 'f', 'h']
            key_sequence2 = ['t', 'g', 'h']
            key_sequence3 = ['r', 't', 'f']
            pressed_keys = [k[0] for k in self.combo_keys[-3:]]
            if pressed_keys == key_sequence1:
                self.attack_type = 5
                self.attack(target)
            elif pressed_keys == key_sequence2:
                self.attack_type = 6
                self.attack(target)
            elif pressed_keys == key_sequence3:
                self.attack_type = 7
                self.attack(target)          
                   
  #handle animation updates  
  def update(self):
    GRAVITY = 2
    self.vel_y += GRAVITY
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1
      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    self.mask = pygame.mask.from_surface(self.image)
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 20
        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.attack_cooldown = 20

  #def get_attack_rect(self):
      #attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      #return attacking_rect
    
  def attack(self, target):
    if self.attack_cooldown == 0:
            # execute attack
            self.attacking = True
            self.attack_sound.play()
            
            # Calculate the offset between the two masks
            if self.player == 1:
              offset_x = target.rect.x - self.rect.x - 190
            else:
              offset_x = target.rect.x - self.rect.x + 190
            offset_y = target.rect.y - self.rect.y
            print(f"Offset_x: {offset_x}, Offset_y: {offset_y}")  # Add this line
            print(f"Self mask: {self.mask}")  # Add this line
            print(f"Target mask: {target.mask}")  # Add this line

            if self.mask.overlap(target.mask, (offset_x, offset_y)):
                target.health -= 10
                print("Fighter health:", target.health)
                target.hit = True
                            
  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x  - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))