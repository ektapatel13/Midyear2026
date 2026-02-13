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
    {"name":"croissant", "kind":"a"},
    {"name":"pancakes", "kind":"plural"},
    {"name":"egg sandwich", "kind":"an"},
    {"name":"avocado toast", "kind":"plural"},
    {"name":"panini", "kind":"a"},
    {"name":"cupcake", "kind":"a"},
    {"name":"cookie", "kind":"a"}
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

bowlRecipes = [
    {"inputs": ["flour", "eggs", "milk", "sugar"], "output": "dough_formed"},
    {"inputs": ["flour", "eggs", "milk"], "output": "batter_bottle"},
    {"inputs": ["dough_formed", "chocolate_chips"], "output": "cookiedough_formed"},
    {"inputs": ["dough_formed", "cream"], "output": "cupcake_unbaked"},
    {"inputs": ["toasted_bread", "fried_egg", "cheese", "bacon_fried"], "output": "egg_sandwich"},
    {"inputs": ["toasted_bread", "chopped_avocado", "chopped_tomato", "bacon_fried"], "output": "avocado_toast"},
    {"inputs": ["toasted_bread", "fried_deli_meat", "cheese"], "output": "panini"},
]
panRecipes = {"eggs": "fried_egg", "raw_bacon": "bacon_fried", "deli_meat": "fried_deli_meat"}
panMultiRecipes = [
    {"inputs": ["batter_bottle", "berries_carton"], "output": "pancakes"}
]
panContents = []
ovenRecipes = {"cookiedough_formed": "cookie", "cupcake_unbaked": "cupcake"}
chopRecipes = {"whole_avocado": "chopped_avocado", "whole_tomato": "chopped_tomato"}
toasterRecipes = {"bread": "toasted_bread"}

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

def isOverRect(px, py, rx, ry, rw, rh):
    return px >= rx and px <= rx + rw and py >= ry and py <= ry + rh

def isOverEllipse(px, py, cx, cy, rx, ry):
    dx = (px - cx) / float(rx)
    dy = (py - cy) / float(ry)
    return dx * dx + dy * dy <= 1.0

def setupMenuUI():
    global menuThumbX, menuThumbY
    menuThumbX = width - menuThumbW - 25
    menuThumbY = height - menuThumbH - 25

def loadMenuAssets():
    global menuImg, recipeCards
    menuImg = loadImage("menu.png")
    try:
        recipeCards["croissant"] = loadImage("croissant_instructions.png")
    except:
        print("Could not load croissant recipe")
    try:
        recipeCards["pancakes"] = loadImage("pancakes_instructions.png")
    except:
        print("Could not load pancakes recipe")
    try:
        recipeCards["egg_sandwich"] = loadImage("eggsandwich_instructions.png")
    except:
        print("Could not load egg sandwich recipe")
    try:
        recipeCards["avocado_toast"] = loadImage("avocadotoast_instructions.png")
    except:
        print("Could not load avocado toast recipe")
    try:
        recipeCards["panini"] = loadImage("panini_instructions.png")
    except:
        print("Could not load panini recipe")
    try:
        recipeCards["cupcake"] = loadImage("cupcake_instructions.png")
    except:
        print("Could not load cupcake recipe")
    try:
        recipeCards["cookie"] = loadImage("cookie_instructions.png")
    except:
        print("Could not load cookie recipe")

def setupMenuFoodItems():
    global menuFoodItems
    menuFoodItems = []
    pad = 35
    
    menuFoodItems.append({"name": "croissant", "x": 80 - pad,  "y": 190 - pad, "w": 140 + pad*2, "h": 140 + pad*2})
    menuFoodItems.append({"name": "pancakes",  "x": 300 - pad, "y": 190 - pad, "w": 140 + pad*2, "h": 140 + pad*2})
    menuFoodItems.append({"name": "egg_sandwich","x": 520 - pad,"y": 190 - pad, "w": 140 + pad*2, "h": 140 + pad*2})
    menuFoodItems.append({"name": "avocado_toast","x": 150 - pad,"y": 400 - pad, "w": 140 + pad*2, "h": 140 + pad*2})
    menuFoodItems.append({"name": "panini",      "x": 500 - pad,"y": 400 - pad, "w": 140 + pad*2, "h": 140 + pad*2})
    menuFoodItems.append({"name": "cupcake", "x": 180 - pad, "y": 590 - pad, "w": 120 + pad*2, "h": 120 + pad*2})
    menuFoodItems.append({"name": "cookie",  "x": 500 - pad, "y": 590 - pad, "w": 120 + pad*2, "h": 120 + pad*2})

