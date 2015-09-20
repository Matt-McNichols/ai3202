===
Assignment 2:
---
The Equation:
*  The second huristic equation I chose was a pythagorean distance.
*  The equation used to caculte the H score is H=sqrt{(x^2)+(y^2)};
*  To implament this in python, I imported the math library
*  I then added to the manhatton distance functon which calculates x and y
   abs(x=current_x-end_x)
   abs(y=current_y-end_y)
*  I then used math.sqrt() function to calculate the sum of x^2 and y^2

---
The Motivation:
* I chose this H equation because I thought it was a more accurate
  guess than the manhattan value.

* This H value takes into account the horses ability to travel on diagnals

---
The Result:
* For both worlds the the distance, and number of nodes were the same when using either huristic equation.
* For world 1 the paths were the same using either huristic equation.
* For world 2 the paths were slightly different.  Although they used the same number of nodes and the
  total distance was the same, when running the pythagorean H, a different route was chosen as the shortest.
* The horse traveled diagnally the same number of times on both paths

