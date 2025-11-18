CREATE TABLE "UserCore"(
    "dek" CHAR(255) NOT NULL,
    "hashed_name" CHAR(255) NOT NULL,
    "hashed_email" CHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "cipher_name" VARCHAR(255) NOT NULL,
    "cipher_email" VARCHAR(255) NOT NULL
);
CREATE INDEX "usercore_hashed_name_index" ON
    "UserCore"("hashed_name");
ALTER TABLE
    "UserCore" ADD PRIMARY KEY("hashed_name");
CREATE INDEX "usercore_hashed_email_index" ON
    "UserCore"("hashed_email");
CREATE TABLE "UserInfos"(
    "dek" CHAR(255) NOT NULL,
    "hashed_userName" CHAR(255) NOT NULL,
    "hashed_nickname" CHAR(255) NOT NULL,
    "hashed_iconProfileName" VARCHAR(255) NOT NULL,
    "cipher_userName" VARCHAR(255) NOT NULL,
    "cipher_description" TEXT NULL,
    "cipher_nickname" TEXT NOT NULL,
    "time_arrival" DOUBLE PRECISION NOT NULL DEFAULT '0',
    "time_viewed_last" DOUBLE PRECISION NOT NULL DEFAULT '0',
    "reputation" INTEGER NOT NULL DEFAULT '0'
);
CREATE INDEX "userinfos_hashed_username_index" ON
    "UserInfos"("hashed_userName");
ALTER TABLE
    "UserInfos" ADD PRIMARY KEY("hashed_userName");
CREATE INDEX "userinfos_hashed_nickname_index" ON
    "UserInfos"("hashed_nickname");
CREATE INDEX "userinfos_hashed_iconprofilename_index" ON
    "UserInfos"("hashed_iconProfileName");
CREATE TABLE "UserCard"(
    "hashed_userName" CHAR(255) NOT NULL,
    "balance" BIGINT NOT NULL
);
CREATE INDEX "usercard_hashed_username_index" ON
    "UserCard"("hashed_userName");
ALTER TABLE
    "UserCard" ADD PRIMARY KEY("hashed_userName");
CREATE TABLE "UserToken"(
    "dek" CHAR(255) NOT NULL,
    "hashed_ip" CHAR(255) NOT NULL,
    "hashed_userName" CHAR(255) NOT NULL,
    "token" VARCHAR(255) NOT NULL,
    "validity" DOUBLE PRECISION NOT NULL DEFAULT '0',
    "field" INTEGER NOT NULL
);
ALTER TABLE
    "UserToken" ADD PRIMARY KEY("hashed_ip", "field");
CREATE INDEX "usertoken_hashed_ip_index" ON
    "UserToken"("hashed_ip");
CREATE INDEX "usertoken_hashed_username_index" ON
    "UserToken"("hashed_userName");
CREATE INDEX "usertoken_field_index" ON
    "UserToken"("field");
CREATE TABLE "UserEmailCode"(
    "dek" CHAR(255) NOT NULL,
    "hashed_ip" CHAR(255) NOT NULL,
    "hashed_userName" CHAR(255) NULL,
    "hashed_email" CHAR(255) NOT NULL,
    "token" VARCHAR(255) NOT NULL,
    "cipher_email" VARCHAR(255) NOT NULL,
    "validity" DOUBLE PRECISION NOT NULL DEFAULT '0',
    "field" INTEGER NOT NULL
);
ALTER TABLE
    "UserEmailCode" ADD PRIMARY KEY("hashed_ip", "field");
CREATE INDEX "useremailcode_hashed_ip_index" ON
    "UserEmailCode"("hashed_ip");
CREATE INDEX "useremailcode_hashed_username_index" ON
    "UserEmailCode"("hashed_userName");
CREATE INDEX "useremailcode_hashed_email_index" ON
    "UserEmailCode"("hashed_email");
CREATE INDEX "useremailcode_field_index" ON
    "UserEmailCode"("field");
CREATE TABLE "ObjectCore"(
    "dek" CHAR(255) NOT NULL,
    "hashed_id" CHAR(255) NOT NULL,
    "hashed_objectPhysical" CHAR(255) NOT NULL,
    "hashed_userName" CHAR(255) NOT NULL,
    "hashed_iconBidName" CHAR(255) NOT NULL,
    "cipher_objectPhysical" VARCHAR(255) NOT NULL,
    "cipher_nickname" VARCHAR(255) NOT NULL,
    "time_changed" DOUBLE PRECISION NOT NULL
);
ALTER TABLE
    "ObjectCore" ADD PRIMARY KEY("hashed_id");
CREATE INDEX "objectcore_hashed_username_index" ON
    "ObjectCore"("hashed_userName");
CREATE TABLE "ObjectExpost"(
    "dek" CHAR(255) NOT NULL,
    "id" CHAR(255) NOT NULL,
    "hashed_title" CHAR(255) NOT NULL,
    "hashed_topicName" CHAR(255) NOT NULL,
    "hashed_iconBidName" VARCHAR(255) NOT NULL,
    "cipher_title" VARCHAR(255) NOT NULL,
    "cipher_description" TEXT NOT NULL,
    "cipher_addctionalInfos" TEXT NULL,
    "time_init" DOUBLE PRECISION NOT NULL,
    "time_end" DOUBLE PRECISION NOT NULL,
    "status" INTEGER NOT NULL,
    "price" INTEGER NOT NULL
);
ALTER TABLE
    "ObjectExpost" ADD PRIMARY KEY("id");
CREATE INDEX "objectexpost_hashed_title_index" ON
    "ObjectExpost"("hashed_title");