def getRecipeCardPos():
    x = width/2 - recipeCardW/2
    y = height/2 - recipeCardH/2

    if recipeCardW > width:
        x = 0
    else:
        if x < 0:
            x = 0
        if x + recipeCardW > width:
            x = width - recipeCardW
    if recipeCardH > height:
        y = 0
    else:
        if y < 0:
            y = 0
        if y + recipeCardH > height:
            y = height - recipeCardH
    return x, y

def drawRecipeCardExitButton(cardX, cardY, cardW, cardH):
    ex = cardX + cardW - exitSize - 12
    ey = cardY + 12
    noStroke()
    fill(255, 80, 80)
    rect(ex, ey, exitSize, exitSize, 10)
    stroke(255)
    strokeWeight(5)
    line(ex + 12, ey + 12, ex + exitSize - 12, ey + exitSize - 12)
    line(ex + exitSize - 12, ey + 12, ex + 12, ey + exitSize - 12)
    strokeWeight(1)

def drawRecipeCard():
    fill(0, 0, 0, 200)
    noStroke()
    rect(0, 0, width, height)
    cardX, cardY = getRecipeCardPos()
    if currentRecipe in recipeCards and recipeCards[currentRecipe] != None:
        image(recipeCards[currentRecipe], cardX, cardY, recipeCardW, recipeCardH)
    else:
        fill(255)
        rect(cardX, cardY, recipeCardW, recipeCardH, 10)
        fill(0)
        textAlign(CENTER, CENTER)
        textSize(24)
        text("Recipe card for " + str(currentRecipe), width/2, height/2)
    drawRecipeCardExitButton(cardX, cardY, recipeCardW, recipeCardH)

def drawMenuUI():
    image(menuImg, menuThumbX, menuThumbY, menuThumbW, menuThumbH)
    if menuOpen:
        x = width/2 - menuW/2
        y = height/2 - menuH/2
        image(menuImg, x, y, menuW, menuH)
        drawMenuExitButton(x, y, menuW, menuH)

def drawMenuExitButton(mx, my, mw, mh):
    global exitX, exitY
    exitX = mx + mw - exitSize - 12
    exitY = my + 12
    noStroke()
    fill(255, 80, 80)
    rect(exitX, exitY, exitSize, exitSize, 10)
    stroke(255)
    strokeWeight(5)
    line(exitX + 12, exitY + 12, exitX + exitSize - 12, exitY + exitSize - 12)
    line(exitX + exitSize - 12, exitY + 12, exitX + 12, exitY + exitSize - 12)
    strokeWeight(1)

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
        menuX0 = width/2 - menuW/2
        menuY0 = height/2 - menuH/2
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

def drawHowToPlay():
    fill(0, 0, 0, 180)
    noStroke()
    rect(0, 0, width, height)
    hw = 800
    hh = 800
    hx = width/2 - hw/2
    hy = height/2 - hh/2
    if howtoplayImg:
        image(howtoplayImg, hx, hy, hw, hh)
    drawHowToPlayExitButton(hx, hy, hw, hh)

def drawHowToPlayExitButton(hx, hy, hw, hh):
    ex = hx + hw - exitSize - 12
    ey = hy + 12
    noStroke()
    fill(255, 80, 80)
    rect(ex, ey, exitSize, exitSize, 10)
    stroke(255)
    strokeWeight(5)
    line(ex + 12, ey + 12, ex + exitSize - 12, ey + exitSize - 12)
    line(ex + exitSize - 12, ey + 12, ex + 12, ey + exitSize - 12)
    strokeWeight(1)

