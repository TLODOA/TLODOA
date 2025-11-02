CREATE TABLE "UserCore"(
    "dek" CHAR(255) NOT NULL,
    "hashed_name" CHAR(255) NOT NULL,
    "hashed_email" CHAR(255) NOT NULL,
    "cipher_name" VARCHAR(255) NOT NULL,
    "cipher_email" VARCHAR(255) NOT NULL,
    "cipher_password" VARCHAR(255) NOT NULL
);
CREATE INDEX "usercore_hashed_name_index" ON
    "UserCore"("hashed_name");
ALTER TABLE
    "UserCore" ADD PRIMARY KEY("hashed_name");
CREATE INDEX "usercore_hashed_email_index" ON
    "UserCore"("hashed_email");
CREATE TABLE "UserInfos"(
    "dek" CHAR(255) NOT NULL,
    "User_name" CHAR(255) NOT NULL,
    "cipher_description" TEXT NULL,
    "cipher_region" TEXT NULL,
    "cipher_photoPath" VARCHAR(255) NULL,
    "time_arrival" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "time_viewed_last" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "reputation" INTEGER NOT NULL
);
CREATE INDEX "userinfos_user_name_index" ON
    "UserInfos"("User_name");
ALTER TABLE
    "UserInfos" ADD PRIMARY KEY("User_name");
CREATE TABLE "UserCard"(
    "User_name" CHAR(255) NOT NULL,
    "balance" BIGINT NOT NULL
);
CREATE INDEX "usercard_user_name_index" ON
    "UserCard"("User_name");
ALTER TABLE
    "UserCard" ADD PRIMARY KEY("User_name");
CREATE TABLE "UserToken"(
    "dek" CHAR(255) NOT NULL,
    "ip" CHAR(255) NOT NULL,
    "user_name" CHAR(255) NOT NULL,
    "cipher_token" VARCHAR(255) NOT NULL,
    "validity" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "field" INTEGER NOT NULL
);
ALTER TABLE
    "UserToken" ADD PRIMARY KEY("ip", "field");
CREATE INDEX "usertoken_ip_index" ON
    "UserToken"("ip");
CREATE INDEX "usertoken_user_name_index" ON
    "UserToken"("user_name");
CREATE TABLE "UserEmailCode"(
    "dek" CHAR(255) NOT NULL,
    "ip" CHAR(255) NOT NULL,
    "user_name" CHAR(255) NULL,
    "hashed_email" CHAR(255) NOT NULL,
    "cipher_token" VARCHAR(255) NOT NULL,
    "validity" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "field" INTEGER NOT NULL
);
ALTER TABLE
    "UserEmailCode" ADD PRIMARY KEY("ip", "field");
CREATE INDEX "useremailcode_ip_index" ON
    "UserEmailCode"("ip");
CREATE INDEX "useremailcode_user_name_index" ON
    "UserEmailCode"("user_name");
CREATE INDEX "useremailcode_hashed_email_index" ON
    "UserEmailCode"("hashed_email");
CREATE TABLE "ObjectCore"(
    "dek" CHAR(255) NOT NULL,
    "hashed_id" CHAR(255) NOT NULL,
    "hashed_name" CHAR(255) NOT NULL,
    "author" CHAR(255) NOT NULL,
    "cipher_id" CHAR(255) NOT NULL,
    "cipher_name" VARCHAR(255) NOT NULL,
    "cipher_author" VARCHAR(255) NOT NULL,
    "object_physical" VARCHAR(255) NOT NULL
);
CREATE INDEX "objectcore_hashed_id_index" ON
    "ObjectCore"("hashed_id");
ALTER TABLE
    "ObjectCore" ADD PRIMARY KEY("hashed_id");
CREATE INDEX "objectcore_hashed_name_index" ON
    "ObjectCore"("hashed_name");
CREATE INDEX "objectcore_author_index" ON
    "ObjectCore"("author");
CREATE TABLE "ObjectInfos"(
    "dek" CHAR(255) NOT NULL,
    "id" CHAR(255) NOT NULL,
    "cipher_id" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "time_init" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "time_end" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "price" BIGINT NOT NULL
);
CREATE INDEX "objectinfos_id_index" ON
    "ObjectInfos"("id");
ALTER TABLE
    "ObjectInfos" ADD PRIMARY KEY("id");
CREATE TABLE "ObjectExpost"(
    "dek" CHAR(255) NOT NULL,
    "id" CHAR(255) NOT NULL,
    "hashed_title" CHAR(255) NOT NULL,
    "cipher_id" VARCHAR(255) NOT NULL,
    "cipher_title" VARCHAR(255) NOT NULL,
    "cipher_description" TEXT NOT NULL,
    "cipher_addctionalInfos" TEXT NULL,
    "cipher_thumbnailPath" VARCHAR(255) NOT NULL
);
CREATE INDEX "objectexpost_id_index" ON
    "ObjectExpost"("id");
