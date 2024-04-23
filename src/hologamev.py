# title:   HoloGameV
# author:  AILab-FOI
# desc:    short description
# site:    https://ai.foi.hr
# license: GPLv3
# version: 0.1
# script:  python

t=0
state='menu' #varijabla za game state

def TIC():
 Final()

 global state
 if state=='game':
   cls(0)

   map(0, 0, 36, 18, -int(pogled.x), -int(pogled.y), 0)

   collidables = DefinirajKolizije([player, enemy])
   enemy.movement(enemy, collidables)
   for projektil in projectiles:
      projektil.movement()
   Pucanje()
   player.PlayerKontroler(player, collidables)
   pogled.pratiIgraca()
 elif state=='menu':
   menu.Menu()

def Final():
	cls(13)
    print("A i D za kretanje, SPACE za skakanje", 0, 0)
    print("W za jetpack, F i G za pucanje", 0, 8)
 
	t=t+1


class collidable:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.draw_self()

    def check_collision(self, other):
        if self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y:
            return True
        return False

    def check_collision_rectangle(self, xleft, ytop, xright, ybottom):
        if self.x < xright and self.x + self.width > xleft and self.y < ybottom and self.y + self.height > ytop:
            return True
        return False

    def draw_self(self):
        rect(self.x - int(pogled.x), self.y - int(pogled.y), self.width, self.height, 15)


def DefinirajKolizije(listaObjekata):
    collidables = []

    tile_size = 8
    for objekt in listaObjekata:
        px = min(max(int(objekt.x/tile_size) - 4, 0), 239)
        py = min(max(int(objekt.y/tile_size) - 4, 0), 135)
        xrepeat = 10
        yrepeat = 10

        for xx in range(xrepeat):
            for yy in range(yrepeat):
                tileHere = mget(xx + px, yy + py)
                if tileHere != 0:
                    collidables.append(collidable((xx + px)*tile_size, (yy + py)*tile_size, tile_size, tile_size))

    

    return collidables
def pomakni(a, b, vrijednost):
    if vrijednost == 0:
        return a
    elif a < b:
        return min(a + vrijednost, b)
    else:
        return max(a - vrijednost, b)

class player: 
    x=96
    y=24
    width=16
    height=16
    hsp=0
    vsp=0
    desno=False
    is_walking = False
    frame = 256
    shootTimer=0
    jetpackGorivo=0
    skok=0
    coll=[]
    spriteTimer = 0

    def ProvjeriKolizije(self, xdodatak, ydodatak):
        self.x += xdodatak
        self.y += ydodatak
        for obj in self.coll:
            if obj.check_collision(self):
                self.x -= xdodatak
                self.y -= ydodatak
                return True
        self.x -= xdodatak
        self.y -= ydodatak
        return False
    
    minY=120 #najniza tocka
    minX=10000 #najdesnija tocka

    #Osnovne Varijable
    akceleracija=0.5
    maxBrzina=3
    gravitacija=0.3


    #Varijable skakanja
    skokJacina=5.2

    #jetpack
    jetpackTrajanje=50
    jetpackJacina=2

    def PlayerKontroler(self, coll):
        self.coll=coll

        #skakanje
        if key(48) and self.vsp == 0:
            if self.ProvjeriKolizije(self, 0, 1) or self.y>=self.minY:
                self.vsp = -self.skokJacina

        #kretanje lijevo desno
        if key(1): 
            self.hsp=pomakni(self.hsp,-self.maxBrzina,self.akceleracija)
            self.desno=False
            self.is_walking = True
        elif key(4):
            self.hsp=pomakni(self.hsp,self.maxBrzina,self.akceleracija)
            self.is_walking = True
            self.desno=True
        else:
            self.hsp=pomakni(self.hsp,0,self.akceleracija)
            self.is_walking = False

        if key(23):
            self.JetpackJoyride(self)
            

        #gravitacija i kolizije
        if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(self, 0, self.vsp + 1):
            self.vsp=0
            while self.y<self.minY and not self.ProvjeriKolizije(self, 0, 1):
                self.y+=1
        else:
            self.vsp=self.vsp+self.gravitacija

        if self.vsp<0:
            if self.ProvjeriKolizije(self, 0, self.vsp - 1):
                self.vsp=0

        

        #blokiranje lijevo i desno
        if self.x>(pogled.ogranicenjeX - self.width) or self.ProvjeriKolizije(self, 1+self.hsp, 0):
            self.hsp=0
            while self.ProvjeriKolizije(self, 0, 0) or self.x > (pogled.ogranicenjeX - self.width):
                self.x-=1
            
        if self.x<0 or self.ProvjeriKolizije(self, -1+self.hsp, 0):
            self.hsp=0
            while self.ProvjeriKolizije(self, 0, 0) or self.x < 0:
                self.x+=1

        self.x=self.x+self.hsp
        self.y=self.y+self.vsp
            
        
        #jetpack
        
        if self.ProvjeriKolizije(self, 0, 1) or self.y>=self.minY: # ZAMIJENITI SA DOK STOJI NA NEKOM OBJEKTU
            self.jetpackGorivo=self.jetpackTrajanje

        if self.is_walking == True:
            self.spriteTimer += 0.1

        #renderanje spritea
        if self.desno==True and self.is_walking==True:
            spr(258 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),6,1,0,0,2,2)
        elif self.desno==False and self.is_walking==True:
            spr(258 + 2*(round(self.spriteTimer)%2==0),int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),6,1,1,0,2,2)
        else:
            spr(self.frame,int(self.x) - int(pogled.x),int(self.y) - int(pogled.y),6,1,int(self.desno==False),0,2,2)

            
            
    def JetpackJoyride(self):
        if self.jetpackGorivo > 0:
            self.vsp = -self.jetpackJacina
            self.jetpackGorivo = self.jetpackGorivo - 1
            self.skok = 0
     
    