def handleHowToPlayClick():
    global howtoplayOpen
    if howtoplayOpen:
        hw = 800
        hh = 800
        hx = width/2 - hw/2
        hy = height/2 - hh/2
        ex = hx + hw - exitSize - 12
        ey = hy + 12
        if isOverRect(mouseX, mouseY, ex, ey, exitSize, exitSize):
            howtoplayOpen = False
            return True
    return False

def buildOrderCounts():
    n = int(random(1, 5))
    counts = {}
    kinds = {}
    i = 0
    while i < n:
        item = menuItems[int(random(len(menuItems)))]
        name = item["name"]
        kind = item["kind"]
        kinds[name] = kind
        if name in counts:
            counts[name] += 1
        else:
            counts[name] = 1
        i += 1
    return counts, kinds

def pluralize(word):
    if word.endswith("s"):
        return word
    if word.endswith("y") and len(word) > 1 and word[-2].lower() not in ["a","e","i","o","u"]:
        return word[:-1] + "ies"
    if word.endswith("ch") or word.endswith("sh") or word.endswith("x") or word.endswith("z"):
        return word + "es"
    return word + "s"

def joinParts(parts):
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return parts[0] + " and " + parts[1]
    s = ""
    i = 0
    while i < len(parts) - 1:
        s += parts[i] + ", "
        i += 1
    s += "and " + parts[len(parts) - 1]
    return s

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
    greetingText = greetings[int(random(len(greetings)))]
    orderText = generateNewOrder()

def advanceDialog():
    global dialogOpen, dialogStep
    if dialogStep == 0:
        dialogStep = 1
    else:
        dialogOpen = False

def drawSpeechBubble(textMain):
    bubbleW = 290
    bubbleH = 140
    bubbleX = width/2 - bubbleW/2 + 82
    bubbleY = 55
    noStroke()
    fill(255)
    rect(bubbleX, bubbleY, bubbleW, bubbleH, 18)
    tailX = bubbleX + 60
    tailY = bubbleY + bubbleH
    triangle(tailX, tailY, tailX + 40, tailY, tailX + 20, tailY + 28)
    fill(0)
    textAlign(LEFT, TOP)
    textSize(22)
    text(textMain, bubbleX + 20, bubbleY + 18, bubbleW - 40, bubbleH - 60)
    fill(60)
    textSize(16)
    text("(tap to continue)", bubbleX + 20, bubbleY + bubbleH - 30)

def drawMoney():
    fill(0, 150)
    noStroke()
    rect(30, 20, 240, 80)
    fill(255)
    textAlign(LEFT, TOP)
    textSize(28)
    text("Money: $" + str(money), 50, 30)
    fill(255, 255, 100)
    textSize(22)
    text("Order: $" + str(orderValue), 50, 65)

def drawScorePopups():
    global scorePopups
    popupsToRemove = []
    i = 0
    while i < len(scorePopups):
        popup = scorePopups[i]
        age = millis() - popup['time']
        if age > 1500:
            popupsToRemove.append(popup)
        else:
            alpha = 255 - (age / 1500.0 * 255)
            yOffset = age / 10.0
            noStroke()
            fill(popup['color'][0], popup['color'][1], popup['color'][2], alpha)
            textAlign(CENTER, CENTER)
            textSize(32)
            text(popup['text'], popup['x'], popup['y'] - yOffset)
        i += 1
    i = 0
    while i < len(popupsToRemove):
        scorePopups.remove(popupsToRemove[i])
        i += 1

def startGameRound():
    global showCustomer, gameStartTime, money, currentCustomer, orderActive, dialogOpen, dialogStep, bowlContents, counterItems, panContents
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

