import sys     # Oyuncunun oyundan çıkışını sağlamak için.
from time import sleep
import pygame  # Oyun oluşturmak için gerekli işlevsellik.
import random

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """
    Oyunun değerlerini ve davranışlarını yönetmek için genel bir sınıf.
    """
    def __init__(self):
        """Oyunu başlat ve oyun kaynaklarını oluştur."""
        
        pygame.init()
        self.settings = Settings()  # Settingsin bir örneğini oluşturduk ve bunu self.settingse atadık.
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)  # Oyunu tam ekran modunda oynayabilmek için.
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self) # oyun istatistiklerini saklamak için bir örnek.
        self.sb = Scoreboard(self) # scoreboard için örnek.
        self.ship = Ship(self)  # Shipin bir örneğini oluşturuyoruz.
        self.bullets = pygame.sprite.Group()  # canlı mermileri saklamak için bir grup oluşturduk.
        self.aliens = pygame.sprite.Group()  # uzaylı filosunu tutmak için bir grup oluşturduk.
        self._create_fleet() 
        self.play_button = Button(self, "Play") # play düğmesini oluştur.
        
        
        
    def run_game(self):
        """Oyun içina ana döngüyü başlat."""
        while True:
            # Klavye ve fare olaylarını gözle.
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            # self.screen.fill(self.bg_color)  # Döngüden her geçişte ekranı yeniden çizdirir.

            
    def _check_events(self):  # Klavye fare olaylarına yanıt ver. run_game metodundan buraya taşıdık daha kodu yalıtmak amacıyla.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                    
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
            
    def _check_keydown_events(self, event):
        """Tuşa basmalara yanıt ver."""
        if event.key == pygame.K_RIGHT:  # Gemiyi sağa hareket ettirir.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: # Gemiyi sola hareket ettirir.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:    # q ile oyundan çıkmasını sağladık.
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if not self.stats.game_active:
                # oyun ayarlarını resetle.
                self.settings.initialize_dynamic_settings()
                # oyun istatistiklerini resetle.
                self.stats.reset_stats()
                self.stats.game_active = True
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
                
                # geri kalan uzaylı ve mermilerden kurtul.
                self.aliens.empty()
                self.bullets.empty()
                # yeni bir filo oluştur ve merkeze koy.
                self._create_fleet()
                self.ship.center_ship()    
            self._fire_bullet() # boşluk tuşuna basınca _fire_bulleti çağır.
        
            
    
    def _check_keyup_events(self, event):
        """Tuşu serbest bırakmalara yanıt ver."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
        
    def _fire_bullet(self):
        """Yeni bir mermi oluştur ve bu mermiyi mermi grubuna ekle."""    
        if len(self.bullets) < (self.settings.bullets_allowed):
            new_bullet = Bullet(self)  # Bulletin bir örneğini oluşturduk.
            self.bullets.add(new_bullet) # oluşturduğumuz örneği bullets grubuna ekledik.
            
     
    def _update_bullets(self):
        """mermilerin konumunu güncelle ve mermilerden kurtul."""  
        # mermi konumlarını güncelle 
        self.bullets.update()  
        # kaybolan mermilerden kurtul
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # uzaylılara çarpan mermileri kontrol et eğer öyleyse mermi ve uzaylıdan kurtul.
        self._check_bullet_alien_collisions()
        
        
    def _check_bullet_alien_collisions(self):
        """mermi - uzaylı çarpışmasına yanıt ver"""
        # çarpışan mermi ve uzaylıları sil.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()  # skor verme
            self.sb.check_high_score()
        
        if not self.aliens:
            # var olan mermileri imha et ve yeni filo oluştur.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
     
     
    def _update_aliens(self):
        """Filonun kenarda olup olmadığını kontrol et ve daha sonra tüm uzaylıların konumlarını güncelle."""
        self._check_fleet_edges()
        self.aliens.update()
        
        # uzaylı gemi çarpışmalarına bak.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # ekranın alt kısmına çarpan uzaylılar ayarla.
        self._check_aliens_bottom()
        
               
    def _check_aliens_bottom(self):
        # herhangi bir uzaylının ekranın alt kısmına ulaşıp ulaşmadığını kontrol et.
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # buna gemiye çarpıldığındaki gibi yanıt ver.
                self._ship_hit()
                break
            
            
    def _ship_hit(self):
        # uzaylı tarafından vurulan gemiye yanıt ver. kalan gemiyi azalt
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # geri kalan uzaylı ve mermilerden kurtul.
            self.aliens.empty()
            self.bullets.empty()
            
            # yeni bir filo oluştur ve gemiyi merkeze koy.
            self._create_fleet()
            self.ship.center_ship()
            
            # durdur.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            
       
    def _create_fleet(self):
        """Uzaylı filosunu oluştur."""
        # bir uzaylı oluştur ve bir satırdaki uzaylı sayısını bul. her bir uzaylı arasındaki boşluk bir uzaylı genişliğine eşittir.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)
        
        # ekrana sığan uzaylı satırları sayısını belirle.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)
        number_rows = available_space_y // (2*alien_height)
        
        # tüm bir uzaylı filosunu oluştur.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
            
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
        
    def _check_fleet_edges(self):
        """herhanngi bir uzaylı bir kenara ulaştığında uygun bir şekilde yanıt ver."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
            
    def _change_fleet_direction(self):
        """tüm bir filoyu düşür ve filonun yönünü değiştir."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    
    def _update_screen(self):  # Ekrandaki resimleri güncelle ve yeni ekrana dön.
        self.screen.fill(self.settings.bg_color)  # Ekranı doldururken arka plan rengine erişmek için self.settingsi kullandık.
        self.ship.blitme()  # Gemiyi ekrana çizdiriyoruz.
        for bullet in self.bullets.sprites(): # bullets.sprites metodu bullets grubundaki tüm hareketli öğe grafiklerinin bir listesini döndürür.
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score() # skor bilgisini çiz.
            
        if not self.stats.game_active: # oyun aktif değilse play düğmesini çiz
            self.play_button.draw_button()
        pygame.display.flip()  # En son çizilen ekranı görünür yap.
    
    
if __name__ == '__main__':
    # Bir oyun örneği oluştur ve çalıştır.
    ai = AlienInvasion()
    ai.run_game()
        
        

