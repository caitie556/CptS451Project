CREATE TABLE IF NOT EXISTS Business (
    business_id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    neighborhood VARCHAR(100),
    address VARCHAR(100),
    city VARCHAR(100),
    state CHAR(2),
    postal_code CHAR(5),
    latitude FLOAT,
    longitude FLOAT,
    stars FLOAT DEFAULT 0.0,
    is_open BOOLEAN,
    review_count INT DEFAULT 0,
    numCheckins INT DEFAULT 0,
    reviewrating FLOAT DEFAULT 0.0
); 

CREATE TABLE IF NOT EXISTS Users (
    user_id VARCHAR(100) PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    fans INT DEFAULT 0,
    average_stars FLOAT DEFAULT 0.0,
    review_count INT DEFAULT 0,
    yelping_since DATE,
    funny INT DEFAULT 0,
    useful INT DEFAULT 0,
    cool INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Review (
    review_id VARCHAR(100),
    user_id VARCHAR(100),
    business_id VARCHAR(100),
    date DATE,
    stars INT DEFAULT 0,
    text VARCHAR(1200),
    funny INT DEFAULT 0,
    useful INT DEFAULT 0,
    cool INT DEFAULT 0,
    PRIMARY KEY (review_id, user_id, business_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS UserFriend(
    user_id VARCHAR(100),
    friend_id VARCHAR(100),
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (friend_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS CheckIn(
    business_id VARCHAR(100),
    checkInDay VARCHAR(20),
    checkInTime VARCHAR(10),
    checkInCount INT DEFAULT 0,
    PRIMARY KEY (business_id, checkInDay, checkInTime),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS BusinessCategories(
    business_id VARCHAR(100),
    categoryName VARCHAR(50),
    PRIMARY KEY (business_id, categoryName),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS BusinessHours(
    business_id VARCHAR(100),
    dayOfWeek VARCHAR(20),
    operatingHours VARCHAR(30),
    PRIMARY KEY (business_id, dayOfWeek),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS BusinessAttributes(
    business_id VARCHAR(100),
    attributeName VARCHAR(50),
    attributeValue VARCHAR(30),
    PRIMARY KEY (business_id, attributeName),
    FOREIGN KEY (business_id) REFERENCES Business(business_id)
);

CREATE TABLE IF NOT EXISTS zipcodeData (
    zipcode CHAR(5) PRIMARY KEY,
    medianIncome INT,
    meanIncome INT,
    population INT
);