def drawTimerBar(charX, charY, charW):
    barWidth = 220
    barHeight = 18
    barX = charX + charW/2 - barWidth/2
    barY = charY + 15
    fill(50)
    stroke(0)
    strokeWeight(2)
    rect(barX, barY, barWidth, barHeight, 6)
    timeElapsed = millis() - gameStartTime
    fillWidth = barWidth - (timeElapsed / 350.0)
    if fillWidth < 0:
        fillWidth = 0
    if fillWidth > barWidth * 0.5:
        fill(100, 200, 100)
    elif fillWidth > barWidth * 0.25:
        fill(255, 200, 0)
    else:
        fill(255, 100, 100)
    noStroke()
    rect(barX, barY, fillWidth, barHeight, 6)

def drawStation():
    if stations[currentStation] == "order":
        image(mainBg, 0, 0, width, height)
    elif stations[currentStation] == "kitchen":
        image(breakfastBg, 0, 0, width, height)

def drawFridgeButton():
    if stations[currentStation] == "kitchen" and fridgeBtn != None:
        image(fridgeBtn, fridgeBtnX, fridgeBtnY, fridgeBtnW, fridgeBtnH)

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
    noStroke()
    fill(50, 50, 50, 170)
    rect(0, 0, width, height)
    gx, gy = getFridgeGridOrigin()
    r = 0
    while r < fridgeGridRows:
        c = 0
        while c < fridgeGridCols:
            x = gx + c * (fridgeBtnSize + fridgeGap)
            y = gy + r * (fridgeBtnSize + fridgeGap)
            name = fridgeGrid[r][c]
            alreadySelected = counterHasItem(name)
            if alreadySelected:
                stroke(80, 200, 80)
                strokeWeight(4)
                fill(200, 240, 200)
            else:
                noStroke()
                fill(255, 200, 210)
            rect(x, y, fridgeBtnSize, fridgeBtnSize, 16)
            strokeWeight(1)
            img = ingredientImgs.get(name, None)
            if img != None:
                pad = 14
                if alreadySelected:
                    tint(255, 160)
                image(img, x + pad, y + pad, fridgeBtnSize - pad * 2, fridgeBtnSize - pad * 2)
                if alreadySelected:
                    noTint()
            else:
                fill(80)
                textAlign(CENTER, CENTER)
                textSize(13)
                text(name, x + fridgeBtnSize / 2, y + fridgeBtnSize / 2)
            c += 1
        r += 1
    drawFridgeCloseButton()

def drawFridgeCloseButton():
    bx = width - 60
    by = 20
    noStroke()
    fill(255, 80, 80)
    rect(bx, by, 42, 42, 10)
    stroke(255)
    strokeWeight(5)
    line(bx + 12, by + 12, bx + 30, by + 30)
    line(bx + 30, by + 12, bx + 12, by + 30)
    strokeWeight(1)

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
    r = 0
    while r < fridgeGridRows:
        c = 0
        while c < fridgeGridCols:
            x = gx + c * (fridgeBtnSize + fridgeGap)
            y = gy + r * (fridgeBtnSize + fridgeGap)
            if isOverRect(mouseX, mouseY, x, y, fridgeBtnSize, fridgeBtnSize):
                name = fridgeGrid[r][c]
                if not counterHasItem(name):
                    idx = len(counterItems)
                    px, py = getCounterItemPos(idx)
                    counterItems.append({"name": name, "x": px, "y": py})
                return True
            c += 1
        r += 1
    return True

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
    i = 0
    while i < len(counterItems):
        if counterItems[i]["name"] == name:
            return True
        i += 1
    return False

def drawCounterItems():
    if stations[currentStation] != "kitchen":
        return
    i = 0
    while i < len(counterItems):
        item = counterItems[i]
        name = item["name"]
        img = ingredientImgs.get(name, None)
        x = item["x"]
        y = item["y"]
        if img != None:
            image(img, x, y, counterItemSize, counterItemSize)
        else:
            fill(255, 200, 210)
            noStroke()
            rect(x, y, counterItemSize, counterItemSize, 10)
            fill(80)
            textAlign(CENTER, CENTER)
            textSize(12)
            text(name, x + counterItemSize / 2, y + counterItemSize / 2)
        i += 1

def drawKitchenTools():
    if stations[currentStation] != "kitchen":
        return
    drawToaster()
    drawPan()
    drawBoard()
    drawBowl()

