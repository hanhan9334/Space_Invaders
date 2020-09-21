import sys
import pygame
import os
from settings import Settings
from ship import Ship
from game_functions import check_events, update_screen, update_bullets, create_fleet, update_aliens
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create the fleet of aliens.
    create_fleet(ai_settings, screen, ship, aliens)

    # Make an alien.
    alien = Alien(ai_settings, screen)

    while True:
        check_events(ai_settings, screen, stats, sb,
                     play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            update_bullets(ai_settings, screen, stats,
                           sb, ship, aliens, bullets)
            update_aliens(ai_settings, screen, stats,
                          sb, ship, aliens, bullets)
        # Redraw the screen during each pass through the loop.
        update_screen(ai_settings, screen, stats, sb, ship,
                      aliens, bullets, play_button)


run_game()
