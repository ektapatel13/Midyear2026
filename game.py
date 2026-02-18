import pygame
import random
import sys
import os

# --- Pygame Init ---
pygame.init()
WIDTH = 1300
HEIGHT = 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kitchen Game")
clock = pygame.time.Clock()
FPS = 60

# Alias for Processing compatibility
width = WIDTH
height = HEIGHT

# --- Font Cache ---
_font_cache = {}
def get_font(sz):
    sz = max(1, int(sz))
    if sz not in _font_cache:
        _font_cache[sz] = pygame.font.Font(None, sz)
    return _font_cache[sz]

# --- Drawing Helpers ---
def load_img(name):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        return None

def draw_img(img, x, y, w=None, h=None):
    if img is None:
        return
    if w is not None and h is not None:
        scaled = pygame.transform.smoothscale(img, (int(w), int(h)))
    else:
        scaled = img
    screen.blit(scaled, (int(x), int(y)))

def draw_img_alpha(img, x, y, w, h, alpha):
    if img is None:
        return
    scaled = pygame.transform.smoothscale(img, (int(w), int(h)))
    scaled = scaled.copy()
    scaled.set_alpha(alpha)
    screen.blit(scaled, (int(x), int(y)))

def draw_rect(x, y, w, h, color, border_radius=0):
    r = max(0, int(border_radius))
    if len(color) == 4 and color[3] < 255:
        s = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
        pygame.draw.rect(s, color, (0, 0, int(w), int(h)), border_radius=r)
        screen.blit(s, (int(x), int(y)))
    else:
        pygame.draw.rect(screen, color[:3], (int(x), int(y), int(w), int(h)), border_radius=r)

def draw_rect_outline(x, y, w, h, color, stroke_w=1, border_radius=0):
    r = max(0, int(border_radius))
    pygame.draw.rect(screen, color[:3], (int(x), int(y), int(w), int(h)), width=int(stroke_w), border_radius=r)

def draw_ellipse(cx, cy, w, h, color):
    bx = int(cx - w / 2)
    by = int(cy - h / 2)
    if len(color) == 4 and color[3] < 255:
        s = pygame.Surface((int(w), int(h)), pygame.SRCALPHA)
        pygame.draw.ellipse(s, color, (0, 0, int(w), int(h)))
        screen.blit(s, (bx, by))
    else:
        pygame.draw.ellipse(screen, color[:3], (bx, by, int(w), int(h)))

def draw_line(x1, y1, x2, y2, color, w=1):
    pygame.draw.line(screen, color[:3], (int(x1), int(y1)), (int(x2), int(y2)), max(1, int(w)))

def draw_triangle(x1, y1, x2, y2, x3, y3, color):
    pygame.draw.polygon(screen, color[:3], [(int(x1), int(y1)), (int(x2), int(y2)), (int(x3), int(y3))])

def draw_text(txt, x, y, sz, color, align_x="left", align_y="top"):
    font = get_font(sz)
    surf = font.render(str(txt), True, color[:3])
    dx = int(x)
    dy = int(y)
    if align_x == "center":
        dx = int(x - surf.get_width() / 2)
    elif align_x == "right":
        dx = int(x - surf.get_width())
    if align_y == "center":
        dy = int(y - surf.get_height() / 2)
    elif align_y == "bottom":
        dy = int(y - surf.get_height())
    screen.blit(surf, (dx, dy))