#lista projektila
projectiles = []

class enemy:
  x = 90 
  y = 90
  width = 16
  height = 16
  sprite = 1  
  dx = -1  
  vsp = 0
  gravitacija = 0.3
  skokJacina = 3
  minY = 120
  desno = False
  shotTimer = 0  # timer za pucanje
  coll = []

  def movement(self, coll):
    self.coll = coll
    self.x = self.x + self.dx
    if self.ProvjeriKolizije(self, 6*self.dx, 0):
      if not self.ProvjeriKolizije(self, 3*self.dx, -9):
        if self.ProvjeriKolizije(self, 0, 1):
          self.vsp = -self.skokJacina
        else:
          self.dx = -self.dx
          self.desno = not self.desno
    elif self.ProvjeriKolizije(self, 3*self.dx, 0):
      self.dx = -self.dx
      self.desno = not self.desno
    if self.x <= 0:
      self.dx = 1  # mijenja stranu kad takne lijevu stranu
      self.desno = True
    elif self.x >= pogled.ogranicenjeX:
      self.dx = -1  # mijenja stranu kad takne desnu stranu
      self.desno = False

    self.shotTimer += 1  # svaki frame se povecava za 1

    # gravitacija
    if self.y+self.vsp>=self.minY or self.ProvjeriKolizije(self, 0, self.vsp + 1):
      self.vsp=0
      while self.y<self.minY and not self.ProvjeriKolizije(self, 0, 1):
        self.y+=1
    else:
      self.vsp=self.vsp+self.gravitacija

    if self.vsp<0:
      if self.ProvjeriKolizije(self, 0, self.vsp - 1):
        self.vsp=0

    self.y = self.y + self.vsp

    # puca svakih dvije sekunde
    if self.shotTimer >= 60 * 2:
      self.shootProjectile(self)  # poziv funkcije za pucanje
      self.shotTimer = 0  # resetiranje timera

    #crtanje samog sebe
    if enemy.desno==True:
      spr(290,int(enemy.x) - int(pogled.x),int(enemy.y) - int(pogled.y),6,1,0,0,2,2)
    else:
      spr(290,int(enemy.x) - int(pogled.x),int(enemy.y) - int(pogled.y),6,1,1,0,2,2)

  def shootProjectile(self):
    projectile = Projectile(self.x + 5, int(self.y)) 

    projectile.desno = self.desno
    # doda projektil u listu
    projectiles.append(projectile)

  def ProvjeriKolizije(self, xdodatak, ydodatak):
    self.x += xdodatak
    self.y += ydodatak
    for obj in self.coll:
      if obj.check_collision(self):
        self.x -= xdodatak
        self.y -= ydodatak
        return True
    self.x -= xdodatak
    self.y -= ydodatak
    return False

