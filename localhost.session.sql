 CREATE TABLE users(  
     id VARCHAR(255) NOT NULL PRIMARY KEY,
     create_time DATETIME COMMENT 'Create Time',
     name VARCHAR(255),
     father_name VARCHAR(255),
     dob DATETIME,
     id_type VARCHAR(255) NOT NULL,
     embedding BLOB
 )
