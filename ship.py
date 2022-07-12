import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """
    Gemiyi yönetecek bir sınıf.
    """
    def __init__(self, ai_game):
        """
        Gemiyi başlat ve başlangıç konumunu belirle.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Gemiyi yükle ve dikdörtgenini al.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Her gemiyi ekranın alt merkezinde başlat.
        self.rect.midbottom = self.screen_rect.midbottom
        # Geminin yatay konumu için ondalık bir değeri sakla.
        self.x = float(self.rect.x)
        self.moving_right = False  # Hareket bayrakları
        self.moving_left = False
        
    def update(self):
        """
        Hareket bayrağına bağlı olarak geminin konumunu güncelle.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:  # recti değil de geminin x değerini güncelle.
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x  # self.x den rect nesnesini güncelle
        
    def blitme(self):
        """
        Gemiyi mevcut konumda çiz.
        """
        self.screen.blit(self.image, self.rect)
        
    
    def center_ship(self):
        # gemiyi ekranda merkeze koy.
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)