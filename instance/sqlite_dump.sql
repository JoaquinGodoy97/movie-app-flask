CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
	username VARCHAR(10) NOT NULL UNIQUE, 
	email VARCHAR(30), 
	password VARCHAR(20) NOT NULL
);
INSERT INTO users (username, email, password) VALUES ('admni', NULL, 'admin');
INSERT INTO users (username, email, password) VALUES ('admin', '', 'ADMIN');
INSERT INTO users (username, email, password) VALUES ('123456', '', '123456');
INSERT INTO users (username, email, password) VALUES ('camaleon', '', '123456');
INSERT INTO users (username, email, password) VALUES ('12345', '', '12345');
INSERT INTO users (username, email, password) VALUES ('123123', NULL, '123123');
INSERT INTO users (username, email, password) VALUES ('123124', NULL, '123123');
INSERT INTO users (username, email, password) VALUES ('123123a', NULL, '123123');
INSERT INTO users (username, email, password) VALUES ('124v124', NULL, '123123');
CREATE TABLE IF NOT EXISTS wishlist_user (
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, 
	mv_id INT NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	username VARCHAR(10) NOT NULL,
	CONSTRAINT fk_wishlist_user_username_user FOREIGN KEY(username) REFERENCES users (username)
);
INSERT INTO wishlist_user (mv_id, title, username) VALUES (382322, 'Batman: The Killing Joke', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (485942, 'Batman Ninja', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (14919, 'Batman: Mask of the Phantasm', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (69735, 'Batman: Year One', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (581997, 'Batman vs Teenage Mutant Ninja Turtles', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (415, 'Batman & Robin', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (408648, 'Batman and Harley Quinn', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (268, 'Batman', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (414906, 'The Batman', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (886396, 'Batman and Superman: Battle of the Super Sons', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (43189, 'Million Dollar Mermaid', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (373879, 'One Piece: Adventure of Nebulandia', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (568012, 'One Piece: Stampede', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (971968, 'Being Maria', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (123025, 'Batman: The Dark Knight Returns, Part 1', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (537056, 'Batman: Hush', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (870358, 'Merry Little Batman', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (364, 'Batman Returns', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (324849, 'The Lego Batman Movie', 'admin');
INSERT INTO wishlist_user (mv_id, title, username) VALUES (125249, 'Batman', 'admin');