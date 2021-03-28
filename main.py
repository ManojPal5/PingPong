from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PingBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    def update_position(self, new_y_position):
        self.center_y = new_y_position

    def address_collision(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player1score = NumericProperty(0)
    player2score = NumericProperty(0)

    def set_ball_velocity(self, velocity):
        self.ball.velocity = velocity

    def update(self, dt):
        self.ball.move()
        if self.ball.x < 0:
            self.ball.velocity_x = self.ball.velocity_x * -1
            self.player2score += 1
        if self.ball.x > self.width:
            self.ball.velocity_x = self.ball.velocity_x * -1
            self.player1score += 1

        if self.ball.center_y > self.height or self.ball.center_y < 0:
            self.ball.velocity_y = self.ball.velocity_y * -1
        self.player1.address_collision(self.ball)
        self.player2.address_collision(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width/4:
            self.player1.update_position(touch.y)
        if touch.x > self.width*3/4:
            self.player2.update_position(touch.y)


class PongApp(App):
    def build(self):
        pong_game = PongGame()
        ball_velocity = Vector(6, 0).rotate(randint(0, 360))
        pong_game.set_ball_velocity(ball_velocity)
        Clock.schedule_interval(pong_game.update, 1.0/60.0)
        return pong_game


PongApp().run()