def drawBoard():
    if boardImg != None:
        image(boardImg, boardX, boardY, boardW, boardH)
    else:
        noStroke()
        fill(170, 130, 75)
        rect(boardX, boardY, boardW, boardH, 6)
        fill(150, 110, 55)
        rect(boardX + 6, boardY + 6, boardW - 12, boardH - 12, 4)

def drawBowl():
    if bowlImg != None:
        image(bowlImg, bowlX, bowlY, bowlW, bowlH)
    else:
        noStroke()
        fill(200, 200, 210)
        ellipse(bowlX + bowlW / 2, bowlY + bowlH / 2, bowlW, bowlH)
        fill(230, 230, 240)
        ellipse(bowlX + bowlW / 2, bowlY + bowlH / 2, bowlW - 40, bowlH - 40)
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
    i = 0
    while i < len(bowlContents):
        name = bowlContents[i]
        ix = sx + i * (iconSize + gap)
        img = ingredientImgs.get(name, None)
        if img != None:
            image(img, ix, sy, iconSize, iconSize)
        else:
            fill(180)
            noStroke()
            rect(ix, sy, iconSize, iconSize, 6)
            fill(40)
            textAlign(CENTER, CENTER)
            textSize(8)
            text(name, ix + iconSize / 2, sy + iconSize / 2)
        i += 1

def drawBowlButtons():
    bw = 70
    bh = 32
    by = bowlY + bowlH + 6
    if len(bowlContents) >= 2:
        mx = bowlX + bowlW / 2 - bw - 5
        noStroke()
        fill(80, 180, 80)
        rect(mx, by, bw, bh, 10)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(16)
        text("Mix!", mx + bw / 2, by + bh / 2)
        cx = bowlX + bowlW / 2 + 5
        noStroke()
        fill(200, 80, 80)
        rect(cx, by, bw, bh, 10)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(16)
        text("Clear", cx + bw / 2, by + bh / 2)
    else:
        cx = bowlX + bowlW / 2 - bw / 2
        noStroke()
        fill(200, 80, 80)
        rect(cx, by, bw, bh, 10)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(16)
        text("Clear", cx + bw / 2, by + bh / 2)

def drawPan():
    if panImg != None:
        image(panImg, panX, panY, panW, panH)
    else:
        noStroke()
        fill(80, 80, 90)
        ellipse(panX + panW / 2, panY + panH / 2, panW, panH)
        fill(55, 55, 63)
        ellipse(panX + panW / 2, panY + panH / 2, panW - 18, panH - 12)
        fill(95, 95, 105)
        rect(panX + panW - 8, panY + panH / 2 - 7, 38, 14, 5)
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
    i = 0
    while i < len(panContents):
        name = panContents[i]
        ix = sx + i * (iconSize + gap)
        img = ingredientImgs.get(name, None)
        if img != None:
            image(img, ix, sy, iconSize, iconSize)
        else:
            fill(180)
            noStroke()
            rect(ix, sy, iconSize, iconSize, 6)
            fill(40)
            textAlign(CENTER, CENTER)
            textSize(8)
            text(name, ix + iconSize / 2, sy + iconSize / 2)
        i += 1

def drawPanButtons():
    bw = 60
    bh = 28
    by = panY + panH + 8
    if len(panContents) >= 2:
        mx = panX + panW / 2 - bw - 4
        noStroke()
        fill(80, 180, 80)
        rect(mx, by, bw, bh, 8)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(14)
        text("Cook!", mx + bw / 2, by + bh / 2)
        cx = panX + panW / 2 + 4
        noStroke()
        fill(200, 80, 80)
        rect(cx, by, bw, bh, 8)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(14)
        text("Clear", cx + bw / 2, by + bh / 2)
    else:
        cx = panX + panW / 2 - bw / 2
        noStroke()
        fill(200, 80, 80)
        rect(cx, by, bw, bh, 8)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(14)
        text("Clear", cx + bw / 2, by + bh / 2)

