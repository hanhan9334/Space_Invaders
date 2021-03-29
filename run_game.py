import sys
import pygame
import os
from settings import Settings
from ui.ship import Ship
from logic.game_logic import check_events, update_screen, update_bullets, create_fleet, update_aliens, check_play_button
from pygame.sprite import Group
from ui.alien import Alien
from logic.game_stats import GameStats
from ui.button_play import ButtonPlay
from ui.button_over import ButtonOver
from ui.scoreboard import Scoreboard
from db.db import getAllRankings, saveScoreToDb


class GameStage():
    def __init__(self):
        self.stage = 'welcome'

    def welcome(self):
        global textUserInput

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    textUserInput = textUserInput[:-1]
                    screen.fill((0, 0, 0))
                    print(textUserInput)
                else:
                    textUserInput += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings, screen, stats, sb, play_button,
                                  ship, aliens, bullets, mouse_x, mouse_y)
                button_clicked = play_button.rect.collidepoint(
                    mouse_x, mouse_y)
                if button_clicked:
                    self.stage = 'game'

        screen.blit(textTitle, textRectTitle)
        screen.blit(textRankTitle, textRectTitleRanking)

        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        screen.blit(text3, text3Rect)
        screen.blit(text4, text4Rect)
        screen.blit(text5, text5Rect)

        play_button.draw_button()

        package_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(package_dir, 'images/alien.png')
        logo = pygame.image.load(filename)
        logo = pygame.transform.scale(logo, (100, 70))
        screen.blit(logo, (550, 150))
        text_username_surface = font.render(textUserInput, True, blue)
        screen.blit(text_username_surface, (600, 550))
        screen.blit(textUserNameLabel, (400, 550))
        pygame.display.flip()

    def game(self):

        global user_score
        if stats.game_active == False:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    over_button_clicked = over_button.rect.collidepoint(
                        mouse_x, mouse_y)
                    start_button_clicked = play_button.rect.collidepoint(
                        mouse_x, mouse_y)
                    if over_button_clicked:
                        user_score = sb.stats.score
                        saveScoreToDb(textUserInput, user_score)
                        self.stage = 'over'
                    elif start_button_clicked:
                        check_play_button(
                            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
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
                      aliens, bullets, play_button, over_button)

    def over(self):
        screen.fill((0, 0, 0))

        listNames = getAllRankings()[0]
        listScores = getAllRankings()[1]

        # Text user score
        textRankTitle = font.render(
            'Your Score: ' + str(user_score), True, green)
        textRectTitleRanking = textRankTitle.get_rect()
        textRectTitleRanking.center = (600, 600)

        # Render ranking1
        text1 = font.render(
            "1      "+listNames[0]+"        " + str(listScores[0]), True, blue)
        text1Rect = text1.get_rect()
        text1Rect.center = (600, 300)
        # Render Ranking 2
        text2 = font.render(
            "2      "+listNames[1]+"        " + str(listScores[1]), True, blue)
        text2Rect = text2.get_rect()
        text2Rect.center = (600, 350)
        # Render Ranking 3
        text3 = font.render(
            "3      "+listNames[2]+"        " + str(listScores[2]), True, blue)
        text3Rect = text2.get_rect()
        text3Rect.center = (600, 400)
        # Render Ranking 4
        text4 = font.render(
            "4      "+listNames[3]+"        " + str(listScores[3]), True, blue)
        text4Rect = text4.get_rect()
        text4Rect.center = (600, 450)
        # Render Ranking 2
        text5 = font.render(
            "5      "+listNames[4]+"        " + str(listScores[4]), True, blue)
        text5Rect = text5.get_rect()
        text5Rect.center = (600, 500)
        screen.blit(textTitle, textRectTitle)
        screen.blit(textRankTitle, textRectTitleRanking)

        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        screen.blit(text3, text3Rect)
        screen.blit(text4, text4Rect)
        screen.blit(text5, text5Rect)

        package_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(package_dir, 'images/alien.png')
        logo = pygame.image.load(filename)
        logo = pygame.transform.scale(logo, (100, 70))
        screen.blit(logo, (550, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Make the most recently drawn screen visible.
        pygame.display.flip()

    def stageManager(self):
        if self.stage == 'welcome':
            self.welcome()
        elif self.stage == 'game':
            self.game()
        elif self.stage == 'over':
            self.over()


pygame.init()
ai_settings = Settings()
screen = pygame.display.set_mode(
    (ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption("Space Invaders")

# Make the Play button.
play_button = ButtonPlay(ai_settings, screen, "Play")

over_button = ButtonOver(ai_settings, screen, "Save Score")

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

font = pygame.font.Font('freesansbold.ttf', 32)
green = (0, 255, 0)
blue = (0, 0, 128)
# Set game title
textTitle = font.render('Game - Space Invaders', True, green, blue)
textRectTitle = textTitle.get_rect()
textRectTitle.center = (600, 100)
# Set "Ranking"
textRankTitle = font.render('Rankings', True, green)
textRectTitleRanking = textRankTitle.get_rect()
textRectTitleRanking.center = (600, 250)

listNames = getAllRankings()[0]
listScores = getAllRankings()[1]
# Render ranking1
text1 = font.render(
    "1      "+listNames[0]+"        " + str(listScores[0]), True, blue)
text1Rect = text1.get_rect()
text1Rect.center = (600, 300)
# Render Ranking 2
text2 = font.render(
    "2      "+listNames[1]+"        " + str(listScores[1]), True, blue)
text2Rect = text2.get_rect()
text2Rect.center = (600, 350)
# Render Ranking 3
text3 = font.render(
    "3      "+listNames[2]+"        " + str(listScores[2]), True, blue)
text3Rect = text2.get_rect()
text3Rect.center = (600, 400)
# Render Ranking 4
text4 = font.render(
    "4      "+listNames[3]+"        " + str(listScores[3]), True, blue)
text4Rect = text4.get_rect()
text4Rect.center = (600, 450)
# Render Ranking 2
text5 = font.render(
    "5      "+listNames[4]+"        " + str(listScores[4]), True, blue)
text5Rect = text5.get_rect()
text5Rect.center = (600, 500)

textUserNameLabel = font.render('Your Name: ', True, green)

user_score = 0
textUserInput = ''

gameStage = GameStage()

while True:

    gameStage.stageManager()
