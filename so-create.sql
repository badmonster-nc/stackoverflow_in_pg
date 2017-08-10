ALTER TABLE Comments DROP CONSTRAINT comments_id_fkey;
DROP TABLE Votes;
DROP TABLE Tagging;
DROP TABLE Tags;
DROP TABLE Posts;
DROP TABLE Comments;
DROP TABLE Users;

CREATE TABLE Users (
    id INTEGER UNIQUE NOT NULL,
    name TEXT, -- Yes, can be null some times
    reputation INTEGER NOT NULL,
    creation TIMESTAMP NOT NULL,
    website TEXT
    -- TODO: age, location (impossible to parse, because there is no formal structure), etc
    );

CREATE TABLE Comments (
    id INTEGER UNIQUE NOT NULL,
    creation TIMESTAMP NOT NULL,
    owner INTEGER REFERENCES Users(id),
    post INTEGER NOT NULL);

CREATE TABLE Posts (
    id INTEGER UNIQUE NOT NULL,
    type INTEGER NOT NULL, -- 1 Question, 2 Answer. TODO: uses an ENUM type
    title TEXT, -- May be NULL if the post is not a Question
    creation TIMESTAMP NOT NULL,
    owner INTEGER REFERENCES Users(id),
    accepted_answer INTEGER -- No REFERENCES Comments(id) because some posts references
                              -- a non-available comment :-(
    -- TODO: score, size of the body, last edition, last editor, etc
    );

CREATE TABLE Tags (
    id INTEGER UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL);

CREATE TABLE Tagging (
    tag INTEGER NOT NULL REFERENCES Tags(id),
    post INTEGER NOT NULL REFERENCES Posts(id));

CREATE TABLE Votes (
    id INTEGER UNIQUE NOT NULL,
    type INTEGER NOT NULL,  -- 2 UpMod, 3 DownMod, etc. TODO: uses an ENUM type
    post INTEGER NOT NULL, -- No REFERENCES Posts(id) because some votes references
                           -- a non-available post :-(
    creation DATE NOT NULL); -- Unfortunately not a timestamp

-- TODO: Badges

-- Add this one by hand after filling in the tables
-- ALTER TABLE Comments ADD FOREIGN KEY (id) REFERENCES Posts(id);