def handlePanButtonClick():
    global panContents
    if len(panContents) == 0:
        return False
    bw = 60
    bh = 28
    by = panY + panH + 8
    if len(panContents) >= 2:
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
            if matched:
                panContents = []
                spawnCounterItem(best["output"])
            return True
        cx = panX + panW / 2 + 4
        if isOverRect(mouseX, mouseY, cx, by, bw, bh):
            i = 0
            while i < len(panContents):
                spawnCounterItem(panContents[i])
                i += 1
            panContents = []
            return True
    else:
        cx = panX + panW / 2 - bw / 2
        if isOverRect(mouseX, mouseY, cx, by, bw, bh):
            i = 0
            while i < len(panContents):
                spawnCounterItem(panContents[i])
                i += 1
            panContents = []
            return True
    return False

def drawToaster():
    if toasterImg != None:
        image(toasterImg, toasterX, toasterY, toasterW, toasterH)

def spawnCounterItem(name):
    idx = len(counterItems)
    px, py = getCounterItemPos(idx)
    counterItems.append({"name": name, "x": px, "y": py})

def handleItemDrop():
    if draggingItem == None:
        return
    item = draggingItem
    name = item["name"]
    cx = item["x"] + counterItemSize / 2
    cy = item["y"] + counterItemSize / 2
    if isOverEllipse(cx, cy, bowlX + bowlW / 2, bowlY + bowlH / 2, bowlW / 2 + 30, bowlH / 2 + 30):
        counterItems.remove(item)
        bowlContents.append(name)
        return
    if isOverEllipse(cx, cy, panX + panW / 2, panY + panH / 2, panW / 2 + 20, panH / 2 + 20):
        if name in panRecipes:
            result = panRecipes[name]
            counterItems.remove(item)
            spawnCounterItem(result)
        else:
            counterItems.remove(item)
            panContents.append(name)
        return
    if isOverRect(cx, cy, toasterX - 15, toasterY - 15, toasterW + 30, toasterH + 30):
        if name in toasterRecipes:
            result = toasterRecipes[name]
            counterItems.remove(item)
            spawnCounterItem(result)
        else:
            item["x"] = dragOrigX
            item["y"] = dragOrigY
        return
    if isOverRect(cx, cy, ovenX - 15, ovenY - 15, ovenW + 30, ovenH + 30):
        if name in ovenRecipes:
            result = ovenRecipes[name]
            counterItems.remove(item)
            spawnCounterItem(result)
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
            bestLen = 0
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
            if matched:
                bowlContents = []
                spawnCounterItem(best["output"])
            return True
        cx = bowlX + bowlW / 2 + 5
        if isOverRect(mouseX, mouseY, cx, by, bw, bh):
            i = 0
            while i < len(bowlContents):
                spawnCounterItem(bowlContents[i])
                i += 1
            bowlContents = []
            return True
    else:
        cx = bowlX + bowlW / 2 - bw / 2
        if isOverRect(mouseX, mouseY, cx, by, bw, bh):
            i = 0
            while i < len(bowlContents):
                spawnCounterItem(bowlContents[i])
                i += 1
            bowlContents = []
            return True
    return False

def drawArrows():
    if currentStation > 0:
        image(leftArrow, arrowLeftX, arrowY, arrowW, arrowH)
    if currentStation < len(stations) - 1:
        image(rightArrow, arrowRightX, arrowY, arrowW, arrowH)

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

def drawCabinetOverlay():
    global overlayX, overlayY
    if not cabinetOpen:
        return
    noStroke()
    fill(0, 0, 0, 140)
    rect(0, 0, width, height)
    overlayX = width/2 - overlayW/2
    overlayY = height/2 - overlayH/2
    if cabinetImg != None:
        image(cabinetImg, overlayX, overlayY, overlayW, overlayH)
    else:
        fill(255)
        rect(overlayX, overlayY, overlayW, overlayH, 20)
    drawCabinetItems(openCabinetKey)
    drawOverlayCloseButton()

