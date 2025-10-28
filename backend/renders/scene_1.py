from manim import *

class ManimScene(Scene):
    def construct(self):
        square = Square().scale(2)
        square.set_fill(WHITE, opacity=0.7)
        self.play(Create(square))
        # Rotate for about 10 seconds
        self.play(Rotate(square, angle=2*PI), run_time=10)