def draw_text_wrapped(txt, x, y, max_w, max_h, sz, color):
    font = get_font(sz)
    words = str(txt).split(' ')
    lines = []
    current = ""
    for word in words:
        test = current + (" " if current else "") + word
        if font.size(test)[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    line_h = font.get_linesize()
    for i, ln in enumerate(lines):
        ly = y + i * line_h
        if ly + line_h > y + max_h:
            break
        surf = font.render(ln, True, color[:3])
        screen.blit(surf, (int(x), int(ly)))

def millis():
    return pygame.time.get_ticks()

# --- Game State ---
homeBg = None
title = None
startbutton = None
howtoplay = None
mainBg = None

startX = 0
startY = 0
startW = 0
startH = 0
howX = 0
howY = 0
howW = 0
howH = 0

currentScreen = "home"
howtoplayImg = None
howtoplayOpen = False

customers = []
currentCustomer = None
lastIndex = -1
showCustomer = False
gameStartTime = 0

money = 20
startMoney = 20
orderValue = 5
scorePopups = []
orderActive = False

timerExpired = False
newCustomerDelay = 2000
newCustomerAt = 0

menuImg = None
menuOpen = False
menuThumbW = 140
menuThumbH = 140
menuThumbX = 0
menuThumbY = 0
menuW = 800
menuH = 800
exitSize = 42
exitX = 0
exitY = 0

leftArrow = None
rightArrow = None
arrowW = 70
arrowH = 70
arrowLeftX = 26
arrowY = 357
arrowRightX = 0

stations = ["order", "kitchen"]
currentStation = 0
breakfastBg = None

greetings = [
    "Hello! I would like to order, please.",
    "Hi there! I am starving.",
    "Good day! I'm ready to order whenever you are.",
    "Hello! I have heard great things about this place.",
    "Hi! Everything smells wonderful in here.",
    "Hey there! I have been looking forward to coming here.",
    "Hey! Can I get started with something?",
    "Hello there! Just looking for a bite to eat.",
    "Good day! I'm glad I found this place.",
    "Hi, I'm looking for something delicious.",
    "Hello! I am ready to place an order",
    "Hi! It looks nice in here."
]

menuItems = [
    {"name": "croissant", "kind": "a"},
    {"name": "pancakes", "kind": "plural"},
    {"name": "egg sandwich", "kind": "an"},
    {"name": "avocado toast", "kind": "plural"},
    {"name": "panini", "kind": "a"},
    {"name": "cupcake", "kind": "a"},
    {"name": "cookie", "kind": "a"}
]

dialogOpen = False
dialogStep = 0
greetingText = ""
orderText = ""
currentOrderCounts = {}
currentOrderKinds = {}
currentOrderText = ""

cabinetImg = None
cabinetOpen = False
openCabinetKey = None
cabinetHitboxes = {
    "TL": {"x": 11, "y": 5, "w": 501, "h": 165},
    "TR": {"x": 998, "y": 5, "w": 502, "h": 163},
    "BL": {"x": 0, "y": 390, "w": 564, "h": 179},
    "BR": {"x": 943, "y": 393, "w": 563, "h": 178},
}
ingredientImgs = {}
cabinetItems = {
    "TL": ["flour", "sugar", "eggs", "milk", "butter_stick"],
    "TR": ["berries_carton", "whole_avocado", "whole_tomato"],
    "BL": ["deli_meat", "cheese", "raw_bacon"],
    "BR": ["cream", "chocolate_chips", "batter_bottle", "syrup_bottle"]
}
overlayW = 900
overlayH = 900
overlayX = 0
overlayY = 0
fridgeBtn = None
fridgeBtnW = 90
fridgeBtnH = 90
fridgeBtnX = 17
fridgeBtnY = 0

fridgeOpen = False
fridgeGrid = [
    ["eggs", "flour", "butter_stick", "milk", "sugar"],
    ["whole_avocado", "whole_tomato", "cheese", "deli_meat", "raw_bacon"],
    ["syrup_bottle", "cream", "chocolate_chips", "bread", "berries_carton"]
]
fridgeBtnSize = 140
fridgeGap = 20
fridgeGridCols = 5
fridgeGridRows = 3

counterItems = []
counterItemSize = 160
counterColGap = -5
counterRowGap = -45
counterMaxPerRow = 2
counterMaxPerSide = 4
counterStartX = 27
counterStartY = 430

draggingItem = None
dragOffsetX = 0
dragOffsetY = 0
wasDragging = False
dragStartX = 0
dragStartY = 0
dragThreshold = 5
dragOrigX = 0
dragOrigY = 0

counterRecipes = [
    {"inputs": ["dough_formed", "butter_stick"], "output": "croissant"},
    {"inputs": ["empty_pancakes", "berries_carton"], "output": "pancakes_nosyrup"},
    {"inputs": ["pancakes_nosyrup", "syrup_bottle"], "output": "pancakes"},
    {"inputs": ["toasted_bread", "fried_egg"], "output": "toasted_bread_egg"},
    {"inputs": ["toasted_bread_egg", "cheese"], "output": "toasted_bread_egg_cheese"},
    {"inputs": ["toasted_bread_egg_cheese", "fried_bacon"], "output": "egg_sandwich"},
    {"inputs": ["toasted_bread", "chopped_avocado"], "output": "toasted_bread_avocado"},
    {"inputs": ["toasted_bread_avocado", "chopped_tomato"], "output": "toasted_bread_avocado_tomato"},
    {"inputs": ["toasted_bread_avocado_tomato", "fried_bacon"], "output": "avocado_toast"},
    {"inputs": ["toasted_bread", "fried_deli_meat"], "output": "toasted_bread_deli"},
    {"inputs": ["toasted_bread_deli", "cheese"], "output": "panini"},
]

bowlRecipes = [
    {"inputs": ["flour", "eggs", "milk", "sugar"], "output": "dough_formed"},
    {"inputs": ["flour", "eggs", "milk"], "output": "batter_bottle"},
    {"inputs": ["dough_formed", "chocolate_chips"], "output": "cookiedough_formed"},
    {"inputs": ["dough_formed", "cream"], "output": "cupcake_unbaked"},
]
panRecipes = {"eggs": "fried_egg", "raw_bacon": "fried_bacon", "deli_meat": "fried_deli_meat"}
panMultiRecipes = [
    {"inputs": ["batter_bottle"], "output": "empty_pancakes"},
    {"inputs": ["batter_bottle", "berries_carton"], "output": "pancakes_nosyrup"}
]
panContents = []
ovenRecipes = {"cookiedough_formed": "cookie", "cupcake_unbaked": "cupcake"}
chopRecipes = {"whole_avocado": "chopped_avocado", "whole_tomato": "chopped_tomato"}
toasterRecipes = {"bread": "toasted_bread"}

menuNameToItemName = {
    "croissant": "croissant",
    "pancakes": "pancakes",
    "egg sandwich": "egg_sandwich",
    "avocado toast": "avocado_toast",
    "panini": "panini",
    "cupcake": "cupcake",
    "cookie": "cookie"
}

boardX = 370
boardY = 430
boardW = 340
boardH = 315
bowlX = 670
bowlY = 455
bowlW = 260
bowlH = 260
panX = 509
panY = 225
panW = 190
panH = 145
ovenX = 745
ovenY = 220
ovenW = 200
ovenH = 160
toasterImg = None
toasterX = 387
toasterY = 224
toasterW = 85
toasterH = 75
boardImg = None
bowlImg = None
panImg = None

bowlContents = []

debugMouse = False
lastClickMs = 0
clickCooldownMs = 180
recipeCardOpen = False
currentRecipe = None
recipeCards = {}
recipeCardW = 500
recipeCardH = 555
menuFoodItems = []

deleteBtn = None
deleteBtnW = 50
deleteBtnH = 50
deleteBtnX = 0
deleteBtnY = 10

toasterCooking = None
toasterStartTime = 0
toasterDuration = 8000
panCooking = None
panStartTime = 0
panDuration = 5000
ovenCooking = None
ovenStartTime = 0
ovenDuration = 10000

mouseX = 0
mouseY = 0

# --- Helper Functions ---
def isOverRect(px, py, rx, ry, rw, rh):
    return px >= rx and px <= rx + rw and py >= ry and py <= ry + rh

def isOverEllipse(px, py, cx, cy, rx, ry):
    dx = (px - cx) / float(rx)
    dy = (py - cy) / float(ry)
    return dx * dx + dy * dy <= 1.0

# --- Menu / Recipe Card ---
def setupMenuUI():
    global menuThumbX, menuThumbY
    menuThumbX = width - menuThumbW - 25
    menuThumbY = height - menuThumbH - 25

def loadMenuAssets():
    global menuImg, recipeCards
    menuImg = load_img("menu.png")
    for name, fname in [("croissant", "croissant_instructions.png"),
                        ("pancakes", "pancakes_instructions.png"),
                        ("egg_sandwich", "eggsandwich_instructions.png"),
                        ("avocado_toast", "avocadotoast_instructions.png"),
                        ("panini", "panini_instructions.png"),
                        ("cupcake", "cupcake_instructions.png"),
                        ("cookie", "cookie_instructions.png")]:
        img = load_img(fname)
        if img is not None:
            recipeCards[name] = img

def setupMenuFoodItems():
    global menuFoodItems
    menuFoodItems = []
    pad = 35
    menuFoodItems.append({"name": "croissant", "x": 80 - pad, "y": 190 - pad, "w": 140 + pad * 2, "h": 140 + pad * 2})
    menuFoodItems.append({"name": "pancakes", "x": 300 - pad, "y": 190 - pad, "w": 140 + pad * 2, "h": 140 + pad * 2})
    menuFoodItems.append({"name": "egg_sandwich", "x": 520 - pad, "y": 190 - pad, "w": 140 + pad * 2, "h": 140 + pad * 2})
    menuFoodItems.append({"name": "avocado_toast", "x": 150 - pad, "y": 400 - pad, "w": 140 + pad * 2, "h": 140 + pad * 2})
    menuFoodItems.append({"name": "panini", "x": 500 - pad, "y": 400 - pad, "w": 140 + pad * 2, "h": 140 + pad * 2})
    menuFoodItems.append({"name": "cupcake", "x": 180 - pad, "y": 590 - pad, "w": 120 + pad * 2, "h": 120 + pad * 2})
    menuFoodItems.append({"name": "cookie", "x": 500 - pad, "y": 590 - pad, "w": 120 + pad * 2, "h": 120 + pad * 2})

def getRecipeCardPos():
    x = width / 2 - recipeCardW / 2
    y = height / 2 - recipeCardH / 2
    if recipeCardW > width:
        x = 0
    else:
        x = max(0, x)
        if x + recipeCardW > width:
            x = width - recipeCardW
    if recipeCardH > height:
        y = 0
    else:
        y = max(0, y)
        if y + recipeCardH > height:
            y = height - recipeCardH
    return x, y

def drawExitButton(ex, ey, sz):
    draw_rect(ex, ey, sz, sz, (255, 80, 80), border_radius=10)
    draw_line(ex + 12, ey + 12, ex + sz - 12, ey + sz - 12, (255, 255, 255), 5)
    draw_line(ex + sz - 12, ey + 12, ex + 12, ey + sz - 12, (255, 255, 255), 5)

def drawRecipeCard():
    draw_rect(0, 0, width, height, (0, 0, 0, 200))
    cardX, cardY = getRecipeCardPos()
    if currentRecipe in recipeCards and recipeCards[currentRecipe] is not None:
        draw_img(recipeCards[currentRecipe], cardX, cardY, recipeCardW, recipeCardH)
    else:
        draw_rect(cardX, cardY, recipeCardW, recipeCardH, (255, 255, 255), border_radius=10)
        draw_text("Recipe card for " + str(currentRecipe), width / 2, height / 2, 24, (0, 0, 0), "center", "center")
    drawExitButton(cardX + recipeCardW - exitSize - 12, cardY + 12, exitSize)

def drawMenuUI():
    draw_img(menuImg, menuThumbX, menuThumbY, menuThumbW, menuThumbH)
    if menuOpen:
        x = width / 2 - menuW / 2
        y = height / 2 - menuH / 2
        draw_img(menuImg, x, y, menuW, menuH)
        global exitX, exitY
        exitX = x + menuW - exitSize - 12
        exitY = y + 12
        drawExitButton(exitX, exitY, exitSize)

def handleMenuClick():
    global menuOpen, recipeCardOpen, currentRecipe
    if recipeCardOpen:
        cardX, cardY = getRecipeCardPos()
        ex = cardX + recipeCardW - exitSize - 12
        ey = cardY + 12
        if isOverRect(mouseX, mouseY, ex, ey, exitSize, exitSize):
            recipeCardOpen = False
            currentRecipe = None
            return True
        return True
    if menuOpen:
        menuX0 = width / 2 - menuW / 2
        menuY0 = height / 2 - menuH / 2
        for item in menuFoodItems:
            itemX = menuX0 + item["x"]
            itemY = menuY0 + item["y"]
            if isOverRect(mouseX, mouseY, itemX, itemY, item["w"], item["h"]):
                currentRecipe = item["name"]
                recipeCardOpen = True
                return True
        ex = menuX0 + menuW - exitSize - 12
        ey = menuY0 + 12
        if isOverRect(mouseX, mouseY, ex, ey, exitSize, exitSize):
            menuOpen = False
            return True
        return True
    if isOverRect(mouseX, mouseY, menuThumbX, menuThumbY, menuThumbW, menuThumbH):
        menuOpen = True
        return True
    return False

# --- How To Play ---
def drawHowToPlay():
    draw_rect(0, 0, width, height, (0, 0, 0, 180))
    hw = 800
    hh = 800
    hx = width / 2 - hw / 2
    hy = height / 2 - hh / 2
    if howtoplayImg:
        draw_img(howtoplayImg, hx, hy, hw, hh)
    drawExitButton(hx + hw - exitSize - 12, hy + 12, exitSize)

def handleHowToPlayClick():
    global howtoplayOpen
    if howtoplayOpen:
        hw = 800
        hh = 800
        hx = width / 2 - hw / 2
        hy = height / 2 - hh / 2
        ex = hx + hw - exitSize - 12
        ey = hy + 12
        if isOverRect(mouseX, mouseY, ex, ey, exitSize, exitSize):
            howtoplayOpen = False
            return True
    return False

# --- Order System ---
def buildOrderCounts():
    n = random.randint(1, 2)
    counts = {}
    kinds = {}
    picked = []
    while len(picked) < n:
        item = menuItems[random.randint(0, len(menuItems) - 1)]
        if item["name"] not in picked:
            picked.append(item["name"])
            counts[item["name"]] = 1
            kinds[item["name"]] = item["kind"]
    return counts, kinds

def pluralize(word):
    if word.endswith("s"):
        return word
    if word.endswith("y") and len(word) > 1 and word[-2].lower() not in ["a", "e", "i", "o", "u"]:
        return word[:-1] + "ies"
    if word.endswith("ch") or word.endswith("sh") or word.endswith("x") or word.endswith("z"):
        return word + "es"
    return word + "s"

def joinParts(parts):
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return parts[0] + " and " + parts[1]
    return ", ".join(parts[:-1]) + ", and " + parts[-1]

def orderTextFromCounts(counts, kinds):
    parts = []
    for name in counts:
        c = counts[name]
        kind = kinds[name]
        if kind == "plural":
            if c == 1:
                parts.append(name)
            else:
                parts.append(str(c) + " orders of " + name)
        else:
            if c == 1:
                parts.append(kind + " " + name)
            else:
                parts.append(str(c) + " " + pluralize(name))
    return "Can I get " + joinParts(parts) + "?"

def generateNewOrder():
    global currentOrderCounts, currentOrderKinds, currentOrderText
    currentOrderCounts, currentOrderKinds = buildOrderCounts()
    currentOrderText = orderTextFromCounts(currentOrderCounts, currentOrderKinds)
    return currentOrderText

def startCustomerDialog():
    global dialogOpen, dialogStep, greetingText, orderText
    dialogOpen = True
    dialogStep = 0
    greetingText = greetings[random.randint(0, len(greetings) - 1)]
    orderText = generateNewOrder()

def advanceDialog():
    global dialogOpen, dialogStep, gameStartTime
    if dialogStep == 0:
        dialogStep = 1
    else:
        dialogOpen = False
        gameStartTime = millis()

def drawSpeechBubble(textMain):
    bubbleW = 290
    bubbleH = 140
    bubbleX = width / 2 - bubbleW / 2 + 82
    bubbleY = 55
    draw_rect(bubbleX, bubbleY, bubbleW, bubbleH, (255, 255, 255), border_radius=18)
    tailX = bubbleX + 60
    tailY = bubbleY + bubbleH
    draw_triangle(tailX, tailY, tailX + 40, tailY, tailX + 20, tailY + 28, (255, 255, 255))
    draw_text_wrapped(textMain, bubbleX + 20, bubbleY + 18, bubbleW - 40, bubbleH - 60, 22, (0, 0, 0))
    draw_text("(tap to continue)", bubbleX + 20, bubbleY + bubbleH - 30, 16, (60, 60, 60))

def drawMoney():
    draw_rect(30, 20, 240, 80, (0, 0, 0, 150))
    draw_text("Money: $" + str(money), 50, 30, 28, (255, 255, 255))
    draw_text("Order: $" + str(orderValue), 50, 65, 22, (255, 255, 100))

def drawScorePopups():
    global scorePopups
    to_remove = []
    for popup in scorePopups:
        age = millis() - popup['time']
        if age > 1500:
            to_remove.append(popup)
        else:
            alpha = max(0, int(255 - (age / 1500.0 * 255)))
            yOffset = age / 10.0
            font = get_font(32)
            surf = font.render(popup['text'], True, (popup['color'][0], popup['color'][1], popup['color'][2]))
            surf.set_alpha(alpha)
            screen.blit(surf, (int(popup['x'] - surf.get_width() / 2), int(popup['y'] - yOffset - surf.get_height() / 2)))
    for p in to_remove:
        scorePopups.remove(p)

# --- Game Round ---
def startGameRound():
    global showCustomer, gameStartTime, money, currentCustomer, orderActive, dialogOpen, dialogStep
    global bowlContents, counterItems, panContents, timerExpired, newCustomerAt
    global toasterCooking, panCooking, ovenCooking
    showCustomer = False
    orderActive = False
    dialogOpen = False
    dialogStep = 0
    gameStartTime = millis()
    money = startMoney
    currentCustomer = None
    bowlContents = []
    panContents = []
    counterItems = []
    timerExpired = False
    newCustomerAt = 0
    toasterCooking = None
    panCooking = None
    ovenCooking = None

def getTimerFillWidth():
    barWidth = 220
    timeElapsed = millis() - gameStartTime
    fw = barWidth - (timeElapsed / 600.0)
    if fw < 0:
        fw = 0
    return fw

def resetForNextCustomer():
    global showCustomer, orderActive, dialogOpen, dialogStep, timerExpired
    global newCustomerAt, currentCustomer, gameStartTime
    showCustomer = False
    orderActive = False
    dialogOpen = False
    dialogStep = 0
    timerExpired = False
    currentCustomer = None
    newCustomerAt = millis() + newCustomerDelay
    gameStartTime = millis() + newCustomerDelay

def serveOrder():
    global money, counterItems, scorePopups
    needed = {}
    for menuName in currentOrderCounts:
        itemName = menuNameToItemName.get(menuName, menuName.replace(" ", "_"))
        needed[itemName] = currentOrderCounts[menuName]
    tempCounter = [item["name"] for item in counterItems]
    allFound = True
    for itemName in needed:
        count = needed[itemName]
        found = tempCounter.count(itemName)
        if found < count:
            allFound = False
            break
    if allFound:
        tempNeeded = dict(needed)
        newCounterItems = []
        for item in counterItems:
            n = item["name"]
            if n in tempNeeded and tempNeeded[n] > 0:
                tempNeeded[n] -= 1
            else:
                newCounterItems.append(item)
        counterItems = newCounterItems
        totalDishes = sum(needed.values())
        earned = orderValue * totalDishes
        money += earned
        scorePopups.append({'text': '+$' + str(earned) + ' Great job!', 'x': width / 2, 'y': 380, 'color': [80, 220, 80], 'time': millis()})
        resetForNextCustomer()
    else:
        missing = []
        tempCounter2 = [item["name"] for item in counterItems]
        for itemName in needed:
            count = needed[itemName]
            have = tempCounter2.count(itemName)
            short = count - have
            if short > 0:
                label = itemName.replace("_", " ")
                if short > 1:
                    missing.append(str(short) + "x " + label)
                else:
                    missing.append(label)
        msg = "Still need: " + ", ".join(missing)
        scorePopups.append({'text': msg, 'x': width / 2, 'y': 380, 'color': [255, 150, 50], 'time': millis()})

def checkTimerExpired():
    global money, scorePopups, timerExpired
    if not orderActive or timerExpired or dialogOpen:
        return
    if getTimerFillWidth() <= 0:
        timerExpired = True
        penalty = orderValue
        money -= penalty
        scorePopups.append({'text': '-$' + str(penalty) + ' Too slow!', 'x': width / 2, 'y': 380, 'color': [255, 80, 80], 'time': millis()})
        resetForNextCustomer()

def drawServeButton():
    if stations[currentStation] != "order":
        return
    if not orderActive or not showCustomer:
        return
    bw = 160
    bh = 55
    bx = width / 2 - bw / 2
    by = height - bh - 30
    draw_rect(bx, by, bw, bh, (40, 180, 80), border_radius=14)
    draw_text("Serve!", bx + bw / 2, by + bh / 2, 26, (255, 255, 255), "center", "center")

def handleServeButtonClick():
    if stations[currentStation] != "order":
        return False
    if not orderActive or not showCustomer:
        return False
    bw = 160
    bh = 55
    bx = width / 2 - bw / 2
    by = height - bh - 30
    if isOverRect(mouseX, mouseY, bx, by, bw, bh):
        serveOrder()
        return True
    return False

def drawTimerBar(charX, charY, charW):
    barWidth = 220
    barHeight = 18
    barX = charX + charW / 2 - barWidth / 2
    barY = charY + 15
    draw_rect(barX, barY, barWidth, barHeight, (50, 50, 50), border_radius=6)
    draw_rect_outline(barX, barY, barWidth, barHeight, (0, 0, 0), 2, border_radius=6)
    fillWidth = getTimerFillWidth()
    if fillWidth > barWidth * 0.5:
        c = (100, 200, 100)
    elif fillWidth > barWidth * 0.25:
        c = (255, 200, 0)
    else:
        c = (255, 100, 100)
    if fillWidth > 0:
        draw_rect(barX, barY, fillWidth, barHeight, c, border_radius=6)

# --- Station Drawing ---
def drawStation():
    if stations[currentStation] == "order":
        draw_img(mainBg, 0, 0, width, height)
    elif stations[currentStation] == "kitchen":
        draw_img(breakfastBg, 0, 0, width, height)

# --- Fridge ---
def drawFridgeButton():
    if stations[currentStation] == "kitchen" and fridgeBtn is not None:
        draw_img(fridgeBtn, fridgeBtnX, fridgeBtnY, fridgeBtnW, fridgeBtnH)

def handleFridgeButtonClick():
    global fridgeOpen
    if stations[currentStation] != "kitchen":
        return False
    if isOverRect(mouseX, mouseY, fridgeBtnX, fridgeBtnY, fridgeBtnW, fridgeBtnH):
        fridgeOpen = True
        return True
    return False

def getFridgeGridOrigin():
    totalW = fridgeGridCols * fridgeBtnSize + (fridgeGridCols - 1) * fridgeGap
    totalH = fridgeGridRows * fridgeBtnSize + (fridgeGridRows - 1) * fridgeGap
    gx = width / 2 - totalW / 2
    gy = height / 2 - totalH / 2
    return gx, gy

def drawFridgeOverlay():
    if not fridgeOpen:
        return
    draw_rect(0, 0, width, height, (50, 50, 50, 170))
    gx, gy = getFridgeGridOrigin()
    for r in range(fridgeGridRows):
        for c in range(fridgeGridCols):
            x = gx + c * (fridgeBtnSize + fridgeGap)
            y = gy + r * (fridgeBtnSize + fridgeGap)
            name = fridgeGrid[r][c]
            selected = counterHasItem(name)
            if selected:
                draw_rect(x, y, fridgeBtnSize, fridgeBtnSize, (200, 240, 200), border_radius=16)
                draw_rect_outline(x, y, fridgeBtnSize, fridgeBtnSize, (80, 200, 80), 4, border_radius=16)
            else:
                draw_rect(x, y, fridgeBtnSize, fridgeBtnSize, (255, 200, 210), border_radius=16)
            img = ingredientImgs.get(name, None)
            if img is not None:
                pad = 14
                if selected:
                    draw_img_alpha(img, x + pad, y + pad, fridgeBtnSize - pad * 2, fridgeBtnSize - pad * 2, 160)
                else:
                    draw_img(img, x + pad, y + pad, fridgeBtnSize - pad * 2, fridgeBtnSize - pad * 2)
            else:
                draw_text(name, x + fridgeBtnSize / 2, y + fridgeBtnSize / 2, 13, (80, 80, 80), "center", "center")
    # Close button
    bx = width - 60
    by = 20
    drawExitButton(bx, by, 42)

def handleFridgeOverlayClick():
    global fridgeOpen, counterItems
    if not fridgeOpen:
        return False
    bx = width - 60
    by = 20
    if isOverRect(mouseX, mouseY, bx, by, 42, 42):
        fridgeOpen = False
        return True
    gx, gy = getFridgeGridOrigin()
    for r in range(fridgeGridRows):
        for c in range(fridgeGridCols):
            x = gx + c * (fridgeBtnSize + fridgeGap)
            y = gy + r * (fridgeBtnSize + fridgeGap)
            if isOverRect(mouseX, mouseY, x, y, fridgeBtnSize, fridgeBtnSize):
                name = fridgeGrid[r][c]
                if not counterHasItem(name):
                    idx = len(counterItems)
                    px, py = getCounterItemPos(idx)
                    counterItems.append({"name": name, "x": px, "y": py})
                return True
    return True

# --- Counter Items ---
def getCounterItemPos(index):
    side = index // counterMaxPerSide
    localIdx = index % counterMaxPerSide
    col = localIdx % counterMaxPerRow
    row = localIdx // counterMaxPerRow
    if side == 0:
        x = counterStartX + col * (counterItemSize + counterColGap)
    else:
        rightStartX = width - counterStartX - counterMaxPerRow * counterItemSize - (counterMaxPerRow - 1) * counterColGap
        x = rightStartX + col * (counterItemSize + counterColGap)
    y = counterStartY + row * (counterItemSize + counterRowGap)
    return x, y

def counterHasItem(name):
    for item in counterItems:
        if item["name"] == name:
            return True
    return False

def drawCounterItems():
    if stations[currentStation] != "kitchen":
        return
    for item in counterItems:
        name = item["name"]
        img = ingredientImgs.get(name, None)
        x = item["x"]
        y = item["y"]
        if img is not None:
            draw_img(img, x, y, counterItemSize, counterItemSize)
        else:
            draw_rect(x, y, counterItemSize, counterItemSize, (255, 200, 210), border_radius=10)
            draw_text(name, x + counterItemSize / 2, y + counterItemSize / 2, 12, (80, 80, 80), "center", "center")

# --- Kitchen Tools ---
def drawKitchenTools():
    if stations[currentStation] != "kitchen":
        return
    drawOvenBar()
    drawToaster()
    drawPan()
    drawBoard()
    drawBowl()

def drawOvenBar():
    if ovenCooking is not None:
        drawCookingBar(ovenX, ovenY + ovenH + 4, ovenW, ovenStartTime, ovenDuration)

def drawBoard():
    if boardImg is not None:
        draw_img(boardImg, boardX, boardY, boardW, boardH)
    else:
        draw_rect(boardX, boardY, boardW, boardH, (170, 130, 75), border_radius=6)
        draw_rect(boardX + 6, boardY + 6, boardW - 12, boardH - 12, (150, 110, 55), border_radius=4)

def drawBowl():
    if bowlImg is not None:
        draw_img(bowlImg, bowlX, bowlY, bowlW, bowlH)
    else:
        draw_ellipse(bowlX + bowlW / 2, bowlY + bowlH / 2, bowlW, bowlH, (200, 200, 210))
        draw_ellipse(bowlX + bowlW / 2, bowlY + bowlH / 2, bowlW - 40, bowlH - 40, (230, 230, 240))
    drawBowlContents()
    if len(bowlContents) >= 1:
        drawBowlButtons()

def drawBowlContents():
    if len(bowlContents) == 0:
        return
    iconSize = 42
    gap = 4
    totalW = len(bowlContents) * (iconSize + gap) - gap
    sx = bowlX + bowlW / 2 - totalW / 2
    sy = bowlY + bowlH / 2 - iconSize / 2
    for i, name in enumerate(bowlContents):
        ix = sx + i * (iconSize + gap)
        img = ingredientImgs.get(name, None)
        if img is not None:
            draw_img(img, ix, sy, iconSize, iconSize)
        else:
            draw_rect(ix, sy, iconSize, iconSize, (180, 180, 180), border_radius=6)
            draw_text(name, ix + iconSize / 2, sy + iconSize / 2, 8, (40, 40, 40), "center", "center")

def drawBowlButtons():
    bw = 70
    bh = 32
    by = bowlY + bowlH + 6
    if len(bowlContents) >= 2:
        mx = bowlX + bowlW / 2 - bw - 5
        draw_rect(mx, by, bw, bh, (80, 180, 80), border_radius=10)
        draw_text("Mix!", mx + bw / 2, by + bh / 2, 16, (255, 255, 255), "center", "center")
        cx = bowlX + bowlW / 2 + 5
        draw_rect(cx, by, bw, bh, (200, 80, 80), border_radius=10)
        draw_text("Clear", cx + bw / 2, by + bh / 2, 16, (255, 255, 255), "center", "center")
    else:
        cx = bowlX + bowlW / 2 - bw / 2
        draw_rect(cx, by, bw, bh, (200, 80, 80), border_radius=10)
        draw_text("Clear", cx + bw / 2, by + bh / 2, 16, (255, 255, 255), "center", "center")

def drawPan():
    if panImg is not None:
        draw_img(panImg, panX, panY, panW, panH)
    else:
        draw_ellipse(panX + panW / 2, panY + panH / 2, panW, panH, (80, 80, 90))
        draw_ellipse(panX + panW / 2, panY + panH / 2, panW - 18, panH - 12, (55, 55, 63))
        draw_rect(panX + panW - 8, panY + panH / 2 - 7, 38, 14, (95, 95, 105), border_radius=5)
    if panCooking is not None:
        drawCookingBar(panX, panY + panH + 4, panW, panStartTime, panDuration)
    drawPanContents()
    if len(panContents) >= 1:
        drawPanButtons()

def drawPanContents():
    if len(panContents) == 0:
        return
    iconSize = 30
    gap = 4
    totalW = len(panContents) * (iconSize + gap) - gap
    sx = panX + panW / 2 - totalW / 2
    sy = panY + panH / 2 - iconSize / 2
    for i, name in enumerate(panContents):
        ix = sx + i * (iconSize + gap)
        img = ingredientImgs.get(name, None)
        if img is not None:
            draw_img(img, ix, sy, iconSize, iconSize)
        else:
            draw_rect(ix, sy, iconSize, iconSize, (180, 180, 180), border_radius=6)
            draw_text(name, ix + iconSize / 2, sy + iconSize / 2, 8, (40, 40, 40), "center", "center")

def drawPanButtons():
    bw = 60
    bh = 28
    by = panY + panH + 8
    mx = panX + panW / 2 - bw - 4
    draw_rect(mx, by, bw, bh, (80, 180, 80), border_radius=8)
    draw_text("Cook!", mx + bw / 2, by + bh / 2, 14, (255, 255, 255), "center", "center")
    cx = panX + panW / 2 + 4
    draw_rect(cx, by, bw, bh, (200, 80, 80), border_radius=8)
    draw_text("Clear", cx + bw / 2, by + bh / 2, 14, (255, 255, 255), "center", "center")

def handlePanButtonClick():
    global panContents
    if len(panContents) == 0:
        return False
    bw = 60
    bh = 28
    by = panY + panH + 8
    mx = panX + panW / 2 - bw - 4
    if isOverRect(mouseX, mouseY, mx, by, bw, bh):
        matched = False
        best = None
        for recipe in panMultiRecipes:
            inputs = recipe["inputs"]
            if len(inputs) != len(panContents):
                continue
            tempPan = list(panContents)
            allFound = True
            for inp in inputs:
                if inp in tempPan:
                    tempPan.remove(inp)
                else:
                    allFound = False
                    break
            if allFound and len(tempPan) == 0:
                best = recipe
                matched = True
                break
        if matched and best is not None:
            panContents = []
            spawnCounterItem(best["output"])
        return True
    cx = panX + panW / 2 + 4
    if isOverRect(mouseX, mouseY, cx, by, bw, bh):
        for name in panContents:
            spawnCounterItem(name)
        panContents = []
        return True
    return False

def drawToaster():
    if toasterImg is not None:
        draw_img(toasterImg, toasterX, toasterY, toasterW, toasterH)
    if toasterCooking is not None:
        drawCookingBar(toasterX, toasterY + toasterH + 4, toasterW, toasterStartTime, toasterDuration)

def drawCookingBar(bx, by, bw, startT, duration):
    barH = 10
    elapsed = millis() - startT
    progress = elapsed / float(duration)
    if progress > 1.0:
        progress = 1.0
    draw_rect(bx, by, bw, barH, (50, 50, 50), border_radius=4)
    if progress < 0.5:
        c = (255, 200, 0)
    elif progress < 0.9:
        c = (200, 220, 80)
    else:
        c = (80, 220, 80)
    if progress > 0:
        draw_rect(bx, by, bw * progress, barH, c, border_radius=4)

def checkCookingTimers():
    global toasterCooking, panCooking, ovenCooking
    if toasterCooking is not None:
        if millis() - toasterStartTime >= toasterDuration:
            spawnCounterItem(toasterCooking)
            toasterCooking = None
    if panCooking is not None:
        if millis() - panStartTime >= panDuration:
            spawnCounterItem(panCooking)
            panCooking = None
    if ovenCooking is not None:
        if millis() - ovenStartTime >= ovenDuration:
            spawnCounterItem(ovenCooking)
            ovenCooking = None

# --- Counter Item Helpers ---
def spawnCounterItem(name):
    idx = len(counterItems)
    px, py = getCounterItemPos(idx)
    counterItems.append({"name": name, "x": px, "y": py})

def findItemAtPosition(x, y, excludeItem):
    for item in counterItems:
        if item is not excludeItem:
            if isOverRect(x, y, item["x"], item["y"], counterItemSize, counterItemSize):
                return item
    return None

def checkCounterCombination(item1Name, item2Name):
    for recipe in counterRecipes:
        inputs = recipe["inputs"]
        if len(inputs) == 2:
            if (inputs[0] == item1Name and inputs[1] == item2Name) or (inputs[0] == item2Name and inputs[1] == item1Name):
                return recipe["output"]
    return None

def handleItemDrop():
    global counterItems, toasterCooking, toasterStartTime, panCooking, panStartTime, ovenCooking, ovenStartTime
    if draggingItem is None:
        return
    item = draggingItem
    name = item["name"]
    cx = item["x"] + counterItemSize / 2
    cy = item["y"] + counterItemSize / 2

    if isOverRect(cx, cy, deleteBtnX, deleteBtnY, deleteBtnW, deleteBtnH):
        counterItems.remove(item)
        return

    overlappingItem = findItemAtPosition(cx, cy, item)
    if overlappingItem is not None:
        combinedResult = checkCounterCombination(name, overlappingItem["name"])
        if combinedResult is not None:
            counterItems.remove(item)
            counterItems.remove(overlappingItem)
            spawnCounterItem(combinedResult)
            return

    if isOverEllipse(cx, cy, bowlX + bowlW / 2, bowlY + bowlH / 2, bowlW / 2 + 30, bowlH / 2 + 30):
        counterItems.remove(item)
        bowlContents.append(name)
        return
    if isOverEllipse(cx, cy, panX + panW / 2, panY + panH / 2, panW / 2 + 20, panH / 2 + 20):
        if name in panRecipes:
            if panCooking is not None:
                item["x"] = dragOrigX
                item["y"] = dragOrigY
            else:
                result = panRecipes[name]
                counterItems.remove(item)
                panCooking = result
                panStartTime = millis()
        else:
            counterItems.remove(item)
            panContents.append(name)
        return
    if isOverRect(cx, cy, toasterX - 15, toasterY - 15, toasterW + 30, toasterH + 30):
        if name in toasterRecipes:
            if toasterCooking is not None:
                item["x"] = dragOrigX
                item["y"] = dragOrigY
            else:
                result = toasterRecipes[name]
                counterItems.remove(item)
                toasterCooking = result
                toasterStartTime = millis()
        else:
            item["x"] = dragOrigX
            item["y"] = dragOrigY
        return
    if isOverRect(cx, cy, ovenX - 15, ovenY - 15, ovenW + 30, ovenH + 30):
        if name in ovenRecipes:
            if ovenCooking is not None:
                item["x"] = dragOrigX
                item["y"] = dragOrigY
            else:
                result = ovenRecipes[name]
                counterItems.remove(item)
                ovenCooking = result
                ovenStartTime = millis()
        else:
            item["x"] = dragOrigX
            item["y"] = dragOrigY
        return
    if isOverRect(cx, cy, boardX - 15, boardY - 15, boardW + 30, boardH + 30):
        if name in chopRecipes:
            result = chopRecipes[name]
            counterItems.remove(item)
            spawnCounterItem(result)
        else:
            item["x"] = dragOrigX
            item["y"] = dragOrigY
        return

def handleBowlButtonClick():
    global bowlContents
    if len(bowlContents) == 0:
        return False
    bw = 70
    bh = 32
    by = bowlY + bowlH + 6
    if len(bowlContents) >= 2:
        mx = bowlX + bowlW / 2 - bw - 5
        if isOverRect(mouseX, mouseY, mx, by, bw, bh):
            matched = False
            best = None
            for recipe in bowlRecipes:
                inputs = recipe["inputs"]
                if len(inputs) != len(bowlContents):
                    continue
                tempBowl = list(bowlContents)
                allFound = True
                for inp in inputs:
                    if inp in tempBowl:
                        tempBowl.remove(inp)
                    else:
                        allFound = False
                        break
                if allFound and len(tempBowl) == 0:
                    best = recipe
                    matched = True
                    break
            if matched and best is not None:
                bowlContents = []
                spawnCounterItem(best["output"])
            return True
        cx = bowlX + bowlW / 2 + 5
        if isOverRect(mouseX, mouseY, cx, by, bw, bh):
            for name in bowlContents:
                spawnCounterItem(name)
            bowlContents = []
            return True
    else:
        cx = bowlX + bowlW / 2 - bw / 2
        if isOverRect(mouseX, mouseY, cx, by, bw, bh):
            for name in bowlContents:
                spawnCounterItem(name)
            bowlContents = []
            return True
    return False

# --- Arrows ---
def drawArrows():
    if currentStation > 0:
        draw_img(leftArrow, arrowLeftX, arrowY, arrowW, arrowH)
    if currentStation < len(stations) - 1:
        draw_img(rightArrow, arrowRightX, arrowY, arrowW, arrowH)

def handleArrowClick():
    global currentStation
    if currentStation > 0:
        if isOverRect(mouseX, mouseY, arrowLeftX, arrowY, arrowW, arrowH):
            currentStation -= 1
            return True
    if currentStation < len(stations) - 1:
        if isOverRect(mouseX, mouseY, arrowRightX, arrowY, arrowW, arrowH):
            currentStation += 1
            return True
    return False

# --- Cabinet ---
def drawCabinetOverlay():
    global overlayX, overlayY
    if not cabinetOpen:
        return
    draw_rect(0, 0, width, height, (0, 0, 0, 140))
    overlayX = width / 2 - overlayW / 2
    overlayY = height / 2 - overlayH / 2
    if cabinetImg is not None:
        draw_img(cabinetImg, overlayX, overlayY, overlayW, overlayH)
    else:
        draw_rect(overlayX, overlayY, overlayW, overlayH, (255, 255, 255), border_radius=20)
    drawCabinetItems(openCabinetKey)
    # Close button
    bx = overlayX + overlayW - 55
    by = overlayY + 15
    drawExitButton(bx, by, 40)

def drawCabinetItems(key):
    if key is None:
        return
    items = cabinetItems[key]
    cols = 2
    iconSize = 150
    gap = 0
    startX2 = overlayX + 295
    startY2 = overlayY + 250
    for i, name in enumerate(items):
        r = i // cols
        c = i % cols
        x = startX2 + c * (iconSize + gap)
        y = startY2 + r * (iconSize + gap)
        img = ingredientImgs.get(name, None)
        if img is not None:
            draw_img(img, x, y, iconSize, iconSize)
        else:
            draw_rect(x, y, iconSize, iconSize, (255, 255, 255, 180), border_radius=12)
            draw_rect_outline(x, y, iconSize, iconSize, (120, 120, 120), 1, border_radius=12)
            draw_text(name, x + iconSize / 2, y + iconSize / 2, 14, (60, 60, 60), "center", "center")

def handleKitchenCabinetClick():
    global cabinetOpen, openCabinetKey
    if stations[currentStation] != "kitchen":
        return False
    if cabinetOpen:
        bx = overlayX + overlayW - 55
        by = overlayY + 15
        if isOverRect(mouseX, mouseY, bx, by, 40, 40):
            cabinetOpen = False
            openCabinetKey = None
            return True
        return True
    if debugMouse:
        return False
    for key in cabinetHitboxes:
        hb = cabinetHitboxes[key]
        if isOverRect(mouseX, mouseY, hb["x"], hb["y"], hb["w"], hb["h"]):
            cabinetOpen = True
            openCabinetKey = key
            return True
    return False

# --- Delete Button ---
def drawDeleteButton():
    if stations[currentStation] != "kitchen":
        return
    if deleteBtn is not None:
        draw_img(deleteBtn, deleteBtnX, deleteBtnY, deleteBtnW, deleteBtnH)

# --- Event Handlers ---
def on_mouse_pressed(mx, my):
    global draggingItem, dragOffsetX, dragOffsetY, wasDragging, dragStartX, dragStartY, dragOrigX, dragOrigY
    wasDragging = False
    if currentScreen != "game" or stations[currentStation] != "kitchen":
        return
    if fridgeOpen or cabinetOpen or menuOpen or recipeCardOpen:
        return
    dragStartX = mx
    dragStartY = my
    i = len(counterItems) - 1
    while i >= 0:
        item = counterItems[i]
        if isOverRect(mx, my, item["x"], item["y"], counterItemSize, counterItemSize):
            draggingItem = item
            dragOffsetX = mx - item["x"]
            dragOffsetY = my - item["y"]
            dragOrigX = item["x"]
            dragOrigY = item["y"]
            counterItems.remove(item)
            counterItems.append(item)
            return
        i -= 1

def on_mouse_dragged(mx, my):
    global wasDragging
    if draggingItem is not None:
        draggingItem["x"] = mx - dragOffsetX
        draggingItem["y"] = my - dragOffsetY
        wasDragging = True

def on_mouse_released():
    global draggingItem
    if wasDragging and draggingItem is not None:
        handleItemDrop()
    draggingItem = None

def on_mouse_clicked():
    global currentScreen, howtoplayOpen, lastClickMs, wasDragging
    if wasDragging:
        wasDragging = False
        return
    now = millis()
    if now - lastClickMs < clickCooldownMs:
        return
    lastClickMs = now

    if recipeCardOpen:
        handleMenuClick()
        return
    if howtoplayOpen:
        handleHowToPlayClick()
        return
    if currentScreen == "home":
        pad = 20
        if isOverRect(mouseX, mouseY, startX - pad, startY - pad, startW + pad * 2, startH + pad * 2):
            currentScreen = "game"
            startGameRound()
            return
        if isOverRect(mouseX, mouseY, howX, howY, howW, howH):
            howtoplayOpen = True
            return
    if currentScreen == "game":
        if fridgeOpen:
            handleFridgeOverlayClick()
            return
        if menuOpen:
            if handleMenuClick():
                return
        if handleMenuClick():
            return
        if stations[currentStation] == "order":
            if handleServeButtonClick():
                return
        if stations[currentStation] == "kitchen":
            if handlePanButtonClick():
                return
            if handleBowlButtonClick():
                return
        if handleFridgeButtonClick():
            return
        if handleArrowClick():
            return
        if stations[currentStation] == "order" and dialogOpen:
            advanceDialog()
            return

def on_key_pressed(key):
    global debugMouse
    if key == pygame.K_d:
        debugMouse = not debugMouse

# --- Setup ---
def setup():
    global homeBg, title, startbutton, howtoplay, mainBg
    global howtoplayImg
    global leftArrow, rightArrow, breakfastBg, arrowRightX
    global cabinetImg, ingredientImgs
    global fridgeBtn, fridgeBtnY
    global toasterImg, boardImg, bowlImg, panImg
    global deleteBtn, deleteBtnX

    leftArrow = load_img("left_arrow.png")
    rightArrow = load_img("right_arrow.png")
    breakfastBg = load_img("breakfast_screen.png")
    arrowRightX = width - arrowW - 30

    homeBg = load_img("background_image.png")
    title = load_img("kitchen_text.png")
    startbutton = load_img("start_button_2.png")
    howtoplay = load_img("how_to_play_button.png")
    howtoplayImg = load_img("how_to_play.png")
    mainBg = load_img("main_background.png")

    cabinetImg = load_img("cabinet_expanded.png")

    fridgeBtn = load_img("fridge_button.png")
    fridgeBtnY = height - fridgeBtnH - 20

    toasterImg = load_img("toaster.png")
    boardImg = load_img("cutting_board.png")
    bowlImg = load_img("empty_bowl.png")
    panImg = load_img("empty_pan.png")
    deleteBtn = load_img("delete_button.png")
    deleteBtnX = width - deleteBtnW - 10

    ingredientImgs["flour"] = load_img("flour.png")
    ingredientImgs["sugar"] = load_img("sugar.png")
    ingredientImgs["eggs"] = load_img("eggs.png")
    ingredientImgs["milk"] = load_img("milk.png")
    ingredientImgs["butter_stick"] = load_img("butter_stick.png")
    ingredientImgs["berries_carton"] = load_img("berries_carton.png")
    ingredientImgs["whole_avocado"] = load_img("whole_avocado.png")
    ingredientImgs["whole_tomato"] = load_img("whole_tomato.png")
    ingredientImgs["cheese"] = load_img("cheese.png")
    ingredientImgs["raw_bacon"] = load_img("raw_bacon.png")
    ingredientImgs["batter_bottle"] = load_img("batter_bottle.png")
    ingredientImgs["cream"] = load_img("icing_tub.png")
    ingredientImgs["chocolate_chips"] = load_img("chocochips_bag.png")
    ingredientImgs["deli_meat"] = load_img("deli_meat_raw.png")
    ingredientImgs["syrup_bottle"] = load_img("maple_syrup.png")
    ingredientImgs["bread"] = load_img("bread.png")

    productNames = ["dough_formed", "cookiedough_formed", "cupcake_unbaked",
                     "fried_egg", "fried_bacon", "fried_deli_meat",
                     "toasted_bread", "chopped_avocado", "chopped_tomato",
                     "empty_pancakes", "pancakes_nosyrup", "pancakes",
                     "toasted_bread_egg", "toasted_bread_egg_cheese", "egg_sandwich",
                     "toasted_bread_avocado", "toasted_bread_avocado_tomato", "avocado_toast",
                     "toasted_bread_deli", "panini",
                     "cupcake", "cookie", "croissant"]
    for pn in productNames:
        img = load_img(pn + ".png")
        if img is not None:
            ingredientImgs[pn] = img

    c1 = load_img("character_1_happy.png")
    c2 = load_img("character_2_happy.png")
    if c1:
        customers.append(c1)
    if c2:
        customers.append(c2)

    setupMenuUI()
    loadMenuAssets()
    setupMenuFoodItems()

# --- Draw Screens ---
def drawHome():
    global startX, startY, startW, startH, howX, howY, howW, howH
    draw_img(homeBg, 0, 0, width, height)

    if title is not None:
        scaleFactor = 1.5
        titleW = title.get_width() * scaleFactor
        titleH = title.get_height() * scaleFactor
        titleX = width / 2 - titleW / 2
        titleY = height / 2 - titleH / 2 - 140
        draw_img(title, titleX, titleY, titleW, titleH)
    else:
        titleY = 100
        titleH = 80

    if startbutton is not None:
        sc = 0.158
        startW = int(startbutton.get_width() * sc)
        startH = int(startbutton.get_height() * sc)
        startX = int(width / 2 - startW / 2)
        startY = int(titleY + titleH + 20)
        draw_img(startbutton, startX, startY, startW, startH)

    if howtoplay is not None:
        howScale = 0.165
        howW = int(howtoplay.get_width() * howScale)
        howH = int(howtoplay.get_height() * howScale)
        howX = int(width / 2 - howW / 2)
        howY = int(titleY + titleH + 100)
        if howY + howH > height:
            howY = height - howH - 20
        draw_img(howtoplay, howX, howY, howW, howH)

def drawGame():
    global showCustomer, orderActive, currentCustomer, dialogOpen, gameStartTime, newCustomerAt

    checkCookingTimers()
    drawStation()

    if debugMouse and stations[currentStation] == "kitchen":
        draw_text("mouse: " + str(mouseX) + ", " + str(mouseY), 20, 140, 18, (255, 0, 0))

    if newCustomerAt > 0 and millis() >= newCustomerAt:
        newCustomerAt = 0
        gameStartTime = millis()
        showCustomer = True
        orderActive = True
        if currentCustomer is None and len(customers) > 0:
            currentCustomer = customers[random.randint(0, len(customers) - 1)]
        startCustomerDialog()

    if stations[currentStation] == "order":
        if not showCustomer and newCustomerAt == 0 and millis() - gameStartTime >= 1500:
            showCustomer = True
            orderActive = True
            if currentCustomer is None and len(customers) > 0:
                currentCustomer = customers[random.randint(0, len(customers) - 1)]
            startCustomerDialog()

    checkTimerExpired()

    if stations[currentStation] == "order" and showCustomer and currentCustomer is not None:
        charW = 320
        charH = 320
        charX = width / 2 - charW / 2 - 20
        charY = 225
        draw_img(currentCustomer, charX, charY, charW, charH)
        drawTimerBar(charX, charY, charW)

    if stations[currentStation] == "order" and showCustomer and dialogOpen:
        if dialogStep == 0:
            drawSpeechBubble(greetingText)
        else:
            drawSpeechBubble(orderText)

    drawKitchenTools()
    drawCounterItems()
    drawMoney()
    drawScorePopups()
    drawMenuUI()
    drawFridgeButton()
    drawArrows()
    drawFridgeOverlay()
    drawDeleteButton()
    drawServeButton()

def draw_frame():
    if currentScreen == "home":
        drawHome()
    elif currentScreen == "game":
        drawGame()
    if howtoplayOpen and not recipeCardOpen:
        drawHowToPlay()
    if recipeCardOpen:
        drawRecipeCard()

# --- Main Loop ---
def main():
    global mouseX, mouseY

    setup()

    mouse_down = False
    running = True

    while running:
        mouseX, mouseY = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                on_key_pressed(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
                on_mouse_pressed(event.pos[0], event.pos[1])

            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    on_mouse_dragged(event.pos[0], event.pos[1])

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_down = False
                on_mouse_released()
                on_mouse_clicked()

        screen.fill((0, 0, 0))
        draw_frame()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