def drawOverlayCloseButton():
    bx = overlayX + overlayW - 55
    by = overlayY + 15
    noStroke()
    fill(255, 80, 80)
    rect(bx, by, 40, 40, 10)
    stroke(255)
    strokeWeight(4)
    line(bx+12, by+12, bx+28, by+28)
    line(bx+28, by+12, bx+12, by+28)
    strokeWeight(1)

def drawCabinetItems(key):
    if key == None:
        return
    items = cabinetItems[key]
    cols = 2
    iconSize = 150
    gap = 0
    startX2 = overlayX + 295
    startY2 = overlayY + 250
    i = 0
    while i < len(items):
        name = items[i]
        r = i // cols
        c = i % cols
        x = startX2 + c * (iconSize + gap)
        y = startY2 + r * (iconSize + gap)
        img = ingredientImgs.get(name, None)
        if img != None:
            image(img, x, y, iconSize, iconSize)
        else:
            fill(255, 255, 255, 180)
            stroke(120)
            rect(x, y, iconSize, iconSize, 12)
            fill(60)
            noStroke()
            textAlign(CENTER, CENTER)
            textSize(14)
            text(name, x + iconSize/2, y + iconSize/2)
        i += 1

def handleKitchenCabinetClick():
    global cabinetOpen, openCabinetKey, debugMouse
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

def keyPressed():
    global debugMouse
    if key == 'd' or key == 'D':
        debugMouse = not debugMouse

def mousePressed():
    global draggingItem, dragOffsetX, dragOffsetY, wasDragging, dragStartX, dragStartY, dragOrigX, dragOrigY
    wasDragging = False
    if currentScreen != "game" or stations[currentStation] != "kitchen":
        return
    if fridgeOpen or cabinetOpen or menuOpen or recipeCardOpen:
        return
    dragStartX = mouseX
    dragStartY = mouseY
    i = len(counterItems) - 1
    while i >= 0:
        item = counterItems[i]
        if isOverRect(mouseX, mouseY, item["x"], item["y"], counterItemSize, counterItemSize):
            draggingItem = item
            dragOffsetX = mouseX - item["x"]
            dragOffsetY = mouseY - item["y"]
            dragOrigX = item["x"]
            dragOrigY = item["y"]
            counterItems.remove(item)
            counterItems.append(item)
            return
        i -= 1

def mouseDragged():
    global wasDragging
    if draggingItem != None:
        draggingItem["x"] = mouseX - dragOffsetX
        draggingItem["y"] = mouseY - dragOffsetY
        wasDragging = True

def mouseReleased():
    global draggingItem
    if wasDragging and draggingItem != None:
        handleItemDrop()
    draggingItem = None

def mouseClicked():
    global currentScreen, howtoplayOpen, lastClickMs, debugMouse, wasDragging
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
        if isOverRect(mouseX, mouseY, startX - pad, startY - pad, startW + pad*2, startH + pad*2):
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

