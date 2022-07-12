import pygame.font

class Button:
    
    def __init__(self, ai_game, msg):
        """Düğmenin niteliklerine ilk değer ata."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        # Düğmenin boyutlarını ve özelliklerini ayarla.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # düğmenin rect nesnesini oluştur ve merkeze koy
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # düğmenin mesajının sadece bir kez hazırlanması gerekir.
        self._prep_msg(msg)
        
        
    def _prep_msg(self, msg):
        """msg yi işlenmiş bir resme dönüştür. ve metni düğmenin merkezine yerleştir."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) # msgde saklı olan mesajı resme dönüştürür.
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
        
    def draw_button(self):
        # boş bir düğme çiz ve sonra mesajı çiz.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
        