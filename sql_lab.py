'''
This is the framework you'll fill out for this assignment.
Each question on the lab corresponds to one of the functions in the LabSuite class.
You should fill out each function so that it returns the desired results from the database.

Because changes to the framework can interfere with the autograding tests,
you shouldn't modify any other parts of the framework beyond those indicated.
'''

import sqlite3

class LabSuite(object):

    def __init__(self):
        """Initializes the LabSuite object.      
        """
        self.db_name = './assignment.db'

    def connect(self):
        """Establishes a connection to the database.

        Returns a SQLite connection object to the database defined in self.db_name.

        Returns:
            An open sqlite3.Connection object.
        """
        conn = sqlite3.connect(self.db_name)
        return conn    
    
    def five_year_rangers(self):
        """Returns the first and last names of all rangers who have worked for exactly five years,
        sorted alphabetically by last name, then first name.
        Don't modify this function - it's already filled in for you as an example.
        If your submission is working correctly, the test for this one
        should work without you changing anything.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # You'll write your SQL queries as the string argument passed to cursor.execute(),
        # like so:
        cursor.execute("""SELECT firstname, lastname
                          FROM Ranger
                          WHERE years_worked = 5
                          ORDER BY lastname, firstname;""")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_overlooks(self):
        """Returns the names of all overlook stations, sorted alphabetically.
        A station is an overlook station if its name begins with the word "Overlook."
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                        SELECT name
                        FROM Station s
                        WHERE name LIKE "Overlook%"
                        ORDER BY name ASC
                         """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_station_elevation(self):
        """Returns the names of all stations and their elevations in miles, 
        sorted alphabetically by station name.
        Note that in the database, elevation is stored in feet.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                    SELECT name, elevation / 5280.0
                       FROM Station
                       ORDER BY name ASC """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_average_deer(self):
        """Returns the average number of deer spotted per deer sighting.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute("""
                    SELECT AVG(number)
                       FROM Sighting
                       WHERE species = "Deer" """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_station_seven_animals(self):
        """Returns the species and total number of each animal that has been
           sighted at the station with station ID 7, sorted alphabetically by 
           species name.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute(""" 
                       SELECT si.species, SUM(si.number)
                       FROM Sighting si
                       JOIN Shift sh ON si.shift_id = sh.shift_id
                       JOIN Station st on sh.station_id = st.station_id
                       WHERE st.station_id = 7
                       GROUP BY si.species
                       ORDER BY si.species ASC""")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_birdwatchers(self):
        """Returns the first and last names of all rangers who have seen at least one eagle
        and at least one falcon, sorted alphabetically by last name, then first name.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute(""" 
                       SELECT r.firstname, r.lastname
                       FROM Ranger r
                       JOIN Shift sh ON r.ranger_id = sh.ranger_id
                       JOIN Sighting si ON si.shift_id = sh.shift_id
                       WHERE si.species = "Eagle"
                       INTERSECT
                       SELECT r.firstname, r.lastname
                       FROM Ranger r
                       JOIN Shift sh ON r.ranger_id = sh.ranger_id
                       JOIN Sighting si ON si.shift_id = sh.shift_id
                       WHERE si.species = "Falcon"
                       ORDER BY lastname ASC, firstname ASC """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_distant_stations(self):
        """Returns the names of all stations that are further along the trail
        than the station with station ID 4, sorted by trail distance in increasing order.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute(""" 
                       SELECT name, trail_distance
                       FROM Station
                       WHERE trail_distance > (SELECT trail_distance
                                                FROM Station
                                                WHERE station_id = 4)
                       ORDER BY trail_distance ASC""")
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_wild_stations(self):
        """Returns the name of each station and the number of unique species that
        have been spotted there for each station where at least six unique species
        have been spotted. Results should be sorted alphabetically by station name.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute(""" 
                       SELECT name, COUNT(DISTINCT si.species) AS num_distinct
                       FROM Station st
                       JOIN Shift sh ON sh.station_id = st.station_id
                       JOIN Sighting si ON si.shift_id = sh.shift_id
                       GROUP BY st.station_id
                       HAVING num_distinct > 5
                       ORDER BY name
                       """)
        results = cursor.fetchall()
        conn.close()
        return results
    
    def find_first_worker(self):
        """Returns the first and last name of the ranger who worked the 
        earliest recorded shift in the database.
        """
        conn = self.connect()
        cursor = conn.cursor()
        # Write your SQL query below. 
        # You shouldn't need to modify any other part of this function.
        cursor.execute(""" 
                       SELECT firstname, lastname
                       FROM (SELECT firstname, lastname, start_time
                            FROM Ranger r
                            JOIN Shift s ON r.ranger_id = s.ranger_id
                            EXCEPT
                            SELECT firstname, lastname, start_time
                            FROM Ranger r
                            JOIN Shift s ON r.ranger_id = s.ranger_id
                            WHERE s.start_time > (SELECT MIN(start_time) FROM Shift))""")
        results = cursor.fetchall()
        conn.close()
        return results