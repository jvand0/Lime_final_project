from math import sqrt
import random

directions = ['north', 'south', 'east', 'west']

class Arrow:
    """
    Creates an arrow object (Ethan P.)

    Attributes:
      distance (int): the archer's distance from the board
      vert_angle (int): the archer's bow vertical angle
      horiz_angle (int): the archer's bow horizontal angle
      power (int): how powerful the archer makes the shot
      bow_type (str): the type of bow the archer uses
      speed (int): the wind's speed
      direction (str): the wind's direction
    """
    def __init__(self, distance, vert_angle, horiz_angle, power, bow_type, speed=random.randint(0,30), direction = random.choice(directions)):
        self.vert_angle = vert_angle
        self.horiz_angle = horiz_angle
        self.power = power
        self.bow_type = bow_type
        self.speed = speed
        self.direction = direction
        print(f"There is {self.speed} mph wind, coming from the {self.direction}.")
        distance = 15
        self.distance = distance
        self.bow_type = input("Enter the type of bow: Long, Short, or Mech: ")
        
        while(self.bow_type != "Long" and self.bow_type != "Short" and self.bow_type != "Mech"):
          print("Bow type must be Long, Short, or Mech.")
          self.bow_type = input("Enter the type of bow: Long, Short, or Mech: ")

        self.vert_angle = int(input("Enter the angle (going up and down) you'd like to shoot at: "))
        self.horiz_angle = int(input("Enter the angle (going side to side) you'd like to shoot at: "))
        self.power = int(input("Enter the power you'd like to shoot (0-100) at (Disclaimer: shooting with more power is often less accurate): "))

        if self.bow_type == "Long":
          self.power += 1
        elif self.bow_type == "Short":
          self.power -= 1
        elif self.bow_type == "Mech":
          self.power *= 2

        
    def shot(self):
        """ (Ethan P.)
        Creates an arrow shot based on power and both vertical and 
        horizontal angles.

        Returns:
          self.point (tuple): coordinates of where the shot hit

        """
        self.x = 0
        self.y = 0
        rando = 0
        opt_power = abs((self.distance * 4) - self.power) # optimal power is distance * 4, this checks how close the input power is to the optimal power
        if opt_power > 20: # if the input power isn't within 20 of the optimal power then the dart has a bigger random factor
            rando = rando + 40
        else:
            rando = int(rando) + opt_power
        rando = int(rando) * (1 + (self.distance / 100)) # makes it less accurate if you are further away
        self.x = random.uniform(-rando, rando)
        self.y = random.uniform(-rando, rando)
        opt_angle = 27 # optimal angle when shooting an arrow
        self.y = self.y + (self.vert_angle - opt_angle) + random.uniform(-5, 5) # vertical coordinate is dependent on vertical angle minus the optimal throwing angle (random is for some human error)
        self.x = self.x + self.horiz_angle + random.uniform(-5, 5) # horizontal coordinate is dependent on horizontal angle (random is for some human error)
        point = (self.x, self.y)
        self.point = point
        return self.point
    
    def gravity(self, x=0, y=0):
        """ (Ethan P.)
        Accounts for gravity affecting the arrow's landing coordinates.

        Args:
          x (int): starting x coordinate of arrow
          y (int): starting y coordinate of arrow

        Returns:
          y (int): new y coordinate of arrow after accounting for gravity
        """

        gravity = -385.8 # -9.8 m/s^2 in inches per second
        gravity = (gravity * 1/self.power) # makes it so that more power is "less" affected by gravity
        gravity = gravity * (self.distance * .1) # makes it so that a larger distance has more gravitational effect
        y = y - gravity # gravity affects y coordinate only
        
        return y

    def wind(self, x=0, y=0):
        """
        Accounts for wind affecting the arrow's landing coordinates. (Ike)

        Args:
          x (int): starting x coordinate of arrow
          y (int): starting y coordinate of arrow

        Returns:
          new_point (tuple): new coordinates of arrow after accounting for wind
        """
        directions = ['north', 'south', 'east', 'west']
        
        direction = random.choice(directions)
            
        new_x = x
        new_y = y
            
        if direction == 'north':
            new_y = y + self.speed
        elif direction == 'south':
            new_y = y - self.speed
        elif direction == 'east':
            new_x = x + self.speed
        elif direction == 'west':
            new_x = x - self.speed
            
        new_point = (new_x, new_y)
        
        return new_point
        

class Round(Arrow):
    """
    Creates one round of the archery game using Arrow class. (Ethan D.)

    Attributes:
      speed (int): default wind speed
      direction (str): default wind direction
      x (int): starting x coordinate of arrow
      y (int): starting y coordinate of arrow

    """
    def __init__(self, speed=0, direction="", x=0, y=0):
        arrow = Arrow(0,0,0,0,0,0)
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        
        wind_x = arrow.wind()[0]
        wind_y = arrow.wind()[1]
        
        gravity_y = arrow.gravity()
        
        shot_x = arrow.shot()[0]
        shot_y = arrow.shot()[1]
        
        self.x = wind_x + shot_x
        self.y = wind_y + shot_y + gravity_y
        
        
    def section(self):
        """
        Determines which ring of archery board the arrow hit. (Ethan D.)

        Returns:
          points (int): amount of points assigned for the arrow hit
        """
        sect = ""
        dist = sqrt(self.x**2 + self.y**2)
        self.sect = sect
        if dist < 10:
            sect = "10 ring"
            points = 10
        elif dist < 20 and dist >= 10:
            sect = "9 ring"
            points = 9
        elif dist < 30 and dist >= 20:
            sect = "8 ring"
            points = 8
        elif dist < 40 and dist >= 30:
            sect = "7 ring"
            points = 7
        elif dist < 50 and dist >= 40:
            sect = "6 ring"
            points = 6
        elif dist < 60 and dist >= 50:
            sect = "5 ring"
            points = 5
        elif dist < 70 and dist >= 60:
            sect = "3 ring"
            points = 3
        elif dist < 80 and dist >= 70:
            sect = "3 ring"
            points = 3
        elif dist < 90 and dist >= 80:
            sect = "2 ring"
            points = 2
        elif dist < 100 and dist >= 90:
            sect = "1 ring"
            points = 0
        elif dist > 100:
            sect = "outside of the board"
            points = 0
        
        return points

class Game:
  """
  Creates a game of archery between two players (James)

  Attributes:
    p1_name (str): name of the first player
    p2_name (str): name of the second player
  """
  def __init__(self, p1_name="Player 1", p2_name="Player 2"):
    self.p1_name = p1_name
    self.p2_name = p2_name

    self.p1_name = input("Enter Player 1's name: ")
    self.p2_name = input("Enter Player 2's name: ")

  def game(self):
    """
    Simulates a game of archery between two players.

    Args:
      p1_name (str): The name of the first player
      p2_name (str): The name of the second player
    """

    print(f"{self.p1_name}, enter the angles, power, and bow for your shot: ")
    player1 = Round()
    
    print(f"{self.p2_name}, enter the angles, power, and bow for your shot: ")
    player2 = Round()

    p1_score = player1.section()
    p2_score = player2.section()
    
    if p1_score > p2_score:
      print(f"{self.p1_name} wins with a score of {p1_score} compared to {self.p2_name}'s score of {p2_score}.")
    elif p2_score > p1_score:
      print(f"{self.p2_name} wins with a score of {p2_score} compared to {self.p1_name}'s score of {p1_score}.")
    else:
      print(f"Both players had a score of {p1_score}.")


def main():
    """Creates an object of Game class"""
    game1 = Game()
    game1.game()

if __name__ == "__main__":   
    main()