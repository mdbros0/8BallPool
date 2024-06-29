import phylib
import sqlite3
import os
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
PHYLIB_DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
STILL_BALL = phylib.PHYLIB_STILL_BALL
ROLLING_BALL = phylib.PHYLIB_ROLLING_BALL
HOLE = phylib.PHYLIB_HOLE
HCUSHION = phylib.PHYLIB_HCUSHION
VCUSHION = phylib.PHYLIB_VCUSHION
FRAME_RATE = 0.01


# add more here
HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""
FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ]

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall


    # add an svg method here
    def svg( self ):
            """
            Returns a string representation of the table that matches
            the phylib_print_table function from A1Test1.c.
            """
            result = ""    # create empty string
            result += """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %  (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y,phylib.PHYLIB_BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
            return result  # return the string
################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__( self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall


    # add an svg method here
    def svg( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" %  (self.obj.rolling_ball.pos.x,self.obj.rolling_ball.pos.y, phylib.PHYLIB_BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return result  # return the string
################################################################################

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__( self, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       None, 
                                       pos, None, None, 
                                       0.0, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = Hole


    # add an svg method here
    def svg( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" %  (self.obj.hole.pos.x, self.obj.hole.pos.y, phylib.PHYLIB_HOLE_RADIUS)
        return result  # return the string
################################################################################

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__( self, y ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       None, 
                                       None, None, None, 
                                       0.0, y )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = HCushion


    # add an svg method here
    def svg( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        if (self.obj.hcushion.y == 0):
            result += """ <rect width="1400" height="25" x="-25" y="-25" fill="darkgreen" />\n"""    # append time
        else:
            result += """ <rect width="1400" height="25" x="-25" y="2700" fill="darkgreen" />\n"""    # append time            
        return result  # return the string
################################################################################

class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__( self, x ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       None, 
                                       None, None, None, 
                                       x, 0.0 )
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = VCushion


    # add an svg method here
    def svg( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        if (self.obj.vcushion.x == 0):
            result += """ <rect width="25" height="2750" x="-25" y="-25" fill="darkgreen" />\n"""   # append time
        else:
            result += """ <rect width="25" height="2750" x="1350" y="-25" fill="darkgreen" />\n"""    # append time       
        return result  # return the string

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self )
        self.current = -1

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other )
        return self

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ] # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1    # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ) 
        if result==None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += "time = %6.1f\n" % self.time    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj)  # append object description
        return result  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self )
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here
    def svg( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += HEADER    # append time
        for object in self: # loop over all objects and number them
            if object == None:
                continue
            result += "%s" % object.svg()  # append object description
        result += FOOTER
        return result  # return the string
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                
                # add ball to table
                new += new_ball;
            
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y ) );
                
                # add ball to table
                new += new_ball;
                
        # return table
        return new;

    def cueBall(self,xvel,yvel):
        for ball in self:
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == 0:
                cue_ball = ball
                xpos = cue_ball.obj.still_ball.pos.x
                ypos = cue_ball.obj.still_ball.pos.y
                
                cue_ball.type = phylib.PHYLIB_ROLLING_BALL
                vel = Coordinate(xvel, yvel)
                speed = phylib.phylib_length(vel)
                acc = Coordinate(xvel * -1.0 / speed * phylib.PHYLIB_DRAG, yvel * -1.0 / speed * phylib.PHYLIB_DRAG)
                
                cue_ball.obj.rolling_ball.pos.x = xpos
                cue_ball.obj.rolling_ball.pos.y = ypos
                cue_ball.obj.rolling_ball.vel.x = xvel
                cue_ball.obj.rolling_ball.vel.y = yvel
                cue_ball.obj.rolling_ball.acc.x = acc.x
                cue_ball.obj.rolling_ball.acc.y = acc.y
                cue_ball.obj.rolling_ball.number = 0

class Database():

    def __init__( self, reset=False ):
        
        if reset:
          if os.path.exists("phylib.db"):
                os.remove("phylib.db")
            
        self.conn = sqlite3.connect("phylib.db")
        self.createDB()

    def createDB( self ):
        cur = self.conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS Ball
                    (
                        BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        BALLNO INTEGER NOT NULL,
                        XPOS FLOAT NOT NULL,
                        YPOS FLOAT NOT NULL,
                        XVEL FLOAT,
                        YVEL FLOAT
                    );
                    """)


        cur.execute("""CREATE TABLE IF NOT EXISTS TTable
                    (
                        TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        TIME FLOAT NOT NULL
                    );
                    """)


        cur.execute("""CREATE TABLE IF NOT EXISTS BallTable (
                        BALLID INTEGER NOT NULL,
                        TABLEID INTEGER NOT NULL,
                        FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID)
                    );
                    """)

        
        cur.execute("""CREATE TABLE IF NOT EXISTS Shot
                    (
                        SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        PLAYERID INTEGER NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                    );
                    """)

        cur.execute("""CREATE TABLE IF NOT EXISTS TableShot
                    (
                        TABLEID INTEGER NOT NULL,
                        SHOTID INTEGER NOT NULL,
                        FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                        FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID)
                    );
                    """)
        
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Game
                    (
                        GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMENAME VARCHAR(64)  NOT NULL
                    );
                    """)
        
        
        cur.execute("""CREATE TABLE IF NOT EXISTS Player
                    (
                        PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        GAMEID INTEGER NOT NULL,
                        PLAYERNAME VARCHAR(64) NOT NULL,
                        FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID)
                    );
                    """)       
        cur.close()
        self.conn.commit()
        
    def readTable( self, tableID ):
        cur = self.conn.cursor()
        
        cur.execute("""
                        SELECT Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME
                        FROM Ball
                        INNER JOIN BallTable ON Ball.BallID = BallTable.BALLID
                        INNER JOIN TTable ON BallTable.TableID = TTable.TABLEID
                        WHERE TTable.TABLEID = ?;
                    """, (tableID + 1,))
        
        rows = cur.fetchall()
        
        if not rows:
            cur.close()
            return None

        table = Table()
        
        for row in rows:
            ballNumber, xPos, yPos, xVel, yVel,time = row
            pos = Coordinate(xPos, yPos)
            
            if xVel == 0 and yVel == 0:
                ball = StillBall(ballNumber, pos)
        
            else:
                vel = Coordinate(xVel, yVel)            
                speed = phylib.phylib_length(vel)
                acc = Coordinate(vel.x * -1.0 / speed * phylib.PHYLIB_DRAG, vel.y * -1.0  / speed * phylib.PHYLIB_DRAG)
                ball = RollingBall(ballNumber, pos, vel, acc)
                
            table += ball
            
        table.time = time
        cur.close()
        self.conn.commit()
        
        return table
        
    def writeTable( self, table ):
        cur = self.conn.cursor()
            
        cur.execute('INSERT INTO TTable (TIME) VALUES (?);', (table.time,))
        
        tableID = cur.lastrowid
        
        for ball in table:
            if isinstance(ball, StillBall):
                cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, 0, 0);", (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
            elif isinstance(ball, RollingBall):
                cur.execute("INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?, ?, ?, ?, ?);", (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y, ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
            else:
                continue
            
            ballID = cur.lastrowid
            
            cur.execute("INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?);", (ballID, tableID))
                
        self.conn.commit()
        cur.close()       
        
        return tableID -1

    def close( self ):
        self.conn.commit()
        self.conn.close()
        
    def setGame(self, gameName, player1Name, player2Name):
        cur = self.conn.cursor()
        
        cur.execute("""
            INSERT INTO Game (GAMENAME) VALUES (?);
        """, (gameName,))
        
        gameID = cur.lastrowid
        
        cur.execute("""
            INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?), (?, ?);
        """, (gameID, player1Name, gameID, player2Name))
        
        self.conn.commit()
        cur.close()
        
        return gameID

    def newShot(self, playerID, gameID):
        cur = self.conn.cursor()
        
        cur.execute("""
            INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?);
        """, (playerID, gameID))
        
        shotID = cur.lastrowid
        self.conn.commit()
        cur.close()
        return shotID
       
class Game:
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        
        db = Database()
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            self.gameID = gameID + 1
            game_details = db.getGame(self.gameID)
            
            self.gameName = game_details['gameName']
            self.player1Name = game_details['player1Name']
            self.player2Name = game_details['player2Name']
            
            self.table = db.readTable(self.gameID)
            
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            
            self.gameID = db.setGame(self.gameName, self.player1Name, self.player2Name)
            self.table = Table()
            
        else:
            raise TypeError("Invalid combination of arguments provided")

        db.close()
        
    def shoot(self, gameName, playerName, table, xvel, yvel,svg):
        db = Database();
        cur = db.conn.cursor()

        cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ? AND GAMEID = ?;", (playerName, self.gameID))
        playerID = cur.fetchone()
        playerID = playerID[0]


        shotID = Database().newShot(playerID, self.gameID)
        table.cueBall(xvel,yvel)
                
        while table:
            start = table.time
            newTable = table.segment()
            if newTable is None:
                tableID = db.writeTable(table)
                cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) values (?, ?);""",(tableID + 1, shotID))
                svg.append( table.svg() );                
                break
            
            timeElapsed = newTable.time - start
            segmentLength = int(timeElapsed / FRAME_RATE)
            for i in range(segmentLength):
                t = i * FRAME_RATE
                new = table.roll(t)
                new.time = start + t
                tableID = db.writeTable(new)
                cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) values (?, ?);""",(tableID + 1, shotID))
                svg.append( new.svg() );
            table = newTable
            start = newTable.time
            
        cur.close()
        db.close()
        
        return tableID
        # return svg
    
