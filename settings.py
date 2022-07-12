class Settings:
    """
    Uzaylı istilası için bütün ayarları saklayan bit sınıf.
    """
    
    def __init__(self):
        """
        Oyunun ayarlarına ilk değer atayınız.
        """
        # Ekran ayarları 
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        # Gemi ayarları
        self.ship_limit = 3
        
        # Mermi ayarları
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3 # oyuncuyu tek seferde üç mermi ile sınırladık.
        
        # uzaylı hızını kontrol etmek için gerekli ayar. 
        self.fleet_drop_speed = 10
        
        # oyunun ne kadar çabuk hızlandığı
        self.speedup_scale = 1.1
        
        # filo yönü ; 1 sağı , -1 solu temsil etmektedir.
        # self.fleet_direction = 1
        
        self.score_scale = 1.5  # uzaylı puanları artışı
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        # oyun boyunca değişen değerlere ilk değer ata.
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.8
        
        # filo yönü olarak 1 sağa 1 sola temsil eder
        self.fleet_direction = 1
        
        # skor verme
        self.alien_points = 50
        
    def increase_speed(self):
        # hız ayarlarını arttır.
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
        
       