ALTER TABLE
    "ObjectExpost" ADD CONSTRAINT "objectexpost_hashed_title_unique" UNIQUE("hashed_title");
ALTER TABLE
    "ObjectExpost" ADD PRIMARY KEY("id");
CREATE INDEX "objectexpost_hashed_title_index" ON
    "ObjectExpost"("hashed_title");
CREATE TABLE "Message"(
    "dek" CHAR(255) NOT NULL,
    "hashed_id" CHAR(255) NOT NULL,
    "user_name" CHAR(255) NOT NULL,
    "object_title" CHAR(255) NOT NULL,
    "cipher_id" VARCHAR(255) NOT NULL,
    "cipher_content" VARCHAR(255) NOT NULL,
    "time_send" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
CREATE INDEX "message_hashed_id_index" ON
    "Message"("hashed_id");
ALTER TABLE
    "Message" ADD PRIMARY KEY("hashed_id");
CREATE INDEX "message_user_name_index" ON
    "Message"("user_name");
CREATE INDEX "message_object_title_index" ON
    "Message"("object_title");
CREATE TABLE "IpInfos"(
    "dek" CHAR(255) NOT NULL,
    "hashed_ip" CHAR(255) NOT NULL,
    "cipher_ip" VARCHAR(255) NOT NULL,
    "email_send_count" INTEGER NOT NULL,
    "email_send_last_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "auth_attempts" INTEGER NOT NULL,
    "block_time_init" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "validity" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
CREATE INDEX "ipinfos_hashed_ip_index" ON
    "IpInfos"("hashed_ip");
ALTER TABLE
    "IpInfos" ADD PRIMARY KEY("hashed_ip");
CREATE TABLE "Bid"(
    "dek" CHAR(255) NOT NULL,
    "hashed_id" CHAR(255) NOT NULL,
    "user_name" CHAR(255) NOT NULL,
    "object_title" CHAR(255) NOT NULL,
    "cipher_id" BIGINT NOT NULL,
    "time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "value" BIGINT NOT NULL
);
CREATE INDEX "bid_hashed_id_index" ON
    "Bid"("hashed_id");
ALTER TABLE
    "Bid" ADD PRIMARY KEY("hashed_id");
CREATE INDEX "bid_user_name_index" ON
    "Bid"("user_name");
CREATE INDEX "bid_object_title_index" ON
    "Bid"("object_title");
ALTER TABLE
    "UserInfos" ADD CONSTRAINT "userinfos_user_name_foreign" FOREIGN KEY("User_name") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "ObjectInfos" ADD CONSTRAINT "objectinfos_id_foreign" FOREIGN KEY("id") REFERENCES "ObjectCore"("hashed_id");
ALTER TABLE
    "ObjectExpost" ADD CONSTRAINT "objectexpost_id_foreign" FOREIGN KEY("id") REFERENCES "ObjectCore"("hashed_id");
ALTER TABLE
    "UserToken" ADD CONSTRAINT "usertoken_ip_foreign" FOREIGN KEY("ip") REFERENCES "IpInfos"("hashed_ip");
ALTER TABLE
    "Message" ADD CONSTRAINT "message_user_name_foreign" FOREIGN KEY("user_name") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "UserToken" ADD CONSTRAINT "usertoken_user_name_foreign" FOREIGN KEY("user_name") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "Message" ADD CONSTRAINT "message_object_title_foreign" FOREIGN KEY("object_title") REFERENCES "ObjectExpost"("hashed_title");
ALTER TABLE
    "Bid" ADD CONSTRAINT "bid_user_name_foreign" FOREIGN KEY("user_name") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "UserCard" ADD CONSTRAINT "usercard_user_name_foreign" FOREIGN KEY("User_name") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "UserEmailCode" ADD CONSTRAINT "useremailcode_ip_foreign" FOREIGN KEY("ip") REFERENCES "IpInfos"("hashed_ip");
ALTER TABLE
    "Bid" ADD CONSTRAINT "bid_object_title_foreign" FOREIGN KEY("object_title") REFERENCES "ObjectExpost"("hashed_title");
ALTER TABLE
    "UserEmailCode" ADD CONSTRAINT "useremailcode_user_name_foreign" FOREIGN KEY("user_name") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "ObjectCore" ADD CONSTRAINT "objectcore_author_foreign" FOREIGN KEY("author") REFERENCES "UserCore"("hashed_name");