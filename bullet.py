import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """Gemiden ateşlenen mermileri yöneten bir sınıf"""
    
    def __init__(self, ai_game):
        
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # (0,0) da bir mermi recti oluştur ve doğru konuma ayarla.
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # merminin konumunu ondalık bir değer olarak sakla.
        self.y = float(self.rect.y)
        
        
    def update(self):
        """Mermiyi ekranda yukarı hareket ettirir."""
        
        self.y  -= self.settings.bullet_speed
        
        # rect konumunu güncelle
        self.rect.y = self.y
        
        
    def draw_bullet(self):
        """Mermiyi ekrana çiz"""
        
        pygame.draw.rect(self.screen, self.color, self.rect)
        
        