CREATE TABLE UserCore (
    dek TEXT NOT NULL,
    hashed_name TEXT NOT NULL PRIMARY KEY,
    hashed_email TEXT NOT NULL,
    password TEXT NOT NULL,
    cipher_name TEXT NOT NULL,
    cipher_email TEXT NOT NULL
);
CREATE INDEX usercore_hashed_name_index ON UserCore(hashed_name);
CREATE INDEX usercore_hashed_email_index ON UserCore(hashed_email);

CREATE TABLE UserInfos (
    dek TEXT NOT NULL,
    User_name TEXT NOT NULL PRIMARY KEY,
    cipher_description TEXT,
    cipher_region TEXT,
    cipher_photoPath TEXT,
    time_arrival TEXT NOT NULL,
    time_viewed_last TEXT NOT NULL,
    reputation INTEGER NOT NULL,
    FOREIGN KEY(User_name) REFERENCES UserCore(hashed_name)
);
CREATE INDEX userinfos_user_name_index ON UserInfos(User_name);

CREATE TABLE UserCard (
    User_name TEXT NOT NULL PRIMARY KEY,
    balance INTEGER NOT NULL,
    FOREIGN KEY(User_name) REFERENCES UserCore(hashed_name)
);
CREATE INDEX usercard_user_name_index ON UserCard(User_name);

CREATE TABLE UserToken (
    dek TEXT NOT NULL,
    hashed_ip TEXT NOT NULL,
    hashed_userName TEXT NOT NULL,
    token TEXT NOT NULL,
    validity NUMERIC NOT NULL DEFAULT 0,
    field INTEGER NOT NULL,
    PRIMARY KEY (hashed_ip, field),
    FOREIGN KEY(hashed_ip) REFERENCES IpInfos(hashed_ip),
    FOREIGN KEY(hashed_userName) REFERENCES UserCore(hashed_name)
);
CREATE INDEX usertoken_hashed_ip_index ON UserToken(hashed_ip);
CREATE INDEX usertoken_hashed_username_index ON UserToken(hashed_userName);
CREATE INDEX usertoken_field_index ON UserToken(field);

CREATE TABLE UserEmailCode (
    dek TEXT NOT NULL,
    hashed_ip TEXT NOT NULL,
    hashed_userName TEXT,
    hashed_email TEXT NOT NULL,
    token TEXT NOT NULL,
    cipher_email TEXT NOT NULL,
    validity NUMERIC NOT NULL DEFAULT 0,
    field INTEGER NOT NULL,
    PRIMARY KEY (hashed_ip, field),
    FOREIGN KEY(hashed_ip) REFERENCES IpInfos(hashed_ip),
    FOREIGN KEY(hashed_userName) REFERENCES UserCore(hashed_name)
);
CREATE INDEX useremailcode_hashed_ip_index ON UserEmailCode(hashed_ip);
CREATE INDEX useremailcode_hashed_username_index ON UserEmailCode(hashed_userName);
CREATE INDEX useremailcode_hashed_email_index ON UserEmailCode(hashed_email);
CREATE INDEX useremailcode_field_index ON UserEmailCode(field);

CREATE TABLE ObjectCore (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    hashed_name TEXT NOT NULL,
    author TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    cipher_name TEXT NOT NULL,
    cipher_author TEXT NOT NULL,
    object_physical TEXT NOT NULL,
    FOREIGN KEY(author) REFERENCES UserCore(hashed_name)
);
CREATE INDEX objectcore_hashed_id_index ON ObjectCore(hashed_id);
CREATE INDEX objectcore_hashed_name_index ON ObjectCore(hashed_name);
CREATE INDEX objectcore_author_index ON ObjectCore(author);

CREATE TABLE ObjectInfos (
    dek TEXT NOT NULL,
    id TEXT NOT NULL PRIMARY KEY,
    cipher_id TEXT NOT NULL,
    status TEXT NOT NULL,
    time_init TEXT NOT NULL,
    time_end TEXT,
    price INTEGER NOT NULL,
    FOREIGN KEY(id) REFERENCES ObjectCore(hashed_id)
);
CREATE INDEX objectinfos_id_index ON ObjectInfos(id);

CREATE TABLE ObjectExpost (
    dek TEXT NOT NULL,
    id TEXT NOT NULL PRIMARY KEY,
    hashed_title TEXT NOT NULL UNIQUE,
    cipher_id TEXT NOT NULL,
    cipher_title TEXT NOT NULL,
    cipher_description TEXT NOT NULL,
    cipher_addctionalInfos TEXT,
    cipher_thumbnailPath TEXT NOT NULL,
    FOREIGN KEY(id) REFERENCES ObjectCore(hashed_id)
);
CREATE INDEX objectexpost_id_index ON ObjectExpost(id);
CREATE INDEX objectexpost_hashed_title_index ON ObjectExpost(hashed_title);

CREATE TABLE Message (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    user_name TEXT NOT NULL,
    object_title TEXT NOT NULL,
    cipher_id TEXT NOT NULL,
    cipher_content TEXT NOT NULL,
    time_send TEXT NOT NULL,
    FOREIGN KEY(user_name) REFERENCES UserCore(hashed_name),
    FOREIGN KEY(object_title) REFERENCES ObjectExpost(hashed_title)
);
CREATE INDEX message_hashed_id_index ON Message(hashed_id);
CREATE INDEX message_user_name_index ON Message(user_name);
CREATE INDEX message_object_title_index ON Message(object_title);

CREATE TABLE IpInfos (
    dek TEXT NOT NULL,
    hashed_ip TEXT NOT NULL PRIMARY KEY,
    cipher_ip TEXT NOT NULL,
    email_send_count INTEGER NOT NULL DEFAULT 0,
    email_send_last_time NUMERIC DEFAULT 0,
    auth_attempts INTEGER NOT NULL DEFAULT 0,
    block_time_init NUMERIC DEFAULT 0,
    validity NUMERIC NOT NULL DEFAULT 0
);
CREATE INDEX ipinfos_hashed_ip_index ON IpInfos(hashed_ip);

CREATE TABLE Bid (
    dek TEXT NOT NULL,
    hashed_id TEXT NOT NULL PRIMARY KEY,
    user_name TEXT NOT NULL,
    object_title TEXT NOT NULL,
    cipher_id INTEGER NOT NULL,
    time TEXT NOT NULL,
    value INTEGER NOT NULL,
    FOREIGN KEY(user_name) REFERENCES UserCore(hashed_name),
    FOREIGN KEY(object_title) REFERENCES ObjectExpost(hashed_title)
);
CREATE INDEX bid_hashed_id_index ON Bid(hashed_id);
CREATE INDEX bid_user_name_index ON Bid(user_name);
CREATE INDEX bid_object_title_index ON Bid(object_title);