class Projectile:
  def __init__(self, x, y):  # konstruktor klase
    self.x = x
    self.y = y
    self.dx = 1 
    self.dy = 0
    self.speed = 5  # brzina projektila
    self.desno = True
  
  def movement(self):
    if self.desno == True:
      self.x = self.x + self.speed
    else:
      self.x = self.x - self.speed

    #crtanje sebe
    spr(80, self.x - int(pogled.x), self.y - int(pogled.y), 14, 1, 0, 0, 1, 1)

    #brisanje ako se unisti
    if self.x < 0 or self.x > pogled.ogranicenjeX:
      del self
     


class menu:
    m_ind=0

    def Menu():
        global state
        cls(0)
        menu.AnimateFrame()
        menu.AnimateTitle()

        # Opcije menija
        rect(1,48+10*menu.m_ind,238,10,2)
        print('Play', 100, 50, 4, False, 1, False)
        print('Quit', 100, 60, 4, False, 1, False)

        #  Šetanje po opcijama na meniju
        if btnp(1) and 48+10*menu.m_ind<50: #ako se budu dodavale još koje opcije, promijeniti uvijet
            menu.m_ind += 1
        elif btnp(0) and 48+10*menu.m_ind>=50:
            menu.m_ind += -1

        # Odabir 
        if key(48) and menu.m_ind==0:
            state = 'game'
        elif key(48) and menu.m_ind==1:
            exit()

    def AnimateTitle():
        if(time()%500>250):
            print('NEON ESCAPE', 57, 20, 6, False, 2, False)
        elif(time()%500>150):
            print('NEON ESCAPE', 57, 20, 2, False, 2, False)
        elif(time()%500>350):
            print('NEON ESCAPE', 57, 20, 3, False, 2, False)
        elif(time()%500>550):
            print('NEON ESCAPE', 57, 20, 10, False, 2, False)

    def AnimateFrame():
        if(time()%500>250):
            rectb(0,0,240,136,6)
        elif(time()%500>150):
            rectb(0,0,240,136,2)
        elif(time()%500>350):
            rectb(0,0,240,136,3)
        elif(time()%500>550):
            rectb(0,0,240,136,10)


def lerp(a, b, t):
    return (1-t)*a + t*b

class Pogled:
    x = 0
    y = 0
    w = 240
    h = 136
    ograniceno = False
    ogranicenjeX = 0

    def __init__(self):
        self.postaviOgranicenja(1000)

    def prati(self, objekt):
        self.x = objekt.x - (self.w - objekt.width)/2
        #self.y = objekt.y - (self.h - objekt.height)/2

    def postaviOgranicenja(self, maxX):
        self.ograniceno = True
        self.ogranicenjeX = maxX

    def pratiIgraca(self):
        lerpSnaga = 0.05
        lerpSnagaHoda = 0.2
        ispredStoji = 6
        ispredHoda = 16
        if player.is_walking:
            self.x = lerp(self.x, player.x - (self.w - player.width)/2 + ispredHoda*int(player.desno == True) - ispredHoda*int(player.desno == False), lerpSnagaHoda)
        else:
            self.x = lerp(self.x, player.x - (self.w - player.width)/2 + ispredStoji*int(player.desno == True) - ispredStoji*int(player.desno == False), lerpSnaga)

        if self.ograniceno:
            self.x = min(max(0, self.x), self.ogranicenjeX - self.w)

pogled = Pogled()



class prvaPuska:
    x=0
    y=0
    
    desno=False
    
    firerate = 0.6
    speed=16
    dmg=4
    
