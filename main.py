import pygame
from io import BytesIO
from PIL import Image
import win32clipboard

pygame.font.init()


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.toolbar = pygame.Surface((800, 50))
        self.colorbar = pygame.Surface((35, 550))
        self.tools = [
            "brush",
            "line",
            "arrow",
            "square",
            "circle",
            "text",
            "copy",
            "back",
        ]
        self.colors = [
            (0, 0, 0),  # black
            (255, 255, 255),  # white
            (128, 128, 128),  # gray
            (255, 0, 0),  # red
            (255, 165, 0),  # orange
            (255, 255, 0),  # yellow
            (0, 128, 0),  # green
            (0, 0, 255),  # blue
            (128, 0, 128),  # purple
            (255, 192, 203),  # pink
            (165, 42, 42),  # brown
            (210, 180, 140),  # tan
            (245, 245, 220),  # beige
            (0, 0, 128),  # navy
            (0, 128, 128),  # teal
            (128, 0, 0),  # maroon
        ]
        self.arrow = pygame.image.load("arrow.png")
        self.curr_color = 0
        self.canvas = pygame.Surface((800, 550))
        self.objs = []
        self.curr_op = 0
        self.size = 10
        self.angle = 0
        self.clicked = False
        self.last_pos = (0, 0)
        self.temp_text = ""

    def draw_toolbar(self, last):
        self.toolbar.fill((255, 255, 255))
        self.draw_values()
        x = 0
        for tool in self.tools:
            self.toolbar.blit(
                pygame.transform.scale(pygame.image.load(tool + ".png"), (40, 40)),
                (x + 5, 5),
            )
            x += 50
        pygame.draw.rect(self.toolbar, (50, 50, 50), (self.curr_op * 50, 0, 50, 50), 5)
        mouse = pygame.mouse.get_pos()
        if mouse[1] < 50 and pygame.mouse.get_pressed()[0]:
            self.temp_text = ""
            if int(mouse[0] / 50) < len(self.tools):
                self.curr_op = int(mouse[0] / 50)
            else:
                self.curr_op = len(self.tools) - 1
            if self.curr_op == 6 and not last:
                try:
                    self.objs.pop()
                except:
                    pass
            pygame.draw.rect(
                self.toolbar, (50, 50, 50), (self.curr_op * 50, 0, 50, 50), 5
            )
        self.screen.blit(self.toolbar, (0, 0))

    def draw_colorbar(self):
        self.colorbar.fill((255, 255, 255))
        x = 0
        for color in self.colors:
            pygame.draw.rect(self.colorbar, color, (0, x, 35, 34.375))
            x += 34.375
        pygame.draw.rect(
            self.colorbar, (50, 50, 50), (0, self.curr_color * 34.375, 35, 34.375), 5
        )
        mouse = pygame.mouse.get_pos()
        if (
            mouse[1] > 50
            and mouse[1] < 600
            and pygame.mouse.get_pressed()[0]
            and mouse[0] < 35
        ):
            self.clicked = False
            self.curr_color = int((mouse[1] - 50) / 34.375)
            pygame.draw.rect(
                self.colorbar,
                (50, 50, 50),
                (0, self.curr_color * 34.375, 35, 34.375),
                5,
            )

        self.screen.blit(self.colorbar, (0, 50))

    def draw_values(self):
        # draw the current tool and size at the end of the tool bar
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(f"{self.tools[self.curr_op]} ({self.size})", True, (0, 0, 0))
        text2 = font.render(f"{self.angle}", True, (0, 0, 0))
        self.toolbar.blit(text, (800 - (text.get_width() + 10), 0))
        self.toolbar.blit(text2, (800 - (text2.get_width() + 10), 25))

    def draw_curr_tool(self, last):
        mouse = pygame.mouse.get_pos()
        if mouse[1] > 50 and mouse[1] < 600 and mouse[0] > 35:
            x, y = mouse[0] - 35, mouse[1] - 50
            if self.curr_op == 0:
                pygame.draw.circle(
                    self.canvas, self.colors[self.curr_color], (x, y), self.size
                )
                if pygame.mouse.get_pressed()[0]:
                    self.objs.append(
                        [self.curr_op, self.colors[self.curr_color], self.size, (x, y)]
                    )
            elif self.curr_op == 1:
                if pygame.mouse.get_pressed()[0] and not last:
                    self.clicked = not self.clicked
                    if self.clicked:
                        self.last_pos = (x, y)
                    else:
                        self.objs.append(
                            [
                                self.curr_op,
                                self.colors[self.curr_color],
                                self.size,
                                tuple(self.last_pos),
                                (x, y),
                            ]
                        )
                if self.clicked:
                    pygame.draw.line(
                        self.canvas,
                        self.colors[self.curr_color],
                        self.last_pos,
                        (x, y),
                        self.size,
                    )
            elif self.curr_op == 2:
                if pygame.mouse.get_pressed()[0] and not last:
                    self.objs.append(
                        [
                            self.curr_op,
                            self.colors[self.curr_color],
                            self.size,
                            (x, y),
                            self.angle,
                        ]
                    )
                arrow = pygame.transform.scale(
                    self.arrow, (self.size * 2, self.size * 2)
                )
                rect = arrow.get_rect()
                rect.center = (x, y)
                self.canvas.blit(pygame.transform.rotate(arrow, self.angle), rect)
            elif self.curr_op == 3:
                if pygame.mouse.get_pressed()[0] and not last:
                    self.clicked = not self.clicked
                    if self.clicked:
                        self.last_pos = (x, y)
                    else:
                        self.objs.append(
                            [
                                self.curr_op,
                                self.colors[self.curr_color],
                                self.size,
                                (self.last_pos[0], self.last_pos[1]),
                                (x, y),
                            ]
                        )
                if self.clicked:
                    pygame.draw.rect(
                        self.canvas,
                        self.colors[self.curr_color],
                        (
                            self.last_pos[0],
                            self.last_pos[1],
                            x - self.last_pos[0],
                            y - self.last_pos[1],
                        ),
                        self.size,
                    )
            elif self.curr_op == 4:
                if pygame.mouse.get_pressed()[0] and not last:
                    self.clicked = not self.clicked
                    if self.clicked:
                        self.last_pos = (x, y)
                    else:
                        self.objs.append(
                            [
                                self.curr_op,
                                self.colors[self.curr_color],
                                self.size,
                                (self.last_pos[0], self.last_pos[1]),
                                (x, y),
                            ]
                        )
                if self.clicked:
                    pygame.draw.ellipse(
                        self.canvas,
                        self.colors[self.curr_color],
                        (
                            self.last_pos[0],
                            self.last_pos[1],
                            x - self.last_pos[0],
                            y - self.last_pos[1],
                        ),
                        self.size,
                    )
            elif self.curr_op == 5:
                if pygame.mouse.get_pressed()[0] and not last and self.temp_text != "":
                    self.objs.append(
                        [
                            self.curr_op,
                            self.colors[self.curr_color],
                            self.size,
                            (x, y),
                            self.temp_text,
                            self.angle,
                        ]
                    )
                font = pygame.font.SysFont("Arial", self.size)
                text = font.render(self.temp_text, True, self.colors[self.curr_color])
                text = pygame.transform.rotate(text, self.angle)
                rect = text.get_rect()
                rect.center = (x, y)
                self.canvas.blit(text, rect)
            elif self.curr_op == 6:
                if pygame.mouse.get_pressed()[0] and not last:
                    self.clicked = not self.clicked
                    if self.clicked:
                        self.last_pos = (x, y)
                    else:
                        img = Image.frombytes(
                            "RGBA",
                            (self.canvas.get_width(), self.canvas.get_height()),
                            pygame.image.tostring(self.canvas, "RGBA"),
                        )
                        img = img.crop((self.last_pos[0], self.last_pos[1], x, y))
                        output = BytesIO()
                        img.save(output, format="BMP")
                        data = output.getvalue()[14:]
                        output.close()
                        win32clipboard.OpenClipboard()
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                        win32clipboard.CloseClipboard()
                if self.clicked:
                    pygame.draw.rect(
                        self.canvas,
                        (0, 0, 0),
                        (
                            self.last_pos[0],
                            self.last_pos[1],
                            x - self.last_pos[0],
                            y - self.last_pos[1],
                        ),
                        1,
                    )

    def draw_objs(self):
        for obj in self.objs:
            if obj[0] == 0:
                pygame.draw.circle(self.canvas, obj[1], obj[3], obj[2])
            elif obj[0] == 1:
                pygame.draw.line(self.canvas, obj[1], obj[3], obj[4], obj[2])
            elif obj[0] == 2:
                arrow = pygame.transform.scale(self.arrow, (obj[2] * 2, obj[2] * 2))
                rect = arrow.get_rect()
                rect.center = obj[3]
                self.canvas.blit(pygame.transform.rotate(arrow, obj[4]), rect)
            elif obj[0] == 3:
                pygame.draw.rect(
                    self.canvas,
                    obj[1],
                    (
                        obj[3][0],
                        obj[3][1],
                        obj[4][0] - obj[3][0],
                        obj[4][1] - obj[3][1],
                    ),
                    obj[2],
                )
            elif obj[0] == 4:
                pygame.draw.ellipse(
                    self.canvas,
                    obj[1],
                    (
                        obj[3][0],
                        obj[3][1],
                        obj[4][0] - obj[3][0],
                        obj[4][1] - obj[3][1],
                    ),
                    obj[2],
                )
            elif obj[0] == 5:
                font = pygame.font.SysFont("Arial", obj[2])
                text = font.render(obj[4], True, obj[1])
                text = pygame.transform.rotate(text, obj[5])
                rect = text.get_rect()
                rect.center = obj[3]
                self.canvas.blit(text, rect)

    def draw_canvas(self, last):
        self.canvas.fill((255, 255, 255))
        self.draw_objs()
        self.draw_curr_tool(last)
        self.screen.blit(self.canvas, (35, 50))

    def run(self):
        last_frame = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEWHEEL:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                        if event.y > 0:
                            self.angle += 5
                        else:
                            self.angle -= 5
                        if self.angle < 0:
                            self.angle = 360
                        if self.angle > 360:
                            self.angle = 0
                    else:
                        if event.y > 0:
                            self.size += 1
                        else:
                            self.size -= 1
                        if self.size < 1:
                            self.size = 1
                        if self.size > 100:
                            self.size = 100
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clicked = False
                    if self.curr_op == 3:
                        if event.key == pygame.K_BACKSPACE:
                            self.temp_text = self.temp_text[:-1]
                        else:
                            self.temp_text += event.unicode

            self.screen.fill((255, 255, 255))
            self.draw_toolbar(last_frame)
            self.draw_colorbar()
            self.draw_canvas(last_frame)
            last_frame = pygame.mouse.get_pressed()[0]
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    app = App()
    app.run()
