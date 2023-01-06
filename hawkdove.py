import random
import tkinter
random.seed()

def plot(xvals, yvals):
    # This is a function for creating a simple scatter plot.  You will use it,
    # but you can ignore the internal workings.
    root = tkinter.Tk()
    c = tkinter.Canvas(root, width=700, height=400, bg='white') # Was 350 x 280
    c.grid()
    # Create the x-axis.
    c.create_line(50,350,650,350, width=3)
    for i in range(5):
        x = 50 + (i * 150)
        c.create_text(x,355,anchor='n', text='%s'% (.5*(i+2) ) )
    # Create the y-axis.
    c.create_line(50,350,50,50, width=3)
    for i in range(5):
        y = 350 - (i * 75)
        c.create_text(45,y, anchor='e', text='%s'% (.25*i))
    # Plot the points.
    for i in range(len(xvals)):
        x, y = xvals[i], yvals[i]
        xpixel = int(50 + 300*(x-1))
        ypixel = int(350 - 300*y)
        c.create_oval(xpixel-3,ypixel-3,xpixel+3,ypixel+3, width=1, fill='red')
    root.mainloop()

# Constants - setting these values controls the parameters of your experiment.
injurycost     = 10   # Cost of losing a fight  
displaycost    = 1   # Cost of displaying between two passive birds  
foodbenefit    = 8   # Value of the food being fought over   
init_hawk      = 0
init_dove      = 0
init_defensive = 0
init_evolving  = 150

########

class World: 
    "A class representing the simulation world as a whole."
    def __init__(self):
        ## instance variable; empty list of currently-existing birds
        self.birdList = []
    
    # 'update' method calls update method for each bird in birdList
    def update(self):
        for eachBird in self.birdList:
            eachBird.update()
    
    # 'free_food' method awards a unit of food however many times the int input feedingrepeats specifies. 
    # for every single occurence in feedingrepeats, a random bird is chosen and the eat method is called.
    def free_food(self,feedingrepeats):
        # loops through occurences of feedingrepeats
        listLength = len(self.birdList)
        while feedingrepeats > 0:
            # choose a random bird
            rand = random.randint(0,listLength-1)
            bird = self.birdList[rand]
            # award this bird food
            bird.eat()
            # advance loop
            feedingrepeats -= 1
    
    # 'conflict' method creates encounters between birds over food.
    def conflict(self,encounters):
        # randomly choose a first and second bird for encounters depending on number of conflict occurences - encounters
        while encounters > 0:
            length = len(self.birdList)
            firstBird = self.birdList[random.randint(0,length-1)]
            secondBird = self.birdList[random.randint(0,length-1)]
            while firstBird == secondBird:
                secondBird = self.birdList[random.randint(0,length-1)]
            firstBird.encounter(secondBird)
            encounters -= 1
    
    # 'status' method that counts the number of birds in each existing species and prints a summary to terminal
    
    def status(self):
        totalDoves = 0
        totalHawks = 0
        totalDefensive = 0 
        totalEvolved = 0

        for bird in self.birdList:
            
            if bird.species == "Dove":
                totalDoves += 1
            elif bird.species == "Hawk":
                totalHawks += 1
            elif bird.species == "Defensive":
                totalDefensive += 1
            elif bird.species == "Evolving":
                totalEvolved += 1


        print("Total number of doves = " + str(totalDoves) + "\n" + "Total number of hawks = " + str(totalHawks) + "\n" + "Total number of defensive birds = " + str(totalDefensive) + "\n" + "Total number of evolved birds = " + str(totalEvolved))
    

  
    ## dear lovely graders
    ## please do comment this function out when running the first two parts of the project with doves, hawks and defensive birds
    ## also comment out the end script that calls the plot! thank you, I appreciate all that y'all do!

    # method 'evolvingPlot' that creates a scatter plot of all current Evolving birds

    def evolvingPlot(self):
        
        birdWeights = []
        birdAggression = []

        for bird in self.birdList:
            birdWeights.append(bird.weight)
            birdAggression.append(bird.aggression)

        return plot(birdWeights, birdAggression)

# # # # #  

class Bird:

    "A superclass parent for specific types of birds. "
    def __init__(self,w):
        w.birdList.append(self)
        ## instance variable storing bird's world
        self.birdWorld = w
        ## instance variable tracking bird's current health
        self.birdHealth = 100
        ## bird is added to list of birds existing in that world
        

    # 'eat' method increasing bird's health by foodbenefit constant
    def eat(self):
        self.birdHealth += foodbenefit
    
    # 'injured' method reducing bird's health by injurycost constant
    def injured(self):
        self.birdHealth -= injurycost
        

    
    # 'display' method reducing bird's health by displaycost constant
    def display(self):
        self.birdHealth -= displaycost
    
    # BEGONE BIRD method removing the beast from it's place in the heavens
    def die(self):
        w.birdList.remove(self)

    # 'update' method representing one unit of time passing!
    def update(self):
        self.birdHealth -= 1
        if self.birdHealth <= 0:
            self.die()
        
# # #

class Dove(Bird):
    "A subclass representing the Dove type of bird"

    # class variable representing the species of bird
    species = "Dove"

    # 11. modified 'update' method from superclass
    def update(self):
        super().update()
        # BIRD BABIES TIME (extension of Bird superclass update method)
        if self.birdHealth >= 200: # min health for reproduction is 200
            self.birdHealth -= 100
            
            # create a new bird of the same Dove type
            Dove(self.birdWorld)
    
    # 12. 'defend_choice' method that scripts an interaction if this bird has food and another bird encounters it 
    def defend_choice(self):
        return False
    
    # 13. 'encounter' method for when the dove comes upon another bird with food. Responds depending on defend_choice for other bird.
    def encounter(self,otherBird):
        # if the other bird defends itself... it can eat :)
        if otherBird.defend_choice():
            otherBird.eat()
        else: # if the other bird doesn't defend itself... display, eat
            self.display()
            otherBird.display()
            randomBird = random.choice([self,otherBird])
            randomBird.eat()


