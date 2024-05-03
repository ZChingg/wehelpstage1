## Task2: Create database and table in your MySQL server
* Create a new database named website.
    ```sql
    CREATE DATABASE website;
    ```
    ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task2-1.png?raw=true)

* Create a new table named member, in the website database.
  ```sql
  CREATE TABLE member(
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      name VARCHAR(255) NOT NULL,
      username VARCHAR(255) NOT NULL,
      password VARCHAR(255) NOT NULL,
      follower_count INT UNSIGNED NOT NULL DEFAULT 0,
      time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task2-2.png?raw=tru)

## Task3: SQL CRUD
* INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
  ```sql
  INSERT INTO member(name, username, password) VALUES('test', 'test', 'test');
  INSERT INTO member(name, username, password) VALUES('apple', 'apple', 'apple');
  INSERT INTO member(name, username, password) VALUES('banana', 'banana', 'banana');
  INSERT INTO member(name, username, password) VALUES('cat', 'cat', 'cat');
  INSERT INTO member(name, username, password) VALUES('dog', 'dog', 'dog');
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-1.png?raw=true)

* SELECT all rows from the member table.
  ```sql
  SELECT * FROM member;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-2.png?raw=true)

* SELECT all rows from the member table, in descending order of time.
  ```sql
  SELECT * FROM member ORDER BY time DESC;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-3.png?raw=true)

* SELECT total 3 rows, second to fourth, from the member table, in descending order of time.
  ```sql
  SELECT * FROM member ORDER BY time DESC LIMIT 1, 3;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-4.png?raw=true)

* SELECT rows where username equals to test.
  ```sql
  SELECT * FROM member WHERE username = 'test';
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-5.png?raw=true)

* SELECT rows where name includes the es keyword.
  ```sql
  SELECT * FROM member WHERE name LIKE '%es%';
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-6.png?raw=true)

* SELECT rows where both username and password equal to test.
  ```sql
  SELECT * FROM member WHERE username = 'test' and password = 'test';
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-7.png?raw=true)

* UPDATE data in name column to test2 where username equals to test.
  ```sql
  SET SQL_SAFE_UPDATES = 0;
  UPDATE member SET name = 'test2' WHERE name = 'test';
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task3-8.png?raw=true)

## Task4: SQL Aggregation Functions
* SELECT how many rows from the member table.
  ```sql
  SELECT COUNT(*)FROM member;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task4-1.png?raw=true)

* SELECT the sum of follower_count of all the rows from the member table.
  ```sql
  SELECT SUM(follower_count)FROM member;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task4-2.png?raw=true)

* SELECT the average of follower_count of all the rows from the member table.
  ```sql
  SELECT AVG(follower_count)FROM member;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task4-3.png?raw=true)

* SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
  ```sql
  SELECT AVG(follower_count)FROM member ORDER BY follower_count DESC LIMIT 2;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task4-4.png?raw=true)

## Task 5: SQL JOIN
* Create a new table named message, in the website database.
  ```sql
  CREATE TABLE message(
      id BIGINT PRIMARY KEY AUTO_INCREMENT,
      member_id BIGINT NOT NULL,
      content VARCHAR(255) NOT NULL,
      like_count INT UNSIGNED NOT NULL DEFAULT 0,
      time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(member_id) REFERENCES member(id)
      );
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task5-1.png?raw=true)

* SELECT all messages, including sender names. We have to JOIN the member table to get that.
  ```sql
  SELECT * FROM member INNER JOIN message ON member.id = message.member_id;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task5-2.png?raw=true)

* SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
  ```sql
  SELECT * FROM member INNER JOIN message ON member.id = message.member_id WHERE username = 'test';
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task5-3.png?raw=true)

* Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
  ```sql
  SELECT AVG(like_count) FROM member INNER JOIN message ON member.id = message.member_id WHERE username = 'test';
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task5-4.png?raw=true)

* Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
  ```sql
  SELECT username, AVG(like_count) FROM member INNER JOIN message ON member.id = message.member_id GROUP BY username;
  ```
  ![](https://github.com/ZChingg/wehelpstage1/blob/main/week5/screenshot/task5-5.png?raw=true)