def setup():
    global homeBg, title, startbutton, howtoplay, mainBg
    global howtoplayImg
    global leftArrow, rightArrow, breakfastBg, arrowRightX
    global cabinetImg, ingredientImgs
    global fridgeBtn, fridgeBtnY
    global toasterImg, boardImg, bowlImg, panImg
    size(1300, 760)

    leftArrow = loadImage("left_arrow.png")
    rightArrow = loadImage("right_arrow.png")
    breakfastBg = loadImage("breakfast_screen.png")
    arrowRightX = width - arrowW - 30

    homeBg = loadImage("background_image.png")
    title = loadImage("kitchen_text.png")
    startbutton = loadImage("start_button_2.png")
    howtoplay = loadImage("how_to_play_button.png")
    howtoplayImg = loadImage("how_to_play.png")
    mainBg = loadImage("main_background.png")

    cabinetImg = loadImage("cabinet_expanded.png")

    fridgeBtn = loadImage("fridge_button.png")
    fridgeBtnY = height - fridgeBtnH - 20

    try:
        toasterImg = loadImage("toaster.png")
    except:
        toasterImg = None
    try:
        boardImg = loadImage("cutting_board.png")
    except:
        boardImg = None
    try:
        bowlImg = loadImage("empty_bowl.png")
    except:
        bowlImg = None
    try:
        panImg = loadImage("empty_pan.png")
    except:
        panImg = None

    ingredientImgs["flour"] = loadImage("flour.png")
    ingredientImgs["sugar"] = loadImage("sugar.png")
    ingredientImgs["eggs"] = loadImage("eggs.png")
    ingredientImgs["milk"] = loadImage("milk.png")
    ingredientImgs["butter_stick"] = loadImage("butter_stick.png")

    ingredientImgs["berries_carton"] = loadImage("berries_carton.png")
    ingredientImgs["whole_avocado"] = loadImage("whole_avocado.png")
    ingredientImgs["whole_tomato"] = loadImage("whole_tomato.png")

    ingredientImgs["cheese"] = loadImage("cheese.png")
    ingredientImgs["raw_bacon"] = loadImage("raw_bacon.png")

    ingredientImgs["batter_bottle"] = loadImage("batter_bottle.png")

    ingredientImgs["cream"] = loadImage("icing_tub.png")
    ingredientImgs["chocolate_chips"] = loadImage("chocochips_bag.png")
    ingredientImgs["deli_meat"] = loadImage("deli_meat_raw.png")
    ingredientImgs["syrup_bottle"] = loadImage("maple_syrup.png")
    ingredientImgs["bread"] = loadImage("bread.png")

    productNames = ["dough_formed", "cookiedough_formed", "cupcake_unbaked",
                     "fried_egg", "bacon_fried", "fried_deli_meat",
                     "toasted_bread", "chopped_avocado", "chopped_tomato",
                     "pancakes", "egg_sandwich", "avocado_toast",
                     "panini", "cupcake", "cookie"]
    for pn in productNames:
        try:
            ingredientImgs[pn] = loadImage(pn + ".png")
        except:
            pass

    customer1 = loadImage("character_1_happy.png")
    customer2 = loadImage("character_2_happy.png")
    customers[:] = [customer1, customer2]
    setupMenuUI()
    loadMenuAssets()
    setupMenuFoodItems()

def draw():
    if currentScreen == "home":
        drawHome()
    elif currentScreen == "game":
        drawGame()
    if howtoplayOpen and not recipeCardOpen:
        drawHowToPlay()
    if recipeCardOpen:
        drawRecipeCard()

def drawHome():
    global startX, startY, startW, startH, howX, howY, howW, howH
    image(homeBg, 0, 0, width, height)

    scaleFactor = 1.5
    titleW = title.width * scaleFactor
    titleH = title.height * scaleFactor
    titleX = width/2 - titleW/2
    titleY = height/2 - titleH/2 - 140
    image(title, titleX, titleY, titleW, titleH)

    scale = 0.158
    startW = int(startbutton.width * scale)
    startH = int(startbutton.height * scale)
    startX = int(width/2 - startW/2)
    startY = int(titleY + titleH + 20)
    image(startbutton, startX, startY, startW, startH)

    howScale = 0.165
    howW = int(howtoplay.width * howScale)
    howH = int(howtoplay.height * howScale)
    howX = int(width/2 - howW/2)
    howY = int(titleY + titleH + 100)
    if howY + howH > height:
        howY = height - howH - 20
    image(howtoplay, howX, howY, howW, howH)

def drawGame():
    global showCustomer, orderActive, currentCustomer, dialogOpen
    drawStation()

    if debugMouse and stations[currentStation] == "kitchen":
        fill(255, 0, 0)
        textSize(18)
        text("mouse: " + str(mouseX) + ", " + str(mouseY), 20, 140)

    if stations[currentStation] == "order":
        if not showCustomer and millis() - gameStartTime >= 1500:
            showCustomer = True
            orderActive = True
            if currentCustomer == None and len(customers) > 0:
                currentCustomer = customers[int(random(len(customers)))]
            startCustomerDialog()

    if stations[currentStation] == "order" and showCustomer and currentCustomer != None:
        charW = 320
        charH = 320
        charX = width/2 - charW/2 - 20
        charY = 225
        image(currentCustomer, charX, charY, charW, charH)
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