class drugaPuska:
    x=0
    y=0
    
    desno=False
    
    firerate = 0.1
    speed=6
    dmg=1


metci = []



   

def Pucanje():
    
    player.shootTimer = player.shootTimer - 1
    
    if player.shootTimer < 0:
        if key(6):
            pucaj(prvaPuska)
        if key(7):
            pucaj(drugaPuska)
        
    for metak in metci:
            spr(80,metak.x - int(pogled.x),metak.y - int(pogled.y),14,1,0,1,1,1)
            
            if metak.desno == True:   
                metak.x = metak.x + metak.speed
            else:
                metak.x = metak.x - metak.speed
            
            if metak.x < 0 or metak.x > pogled.ogranicenjeX:
                del metak

def pucaj(puska):
  metak = puska()  
  metak.x = int(player.x)
  metak.y = int(player.y)
  metak.desno = player.desno

  metci.append(metak)
  player.shootTimer=puska.firerate*60
  




def test( a, b ):
    return a+b
# <TILES>
# 001:8888888888888888888888888888888888888888888888888888888888888888
# 002:9999999999999999999999999999999999999999999999999999999999999999
# 003:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
# 004:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 005:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
# 006:00dddddd0deeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee0deeeeee00dfffff
# 007:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 008:dddddf00eeeeeef0eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeef0ffffff00
# 009:dddddddfdeeeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdfffffff
# 010:dddddddfdeeeeeefdedeefefdeeeeeefdeeeeeefdedeefefdeeeeeefdfffffff
# 011:dddddddddd9eafa8d9eafad8deafad98dafad9e8dfad9ea8dad9eaf8d8888888
# 012:00dddddd0deeeeeedeedeeeedeeeeeeedeeeeeeedeedeeee0deeeeee00dfffff
# 013:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 014:dddddf00eeeeeef0eeeefeefeeeeeeefeeeeeeefeeeefeefeeeeeef0ffffff00
# 016:dddddddddeeeeeeededdeeeededdeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 017:ddddddddeeeeeeefeeeeffefeeeeffefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 018:ffffffffffeeeeeefefeeeeefeefeeeefeeefeeefeeeeffffeeeeff2feeeef2f
# 019:ffffffffeeeeeeffeeeeefefeeeefeefeeefeeeffffeeeef2ffeeeeff2feeeef
# 020:000ddddd00deeeef0deeeeefdeeeeeefdeeeeeefdeeeeeefdeeeeeefdfffffff
# 021:ddddf000feeeef00feeeeef0feeeeeeffeeeeeeffeeeeeeffeeeeeefffffffff
# 022:000ddddd00deeeee0deeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 023:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 024:ddddf000eeeeef00eeeeeef0eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 025:000ddddd00deeeee0deeddeedeeeddeedeeeeeeedeeeeeeedeeeeeeedeeeeeee
# 026:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# 027:ddddf000eeeeef00eeffeef0eeffeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeef
# 028:3333333333444444343444443443444434443444344443443444443434444443
# 029:3333333344444433444443434444344344434443443444434344444334444443
# 030:8888888888bbbb888b8bb8b88bb88bb88bb88bb88b8bb8b888bbbb8888888888
# 032:deeeeeeedeeeeeeedeeeeeeedeeeeeeededdeeeededdeeeedeeeeeeeffffffff
# 033:eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeffefeeeeffefeeeeeeefffffffff
# 034:feeeef2ffeeeeff2feeeeffffeeefeeefeefeeeefefeeeeeffeeeeeeffffffff
# 035:f2feeeef2ffeeeeffffeeeefeeefeeefeeeefeefeeeeefefeeeeeeffffffffff
# 036:dfffffffdeeeeeefdeeeeeefdeeeeeefdeeeeeef0deeeeef00deeeef000fffff
# 037:fffffffffeeeeeeffeeeeeeffeeeeeeffeeeeeeffeeeeef0feeeef00fffff000
# 038:deeeeeeedeeeeeeedeeeeeeedeeeeeeedeeeeeee0deeeeee00deeeee000fffff
# 039:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 040:eeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeeefeeeeeef0eeeeef00fffff000
# 041:deeeeeeedeeeeeeedeeeeeeedeeeddeedeeeddee0deeeeee00deeeee000fffff
# 042:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffff
# 043:eeeeeeefeeeeeeefeeeeeeefeeffeeefeeffeeefeeeeeef0eeeeef00fffff000
# 044:3444444334444434344443443444344434434444343444443344444433333333
# 045:3444444343444443443444434443444344443443444443434444443333333333
# 046:3333333333444433343443433443344334433443343443433344443333333333
# 048:dddddddddd000000dddddddddd000000dddddddedd000000dddddeeedd000000
# 049:dddeeeee000000eedeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 050:dddddddddeeeeeeedeeeeeeedeeeeeeedeeeffffffefddedffefdedddeefedde
# 051:ddddddddeeeeeeeeeeeeeeeeeeeeeeeeffffffffdeeddddeeeddddededdddedd
# 052:dddddddfeeeeeeefeeeeeeefeeeeeeefffffeeefddddfeffdddefeffddeefeef
# 053:00aaaaaa0aaaaaaaa8888888a8aa8aa8a8aa8aa8a88888880a88888800aaaaaa
# 054:aaaaaaaaaaaaaaaa88888888aa8aa8aaaa8aa8aa8888888888888888aaaaaaaa
# 055:aaaaaa00aaaaaaa08888888a8aa8aa8a8aa8aa8a8888888a888888a0aaaaaa00
# 056:0000000800000084000008440000844400084444008444480888888084884800
# 057:8888800083384800833844808888444880084448000088880000088800000008
# 058:000000000000000000000000800000008000000088888800eeeee880e8888e88
# 059:2222222222222222222222222222222222222222222222222222222222222222
# 060:3333333333333333333333333333333333333333333333333333333333333333
# 061:4444444444444444444444444444444444444444444444444444444444444444
# 062:1111111111111111111111111111111111111111111111111111111111111111
# 064:dddeeeeedd000000ddeeeeeede000000deeeeeeede000000deeeeeeede000000
# 065:eeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 066:deefddeedeefdeeddeeeffffdeeeeeeedeeeeeeedeeddddddeedeeeedeedeeee
# 067:ddddeddddddeddddffffffffeeeeeeeeeeeeeeeeddddddddeeeeeeeeeeeeeeee
# 068:deedfeefeeddfeefffffeeefeeeeeeefeeeeeeefddddfeefeeeefeefeeeefeef
# 069:ddddddddd77777770f77777700ffffff0007f0000007f0000007f0000007f000
# 070:dddddddd7777777777777777ffffffff00000000000000000000000000000000
# 071:dddddddd7777777f777777f0ffffff000007f0000007f0000007f0000007f000
# 072:8888880084884800888888800844444800844444000844440008444400888888
# 073:0000000800000008000000080000000880000000800000008000000088000000
# 074:e80008e8e8000080e8000000ee8000008ee80000088000000000000000000000
# 075:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
# 076:7777777777777777777777777777777777777777777777777777777777777777
# 077:6666666666666666666666666666666666666666666666666666666666666666
# 078:5555555555555555555555555555555555555555555555555555555555555555
# 080:eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000
# 081:eeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 082:deedeeeeffedeeeeffedeeeedeedeeeedeedffffdeeeeeeedeeeeeeedfffffff
# 083:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffffeeeeeeeeeeeeeeeeffffffff
# 084:eeeefeefeeeefeffeeeefeffeeeefeeffffffeefeeeeeeefeeeeeeefffffffff
# 085:ddddddddd33383330f33383300ffffff0003f0000003f0000003f0000003f000
# 086:dddddd8d8333383333333833ffffffff00000000000000000000000000000000
# 087:dddddddf3333333f333833f0ffffff000003f0000003f0000003f0000003f000
# 088:00888888ddeeeeefddeeeeeeddeeeeeeddeeeeeeddeeeeeeddeeeeeeddeeeeee
# 089:88000000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000ffff0000
# 091:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 096:eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000
# 097:eeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000eeeeeeeeee000000ee
# 098:ddf00000deef0000deeedddddeeeeeeedeeeeeeedeeeffffdeef0000dff00000
# 099:0000000000000000ddddddddeeeeeeeeeeeeeeeeffffffff0000000000000000
# 100:0000000000000000ddddddddeeeeeeeeeeeeeeeeffffffff0000000000000000
# 101:00000ddf0000deefddddeeefeeeeeeefeeeeeeefffffeeef0000deef00000dff
# 102:0000004800000848000088400004440000088000000880000084480008888880
# 103:8000000088bb000088bbb000bbbbb0000bbbb000000000000000000000000000
# 104:ddddddd8dbbbbbb8d9999998dbbbbbb8d9999998dbbbbbb8d9999998d8888888
# 112:888888888fffffff8fff22228222ff3382ff333f8f3333ff83322fff8fff2222
# 113:88888888ffffff33223333ff33ff2222fffff3fff3333fff3ffffff222f22f2f
# 114:8888888833333338fff3fff8233f33f822222228fffff33822fffff8ff2ffff8
# 115:ffffffffffeeeeeefefeeeeefeefeeeefeeefeeefeeeeffffeeeeff5feeeef5f
# 116:ffffffffeeeeeeffeeeeefefeeeefeefeeefeeeffffeeeef5ffeeeeff5feeeef
# 118:ddddddddd44444440f44444400ffffff0004f0000004f0000004f0000004f000
# 119:dddddddd4444444444444444ffffffff00000000000000000000000000000000
# 120:dddddddd4444444f444444f0ffffff000004f0000004f0000004f0000004f000
# 128:82fff3ff832333ff8ff2fff28fff222f8f33333f83fffff38fffffff88888888
# 129:ff2ff2ffffffffff2ffffff32f22233ff2ff22fffff3322f3333ff2288888888
# 130:fff22ff8fffff2f833fffff8ff33f228ffff2ff8fff2f3f8ff2fff3888888888
# 131:feeeef5ffeeeeff5feeeeffffeeefeeefeefeeeefefeeeeeffeeeeeeffffffff
# 132:f5feeeef5ffeeeeffffeeeefeeefeeefeeeefeefeeeeefefeeeeeeffffffffff
# </TILES>

