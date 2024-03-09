CREATE TABLE Business (
    businessID VARCHAR(30) PRIMARY KEY,
    businessName VARCHAR(100) NOT NULL,
    businessAddress VARCHAR(100),
    city VARCHAR(100),
    businessState CHAR(2),
    postalCode CHAR(5),
    latitude FLOAT,
    longitude FLOAT,
    stars FLOAT DEFAULT 0.0,
    isOpen BOOLEAN,
    reviewCount INT DEFAULT 0
); 

CREATE TABLE User (
    userID VARCHAR(30) PRIMARY KEY,
    userName VARCHAR (100) NOT NULL,
    fans INT DEFAULT 0,
    averageStars FLOAT DEFAULT 0.0,
    userReviewCount INT DEFAULT 0,
    yelpingSince DATE,
    funnyVotes INT DEFAULT 0,
    usefulVotes INT DEFAULT 0,
    coolVotes INT DEFAULT 0
);

CREATE TABLE Review (
    reviewID VARCHAR(30) PRIMARY KEY,
    userID VARCHAR(30) PRIMARY KEY,
    businessID VARCHAR(30) PRIMARY KEY,
    reviewDate DATE,
    starsScore FLOAT DEFAULT 0.0,
    funnyReview INT DEFAULT 0,
    usefulReview INT DEFAULT 0,
    coolReview INT DEFAULT 0,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

CREATE TABLE UserFriend(
    userID VARCHAR(30) PRIMARY KEY,
    friendID VARCHAR(30) PRIMARY KEY,
    FOREIGN KEY (userID) REFERENCES Users(userID),
    FOREIGN KEY (friendID) REFERENCES Users(userID)
);

CREATE TABLE CheckIn(
    businessID VARCHAR(30) PRIMARY KEY,
    checkInDay DATE PRIMARY KEY,
    checkInTime TIME PRIMARY KEY,
    checkInCount INT DEFAULT 0,
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

CREATE TABLE BusinessCategories(
    businessID VARCHAR(30) PRIMARY KEY,
    categoryName VARCHAR(50) PRIMARY KEY,
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

CREATE TABLE BusinessHours(
    businessID VARCHAR(30) PRIMARY KEY,
    dayOfWeek VARCHAR(20),
    operatingHours VARCHAR(30),
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);

CREATE TABLE BusinessAttributes(
    businessID VARCHAR(30) PRIMARY KEY,
    attributeName VARCHAR(50) PRIMARY KEY,
    attributeValue VARCHAR(30),
    FOREIGN KEY (businessID) REFERENCES Business(businessID)
);