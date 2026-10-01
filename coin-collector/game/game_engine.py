import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT


NUM_COINS = 6

COIN_TYPES = [
    (1, (184, 115, 51)),   # Bronze
    (3, (192, 192, 192)),  # Silver
    (5, (255, 215, 0)),    # Gold
]


class GameEngine:
    def __init__(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0

        self.lives = 3

        self.obstacles = [
            pygame.Rect(100, 100, 100, 30),
            pygame.Rect(450, 150, 30, 120),
            pygame.Rect(250, 350, 120, 30),
        ]

        self.was_colliding = False
        

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)

        value, color = random.choice(COIN_TYPES)

        return Coin(
            x=x,
            y=y,
            radius=12,
            value=value,
            color=color,
        )

    def handle_input(self, keys_pressed):
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
            self.coins.remove(coin)

        player_rect = self.player.get_rect()

        currently_colliding = any(
            player_rect.colliderect(obstacle)
            for obstacle in self.obstacles
        )

        if currently_colliding and not self.was_colliding:
            self.lives -= 1

        self.was_colliding = currently_colliding

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(
            surface,
            self.player,
            self.coins,
            self.obstacles,
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10),
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40),
        )