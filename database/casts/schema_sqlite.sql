PRAGMA foreign_keys = ON;

-- ===========================
-- UserCore
-- ===========================
CREATE TABLE "UserCore"(
    "dek" TEXT NOT NULL,
    "hashed_name" TEXT NOT NULL,
    "hashed_email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "cipher_name" TEXT NOT NULL,
    "cipher_email" TEXT NOT NULL,
    PRIMARY KEY("hashed_name")
);
CREATE INDEX "usercore_hashed_name_index" ON "UserCore"("hashed_name");
CREATE INDEX "usercore_hashed_email_index" ON "UserCore"("hashed_email");

-- ===========================
-- UserInfos
-- ===========================
CREATE TABLE "UserInfos"(
    "dek" TEXT NOT NULL,
    "hashed_userName" TEXT NOT NULL,
    "hashed_nickname" TEXT NOT NULL,
    "hashed_iconProfileName" TEXT NOT NULL,
    "cipher_userName" TEXT NOT NULL,
    "cipher_description" TEXT,
    "cipher_nickname" TEXT NOT NULL,
    "time_arrival" REAL NOT NULL DEFAULT 0,
    "time_viewed_last" REAL NOT NULL DEFAULT 0,
    "reputation" INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY("hashed_userName"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name"),
    FOREIGN KEY("hashed_iconProfileName") REFERENCES "Icon"("hashed_name")
);
CREATE INDEX "userinfos_hashed_username_index" ON "UserInfos"("hashed_userName");
CREATE INDEX "userinfos_hashed_nickname_index" ON "UserInfos"("hashed_nickname");
CREATE INDEX "userinfos_hashed_iconprofilename_index" ON "UserInfos"("hashed_iconProfileName");

-- ===========================
-- UserCard
-- ===========================
CREATE TABLE "UserCard"(
    "hashed_userName" TEXT NOT NULL,
    "balance" INTEGER NOT NULL,
    PRIMARY KEY("hashed_userName"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name")
);
CREATE INDEX "usercard_hashed_username_index" ON "UserCard"("hashed_userName");

-- ===========================
-- UserToken
-- ===========================
CREATE TABLE "UserToken"(
    "dek" TEXT NOT NULL,
    "hashed_ip" TEXT NOT NULL,
    "hashed_userName" TEXT NOT NULL,
    "token" TEXT NOT NULL,
    "validity" REAL NOT NULL DEFAULT 0,
    "field" INTEGER NOT NULL,
    PRIMARY KEY("hashed_ip", "field"),
    FOREIGN KEY("hashed_ip") REFERENCES "IpInfos"("hashed_ip"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name")
);
CREATE INDEX "usertoken_hashed_ip_index" ON "UserToken"("hashed_ip");
CREATE INDEX "usertoken_hashed_username_index" ON "UserToken"("hashed_userName");
CREATE INDEX "usertoken_field_index" ON "UserToken"("field");

-- ===========================
-- UserEmailCode
-- ===========================
CREATE TABLE "UserEmailCode"(
    "dek" TEXT NOT NULL,
    "hashed_ip" TEXT NOT NULL,
    "hashed_userName" TEXT,
    "hashed_email" TEXT NOT NULL,
    "token" TEXT NOT NULL,
    "cipher_email" TEXT NOT NULL,
    "validity" REAL NOT NULL DEFAULT 0,
    "field" INTEGER NOT NULL,
    PRIMARY KEY("hashed_ip", "field"),
    FOREIGN KEY("hashed_ip") REFERENCES "IpInfos"("hashed_ip"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name")
);
CREATE INDEX "useremailcode_hashed_ip_index" ON "UserEmailCode"("hashed_ip");
CREATE INDEX "useremailcode_hashed_username_index" ON "UserEmailCode"("hashed_userName");
CREATE INDEX "useremailcode_hashed_email_index" ON "UserEmailCode"("hashed_email");
CREATE INDEX "useremailcode_field_index" ON "UserEmailCode"("field");

-- ===========================
-- ObjectCore
-- ===========================
CREATE TABLE "ObjectCore"(
    "dek" TEXT NOT NULL,
    "hashed_id" TEXT NOT NULL,
    "hashed_objectPhysical" TEXT NOT NULL,
    "hashed_userName" TEXT NOT NULL,
    "hashed_iconBidName" TEXT NOT NULL,
    "cipher_objectPhysical" TEXT NOT NULL,
    "cipher_nickname" TEXT NOT NULL,
    "time_changed" REAL NOT NULL,
    PRIMARY KEY("hashed_id"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name"),
    FOREIGN KEY("hashed_iconBidName") REFERENCES "Icon"("hashed_name")
);
CREATE INDEX "objectcore_hashed_username_index" ON "ObjectCore"("hashed_userName");

-- ===========================
-- ObjectExpost
-- ===========================
CREATE TABLE "ObjectExpost"(
    "dek" TEXT NOT NULL,
    "id" TEXT NOT NULL,
    "hashed_title" TEXT NOT NULL,
    "hashed_topicName" TEXT NOT NULL,
    "hashed_iconBidName" TEXT NOT NULL,
    "cipher_title" TEXT NOT NULL,
    "cipher_description" TEXT NOT NULL,
    "cipher_addctionalInfos" TEXT,
    "time_init" REAL NOT NULL,
    "time_end" REAL NOT NULL,
    "status" INTEGER NOT NULL,
    "price" INTEGER NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("id") REFERENCES "ObjectCore"("hashed_id"),
    FOREIGN KEY("hashed_topicName") REFERENCES "Topic"("hashed_name")
);
CREATE INDEX "objectexpost_hashed_title_index" ON "ObjectExpost"("hashed_title");
CREATE INDEX "objectexpost_hashed_topicname_index" ON "ObjectExpost"("hashed_topicName");
CREATE INDEX "objectexpost_hashed_iconbidname_index" ON "ObjectExpost"("hashed_iconBidName");

-- ===========================
-- Message
-- ===========================
CREATE TABLE "Message"(
    "dek" TEXT NOT NULL,
    "hashed_id" TEXT NOT NULL,
    "hashed_userName" TEXT NOT NULL,
    "object_id" TEXT NOT NULL,
    "cipher_content" TEXT NOT NULL,
    "time_send" REAL NOT NULL,
    PRIMARY KEY("hashed_id"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name"),
    FOREIGN KEY("object_id") REFERENCES "ObjectExpost"("id")
);
CREATE INDEX "message_hashed_id_index" ON "Message"("hashed_id");
CREATE INDEX "message_hashed_username_index" ON "Message"("hashed_userName");
CREATE INDEX "message_object_id_index" ON "Message"("object_id");

-- ===========================
-- IpInfos
-- ===========================
CREATE TABLE "IpInfos"(
    "dek" TEXT NOT NULL,
    "hashed_ip" TEXT NOT NULL,
    "cipher_ip" TEXT NOT NULL,
    "email_send_count" INTEGER NOT NULL DEFAULT 0,
    "email_send_last_time" REAL DEFAULT 0,
    "auth_attempts" INTEGER NOT NULL DEFAULT 0,
    "block_time_init" REAL DEFAULT 0,
    "object_create_last_time" REAL NOT NULL DEFAULT 9,
    "validity" REAL NOT NULL DEFAULT 0,
    PRIMARY KEY("hashed_ip")
);
CREATE INDEX "ipinfos_hashed_ip_index" ON "IpInfos"("hashed_ip");

-- ===========================
-- Bid
-- ===========================
CREATE TABLE "Bid"(
    "dek" TEXT NOT NULL,
    "hashed_id" TEXT NOT NULL,
    "hashed_userName" TEXT NOT NULL,
    "object_id" TEXT NOT NULL,
    "time" TEXT NOT NULL,
    "value" INTEGER NOT NULL,
    PRIMARY KEY("hashed_id"),
    FOREIGN KEY("object_id") REFERENCES "ObjectExpost"("id"),
    FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name")
);
CREATE INDEX "bid_hashed_id_index" ON "Bid"("hashed_id");
CREATE INDEX "bid_hashed_username_index" ON "Bid"("hashed_userName");
CREATE INDEX "bid_object_id_index" ON "Bid"("object_id");

-- ===========================
-- Icon
-- ===========================
CREATE TABLE "Icon"(
    "dek" TEXT NOT NULL,
    "hashed_name" TEXT NOT NULL,
    "hashed_pathIcon" TEXT NOT NULL,
    "cipher_name" TEXT NOT NULL,
    "cipher_pathIcon" TEXT NOT NULL,
    "type" INTEGER NOT NULL,
    PRIMARY KEY("hashed_pathIcon", "type"),
    UNIQUE("hashed_name")
);

-- ===========================
-- Topic
-- ===========================
CREATE TABLE "Topic"(
    "dek" TEXT NOT NULL,
    "hashed_name" TEXT NOT NULL,
    "cipher_name" TEXT NOT NULL,
    "weigth" INTEGER NOT NULL,
    PRIMARY KEY("hashed_name")
);

