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
                self.explosion_vaisseau_creation()
                      
    def tir_colision(self):
        """S'il y a colision entre un tir et un ennemi, supprimer l'ennemi"""
        for tir in self.tirs_liste:
            for ennemi in self.ennemis_liste:
                if tir["x"] - ennemi["x"] in range (-1, 9) and tir["y"] - ennemi["y"] in range (-1, 9):
                    self.ennemis_liste.remove(ennemi)
                    
    def explosion_vaisseau_creation(self):
        """Creation d'une explosion quand il y a colision entre un ennemi et le vaisseau"""
        self.explosions_liste.append({"x" : self.vaisseau_x+4, "y" : self.vaisseau_y+4})        
    

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
        
        self.vaisseau_colision()
        self.tir_colision()


    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)
        
        if self.vies > 0:
            # vaisseau (carre 8x8)
            pyxel.rect(self.vaisseau_x, self.vaisseau_y, 8, 8, 1)
            
            #tirs
            for tir in self.tirs_liste:
                pyxel.rect(tir["x"], tir["y"], 1, 4, 10)
                
            # un ennemi par seconde
            for ennemi in self.ennemis_liste:
                pyxel.rect(ennemi["x"], ennemi["y"], 8, 8, 2)
                
            # explosions
            for explosion in self.explosions_liste:
                pyxel.circ(explosion["x"], explosion["y"], 3, 9)
                
        
        else:
            pyxel.text(50,64, 'GAME OVER', 7)
            #pyxel.text(57,80, 'cheh', 5)

Jeu()