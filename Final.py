import pygame, csv, os ,math
width=1440
height=810
window=pygame.display.set_mode(((width,height)))
PlayerList=[]
pygame.init()
index=0
class Tile(object):
    def __init__(self,image,x,y):
        self.width=45
        self.height=45
        self.image=pygame.transform.scale(pygame.image.load(f'{image}'+'.png'),(self.width,self.height))
        self.x=x
        self.y=y
        self.dy=5
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y))


class Box (Tile):
    def __init__(self,image,x,y):
        self.width=45
        self.height=45
        self.dy=5
        self.dx=5
        super().__init__(image,x,y)
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)

class Elevator(Tile):
    def __init__(self,image,x,y):
        self.width=45
        self.height=45
        self.dy=10
        self.initY=y
        self.halfY=y-20
        self.position='still'  
        super().__init__(image,x,y)
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)      
    def elevreinitiate(self):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)    
class Liquid(Tile):
    def __init__(self,image,x,y):
        self.width=45
        self.height=45
        super().__init__(image,x,y)
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        
class Button(Tile):
    def __init__(self,image,x,y):
        self.width=45
        self.height=45
        self.state='notPressed'
        self.PressedImage=pygame.transform.scale(pygame.image.load(f'{image}'+'_Pressed'+'.png'),(self.width,self.height))
        self.notPressedImage=pygame.transform.scale(pygame.image.load(f'{image}'+'.png'),(self.width,self.height))
        super().__init__(image,x,y)
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
    def ButtonPress(self):
        for i in PlayerList:
            if pygame.Rect.colliderect(self.rect,i.rect):
                self.state='Pressesd'
                self.image=self.PressedImage
        if pygame.Rect.colliderect(self.rect,PlayerList[0].rect)==False:
            #self.state='notPressed'
            self.image=self.notPressedImage
        for item in level.tiles[3]:
            boxrect=item.rect
            if pygame.Rect.colliderect(self.rect,boxrect):
                 self.image=pygame.transform.scale(pygame.image.load(f'{image}'+'_Pressed'+'.png'),(self.width,self.height))
                 self.state='Pressesd'
                 self.image=self.PressedImage
     
    def buttonStates(self):
        self.ButtonPress()
        if self.state=='Pressed':
            print('hi')
            for key in level.controllerDic:
                for elev in level.controllerDic[key]:
                    print(elev.position,elev.dy,elev.y)
                    if elev.position=='still':
                        elev.position='down'
                    if elev.position=='down':
                        elev.dy+=5
                        elev.y += elev.dy
                        self.elevreinitiate()
                    if elev.dy==20:
                        elev.y=elev.halfY
                        self.elevreinitiate()
                        elev.position='still'
                key.ButtonPress()
        if self.state=='notPressed':
            for key in level.controllerDic:
                for elev in level.controllerDic[key]:
                    if elev.position=='still':
                        elev.position=='up'
                    if elev.position=='up':  
                        elev.dy+=5
                        elev.y -= elev.dy
                        elev.elevreinitiate()
                    if elev.dy==20:
                        elev.y= elev.initY
                        elev.elevreinitiate()
                        elev.position=='still'
                key.ButtonPress()    