# # # 
class Hawk(Bird):
    "A subclass representing the Hawk type of bird"

    # class variable representing the species of bird
    species = "Hawk"

    # modified 'update' method from superclass
    def update(self):
        super().update()
        # BIRD BABIES TIME (reproduction extension of Bird superclass update method)
        if self.birdHealth >= 200: # min health for reproduction is 200
            self.birdHealth -= 100

            # create a new bird of the same Hawk type 
            Hawk(self.birdWorld)
    
    # 'defend_choice' method that scripts an interaction if this bird has food and another bird encounters it 
    def defend_choice(self):
        return True 

    # 13. 'encounter' method for when the hawk comes upon another bird with food. Responds depending on defend_choice for other bird.
    def encounter(self,otherBird):
        # if the other bird defends itself... fight!
        if otherBird.defend_choice():
            randomWinner = random.choice([self,otherBird])
            randomWinner.eat()
        
            ## if self wins, the other bird gets injured
            if randomWinner == self:
                otherBird.injured()
                

            ## if the other bird wins, self gets injured...
            elif randomWinner == otherBird:
                self.injured()
                

        # if the other bird doesn't defend itself, hawk eats
        else:
            Bird.eat(self)


# # # 
# Part 2 - Defensive

class Defensive(Bird):
    " 2. A subclass representing a defensive type of bird."

    # class variable representing the species of bird
    species = "Defensive"
    
    # modified 'update' that creates additional defensive birds
    def update(self):
        super().update()
        # BIRD BABIES TIME (extension of Bird superclass update method)
        if self.birdHealth >= 200: # min health for reproduction is 200
            self.birdHealth -= 100
            # create a new bird of the same Defensive type
            Defensive(self.birdWorld)
            
    
    # 'defend_choice' method that scripts an interaction if this bird has food and another bird encounters it 
    def defend_choice(self):
        return True
    
    # 'encounter' method for when the dove comes upon another bird with food. Responds depending on defend_choice for other bird.
    def encounter(self,otherBird):
        Dove.encounter(self,otherBird)

# # # 
# Part 3 - Evolution

class Evolving(Bird):
    "Third experiment: Evolution! A subclass representing birds that evolve over time "

    species = "Evolving"
    
    # inherit init and change a BUNCH of stuff

    def __init__(self,w,parent):
        super().__init__(w)
        
        if parent == None: # there is no parent and the bird is a part of the initial population
            self.aggression = random.uniform(0.0,1.0)
            self.weight = random.uniform(1.0,3.0)

        else: # it is NOT a part of the initial population of adam/eve birds at the start of the experiment - there is a parent
         # (biologically) inherit aggression and weight from parents!
         # wait, adam and eve? this class is literally called Evolving! bad joke sorry
         
            # creating the baby bird's aggression levels:
            totalAggression = parent.aggression + random.uniform(-0.05,0.05)
            if totalAggression > 1.0:
                self.aggression = 1.0
            elif totalAggression < 0.0:
                self.aggression = 0.0
            else:
                self.aggression = totalAggression
        
            # creating the baby bird's weight
            totalWeight = parent.weight + random.uniform(-0.1,0.1)
            if totalWeight > 3.0:
                self.weight = 3.0
            elif totalWeight < 1.0:
                self.weight = 1.0
            else:
                self.weight = totalWeight
    
    # modified 'defend_choice' that accounts for birds choosing to fight based on aggression levels, such that more aggressive birds fight more

    def defend_choice(self):
        rand = random.random()
        if rand <= self.aggression:
            return True 

    # modified 'encounter' that accounts for birds winning fights based on weights such that heavier birds win fights more

    def encounter(self,otherBird):

        # aggressive bird 
        if otherBird.defend_choice():
            if self.defend_choice(): # if both birds choose to fight
                # other bird weight calculation
                birdWeightage = otherBird.weight / (otherBird.weight + self.weight)
                rand = random.random()
                # if the other bird is heavier, it wins the fight
                if rand <= birdWeightage:
                    otherBird.eat()
                    self.injured()
                # if self is heavier, it wins the fight 
                else:
                    self.eat()
                    otherBird.injured()
            else: # if the other bird chooses to fight and self doesn't
                otherBird.eat()

        # non-aggressive bird 
        else:
            if self.defend_choice():
                self.eat()
            else:
                otherBird.display()
                self.display()
                # choose a random bird to win
                rand = random.randint(0,1)
                if rand == 0:
                    otherBird.eat()
                else:
                    self.eat()

        
    # modified 'update' 
    def update(self):  

        # as time passes, heavier birds burn more calories, losing more health
        self.birdHealth -= (0.4 + 0.6 * self.weight) + 1
        if self.birdHealth <= 0:
            self.die()

        # reproduction passing self as the parent parameter
        if self.birdHealth >= 200:
            self.birdHealth -= 100
            
            Evolving(self.birdWorld,self) #self needs to be passed as the parent...

    

########
# The code below actually runs the simulation.  You shouldn't have to do anything to it.
########
w = World()
for i in range(init_dove):
    Dove(w)
for i in range(init_hawk):
    Hawk(w)
for i in range(init_defensive):
    Defensive(w)
for i in range(init_evolving):
    Evolving(w,None)

for t in range(10000):
    w.free_food(10)
    w.conflict(50)
    w.update()
w.status()

w.evolvingPlot()    # This line adds a plot of evolving birds. Uncomment it when needed.


