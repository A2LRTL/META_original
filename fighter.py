import pygame
from pygame.sprite import Sprite
import json
import time
import random  


class AIBehaviour:
    def __init__(self, fighter):
        self.fighter = fighter
        self.current_movement_timer = 0
        self.current_action_timer = 0
        self.current_movement = self.idle_ai
        self.current_action = self.idle_ai


    def calculate_distance(self, target):
      # Calculate the distance between the AI and the target
        return abs(self.fighter.rect.x - target.rect.x)
  
    def targets_direction(self, target):
      # Calculate the direction to the target
      return 1 if target.rect.x > self.fighter.rect.x else -1
    
    def approach(self, target):
      SPEED = 10
      self.fighter.running = True
      dx = SPEED * self.targets_direction(target)
      return dx
    
    def retreat(self, target):
      SPEED = 10
      self.fighter.running = True
      dx = -SPEED * self.targets_direction(target)
      return dx

    def jump_ai(self, target):
      if self.fighter.jump_cooldown_1 == 0:
        self.fighter.vel_y = -30
        self.fighter.jump = True
        self.fighter.jump_cooldown_1 = 30
       #print("AI 1 jumps")
      if self.fighter.jump_cooldown_2 == 0:
        self.fighter.vel_y = -30
        self.fighter.jump = True
        self.fighter.jump_cooldown_2 = 30
        #print("AI 2 jumps")
    
    def attack_ai(self, target):
      if self.fighter.attack_cooldown_1 == 0 :
        self.fighter.attacking = True
        self.fighter.attack_type = random.randint(1, 2)
        self.fighter.attack_cooldown_1 = 30
        #self.attack_sound.play()
        print("AI 1 attacks")
        self.fighter.state = "Combat"
      if self.fighter.attack_cooldown_2 == 0 :
        self.fighter.attacking = True
        self.fighter.attack_type = random.randint(1, 2)
        self.fighter.attack_cooldown_2 = 30
        #self.attack_sound.play()
        print("AI 2 attacks")
        self.fighter.state = "Combat"
        
      if self.fighter.fighter_id == 1:
        offset_x = target.rect.x - self.fighter.rect.x + 190
      elif self.fighter.fighter_id == 2:
        offset_x = target.rect.x - self.fighter.rect.x - 190
      

      offset_y = target.rect.y - self.fighter.rect.y

      if self.fighter.mask.overlap(target.mask, (offset_x, offset_y)):
                target.health -= 10
                print("Fighter health:", target.health, "Fighter hit:", target.fighter_id)
                target.hit = True
      
    def defend(self, target):
      self.fighter.vel_y = -3
      self.fighter.jump = True  # makes the character jump to simulate a defense posture
      #print("AI defends")
      self.fighter.state = "Combat"

    def idle_ai(self, target):
      self.fighter.running = False
      self.fighter.jump = False
      #print (f"AI {self.fighter.player} idles")
      dx = 0
      return dx 

    
    def combat_behaviour(self, target):
  # Constant speed
      GRAVITY = 2
      # Distance thresholds
      long_distance = 400
      medium_distance = 150
      close_distance = 50
      superimposed_distance = 5
      # Health thresholds
      high_health = 6 #to change again
      medium_health = 5
      dx = 0
      dy = 0
      # Get the distance to the target
      distance = self.calculate_distance(target)
      # Apply gravity
      self.fighter.vel_y += GRAVITY
      dy += self.fighter.vel_y

      # Action decision-making based on distance to target and own health
      if self.fighter.health > high_health:
            

          #1.1
            if distance > long_distance:
                movements = [self.approach, self.retreat, self.idle_ai]
                weights = [70, 10, 20]
                actions = [self.idle_ai, self.jump_ai, self.attack_ai]
                action_weights = [80, 20, 5]

            #1.2  
            elif medium_distance < distance <= long_distance:
                movements = [self.approach, self.retreat, self.idle_ai]
                weights = [50, 30, 20]
                actions = [self.idle_ai, self.jump_ai, self.attack_ai]
                action_weights = [50, 25, 25]

            #1.3    
            elif medium_distance >= distance > close_distance:
                movements = [self.approach, self.retreat, self.idle_ai]
                weights = [10, 30, 20]
                actions = [self.idle_ai, self.jump_ai, self.attack_ai]
                action_weights = [10, 25, 50]

            #1.4
            elif distance <= close_distance:
                movements = [self.approach, self.retreat, self.idle_ai]
                weights = [10, 30, 20]
                actions = [self.idle_ai, self.jump_ai, self.attack_ai]
                action_weights = [10, 25, 50]

            # Update current movement
            if self.current_movement_timer <= 0:
                self.current_movement = random.choices(movements, weights, k=1)[0]
                self.current_movement_timer = random.randint(20, 80)  # Set the timer for the movement
            
            # Update current action
            if self.current_action_timer <= 0:
                self.current_action = random.choices(actions, action_weights, k=1)[0]  # Select an action based on weights
                self.current_action_timer = random.randint(20, 40)  # Set the timer for the action

            dx = self.current_movement(target)
            self.current_action(target)



              

      elif medium_health < self.fighter.health <= high_health:
          pass
      elif self.fighter.health <= medium_health:
          pass
         # Update player position
      self.fighter.rect.x += dx
      self.fighter.rect.y += dy

      
      if self.fighter.attack_cooldown_1 > 0:
          self.fighter.attack_cooldown_1 -= 1
      if self.fighter.jump_cooldown_1 > 0:
          self.fighter.jump_cooldown_1 -= 1

      if self.fighter.attack_cooldown_2 > 0:
          self.fighter.attack_cooldown_2 -= 1
      if self.fighter.jump_cooldown_2 > 0:
          self.fighter.jump_cooldown_2 -= 1


      self.current_movement_timer -= 1
      self.current_action_timer -= 1



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
    self.fighter_id=player
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
    self.attack_cooldown_1 = 0
    self.attack_cooldown_2 = 0
    self.jump_cooldown_1 = 0
    self.jump_cooldown_2 = 0
    self.attack_sound = sound
    self.hit = False
    self.health = 100
    self.alive = True
    self.mask = pygame.mask.from_surface(self.image)
    self.load_config(fighter_def_file)
    self.combo_keys = []
    self.combo_timer = 0
    self.state = "Combat"
    self.timer = 0
    self.current_movement_timer = 0  # Initialize movement timer
    self.current_action_timer = 0  # Initialize action timer

    self.ai_behaviour = AIBehaviour(self)

            
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
    self.attack_cooldown_1 = 0
    self.attack_cooldown_2 = 0
    self.jump_cooldown_1 = 0
    self.jump_cooldown_2 = 0
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


    # Get the current state of keyboard keys
    key = pygame.key.get_pressed()

    # Check if the character is alive and the round is not over
    if self.alive and not round_over:
      
        if self.state == "Combat":
            self.ai_behaviour.combat_behaviour(target)
        elif self.state == "Defense":
            self.ai_behaviour.defend(target)
        elif self.state == "Retreat":
            self.ai_behaviour.retreat(target)
        else: # AI starts in Combat mode
            self.state = "Combat"
  

        

    # Apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    # Ensure player stays on screen
    dx, dy = self.ensure_on_screen(dx, dy, screen_width, screen_height)

    # Ensure players face each other
    self.face_opponent(target)

    # Apply attack cooldown (prevents switching attacks during an ongoing attack)
    if self.attack_cooldown_1 > 0:
        self.attack_cooldown_1 -= 1
    if self.attack_cooldown_2 > 0:
        self.attack_cooldown_2 -= 1




    # Update player position
    self.rect.x += dx
    self.rect.y += dy

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
        if self.player == 1:
          if self.action == 3 or self.action == 4:
            self.attacking = False
            self.attack_cooldown_1 = 20
          #check if damage was taken
          if self.action == 5:
            self.hit = False
            #if the player was in the middle of an attack, then the attack is stopped
            self.attacking = False
            self.attack_cooldown_1 = 2
        if self.player == 2:
          if self.action == 3 or self.action == 4:
            self.attacking = False
            self.attack_cooldown_2 = 20
          #check if damage was taken
          if self.action == 5:
            self.hit = False
            #if the player was in the middle of an attack, then the attack is stopped
            self.attacking = False
            self.attack_cooldown_2 = 2


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

