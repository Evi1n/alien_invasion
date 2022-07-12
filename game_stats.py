class GameStats:
    # uzaylı istilası için istatistikleri tut.
    
    def __init__(self, ai_game):
        # istatistiklere ilk değer ata.
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False # uzaylı istilasını inaktif bir durumda başlat
        self.high_score = 0
        
    
    def reset_stats(self):
        # oyun esnasında değişebilecek istatistiklere ilk değer ata.
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1