# <SPRITES>
# 000:666666fe66666fee6666feee6666feee66666fee666666fe66600e0066fee034
# 001:d6666666ed66666622d66666eed66666ed666666e66666660e00666640ed6666
# 002:666666fe66666fee6666feee6666ffee66666ffe666666ff66600e0066fee034
# 003:d6666666ed66666622d66666eed66666ed666666e66666660e00666640eed666
# 004:666666fe66666fee6666feee6666ffee66666ffe666666ff66666ee066666e03
# 005:d6666666ed66666622d66666eed66666ed666666e66666660e66666640666666
# 016:66feee0366feffe066fe6fe066fe6eee666ffee66666fe666666fe666666fff6
# 017:0eeed666ef6ee666ee6ee666ed66e666fed66666fee66666fee666666fee6666
# 018:6feeee036fe6f0e06fee6fe066f66eee6666fee66666fe66666fee66666ffee6
# 019:0ee6ed66e0e6ee66ee66eed6ed666d66fed66666ffed66666ffd666666fed666
# 020:6666eee06666eeee6666efee66666ffe66666fee6666fee66666fe6666666ff6
# 021:0e666666e0666666ee666666ed666666fe666666ffe66666fee66666ff666666
# 032:666666fe66666fee6666feee6666ffee66666ffe666666ff66666ee066666e03
# 033:d6666666ed66666622d66666eed66666ed666666e66666660f66666630fefeff
# 034:6666ff66666feef666ffffee6feeffff6feef66666feeff7666feef766ffff7f
# 035:6666666666666666ef66666666666666666666667dd66666fffd6666222f6666
# 036:6666ff66666feef666ffffee6feeffff6feef66666feeff7666feef766ffff7f
# 037:6666666666666666ef66666666666666666666667dd66666fffd6666233f6666
# 048:6666eee06666eeee6666efee66666ffe66666fee6666fee66666fe6666666ff6
# 049:0effeff6eff6f666ee66f666ed666666fe666666ffe66666fee66666ff666666
# 050:66fee777666fe77766fee77766fe777f66fe777666fe77d6666fe77d666ffff7
# 051:f2fd66667f7d66667777666677776666f7776666fe7d66666fe7d6666ffedd66
# 052:66fee777666fe77766fee77766fe777766fe77776ffe77776fffeeee6ffffffe
# 053:f2fd66667f7d66667777666677776666766666667d66666677d66666e7766666
# 064:6666ff66666feef666feffee6fefffff6feef66666feefff666feef766ffff7f
# 065:6666666666666666ef666666666666666666666677d66666fffd6666233f6666
# 066:a6666888aaa68999a9989999a99999ff6a999fdd66a9fddd6699fd226699fd22
# 067:886666f69986fff6999888f6f99988f6df998f66ddf986662df9f6662df9f666
# 068:a6666a99aaa6a999aa9a9999aa9999ff6aa99fdd66a9fddd6699f2226699f222
# 069:886666f69986fff6999888f6f99998f6df998f66ddf98666ddf9f666ddf9f666
# 080:66fee777666fe777666fe777666fe77e66ffe77e66ffe7776feffeee6feefffe
# 081:f2f766667f776666777d666677d66666ed6666667edd6666777d6666ee776666
# 082:66a99fd266a999ff6a9a9999a9999888a9999986999999869999998669988866
# 083:df99f666f998f66699898f66889998f6899998f6899999f6899999f66888ff66
# 084:66a99f2d66a999ff6aaa9999aa999999a9999996999999866999886666666666
# 085:df99f666f999f66699998f66899998f6899998f6899999f6899999f66888ff66
# 096:a6666a99aaa6a999aa9a9999aa9999ff6aa99fdd66a9fddd6699f2226699f222
# 097:886666f69986fff6999888f6f99998f6df998f66ddf98666ddf9f666ddf9f666
# 098:a6666888aaa68999a9989999a99999886a99982266a982236698223366982334
# 099:886666f69986fff6999888f6899988f628998f66228986663228f6663328f666
# 100:a6666888aaa68999a9989999a99999886a99982266a982336698233466982344
# 101:886666f69986fff6999888f6899988f628998f66328986663328f6664328f666
# 112:66a99f2d66a999ff6aaa9999aa999999a9999986a99999869999998669998866
# 113:df99f666f999f66699998f66899998f6899999f6899999f66888ff6666666666
# 114:66a8223366a982236a9a8222a9999888a9999986999999869999998669988866
# 115:3228f6662289f66622898f66889998f6899998f6899999f6899999f66888ff66
# 116:66a8233466a982336a9a8222a9999888a9999986999999869999998669988866
# 117:3328f6663289f66622898f66889998f6899998f6899999f6899999f66888ff66
# </SPRITES>

# <MAP>
# 006:000000000000006137472131810000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 007:000000000000006238482232820000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 011:000000000000000000000000000000000000000000000000011100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 012:000000000000000000000000000000000041510000000000021200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 013:00000000000000000000000000000000a090900000000091a1b100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 014:404040404040404040404000000000a0a090a00000000092a2b200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 015:404040404040404040404040404040404040404040404040404040404040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# 016:404040404040404040404040404040404040404040404040404040404040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </MAP>

# <WAVES>
# 000:00000000ffffffff00000000ffffffff
# 001:0123456789abcdeffedcba9876543210
# 002:0123456789abcdef0123456789abcdef
# </WAVES>

# <SFX>
# 000:000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000304000000000
# </SFX>

# <TRACKS>
# 000:100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
# </TRACKS>

# <PALETTE>
# 000:1a1c2c5d275db13e53ef7d57ffcd75a7f07038b76425717929366f3b5dc941a6f673eff7f4f4f494b0c2566c86333c57
# </PALETTE>

