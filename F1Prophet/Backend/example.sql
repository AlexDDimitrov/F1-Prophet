CREATE DATABASE IF NOT EXISTS f1prophet
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
 
USE f1prophet;
 
CREATE TABLE IF NOT EXISTS users (
    id            INT          NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50)  NOT NULL UNIQUE,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
 
    PRIMARY KEY (id),
    INDEX idx_email    (email),
    INDEX idx_username (username)
)

ALTER TABLE users 
ADD COLUMN is_admin TINYINT(1) NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS races (
    id            INT          NOT NULL AUTO_INCREMENT,
    name          VARCHAR(100) NOT NULL,
    location      VARCHAR(100) NOT NULL,
    race_date     DATETIME     NOT NULL,
    deadline      DATETIME     NOT NULL,
    season        INT          NOT NULL,
    round_number  INT          NOT NULL,
    status        ENUM('upcoming', 'active', 'completed') NOT NULL DEFAULT 'upcoming',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY unique_race (season, round_number),
    INDEX idx_season (season),
    INDEX idx_status (status)
)

CREATE TABLE IF NOT EXISTS predictions (
    id            INT      NOT NULL AUTO_INCREMENT,
    user_id       INT      NOT NULL,
    race_id       INT      NOT NULL,
    fastest_lap   VARCHAR(50),
    submitted_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    points_earned INT      DEFAULT NULL,
    
    PRIMARY KEY (id),
    UNIQUE KEY unique_user_race (user_id, race_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (race_id) REFERENCES races(id) ON DELETE CASCADE,
    INDEX idx_user (user_id),
    INDEX idx_race (race_id)
)

CREATE TABLE IF NOT EXISTS predicted_positions (
    id            INT         NOT NULL AUTO_INCREMENT,
    prediction_id INT         NOT NULL,
    driver_id     VARCHAR(50) NOT NULL,
    position      INT,
    is_dnf        TINYINT(1)  NOT NULL DEFAULT 0,
    
    PRIMARY KEY (id),
    FOREIGN KEY (prediction_id) REFERENCES predictions(id) ON DELETE CASCADE,
    INDEX idx_prediction (prediction_id)
)

-- for 2026 season:
INSERT INTO races (name, location, race_date, deadline, season, round_number, status)
VALUES
('Australian Grand Prix', 'Melbourne', '2026-03-08 15:00:00', '2026-03-07 16:00:00', 2026, 1, 'upcoming'),
('Chinese Grand Prix', 'Shanghai', '2026-03-15 15:00:00', '2026-03-14 16:00:00', 2026, 2, 'upcoming'),
('Japanese Grand Prix', 'Suzuka', '2026-03-29 14:00:00', '2026-03-28 15:00:00', 2026, 3, 'upcoming'),
('Miami Grand Prix', 'Miami', '2026-05-03 16:00:00', '2026-05-02 17:00:00', 2026, 4, 'upcoming'),
('Canadian Grand Prix', 'Montreal', '2026-05-24 16:00:00', '2026-05-23 17:00:00', 2026, 5, 'upcoming'),
('Monaco Grand Prix', 'Monaco', '2026-06-07 15:00:00', '2026-06-06 16:00:00', 2026, 6, 'upcoming'),
('Spanish Grand Prix (Barcelona)', 'Barcelona', '2026-06-14 15:00:00', '2026-06-13 16:00:00', 2026, 7, 'upcoming'),
('Austrian Grand Prix', 'Spielberg', '2026-06-28 15:00:00', '2026-06-27 16:00:00', 2026, 8, 'upcoming'),
('British Grand Prix', 'Silverstone', '2026-07-05 15:00:00', '2026-07-04 16:00:00', 2026, 9, 'upcoming'),
('Belgian Grand Prix', 'Spa', '2026-07-19 15:00:00', '2026-07-18 16:00:00', 2026, 10, 'upcoming'),
('Hungarian Grand Prix', 'Budapest', '2026-07-26 15:00:00', '2026-07-25 16:00:00', 2026, 11, 'upcoming'),
('Dutch Grand Prix', 'Zandvoort', '2026-08-23 15:00:00', '2026-08-22 16:00:00', 2026, 12, 'upcoming'),
('Italian Grand Prix', 'Monza', '2026-09-06 15:00:00', '2026-09-05 16:00:00', 2026, 13, 'upcoming'),
('Spanish Grand Prix (Madrid)', 'Madrid', '2026-09-13 15:00:00', '2026-09-12 16:00:00', 2026, 14, 'upcoming'),
('Azerbaijan Grand Prix', 'Baku', '2026-09-26 15:00:00', '2026-09-25 16:00:00', 2026, 15, 'upcoming'),
('Singapore Grand Prix', 'Singapore', '2026-10-11 20:00:00', '2026-10-10 21:00:00', 2026, 16, 'upcoming'),
('United States Grand Prix', 'Austin', '2026-10-25 15:00:00', '2026-10-24 16:00:00', 2026, 17, 'upcoming'),
('Mexico City Grand Prix', 'Mexico City', '2026-11-01 14:00:00', '2026-10-31 15:00:00', 2026, 18, 'upcoming'),
('Brazilian Grand Prix', 'São Paulo', '2026-11-08 14:00:00', '2026-11-07 15:00:00', 2026, 19, 'upcoming'),
('Las Vegas Grand Prix', 'Las Vegas', '2026-11-21 22:00:00', '2026-11-20 23:00:00', 2026, 20, 'upcoming'),
('Qatar Grand Prix', 'Lusail', '2026-11-29 19:00:00', '2026-11-28 20:00:00', 2026, 21, 'upcoming'),
('Abu Dhabi Grand Prix', 'Abu Dhabi', '2026-12-06 17:00:00', '2026-12-05 18:00:00', 2026, 22, 'upcoming');


CREATE TABLE IF NOT EXISTS race_results (
    id            INT          NOT NULL AUTO_INCREMENT,
    race_id       INT          NOT NULL,
    driver_id     VARCHAR(50)  NOT NULL,
    position      INT,
    is_dnf        TINYINT(1)   NOT NULL DEFAULT 0,
    fastest_lap   TINYINT(1)   NOT NULL DEFAULT 0,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (id),
    UNIQUE KEY unique_driver_race (race_id, driver_id),
    FOREIGN KEY (race_id) REFERENCES races(id) ON DELETE CASCADE,
    INDEX idx_race (race_id)
);

ALTER TABLE users 
ADD COLUMN total_points INT NOT NULL DEFAULT 0 AFTER is_admin;