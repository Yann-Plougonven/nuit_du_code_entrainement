import pyxel
import random

class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau_x = 60
        self.vaisseau_y = 60
        
        self.tirs_liste = []
        self.ennemis_liste = []
        self.frame_count = 0  # Nombre d'image affichées depuis le début du jeu
        self.vies = 3
        self.explosions_liste = []
        
        pyxel.load("images.pyxres") # load les ressources et images METTRE AVANT LE RUN
        pyxel.run(self.update, self.draw)
        


    def vaisseau_deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x<120:
            self.vaisseau_x += 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x>0:
            self.vaisseau_x += -1
        if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y<120:
            self.vaisseau_y += 1
        if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y>0:
            self.vaisseau_y += -1
    
    def tir_creation(self):
        """Creation d'un tir quand la touche space est pressée"""
        if pyxel.btnr(pyxel.KEY_SPACE):
             self.tirs_liste.append({"x" : self.vaisseau_x+4, "y" : self.vaisseau_y-4})
    
    def tir_deplacement(self):
        """Delacement des tirs vers le haut et suppression s'ils sortent du cadre"""
        for tir in self.tirs_liste:
            tir["y"] -= 1
            if tir["y"]<-8:
                self.tirs_liste.remove(tir)
                
    def ennemis_creation(self):
        """Creation d'un ennemi toutes les secondes"""
        if (pyxel.frame_count % 30 == 0):
            self.ennemis_liste.append({"x" : random.randint(0, 120), "y" : 0})
    
    def ennemi_deplacement(self):
        """Delacement des tirs vers le haut et suppression s'ils sortent du cadre"""
        for ennemi in self.ennemis_liste:
            ennemi["y"] += 1
            if ennemi["y"]>120:
                self.ennemis_liste.remove(ennemi)
                
    def vaisseau_colision(self):
        """S'il y a colision entre le vaisseau et un ennemi, game over"""
        for ennemi in self.ennemis_liste:
            if self.vaisseau_x - ennemi["x"] in range (-8, 9) and self.vaisseau_y - ennemi["y"] in range (-8, 9):
                self.vies -= 1
                self.ennemis_liste.remove(ennemi)
                self.explosions_creation(self.vaisseau_x, self.vaisseau_y)
                      
    def tir_colision(self):
        """S'il y a colision entre un tir et un ennemi, supprimer l'ennemi"""
        for tir in self.tirs_liste:
            for ennemi in self.ennemis_liste:
                if tir["x"] - ennemi["x"] in range (-1, 9) and tir["y"] - ennemi["y"] in range (-1, 9):
                    self.ennemis_liste.remove(ennemi)
                    self.tirs_liste.remove(tir)
                    self.explosions_creation(ennemi["x"], ennemi["y"])
                    
    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])
    
    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            explosion[2] +=1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)
    

    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.vaisseau_deplacement()
        
        # creation des tirs en fonction de la position du vaisseau
        self.tir_creation()
        
        # Mise à jour de la position des tirs
        self.tir_deplacement()
        
        # Mise à jour de la position des tirs
        self.frame_count += 1
        self.ennemis_creation()
        
        # Mise à jour de la position des ennemis
        self.ennemi_deplacement()
        
        # Update de l vérification des collisions
        self.vaisseau_colision()
        self.tir_colision()
        
        # evolution de l'animation des explosions
        self.explosions_animation()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
        
        if self.vies >= 1:
            pyxel.blt(0, 1, 0, 8, 24, 8, 8)
            if self.vies >= 2:
                pyxel.blt(9, 1, 0, 8, 24, 8, 8)
            if self.vies == 3:
                pyxel.blt(18, 1, 0, 8, 24, 8, 8)
            
            #vaisseau
            pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 8, 8)
            
            #tirs
            for tir in self.tirs_liste:
                pyxel.rect(tir["x"], tir["y"], 1, 4, 10)
                
            # un ennemi par seconde
            coef = pyxel.frame_count  // 3%3
            for ennemi in self.ennemis_liste:
                pyxel.blt(ennemi["x"], ennemi["y"], 0, 0, 8 + 8*coef, 8, 8)
                #pyxel.rect(ennemi["x"], ennemi["y"], 8, 8, 2)
                
            # explosions
            for explosion in self.explosions_liste:
                for explosion in self.explosions_liste:
                    pyxel.circb(explosion[0]+4, explosion[1]+4, 2*(explosion[2]//4), 8+explosion[2]%3)
                
        else:
            pyxel.text(50,64, 'GAME OVER', 7)
            pyxel.text(57,80, 'cheh', 5)

Jeu()