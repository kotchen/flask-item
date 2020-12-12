DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS map;
DROP TABLE IF EXISTS windows;
DROP TABLE IF EXISTS menu;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE map (
  placename TEXT PRIMARY KEY,
  num INTEGER NOT NULL
);

CREATE TABLE windows (
  placename TEXT PRIMARY KEY,
  windowsOneNum INTEGER NOT NULL,
  windowsTwoNum INTEGER NOT NULL
);

CREATE TABLE menu (
  placename TEXT PRIMARY KEY,
  menu1 TEXT NOT NULL,
  menu2 TEXT NOT NULL,
  menu3 TEXT NOT NULL,
  menu4 TEXT NOT NULL
);