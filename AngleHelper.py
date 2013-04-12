import subprocess
import math
import os

def run_command( command ):
  workingDirectory = os.getcwd()
  p = subprocess.Popen( command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=workingDirectory )
  lines = []
  for line in p.stdout.readlines():
    lines.append( line )
  return lines

def getAngle():
  takePicture = ['uvccapture', '-m', '-odist.jpg', '-x1920', '-y1080', '-B50', '-S45', '-C35', '-G50' ]
  process = ['./getAngle', 'dist.jpg']
  
  for i in range( 3 ):
    run_command( takePicture )
    results = run_command( process )
    if len( results ) > 0:
      angle = float( results[0] )
      distance = math.fabs( float( results[1] ) )
      distance = ( .9 * distance )
      if math.fabs( angle ) > 25.0:
        if angle < 0:
          angle += 8.0
        else:
          angle -= 8.0
      return ( angle, distance )
  
  return ( None, None )
