import pygame
import os
import math
from settings import *
from enemy import *

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """
        #用來判斷enemy是否在tower的攻擊範圍內
        en_x, en_y=enemy.get_pos()  #enemy的座標
        tw_x, tw_y=self.center  #tower的座標
        distance_enemy_tower = math.sqrt((en_x-tw_x)**2+(en_y-tw_y)**2)  #enemy到tower的距離
        if distance_enemy_tower <= self.radius:  #若enemy在tower的攻擊範圍內（enemy到tower的距離<=tower的半徑）
            return True
        else:
            return False


    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        transparent_surface=pygame.Surface((WIN_WIDTH,WIN_HEIGHT),pygame.SRCALPHA)  #要繪製有透明度圓形的畫布大小
        transparency=60  #透明度
        pygame.draw.circle(transparent_surface,(255,255,255,transparency),self.center,self.radius,0)  #圓形的形狀,顏色,大小
        win.blit(transparent_surface,(0,0))  #繪出transparent_surface的位置


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected =True  # the state of whether the tower is selected
        self.type = "tower"
        self.image_range= 70  #tower圖片可點擊的範圍

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """
        #判斷tower是否完全cool down
        if self.cd_count < self.cd_max_count:  #若cd_count小於cd_max_count,cd_count+1且回傳False
            self.cd_count+=1
            return False
        else:  #反之,將cd_count歸零,並回傳True
            self.cd_count=0
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """

        if self.is_cool_down() == True:  #若tower有冷卻
            for en in enemy_group.get():
                if self.range_circle.collide(en)==True:  #若enemy有在tower的攻擊範圍內
                    en.get_hurt(self.damage)  #扣除enemy的生命值
                    return  #因為tower只能同時攻擊範圍內的一個enemy,故終止迴圈
        pass

    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        #判斷游標位置是否在tower image上
        if (self.rect.x <= x <= self.rect.x+self.image_range and  #因為圖片只有一個座標點,故將範圍擴展至70*70
            self.rect.y <= y <= self.rect.y+self.image_range):  #若游標的x,y座標皆在範圍內,回傳True
            return True
        else:  #反之,回傳False
            return False
        pass

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