CREATE INDEX "objectexpost_hashed_topicname_index" ON
    "ObjectExpost"("hashed_topicName");
CREATE INDEX "objectexpost_hashed_iconbidname_index" ON
    "ObjectExpost"("hashed_iconBidName");
CREATE TABLE "Message"(
    "dek" CHAR(255) NOT NULL,
    "hashed_id" CHAR(255) NOT NULL,
    "hashed_userName" CHAR(255) NOT NULL,
    "object_id" CHAR(255) NOT NULL,
    "cipher_content" TEXT NOT NULL,
    "time_send" DOUBLE PRECISION NOT NULL
);
CREATE INDEX "message_hashed_id_index" ON
    "Message"("hashed_id");
ALTER TABLE
    "Message" ADD PRIMARY KEY("hashed_id");
CREATE INDEX "message_hashed_username_index" ON
    "Message"("hashed_userName");
CREATE INDEX "message_object_id_index" ON
    "Message"("object_id");
CREATE TABLE "IpInfos"(
    "dek" CHAR(255) NOT NULL,
    "hashed_ip" CHAR(255) NOT NULL,
    "cipher_ip" VARCHAR(255) NOT NULL,
    "email_send_count" INTEGER NOT NULL DEFAULT '0',
    "email_send_last_time" DOUBLE PRECISION NULL DEFAULT '0',
    "auth_attempts" INTEGER NOT NULL DEFAULT '0',
    "block_time_init" DOUBLE PRECISION NULL DEFAULT '0',
    "validity" DOUBLE PRECISION NOT NULL DEFAULT '0'
);
CREATE INDEX "ipinfos_hashed_ip_index" ON
    "IpInfos"("hashed_ip");
ALTER TABLE
    "IpInfos" ADD PRIMARY KEY("hashed_ip");
CREATE TABLE "Bid"(
    "dek" CHAR(255) NOT NULL,
    "hashed_id" CHAR(255) NOT NULL,
    "hashed_userName" CHAR(255) NOT NULL,
    "object_id" CHAR(255) NOT NULL,
    "time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "value" BIGINT NOT NULL
);
CREATE INDEX "bid_hashed_id_index" ON
    "Bid"("hashed_id");
ALTER TABLE
    "Bid" ADD PRIMARY KEY("hashed_id");
CREATE INDEX "bid_hashed_username_index" ON
    "Bid"("hashed_userName");
CREATE INDEX "bid_object_id_index" ON
    "Bid"("object_id");
CREATE TABLE "Icon"(
    "dek" CHAR(255) NOT NULL,
    "hashed_name" CHAR(255) NOT NULL,
    "hashed_pathIcon" CHAR(255) NOT NULL,
    "cipher_name" VARCHAR(255) NOT NULL,
    "cipher_pathIcon" VARCHAR(255) NOT NULL,
    "type" INTEGER NOT NULL
);
ALTER TABLE
    "Icon" ADD PRIMARY KEY("hashed_pathIcon", "type");
ALTER TABLE
    "Icon" ADD CONSTRAINT "icon_hashed_name_unique" UNIQUE("hashed_name");
CREATE TABLE "Topic"(
    "dek" CHAR(255) NOT NULL,
    "hashed_name" CHAR(255) NOT NULL,
    "cipher_name" VARCHAR(255) NOT NULL,
    "weigth" INTEGER NOT NULL
);
ALTER TABLE
    "Topic" ADD PRIMARY KEY("hashed_name");
ALTER TABLE
    "Bid" ADD CONSTRAINT "bid_object_id_foreign" FOREIGN KEY("object_id") REFERENCES "ObjectExpost"("id");
ALTER TABLE
    "UserInfos" ADD CONSTRAINT "userinfos_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "ObjectExpost" ADD CONSTRAINT "objectexpost_id_foreign" FOREIGN KEY("id") REFERENCES "ObjectCore"("hashed_id");
ALTER TABLE
    "UserToken" ADD CONSTRAINT "usertoken_hashed_ip_foreign" FOREIGN KEY("hashed_ip") REFERENCES "IpInfos"("hashed_ip");
ALTER TABLE
    "Message" ADD CONSTRAINT "message_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "UserInfos" ADD CONSTRAINT "userinfos_hashed_iconprofilename_foreign" FOREIGN KEY("hashed_iconProfileName") REFERENCES "Icon"("hashed_name");
ALTER TABLE
    "UserToken" ADD CONSTRAINT "usertoken_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "ObjectExpost" ADD CONSTRAINT "objectexpost_hashed_topicname_foreign" FOREIGN KEY("hashed_topicName") REFERENCES "Topic"("hashed_name");
ALTER TABLE
    "Bid" ADD CONSTRAINT "bid_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "ObjectCore" ADD CONSTRAINT "objectcore_hashed_iconbidname_foreign" FOREIGN KEY("hashed_iconBidName") REFERENCES "Icon"("hashed_name");
ALTER TABLE
    "UserCard" ADD CONSTRAINT "usercard_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "UserEmailCode" ADD CONSTRAINT "useremailcode_hashed_ip_foreign" FOREIGN KEY("hashed_ip") REFERENCES "IpInfos"("hashed_ip");
ALTER TABLE
    "Message" ADD CONSTRAINT "message_object_id_foreign" FOREIGN KEY("object_id") REFERENCES "ObjectExpost"("id");
ALTER TABLE
    "UserEmailCode" ADD CONSTRAINT "useremailcode_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");
ALTER TABLE
    "ObjectCore" ADD CONSTRAINT "objectcore_hashed_username_foreign" FOREIGN KEY("hashed_userName") REFERENCES "UserCore"("hashed_name");