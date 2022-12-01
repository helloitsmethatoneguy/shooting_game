

from pygame import * 
mixer.init()
font.init()
from random import randint, choice


WIDTH, HEIGHT = 800, 640
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
Score = 0

class ImageSprite(sprite.Sprite):
    def __init__(self, filename, position, size):
        super().__init__()
        self.rect = Rect(position, size)
        self.image = image.load(filename)
        self.image = transform.scale(self.image, size)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class PlayerSprite(ImageSprite):
    def __init__(self,filename,position, size, velocity):
        super().__init__(filename, position, size)
        self.vel = Vector2(0,0)
        self.base_vel = Vector2(velocity)
    
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.vel.x = self.base_vel.x * -1
        if keys[K_d]:
            self.vel.x = self.base_vel.x
        if keys[K_w]:
            self.vel.y = self.base_vel.y * -1
        if keys[K_s]:
            self.vel.y = self.base_vel.y
        if not keys[K_a] and not keys [K_d]:
            self.vel.x = 0
        if not keys[K_w] and not keys [K_s]:
            self.vel.y = 0
        

        self.rect.topleft += self.vel  

        if self.rect.left <0:
            self.rect.left = 0          
        if self.rect.right >WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <0:
            self.rect.top = 0   
        if self.rect.bottom >HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        b = Bullet(filename='r.png', position=(0,0), size=(30,70), velocity=(0,-8))
        b.rect.center = self.rect.center
        bullets.add(b)
        choice(shooting_sounds).play()

class Bullet(ImageSprite):
    def __init__(self, filename, position, size, velocity):
        super().__init__(filename, position, size)
        self.vel = Vector2(velocity)
    def update(self):
        self.rect.topleft += self.vel
        if self.rect.bottom <= 0:
            self.kill()

class EnemySprite(ImageSprite):
    def __init__(self, filename, position, size, velocity):
        super().__init__(filename, position, size)
        self.vel = Vector2(velocity)
    def update(self):
        self.rect.topleft += self.vel
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0,WIDTH)
            
class TextSprite(sprite.Sprite):
    def __init__(self, text, pos, font_size, color):
        super().__init__()
        self.font = font.Font('PoorStory-Regular.ttf', font_size)
        self.color = color
        self.update_text(text)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def update_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        
            

intro = ImageSprite(filename='storyboard6.png', position=(0,0), size=(WIDTH, HEIGHT))
bg = ImageSprite(filename='full moon - background_.png', position=(0,0), size=(WIDTH, HEIGHT))
player = PlayerSprite(filename='i.png', position=(400,500), size=(80,80), velocity=(8,0))
enemies = sprite.Group()
bullets = sprite.Group()
shooting_sounds = []
sound = mixer.Sound('laser1.wav')
shooting_sounds.append(sound)
sound = mixer.Sound('laser4.wav')
shooting_sounds.append(sound)
sound = mixer.Sound('laser5.wav')
shooting_sounds.append(sound)
sound = mixer.Sound('laser6.wav')
shooting_sounds.append(sound)
text = TextSprite('Score: 0',  (50, 50), 40, 'lime')
game_over = TextSprite('GAME OVER', (200, 300), 100, 'crimson') 
you_win = TextSprite('YOU WIN', (300, 300), 100, 'lime')
that_one_game = TextSprite('THAT ONE GAME', (80, 200), 100, 'orange')
start = TextSprite('press S to start', (200, 300), 70, 'orange')
restart = TextSprite('press R to start', (150, 500), 100, 'crimson')
restart2 = TextSprite('press R to start', (150, 500), 100, 'green')
def create_enemy():
    e = EnemySprite(filename='Meteor1.png', position=(0,0), size=(80,80), velocity=(0,randint(1,10)))
    e.rect.x = randint(0,WIDTH)
    enemies.add(e)


for i in range(10):
    create_enemy()




state = 'intro'
while not event.peek(QUIT):
    for ev in  event.get():
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE and state == 'game':
                player.shoot()
            if ev.key == K_s and state == 'intro':
                enemies.empty()
                for i in range(10):
                    create_enemy()
                state ='game'
                Score= 0
                text.update_text("Score: "+str(Score))
            if ev.key == K_r and state == 'game_over' or state == 'you_win':
                state ='intro'
    if state == 'intro':
        intro.draw(window)
        that_one_game.draw(window)
        start.draw(window)
    elif state == 'game':
        bg.draw(window)
        player.update()
        player.draw(window)
        enemies.update()
        bullets.draw(window)
        bullets.update()
        text.draw(window)                         
        enemies.draw(window)
        hit = sprite.groupcollide(enemies, bullets, True, True)
        for hit in hit:
            create_enemy()
            Score += 5
            text.update_text("Score: "+str(Score))
        player_hits = sprite.spritecollide(player, enemies, True)
        for huh in player_hits:
            print(huh)
            create_enemy()
            Score -= 5
            text.update_text("Score: "+str(Score))
        if Score <0:
            bg.draw(window)
            state = 'game_over'
            game_over.draw(window)
        if Score > 500:
            bg.draw(window)
            you_win.draw(window)
            state = 'you_win'

    elif state == 'game_over':
        restart.draw(window)
    elif state == 'you_win':
        restart2.draw(window)
        

    display.update()
    clock.tick(60)