class TileMap():
    def __init__(self, filename):
        self.start_x, self.start_y = 0, 0
        self.tile_size=45
        self.Tiles = []
        self.diamonds=[]
        self.buttons=[]
        self.switches=[]
        self.boxes=[]
        self.liquids=[]
        self.controllers1=[]
        self.controllers2=[]
        self.elevators=[]
        self.elevators1=[]
        self.elevators2=[]
        self.Bdiamonds=[]
        self.Gdiamonds=[]
        self.Bliquids=[]
        self.Gliquids=[]
        self.controllerDic={}
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.image=self.load_map()
        self.buttonsDic={}
        self.Dic={"boy":[self.Bdiamonds]+[self.Bliquids],"girl":[self.Gdiamonds]+[self.Gliquids]}
        self.state="playing"
    def draw_map(self, surface):
        window.blit(self.map_surface, (0, 0))

    def load_map(self):
        for lists in self.tiles:
            for tile in lists:
                tile.draw(window)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        map = self.read_csv(filename)
        x1, y1 = 0,0
        for row in map:
            x1 = 0
            for tile in row:
                #tilesDic[Tile.y]=row
                if tile == '77':
                    self.Tiles.append(Tile('dirtHillRight', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '81':
                    self.Tiles.append(Tile('dirtMid', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '65':
                    self.Tiles.append(Tile('dirtCenter', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '4':
                    self.Bdiamonds.append(Tile('hud_gem_blue', x1 * self.tile_size, y1 * self.tile_size))
                    self.diamonds.append(Tile('hud_gem_blue', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '3':
                    self.Gdiamonds.append(Tile('hud_gem_red', x1 * self.tile_size, y1 * self.tile_size))
                    self.diamonds.append(Tile('hud_gem_red', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '6':
                    self.Bdiamonds.append(Tile('keyBlue', x1 * self.tile_size, y1 * self.tile_size))
                    self.diamonds.append(Tile('keyBlue', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '5':
                    self.diamonds.append(Tile('keyRed', x1 * self.tile_size, y1 * self.tile_size))
                    self.Gdiamonds.append(Tile('keyRed', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '95':
                     self.Gliquids.append(Liquid('WaterOriginal', x1 * self.tile_size, y1 * self.tile_size))
                     self.liquids.append(Liquid('WaterOriginal', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '91':
                     self.Bliquids.append(Liquid('LavaOriginal', x1 * self.tile_size, y1 * self.tile_size))
                     self.liquids.append(Liquid('LavaOriginal', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '1':
                    self.Tiles.append(Box('boxAlt', x1 * self.tile_size, y1 * self.tile_size))
                    self.boxes.append(Box('boxAlt', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '0':
                    self.controllers1.append(Button('buttonYellow', x1 * self.tile_size, y1 * self.tile_size))
                    self.buttons.append(Button('buttonYellow', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '1309' or tile == '99' :
                    self.controllers1.append(Button('buttonGreen', x1 * self.tile_size, y1 * self.tile_size))
                    self.buttons.append(Button('buttonGreen', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '47':
                    self.elevators1.append(Elevator('dirtHalf', x1 * self.tile_size, y1 * self.tile_size))
                    self.elevators.append(Elevator('dirtHalf', x1 * self.tile_size, y1 * self.tile_size))
                elif tile == '28':
                    self.elevators2.append(Elevator('castleHalf', x1 * self.tile_size, y1 * self.tile_size))
                    self.elevators.append(Elevator('castleHalf', x1 * self.tile_size, y1 * self.tile_size))   
#                 #add boxes and the keys and values
                    # Move to next tile in current row
                x1 += 1

            # Move to next row
            y1 += 1
            # Store the size of the tile map
        for controller in self.controllers1:
            self.controllerDic[controller]=self.elevators1
        for controller2 in self.controllers2:
            self.controllerDic[controller]=self.elevators2   
        self.map_w, self.map_h = 2240, 1260
        return [self.Tiles]+[self.switches]+[self.diamonds]+[self.boxes]+[self.buttons]+[self.liquids]+[self.elevators]  

level=TileMap("levelmap2.csv")

class Character(object):
    def __init__(self,x,y,gender):
        self.x=x
        self.y=y
        self.dx=10
        self.dy=10
        self.width=40
        self.height=70
        self.state='alive'
        self.direction="stand"
        self.gender=gender
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)
        self.right=[]
        self.left=[]
        self.index=0
        self.indexL=0
#boy animation images        
        if self.gender=='girl':
            self.StandImage=pygame.transform.scale((pygame.image.load('p3_stand.png')),(self.width,self.height))
            
            self.rightImages=[pygame.image.load('p3_walk01.png'),pygame.image.load('p3_walk02.png'),pygame.image.load('p3_walk03.png'),
            pygame.image.load('p3_walk04.png'),pygame.image.load('p3_walk05.png'),pygame.image.load('p3_walk06.png'),
            pygame.image.load('p3_walk06.png'),pygame.image.load('p3_walk07.png'),pygame.image.load('p3_walk08.png'),
            pygame.image.load('p3_walk09.png'),pygame.image.load('p3_walk10.png'),pygame.image.load('p3_walk11.png')]
            #girl animation images             
        elif self.gender=='boy':
            self.StandImage=pygame.transform.scale((pygame.image.load('p2_stand.png')),(self.width,self.height))

            
            self.rightImages=[pygame.image.load('p2_walk01.png'),pygame.image.load('p2_walk02.png'),pygame.image.load('p2_walk03.png'),
            pygame.image.load('p2_walk04.png'),pygame.image.load('p2_walk05.png'),pygame.image.load('p2_walk06.png'),
            pygame.image.load('p2_walk06.png'),pygame.image.load('p2_walk07.png'),pygame.image.load('p2_walk08.png'),
            pygame.image.load('p2_walk09.png'),pygame.image.load('p2_walk10.png'),pygame.image.load('p2_walk11.png')]
        for image in self.rightImages:
            self.right.append(pygame.transform.scale(image,(self.width,self.height)))
        for image2 in self.right:
            self.left.append(pygame.transform.scale(pygame.transform.flip(image, True,False),(self.width,self.height)))
    def reinitiate(self):
        self.rect=pygame.Rect(self.x,self.y,self.width,self.height)   
    def diamondsCollision(self,gender):
        if gender=="boy":
            for d in level.Dic['boy'][0]:
                if pygame.Rect.colliderect(self.rect,d.rect):
                    for i in range(len(level.diamonds)-1):
                        if level.diamonds[i].x==d.x and level.diamonds[i].y==d.y:
                            level.diamonds.pop(i)
                            break
        if gender=="girl":
            for diamond1 in level.Dic['girl'][0]:
                if pygame.Rect.colliderect(self.rect,diamond1.rect):
                    for i in range(len(level.diamonds)-1):
                        if level.diamonds[i].x==diamond1.x and level.diamonds[i].y==diamond1.y:
                            level.diamonds.pop(i)
                            break
    def liquidCollision(self):
        if gender=="boy":
            for LW in level.Dic['girl'][1]:
                if pygame.Rect.colliderect(self.rect,d.rect):
                    for i in range(len(level.Gliquids)-1):
                        if level.Gliquids[i].x==LW.x and level.Gliquids[i].y==LW.y:
                           boy.state="game over"
        if gender=="girl":
            for LL in level.Dic['boy'][0]:
                if pygame.Rect.colliderect(self.rect,diamond.rect):
                    for i in range(len(level.Bliquids)-1):
                        if level.Bliquids[i].x==LW.x and level.Bliquids[i].y==LW.y:
                           boy.state="game over"
    
    def UpdateCharacter(self):
        keyPressed=pygame.key.get_pressed()
        if self.gender=='boy':
            if keyPressed[pygame.K_LEFT]:
                self.direction='left'
                self.x -= self.dx
                self.reinitiate()
                self.diamondsCollision('boy')
                for i in level.tiles[0]:
                    tilerect=i.rect
                    if pygame.Rect.colliderect(self.rect,tilerect)and abs(self.rect.bottom-tilerect.top)>=10:
                        self.x += self.dx
                        self.reinitiate()
                        break
                for button in level.tiles[4]:
                    button.buttonStates()
            elif keyPressed[pygame.K_RIGHT]:
                self.direction='right'
                self.x += self.dx
                self.reinitiate()
                for i in level.tiles[0]:
                    tilerect=i.rect
                    if pygame.Rect.colliderect(self.rect,tilerect) and abs(self.rect.bottom-tilerect.top)>=10 :
                        self.x -= self.dx
                        self.reinitiate()
                        break
                for button in level.tiles[4]:
                    button.buttonStates()
                self.diamondsCollision(f'{self.gender}')
            if keyPressed[pygame.K_UP]:
                self.direction='up'
        if self.gender=='girl':
            if keyPressed[pygame.K_a]:
                self.direction='left'
                self.x -= self.dx
                self.reinitiate()
                self.diamondsCollision('girl')
                for i in level.tiles[0]:
                    tilerect=i.rect
                    if pygame.Rect.colliderect(self.rect,tilerect)and abs(self.rect.bottom-tilerect.top)>=10:
                        self.x += self.dx
                        self.reinitiate()
                        break
                for button in level.tiles[4]:
                    button.buttonStates()
            elif keyPressed[pygame.K_d]:
                self.x += self.dx
                self.direction='right'
            if keyPressed[pygame.K_w]:
                self.direction='up'
            else:
                self.dy=1
    def downCollision(self,other):
        for i in other:
            tilerect=i.rect
            if pygame.Rect.colliderect(self.rect,tilerect):
                if abs(self.rect.bottom-tilerect.top)<11:
                    return tilerect 
        return 0

    def draw(self,surface):
        if self.direction=='right':
            surface.blit(self.right[index], (self.x, self.y))
            self.index+=1
            if self.index==len(self.right):
                self.index=0
                self.direction='stand'
        if self.direction=='left':
            surface.blit(self.right[self.indexL], (self.x, self.y))
            self.indexL+=1
            if self.indexL==len(self.right):
                self.indexL=0
                self.direction='stand'
        if self.direction=='stand':
            surface.blit(self.StandImage, (self.x, self.y))
        if self.direction=='up':
            surface.blit(self.StandImage, (self.x, self.y))    


def main():
    i=0
    boy=Character(100,550,"boy")
    girl=Character(100,550,"girl")
    levelimg=pygame.image.load('screenshot2.png')
    PlayerList.append(boy)
    PlayerList.append(girl)
    run=True
    clock = pygame.time.Clock()
    while run:
        boy.reinitiate()
        girl.reinitiate()
        if boy.state=="alive":
#checking boy collision with tiles
            if boy.direction!="up":
               if boy.downCollision(level.tiles[0])==0:
                   boy.y+=6
            if boy.direction=="up":
                boy.y-=boy.dy
                boy.dy-=1
                boy.reinitiate()
                for i in level.tiles[0]:
                    tilerect=i.rect
                    if pygame.Rect.colliderect(boy.rect,tilerect):
                        if boy.dy>0:
                            print('collide up')
                            boy.dy=-boy.dy
                            boy.dy-=1
                            boy.reinitiate()
                            break
            print(boy.dy)
            if boy.dy==-10:
                boy.dy=10
                boy.reinitiate()
                boy.direction="stand"
        else:
            boy.image="ghoast.png"
            level.sate="game over"
        if girl.state=="alive":
#checking girl collision with tiles
            if girl.direction!="up":
               if girl.downCollision(level.tiles[0])==0:
                   girl.y+=6
                   girl.reinitiate()
            if girl.direction=="up":
                girl.y-=girl.dy
                girl.dy-=1
                girl.reinitiate()
                for i in level.tiles[0]:
                    tilerect=i.rect
                    if pygame.Rect.colliderect(girl.rect,tilerect):
                        if girl.dy>0:
                            girl.dy=-girl.dy
                            girl.dy-=1
                            girl.reinitiate()
                            break
            if girl.dy==-11:
                girl.dy=10
                girl.reinitiate()
                girl.direction="stand"
        else:
            girl.image="ghoast.png"
            level.sate="game over"    
        
#         if level.sate="game over":
#             
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run =False    
        window.blit(levelimg, (0, 0))
        for box in level.boxes:
            window.blit(box.image,(box.x,box.y))
        for buttons in level.buttons:
            window.blit(buttons.image,(buttons.x,buttons.y))
        for diamonds in level.diamonds:
            window.blit(diamonds.image,(diamonds.x,diamonds.y))
        for liquids in level.liquids:
            window.blit(liquids.image,(liquids.x-4,liquids.y))
        for elevators in level.elevators:
            window.blit(elevators.image,(elevators.x-4,elevators.y))
        boy.UpdateCharacter()
        girl.UpdateCharacter()
        window.blit(level.map_surface, (0, 0))
        boy.draw(window)
        girl.draw(window)
        pygame.display.update()
    pygame.quit()
if __name__=="__main__":
    main()
     