import json
import psycopg2


# These insertions work assuming that the Yelp data is in the same directory


def cleanStr4SQL(s):  # Given def to ensure strings are SQL ready
    return s.replace("'", "`").replace("\n", " ")


def int2BoolStr (value):  # Given def to turn a 0 into a false
    if value == 0:
        return 'False'
    else:
        return 'True'


def insert2BusinessTable():  # Parsing and insertion of JSON file entries into the DB - Business
    # Reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            # INSERT statement for the Business table from the JSON
            sql_str = "INSERT INTO Business (business_id, name, neighborhood, address, city, state, postal_code, latitude, longitude, stars, is_open, review_count, numCheckins, reviewrating) " \
                      "VALUES ('{business_id}', '{name}', '{neighborhood}', '{address}', '{city}', '{state}', '{postal_code}', {latitude}, {longitude}, {stars}, {is_open}, {review_count}, 0, 0.0)".format(
                        business_id=cleanStr4SQL(data['business_id']),
                        name=cleanStr4SQL(data["name"]),
                        neighborhood=cleanStr4SQL(data.get("neighborhood", "")),
                        address=cleanStr4SQL(data["address"]),
                        city=cleanStr4SQL(data["city"]),
                        state=cleanStr4SQL(data["state"]),
                        postal_code=cleanStr4SQL(data["postal_code"]),
                        latitude=data["latitude"],
                        longitude=data["longitude"],
                        stars=data["stars"],
                        is_open=int2BoolStr(data["is_open"]),
                        review_count=data["review_count"]
                      )
            try:
                cur.execute(sql_str)
            except Exception as e:
                print("Insert to Business table failed!")
                conn.rollback()
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2UsersTable():  # Parsing and insertion of JSON file entries into the DB - Users
    # Reading the JSON file
    with open('./yelp_user.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            # INSERT statement for the Users table from the JSON
            sql_str = "INSERT INTO Users (user_id, name, fans, average_stars, review_count, yelping_since, funny, useful, cool) " \
                      "VALUES ('{user_id}', '{name}', {fans}, {average_stars}, {review_count}, '{yelping_since}', {funny}, {useful}, {cool})".format(
                        user_id=cleanStr4SQL(data['user_id']),
                        name=cleanStr4SQL(data["name"]),
                        fans=data["fans"],
                        average_stars=data["average_stars"],
                        review_count=data["review_count"],
                        yelping_since=data["yelping_since"],
                        funny=data["funny"],
                        useful=data["useful"],
                        cool=data["cool"]
                      )
            try:
                cur.execute(sql_str)
            except Exception as e:
                print("Insert to Users table failed!", e)
                conn.rollback()  # Rollback in case of error
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2ReviewTable():  # Parsing and insertion of JSON file entries into the DB - Review
    # Reading the JSON file
    with open('./yelp_review.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            # INSERT statement for the Review table from the JSON
            sql_str = "INSERT INTO Review (review_id, user_id, business_id, date, stars, text, funny, useful, cool) " \
                      "VALUES ('{review_id}', '{user_id}', '{business_id}', '{date}', {stars}, '{text}', {funny}, {useful}, {cool})".format(
                        review_id=cleanStr4SQL(data['review_id']),
                        user_id=cleanStr4SQL(data['user_id']),
                        business_id=cleanStr4SQL(data['business_id']),
                        date=data['date'],
                        stars=data['stars'],
                        text=cleanStr4SQL(data["text"]),
                        funny=data['funny'],
                        useful=data['useful'],
                        cool=data['cool']
                      )
            try:
                cur.execute(sql_str)
            except Exception as e:
                print("Insert to Review table failed!", e)
                conn.rollback()  # Rollback in case of error
            conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2UserFriendTable():  # Parsing and insertion of JSON file entries into the DB - UserFriend
    # Reading the JSON file
    with open('./yelp_user.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            user_id = cleanStr4SQL(data['user_id'])
            friends = data["friends"]

            for friend_id in friends:
                # INSERT statement for the UserFriends table from the JSON
                sql_str = "INSERT INTO UserFriend (user_id, friend_id) " \
                          "VALUES ('{user_id}', '{friend_id}')".format(
                            user_id=user_id,
                            friend_id=cleanStr4SQL(friend_id)
                          )
                try:
                    cur.execute(sql_str)
                except Exception as e:
                    print("Insert to UserFriend table failed!", e)
                    conn.rollback()
                conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2CheckInTable():  # Parsing and insertion of JSON file entries into the DB - CheckIn
    # Reading the JSON file
    with open('./yelp_checkin.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            checkin_info = data["time"]

            for day, times in checkin_info.items():
                for time, count in times.items():
                    # INSERT statement for the CheckIn table from the JSON
                    sql_str = "INSERT INTO CheckIn (business_id, checkInDay, checkInTime, checkInCount) " \
                              "VALUES ('{business_id}', '{day}', '{time}', {count})".format(
                                business_id=business_id,
                                day=day,
                                time=time,
                                count=count
                              )
                    try:
                        cur.execute(sql_str)
                    except Exception as e:
                        print("Insert to CheckIn table failed!", e)
                        conn.rollback()
                    conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2BusinessCategoriesTable():  # Parsing and insertion of JSON file entries into the DB - BusinessCategories
    # Reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)
            business_id = cleanStr4SQL(data['business_id'])
            categories = data["categories"]

            for category in categories:
                # INSERT statement for the BusinessCategories table from the JSON
                sql_str = "INSERT INTO BusinessCategories (business_id, categoryName) " \
                          "VALUES ('{business_id}', '{category}')".format(
                            business_id=business_id,
                            category=cleanStr4SQL(category)
                          )
                try:
                    cur.execute(sql_str)
                except Exception as e:
                    print("Insert to BusinessCategories table failed!", e)
                    conn.rollback()
                conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2BusinessHoursTable():  # Parsing and insertion of JSON file entries into the DB - BusinessHours
    # Reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            business_id = cleanStr4SQL(data['business_id'])
            hours = data.get("hours", {})

            for day, operating_hours in hours.items():
                # INSERT statement for the BusinessHours table from the JSON
                sql_str = "INSERT INTO BusinessHours (business_id, dayOfWeek, operatingHours) " \
                          "VALUES ('{business_id}', '{day}', '{operating_hours}')".format(
                            business_id=business_id,
                            day=day,
                            operating_hours=cleanStr4SQL(operating_hours)
                          )
                try:
                    cur.execute(sql_str)
                except Exception as e:
                    print("Insert to BusinessHours table failed!", e)
                    conn.rollback()
                conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def insert2BusinessAttributesTable():  # Parsing and insertion of JSON file entries into the DB - BusinessAttributes
    # Reading the JSON file
    with open('./yelp_business.JSON', 'r') as f:
        line = f.readline()
        count_line = 0

        # Connect to yelpdb database on postgres server using psycopg2
        try:
            conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
        except:
            print('Unable to connect to the database!')
        cur = conn.cursor()

        while line:
            data = json.loads(line)

            business_id = cleanStr4SQL(data['business_id'])
            attributes = data.get("attributes", {})

            # Iterate through each attribute in the dict
            for attr_name, attr_value in attributes.items():
                if isinstance(attr_value, dict):
                    # Process each sub-attribute if the attribute value is a dict
                    for sub_attr_name, sub_attr_value in attr_value.items():
                        if str(sub_attr_value) not in ['False', 'no']:
                            # Use the full attribute name for nested attributes
                            full_attr_name = f"{attr_name}.{sub_attr_name}"
                            # INSERT statement for the BusinessAttributes table from the JSON
                            sql_str = "INSERT INTO BusinessAttributes (business_id, attributeName, attributeValue) " \
                                      "VALUES ('{business_id}', '{attributeName}', '{attributeValue}')".format(
                                        business_id=business_id,
                                        attributeName=cleanStr4SQL(full_attr_name),
                                        attributeValue=str(sub_attr_value)
                                      )
                            try:
                                cur.execute(sql_str)
                            except Exception as e:
                                print("Insert to BusinessAttributes table failed!", e)
                                conn.rollback()
                            conn.commit()
                # Insertion for non-dict attribute values
                else:
                    if str(attr_value) not in ['False', 'no']:
                        sql_str = "INSERT INTO BusinessAttributes (business_id, attributeName, attributeValue) " \
                                  "VALUES ('{business_id}', '{attributeName}', '{attributeValue}')".format(
                                    business_id=business_id,
                                    attributeName=cleanStr4SQL(attr_name),
                                    attributeValue=str(attr_value)
                                  )
                        try:
                            cur.execute(sql_str)
                        except Exception as e:
                            print("Insert to BusinessAttributes table failed!", e)
                            conn.rollback()
                        conn.commit()

            line = f.readline()
            count_line += 1

        cur.close()
        conn.close()

    print(count_line)
    f.close()


def updateBusinessTable():  # Executing SQL queries to update the Business table
    # Connect to yelpdb database on postgres server using psycopg2
    try:
        conn = psycopg2.connect("dbname='yourdbhere' user='postgres' host='localhost' password='admin'")
    except:
        print('Unable to connect to the database!')
        return

    cur = conn.cursor()

    try:
        # Creating a temp table to hold computed values
        cur.execute("""
            CREATE TEMP TABLE BusinessTemp AS
            SELECT Business.business_id, COALESCE(SUM(CheckIn.checkInCount), 0) AS numCheckins, COALESCE(COUNT(DISTINCT Review.review_id), 0) AS reviewcount, COALESCE(ROUND(AVG(Review.stars), 1), 0) AS reviewrating
            FROM Business LEFT JOIN CheckIn ON Business.business_id = CheckIn.business_id LEFT JOIN Review ON Business.business_id = Review.business_id
            GROUP BY Business.business_id;
        """)

        # Updating the Business table using the temp table
        cur.execute("""
            UPDATE Business
            SET numCheckins = BusinessTemp.numCheckins, review_count = BusinessTemp.reviewcount, reviewrating = BusinessTemp.reviewrating
            FROM BusinessTemp
            WHERE Business.business_id = BusinessTemp.business_id;
        """)

        # Getting rid of the temp table
        cur.execute("DROP TABLE BusinessTemp;")

        conn.commit()

    except Exception as e:
        print("Error updating Business table:", e)
        conn.rollback()

    cur.close()
    conn.close()


#insert2BusinessTable()
#insert2UsersTable()
#insert2ReviewTable()
#insert2UserFriendTable()
#insert2CheckInTable()
#insert2BusinessCategoriesTable()
#insert2BusinessHoursTable()
#insert2BusinessAttributesTable()
updateBusinessTable()
