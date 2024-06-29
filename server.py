import sys 
import Physics
import math
import random
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl

svg_json = None
TableID = 0
player1name = None
player2name = None
gamename = None
game = None
turn = None

class MyHandler( BaseHTTPRequestHandler ):
    velocity_data = {'x':1, 'y':1}
    svg = []
    db = Physics.Database(True)
    
    nudge = lambda: random.uniform(-1.5, 1.5)
    table = Physics.Table()
    # Add balls to the table
    pos1 = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0, Physics.TABLE_WIDTH / 2.0)
    sb1 = Physics.StillBall(1, pos1)
    table += sb1


    pos2 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER + 10.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) + nudge()
    )
    sb2 = Physics.StillBall(2, pos2)
    table += sb2

    pos3 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 10.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER + 4.0) + nudge()
    )
    sb3 = Physics.StillBall(3, pos3)
    table += sb3

    pos4 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - ((Physics.BALL_DIAMETER * 2) + 10.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 2)+ 6.0) + nudge()
    )
    sb4 = Physics.StillBall(4, pos4)
    table += sb4

    pos5 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + ((Physics.BALL_DIAMETER * 2) + 10.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 2)+ 6.0) + nudge()
    )
    sb5 = Physics.StillBall(5, pos5)
    table += sb5

    pos6 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0,
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 2)+ 10.0) + nudge()
    )
    sb6 = Physics.StillBall(8, pos6)
    table += sb6

    pos7 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER + 15.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 10.0) + nudge()
    )
    sb7 = Physics.StillBall(6, pos7)
    table += sb7

    pos8 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER + 15.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 10.0) + nudge()
    )
    sb8 = Physics.StillBall(7, pos8)
    table += sb8

    pos9 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER * 3 + 20.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 10.0) + nudge()
    )
    sb9 = Physics.StillBall(9, pos9)
    table += sb9

    pos10 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER * 3 + 20.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 3 + 10.0) + nudge()
    )
    sb10 = Physics.StillBall(10, pos10)
    table += sb10

    pos11 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0,
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * ((Physics.BALL_DIAMETER * 4)+ 15.0) + nudge()
    )
    sb11 = Physics.StillBall(11, pos11)
    table += sb11

    pos12 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER * 2 + 15.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 15.0) + nudge()
    )
    sb12 = Physics.StillBall(12, pos12)
    table += sb12

    pos13 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER * 2 + 15.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 15.0) + nudge()
    )
    sb13 = Physics.StillBall(13, pos13)
    table += sb13

    pos14 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 - (Physics.BALL_DIAMETER * 4 + 20.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 15.0) + nudge()
    )
    sb14 = Physics.StillBall(14, pos14)
    table += sb14

    pos15 = Physics.Coordinate(
        Physics.TABLE_WIDTH / 2.0 + (Physics.BALL_DIAMETER * 4 + 20.0) / 2.0 + nudge(),
        Physics.TABLE_WIDTH / 2.0 - math.sqrt(3.0) / 2.0 * (Physics.BALL_DIAMETER * 4 + 15.0) + nudge()
    )
    sb15 = Physics.StillBall(15, pos15)
    table += sb15

    pos0 = Physics.Coordinate(Physics.TABLE_WIDTH / 2.0 + random.uniform(-3.0, 3.0),
                                        Physics.TABLE_LENGTH - Physics.TABLE_WIDTH / 2.0)
    sb0 = Physics.StillBall(0, pos0)
    table += sb0
          
    db.writeTable(table)  

    def do_GET(self):
        global svg_json,turn
        parsed  = urlparse( self.path )
        
        if parsed.path in [ "/get_svg" ]:
            if svg_json is not None:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(svg_json.encode('utf-8'))
            else:
                # Send a response indicating that the SVG data is not available yet
                self.send_response(200)  # OK to use 200 if you're sending a meaningful message, or consider 404/204 as appropriate
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_message = json.dumps({"error": "SVG data not available yet"})
                self.wfile.write(response_message.encode('utf-8'))
                
        elif parsed.path in [ "/server_message" ]:
            """Indicate whose turn it is."""
            content = f"{turn}'s turn"
            self.send_response(200)
            self.send_header('Content-type', "text/html")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        
        elif parsed.path in [ "/playerNames.html" ]:
            # global player1name, player2name
            # Serve the display.html page as is, without needing to modify it for the SVG data
            fp = open( '.'+parsed.path )
            content = fp.read()

            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
            
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )


    def do_POST(self):
        global svg_json, TableID,game,player1name,player2name,turn
        parsed  = urlparse( self.path )
        self.svg = []
        
        if parsed.path in [ "/velocity.html" ]:
            print("hahaha")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            velocity_data = json.loads(post_data.decode('utf-8'))  
            turn = player2name if turn == player1name else player1name  # Toggle between player1 and player2
            print(turn)
            print(TableID)
            self.table = self.db.readTable(TableID)
            TableID = game.shoot( "Game 01", turn, self.table, velocity_data['x'],velocity_data['y'],self.svg );
            self.table = self.db.readTable(TableID)
            print(TableID)
            
            svg_json = json.dumps(self.svg)  # Convert Python list to JSON string
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_message = json.dumps({"message": "Velocity data received successfully"})
            self.wfile.write(response_message.encode('utf-8'))
            
        elif parsed.path in [ "/display.html" ]:
            # Serve the display.html page as is, without needing to modify it for the SVG data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = dict(parse_qsl(post_data))

            # Extract player names from form data
            player1name = form_data.get('player1', 'Player 1')
            player2name = form_data.get('player2', 'Player 2')

            game = Physics.Game( gameName="Game 01", player1Name=player1name, player2Name=player2name );

            with open("./index1.html") as fp:
                content = fp.read()
            
            self.send_response(200)  # OK
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(content))
            self.end_headers()
            self.wfile.write(bytes(content, "utf-8"))
        # elif parsed.path in [ "/display.html" ]:

        #     # # get data send as Multipart FormData (MIME format)
        #     # form = cgi.FieldStorage( fp=self.rfile,
        #     #                          headers=self.headers,
        #     #                          environ = { "REQUEST_METHOD": "POST",
        #     #                                      "CONTENT_TYPE": 
        #     #                                        self.headers["Content-Type"],
        #     #                                    } 
        #     #                        )
            
        #     # vel = Physics.Coordinate(float(velocity_data.x),float(velocity_data.y))
        #     # speed = phylib.phylib_length(vel)
        #     # acc = Physics.Coordinate(vel.x * -1.0 / speed * phylib.PHYLIB_DRAG, vel.y * -1.0  / speed * phylib.PHYLIB_DRAG)


        #     fp = open( "./index1.html")
        #     content = fp.read().replace('{{ svg_json }}', self.svg_json)

        #     # fp = open( "./index1.html")
        #     # content = fp.read()
        #     fp.close()
            
        #     self.send_response( 200 ) # OK
        #     self.send_header( "Content-type", "text/html" )
        #     self.send_header( "Content-length", len( content ) )
        #     self.end_headers()
        #     self.wfile.write( bytes( content, "utf-8" ) )

        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )
                    
if __name__ == "__main__":
    httpd = HTTPServer( ( "localhost", int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()