import random
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT
from game import renderer


NUM_COINS = 6

COIN_TYPES = [
    (1, (184, 115, 51)),   # Bronze
    (3, (192, 192, 192)),  # Silver
    (5, (255, 215, 0)),    # Gold
]
ROUND_DURATION = 30


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
        self.round_start_time = pygame.time.get_ticks()
        self.remaining_time = ROUND_DURATION
        self.round_active = True
        

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

    def handle_input(self, keys):
        if not self.round_active:
            if keys[pygame.K_r]:
                self.reset_round()
            return

        dx = 0
        dy = 0

        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1

        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if not self.round_active:
            return

        elapsed = (pygame.time.get_ticks() - self.round_start_time) / 1000
        self.remaining_time = max(0, ROUND_DURATION - elapsed)

        if self.remaining_time <= 0:
            self.round_active = False
            return

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

        if self.lives <= 0:
            self.round_active = False

    def draw(self, surface, font):
        renderer.draw_scene(
            surface,
            self.player,
            self.coins,
            self.obstacles
        )

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40)
        )

        renderer.draw_text(
            surface,
            font,
            f"Time: {int(self.remaining_time)}",
            (10, 70)
        )

        if not self.round_active:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER - Final Score: {self.score} - Press R to Restart"
            )

        renderer.draw_text(
            surface,
            font,
            f"Time: {int(self.remaining_time)}",
            (10, 70)
        )

        if not self.round_active:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER - Final Score: {self.score} - Press R to Restart"
            )
    def reset_round(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        self.coins = [
            self._random_coin()
            for _ in range(NUM_COINS)
        ]

        self.score = 0
        self.lives = 3

        self.was_colliding = False

        self.round_start_time = pygame.time.get_ticks()
        self.remaining_time = ROUND_DURATION
        self.round_active = True