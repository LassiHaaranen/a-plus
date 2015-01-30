import SimpleHTTPServer, SocketServer
from urlparse import parse_qs

PORT = 8888

def grade_first_ex(submission):
  points = 0
  max_points = 2
  if "hello" in submission.lower():
    points += 1
  if "a+" in submission.lower():
    points += 1
  return (points,max_points)

class ExerciseGrader(SimpleHTTPServer.SimpleHTTPRequestHandler):

  # On GET-request return the exercise 
  def do_GET(self):

    # Simple exercise
    if "/first_exercise/" in self.path:
      response = open('first_exercise.html','r').read()     
      self.send_response(200)
      self.send_header('Content-type','text/html')    
      self.send_header("Content-Length", len(response))
      self.end_headers()
      self.wfile.write(response)
    # Attachment exercise 
    elif "/attachment_exercise/" in self.path:
      response = open('attachment_exercise.html','r').read()     
      self.send_response(200)
      self.send_header('Content-type','text/html')    
      self.send_header("Content-Length", len(response))
      self.end_headers()
      self.wfile.write(response)


  # On POSTs get the answer, grade it and return the results
  def do_POST(self):
    length = int(self.headers.getheader('content-length'))
    postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)

    # Simple exercise
    if "/first_exercise/" in self.path:
      points,max_points = grade_first_ex(postvars['answer'][0])

      response = '<html><head>\n' +\
                  '<meta name="points" value="' + str(points) +'" />\n' +\
                  '<meta name="max-points" value="' + str(max_points) + '" />\n' +\
                  '<meta name="status" value="graded" />\n' + \
                  '</head><body>' +\
                  'Submission succesful,  you got ' + str(points) + '/' +\
                  str(max_points)+ ' points!</body></html>'
      self.send_response(200)
      self.send_header('Content-type','text/html')    
      self.send_header("Content-Length", len(response))
      self.end_headers()
      self.wfile.write(response)

    # Attachment exercise. Note that the file is only stored in A+ 
    elif "/attachment_exercise/" in self.path:
      response = '<html><head>\n' +\
                  '<meta name="points" value="0" />\n' +\
                  '<meta name="max-points" value="100" />\n' +\
                  '<meta name="status" value="waiting" />\n' + \
                  '</head><body>' +\
                  'Submission stored, you will be notified when it is assessed.</body></html>'

      self.send_response(200)
      self.send_header('Content-type','text/html')    
      self.send_header("Content-Length", len(response))
      self.end_headers()
      self.wfile.write(response)

    # Demonstrating hook functionality
    elif "/hook" in self.path:
      print "POST Hook!", self.path
      print "postvars:", postvars
      self.send_response(200)


httpd = SocketServer.TCPServer(("", PORT), ExerciseGrader)
print "Serving at port:", PORT
httpd.serve_forever()
