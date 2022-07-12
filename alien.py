import aifc
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    
    def __init__(self, ai_game):
        """Uzaylıyı başlat ve başlangıç konumunu ayarla."""
        
        super().__init__() # üst sınıftaki bir metodu çağırabilmemizi sağlar.
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Uzaylı resmini yükle ve rect niteliği oluştur.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # Her bir uzaylıtı ewkranın üst kısmına yakın bir yerde başlat
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # Uzaylının tam yatay konumunu sakla.
        self.x = float(self.rect.x)
    
    
    def check_edges(self):
        """uzaylı ekranın kenarındaysa true döndür."""   
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        
        """Uzaylıyı sağa hareket ettir."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x