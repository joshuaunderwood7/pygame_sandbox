import pygame
from itertools import combinations
from pprint import pprint

class Physical(object):
   def __init__(self):
      super(Physical, self).__init__()
      self.physical_init()

   def physical_init(self):
      self.mass         = 1.0
      self.heading      = pygame.math.Vector2(1, 0)
      self.position     = pygame.math.Vector2(0, 0)
      self.velocity     = pygame.math.Vector2(0, 0)
      self.acceleration = pygame.math.Vector2(0, 0)
      return self

   def set_mass(self, x): self.mass = x

   def set_heading(self, x,y):      self.heading      = pygame.math.Vector2(x, y)
   def set_position(self, x,y):     self.position     = pygame.math.Vector2(x, y)
   def set_velocity (self, x,y):    self.velocity     = pygame.math.Vector2(x, y)
   def set_acceleration(self, x,y): self.acceleration = pygame.math.Vector2(x, y)

   def rotate(self, degrees):
      self.heading = self.heading.rotate(degrees)
      return self

   def move(self, time):
      self.velocity     += time * self.acceleration
      self.position     += time * self.velocity
      return self

   def add_force(self, force):
      self.acceleration += force / self.mass
      return self

   def set_force(self, force):
      self.acceleration = force / self.mass
      return self

   def unset_force(self):
      self.acceleration = pygame.math.Vector2(0, 0)
      return self

   def thrust_on(self, thrust_force):
      force = self.heading * thrust_force / self.mass
      self.set_force(force)
      return self

   def thrust_off(self): return self.unset_force()

   def bounce(self, normal, reflectivity=1.0):
      self.velocity = self.velocity.reflect(normal) * reflectivity

   def debug_print(self):
      print(f"{self.position} @ {self.velocity} | mass : {self.mass}")


FOREVER = float('+inf')
G       = 1
#G       = 6.67e-11
class PhysicsEnvironment(object):
   def __init__(self, global_clock=None, precision=1):
      self.clock     = global_clock
      self.events    = list()
      self.objects   = list()
      self.precision = precision
      self.gravity   = False

   def activate_gravity(self):   self.gravity = True; self.calc_gravity()
   def deactivate_gravity(self): self.gravity = False

   def add_object(self, object):    self.objects.append(object)
   def remove_object(self, object): self.objects.remove(object)

   def run(self):
      if not self.clock:
         print("no clock")
         return self

      time = int(self.clock.get_time() / self.precision)
      for _ in range(time):
         self.span_time(self.precision)
      return self

   def span_time(self, delta_time):

      for obj in self.objects:
         obj.unset_force()

      self.events.sort(key=lambda x: x[0])

      for _, forces in self.events: 
         for f, obj in forces:
            obj.add_force(f)


      for dt, forces in self.events: 
         if dt in [float('NAN'), FOREVER, -FOREVER]: 
            continue # odd sorting choice in Python
         elif dt < delta_time:
            for o in self.objects: o.move(dt)
            delta_time -= dt
            for f, obj in forces:
               obj.add_force(-f)
         else:
            break
      for o in self.objects: o.move(delta_time)

      realevents = list()
      for event in self.events:
         if event[0] == -FOREVER: 
            continue
         elif event[0] > delta_time:
            realevents.append((event[0] - delta_time, event[1]))
         if event[0] in [float('NAN'), -FOREVER]: 
            realevents.append(event)
      self.events = realevents

      if self.gravity: self.calc_gravity()
      
      return self

   def explosion(self, location, pressure, delta_time):
      forces = list()
      for obj in self.objects:
         r_squared = location.distance_squared_to(obj.position)
         vector    = obj.position - location
         force     = vector * pressure / r_squared
         forces.append((force, obj))
      self.events.append((delta_time, forces))
      return self

   def calc_gravity(self):
      forces = list()
      for a,b in combinations(self.objects, 2):
         r_squared = a.position.distance_squared_to(b.position)
         vector    = b.position - a.position
         force     = vector * G * a.mass * b.mass / r_squared
         forces.append(( force, a))
         forces.append((-force, b))
      self.events.append((-FOREVER, forces))
      return self





if __name__=="__main__":

   env = PhysicsEnvironment()
   a = Physical()
   b = Physical()
   c = Physical()

   env.objects.append(a)
   env.objects.append(b)
   env.objects.append(c)

   a.set_position(-3,-3)
   b.set_position( 0, 0)
   c.set_position( 3, 3)

   a.mass = 1
   b.mass = 10
   c.mass = .1

   print('---')
   print(a)
   print(b)
   print(c)
   # env.explosion(pygame.math.Vector2(0,0), 1, 1)
   # env.explosion(pygame.math.Vector2(0,0), 2, 1)

   env.activate_gravity()
   for _ in range(20):
      env.span_time(3)

      print('---')
      pprint([a, b, c])



