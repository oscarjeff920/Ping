def main(difficulty, party_mode):
    import pygame, sys
    from random import choice, randrange as rr

    pygame.init()
    pygame.font.init()

    """
    Window = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    WindowSize = [Window.get_width(),Window.get_height()]
    SizeMultiplier = [WindowSize[0]/1366,WindowSize[1]/768]

    """
    WindowSize = (1360, 768)
    Center = (WindowSize[0]//2, WindowSize[1]//2)

    Window = pygame.display.set_mode(WindowSize)
    #"""
    class Things:
        def __init__(self, colour, position, size, velocity):
            self.colour = colour
            self.position = position
            self.size = size
            self.velocity = velocity 

    def grid(FractionX = 183, FractionY = 384):
        for n in range(FractionX):
            pygame.draw.line(Window, colours["Red"], (WindowSize[0]*(n/FractionX), 0), (WindowSize[0]*(n/FractionX), WindowSize[1]))
        for n in range(FractionY):
            pygame.draw.line(Window, colours["Red"], (0, WindowSize[1]*(n/FractionY)), (WindowSize[0], WindowSize[1]*(n/FractionY))) 

    def AI(difficulty):
        if type(difficulty) == str:
            if difficulty.lower() == "impossible":
                PC.position["y"] = Ball.position["y"] + Ball.size - (0.5*PC.size["Height"])
            else:
                if difficulty.lower() == "hard":
                    PC_step = 0.4
                elif difficulty.lower() == "normal":
                    PC_step = 0.2
                elif difficulty.lower() == "easy":
                    PC_step = 0.1
                elif difficulty.lower() == "baby":
                    PC_step = 0.05
        else:
            PC_step = difficulty

        if PC.position["y"] < Ball.position["y"] + Ball.size*2 and PC.position["y"] + PC.size["Height"] > Ball.position["y"]:
            return PC.position["y"]
        elif PC.position["y"] > Ball.position["y"] + Ball.size*2:
            PC.position["y"] -= PC.size["Height"] * PC_step
            return PC.position
        elif PC.position["y"] + PC.size["Height"] < Ball.position["y"]:
            PC.position["y"] += PC.size["Height"] * PC_step
            return PC.position

    def motion_blur(obj):
        blur = dict(Position = dict(x = obj.position["x"], y = obj.position["y"]), Size = obj.size)

    def render_text(font, size, colour, text):
        Font = pygame.font.SysFont(font, size)
        Text = Font.render(text, False, colour)
        return Text



    restart = True
    scores = {"pc" : 0, "player" : 0}
    pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
    while restart:

        PC = Things((150,100,100), dict(x = 0, y = WindowSize[1]*(4/10)), dict(Width = WindowSize[0]/100, Height = WindowSize[1]/5), None)
        Player = Things((0,0,200), dict(x = WindowSize[0]*(1 - 1/100), y = WindowSize[1]*(4/10)), dict(Width = WindowSize[0]/100, Height = WindowSize[1]/5), None)
        Ball = Things((140,255,0), dict(x = int(WindowSize[0]*(0.5 - 1/100)), y = int(WindowSize[1]*(0.5 - 1/100))), int(WindowSize[0]/120), dict(x = rr(-4,5), y = rr(-4,5)))
#
        acceleration = True 
        run = True
        start = False

        clock = pygame.time.Clock()
        FPS = 150

        while Ball.velocity["x"] > -2 and Ball.velocity["x"] < 2:
            Ball.velocity["x"] = rr(-4,5)
        while run:

            clock.tick(FPS)

            MousePos = pygame.mouse.get_pos()
            pygame.mouse.set_visible = False 
            if MousePos[1] >= (Player.size["Height"]//2) and MousePos[1] <= (WindowSize[1] - (Player.size["Height"]//2)):
                Player.position["y"] = MousePos[1] - (Player.size["Height"]//2)
            B_ground_colourN = (255, 255, 255)
            Window.fill(B_ground_colourN)

            #Scores and Game difficulty
            player_score_txt, PC_score_txt = render_text("rockwell", 40, Player.colour, str(scores["player"])), render_text("rockwell", 40, PC.colour, str(scores["pc"]))

            Window.blit(player_score_txt, ((7*WindowSize[0]//12) - (player_score_txt.get_width()//2), WindowSize[1]//4))
            Window.blit(PC_score_txt, ((5*WindowSize[0]//12) - (PC_score_txt.get_width()//2), WindowSize[1]//4))

            difficulty_txt, divider_txt = render_text("forte", 40, (0,0,0), difficulty.upper()), render_text("rockwell", 40, (0,0,0), "-")
            
            Window.blit(difficulty_txt, ((WindowSize[0] - difficulty_txt.get_width())//2, WindowSize[1]//8))
            Window.blit(divider_txt, ((WindowSize[0] - divider_txt.get_width())//2, WindowSize[1]//4))
            
            
            
            

            #Computer
            pygame.draw.rect(Window, PC.colour, [PC.position["x"], PC.position["y"], PC.size["Width"], PC.size["Height"]])
            #Player
            pygame.draw.rect(Window, Player.colour, [Player.position["x"], Player.position["y"], Player.size["Width"], Player.size["Height"]])

            #Ball
            pygame.draw.circle(Window, Ball.colour, (Ball.position["x"], Ball.position["y"]), Ball.size)
            pygame.draw.circle(Window, (0,0,0), (Ball.position["x"], Ball.position["y"]), Ball.size, 1)

            #Movement
            #Ball
            if (Ball.velocity["x"]**2 + Ball.velocity["y"]**2)**0.5 > 0.2*WindowSize[1]:
                acceleration = False 
            if start:
                Ball.position["x"] += Ball.velocity["x"]
                Ball.position["y"] += Ball.velocity["y"]
                if Ball.position["y"] + Ball.size >= WindowSize[1] or Ball.position["y"] - Ball.size <= 0 :
                    Ball.velocity["y"] *= -1
                if Ball.position["x"] + (Ball.size) >= Player.position["x"] and (Ball.position["y"] + (2*Ball.size)) >= Player.position["y"] and Ball.position["y"] <= (Player.position["y"] + Player.size["Height"]):
                    if Ball.position["y"] + Ball.size*2 < Player.position["y"] + Player.size["Height"] * 0.4:
                        Ball.velocity["y"] -= 1
                    elif Ball.position["y"] > Player.position["y"] + Player.size["Height"] * 0.6:
                        Ball.velocity["y"] += 1


                    if acceleration:
                        Ball.velocity["x"] += 1

                    if party_mode:
                        party_colours = [(255,255,255), (0,0,0), (200,0,0),(200,255,0),(0,250,0),(0,200,200),(0,0,200),
                                         (255,0,255),(200,200,0),(10,250,100),(255,155,55),(255,150,0), (255,200,210), (140,255,0)]
                        Player.colour = choice(party_colours)
                        Ball.colour = choice(party_colours)
                        while Ball.colour == (255,255,255): # impose a while loop so that the ball doesnt disapear against the white background
                                Ball.colour = choice(party_colours)

                    FPS += 10

                    Ball.velocity["x"] *= -1 
                if Ball.position["x"] <= PC.position["x"] + PC.size["Width"] and Ball.position["y"] <= (PC.position["y"] + PC.size["Height"]) and (Ball.position["y"] + Ball.size) >= PC.position["y"]:
                    
                    if acceleration:
                        Ball.velocity["x"] -= 1

                    FPS += 10
                    Ball.velocity["x"] *= -1
                if Ball.position["x"] + 2*Ball.size < 0 or Ball.position["x"] - 2*Ball.size > WindowSize[0]:
                    if Ball.position["x"] + 2*Ball.size < 0:
                        scores["player"] += 1
                    else:
                        scores["pc"] += 1
                    run = False
                    restart = True 
            if FPS >= 400:
                FPS = 400

            AI(difficulty)
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        start = True

                if event.type == pygame.QUIT:
                    run = False
                    restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        restart = False
                    if event.key == pygame.K_r:
                        run = False
                        restart = True
                    if event.key == pygame.K_p:
                        print(MousePos)
                        print(Player.position)
            #grid()
            pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
        difficulty = input("Which difficulty would you like to play?\nbaby?\neasy?\nnormal?\nhard?\nimpossible?\n       => ")
        if difficulty == "":
                difficulty = "hard"
        party_mode = input("Party Mode? ")
        if party_mode.lower() == "yes" or party_mode.lower() == "true" or party_mode == "":
                party_mode = True
        else:
                party_mode = False
        main(difficulty, party_mode)
