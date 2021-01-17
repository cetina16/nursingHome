DROP TABLE IF EXISTS Diseaseowners
DROP TABLE IF EXISTS Resident
DROP TABLE IF EXISTS Nurse
DROP TABLE IF EXISTS Disease
DROP TABLE IF EXISTS Doctor
DROP TABLE IF EXISTS Nursinghome

CREATE TABLE IF NOT EXISTS Nursinghome(
    homeid INT AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    city VARCHAR(40) NOT NULL,
    type VARCHAR(40) NOT NULL,
    address VARCHAR(40) NOT NULL,
    tel VARCHAR(40) NOT NULL,
    PRIMARY KEY (homeid)
)

CREATE TABLE IF NOT EXISTS Doctor(
    doctorid INT AUTO_INCREMENT,
    email VARCHAR(40) UNIQUE,
    name VARCHAR (40) NOT NULL ,
    password VARCHAR (100)  NOT NULL ,
    nursinghomeid INT,
    FOREIGN KEY (nursinghomeid)  
    REFERENCES Nursinghome(homeid) 
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (doctorid)
)

CREATE TABLE IF NOT EXISTS Nurse(nurseid INT AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    capacity INT NOT NULL,
    capacity_exist INT,
    type VARCHAR(40) NOT NULL,
    address VARCHAR(90) NOT NULL,
    tel VARCHAR(40) NOT NULL,
    nursinghomeid  INT NOT NULL,
    FOREIGN KEY (nursinghomeid) 
    REFERENCES Nursinghome(homeid)
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    PRIMARY KEY (nurseid)
)

CREATE TABLE IF NOT EXISTS Disease(
    diseaseid INT AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    risklevel INT NOT NULL,
    period VARCHAR(40) NOT NULL,
    homeid INT NOT NULL,
    FOREIGN KEY (homeid) 
    REFERENCES Nursinghome(homeid)
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    PRIMARY KEY (diseaseid)
)

CREATE TABLE IF NOT EXISTS Resident(
    residentid INT AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    age INT NOT NULL,
    bedridden VARCHAR(40) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    tel VARCHAR(40) NOT NULL,
    nurseid  INT NOT NULL,
    FOREIGN KEY (nurseid) 
    REFERENCES Nurse(nurseid)
    ON DELETE RESTRICT 
    ON UPDATE CASCADE,
    PRIMARY KEY (residentid)
)

CREATE TABLE IF NOT EXISTS DiseaseOwners(
    residentid INT NOT NULL,
    diseaseid INT NOT NULL,
    FOREIGN KEY (residentid)	
    REFERENCES Resident(residentid)
    ON DELETE CASCADE 
    ON UPDATE CASCADE,
    FOREIGN KEY (diseaseid)	
    REFERENCES Disease (diseaseid)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
    startdate DATE NOT NULL,
    enddate DATE,
    note VARCHAR(100) NOT NULL,
    PRIMARY KEY(residentid , diseaseid)
)