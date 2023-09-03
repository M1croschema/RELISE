from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None, 80)
win = font1.render('Ти переміг!', True, (255, 255, 255))
lose = font1.render('Зомбі дійшли до тебе!', True, (180, 0, 0))
font2 = font.Font(None, 36)

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()

img_back = "fon.png"
img_hero = "Hero.png" 
img_bullet = "bullet.png" 
img_en1 = "en1.png"  
img_en2 = "en2.png"  
img_en3 = "en3.png"  

life = 3
score = 0  
goal = 15
lost = 0  
max_lost = 1

class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 125:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 180:
            self.rect.y += self.speed
 
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 25, 25, -15)
        bullets.add(bullet)
 
# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.x -= self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = (win_width - 60)
            self.rect.y = randint(100, win_height - 80)
            lost = lost + 1



# клас спрайта-кулі  
class Bullet(GameSprite):
    # рух ворога
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x < 0:
            self.kill()


win_width = 900
win_height = 700
display.set_caption("PvZ")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 275, win_height - 200, 80, 100, 10)

monsters = sprite.Group()

for i in range(1, 6):
    vorog = randint(1, 3)
    if vorog == 1:
        monster = Enemy(img_en1, (win_width - 60), randint(100, win_height - 160), 130, 90, randint(3, 8))
        monsters.add(monster)
    elif vorog == 2:
        monster = Enemy(img_en2, (win_width - 60), randint(100, win_height - 160), 130, 90, randint(3, 8))
        monsters.add(monster)
    elif vorog == 3:
        monster = Enemy(img_en3, (win_width - 60), randint(100, win_height - 160), 130, 90, randint(3, 8))
        monsters.add(monster)

bullets = sprite.Group()

finish = False
# Основний цикл гри:
run = True 

rel_time = False  # прапор, що відповідає за перезаряджання

num_fire = 0

while run:

    
    
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        #подія натискання на пробіл - спрайт стріляє
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #перевіряємо, скільки пострілів зроблено і чи не відбувається перезаряджання
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    
                    ship.fire()
                   
                if num_fire >= 5 and rel_time == False : #якщо гравець зробив 5 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки

    collides = sprite.groupcollide(monsters, bullets, True, True)
    for c in collides:
        #Цей цикл повториться стільки разів, скільки монстрів підбито
        score = score + 1
        vorog = randint(1, 3)
        if vorog == 1:
            monster = Enemy(img_en1, (win_width - 40), randint(100, win_height - 160), 130, 90, randint(3, 8))
            monsters.add(monster)
        elif vorog == 2:
            monster = Enemy(img_en2, (win_width - 40), randint(100, win_height - 160), 130, 90, randint(3, 8))
            monsters.add(monster)
        elif vorog == 3:
            monster = Enemy(img_en3, (win_width - 40), randint(100, win_height - 160), 130, 90, randint(3, 8))
            monsters.add(monster)

  

    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))

        if rel_time == True:
            now_time = timer() # зчитуємо час
         
            if now_time - last_time < 3: #поки не минуло 3 секунди виводимо інформацію про перезарядку
                reload = font2.render('Перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (460, 50))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки


        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            life = life -1

        #програш
        if life == 0 or lost >= max_lost:
            finish = True # проиграли, ставим фон и больше не управляем спрайтами.
            window.blit(lose, (200, 200))

        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            monsters
            finish = True
            window.blit(win, (365, 100))

        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # задаємо різний колір залежно від кількості життів
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
       
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()
 

    

    time.delay(50)
