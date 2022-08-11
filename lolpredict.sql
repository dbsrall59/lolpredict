create table matchInfo(
    matchID varchar(30) not null,
    CONSTRAINT match_pk PRIMARY key (matchid)
);

create table userInfo(
    userName varchar(50) not null,
    ranktier number not null,
    CONSTRAINT user_pk PRIMARY key (userName)
);

create table matchDetail(
    matchID varchar(30) not null,
    userName varchar(50) not null,
    win number not null, 
    time number not null,  
    turretsLost number not null, 
    inhibitorsLost number not null, 
    turretTakedowns number not null, 
    inhibitorTakedowns number not null, 
    nexusTakedowns number not null, 
    bountyLevel number not null, 
    turretKills number not null, 
    deaths number not null, 
    damageDealtToTurrets number not null, 
    inhibitorKills number not null, 
    assists number not null, 
    kills number not null, 
    killingSprees number not null, 
    goldEarned number not null, 
    champExperience number not null, 
    champLevel number not null, 
    dragonKills number not null, 
    baronKills number not null, 
    totalDamageDealtToChampions number not null,  
    firstTowerKill number not null, 
    visionScore number not null, 
    neutralMinionsKilled number not null, 
    teamEarlySurrendered number not null, 
    totalTimeCCDealt number not null, 
    detectorWardsPlaced number not null, 
    CONSTRAINT match_fk FOREIGN key (matchid) REFERENCES matchInfo(matchid)
);

CREATE SEQUENCE siteUserIdSeq;
create table siteUserInfo(
    siteUserID number not null,
    siteUserName varchar(50) not null,
    sitePassword varchar(257) not null,
    nickName varchar(50) not null,
    CONSTRAINT siteinfo_pk PRIMARY key(siteUserID),
    CONSTRAINT userName_unique UNIQUE(siteUserName),
    CONSTRAINT nickName_unique UNIQUE(nickName)
);

CREATE SEQUENCE boardIdSeq;
create table board(
    boardID number not null,
    siteUserID number not null,
    title varchar(500) not null,
    contentSrc varchar(500) not null,
    viewCount number not null,
    goodCount number not null,
    badCount number not null,
    CONSTRAINT board_pk PRIMARY key(boardID),
    CONSTRAINT board_fk FOREIGN key(siteUserID) REFERENCES siteUserInfo(siteUserID)
);

CREATE SEQUENCE replyIdSeq;
create table reply(
    replyID number not null,
    siteUserID number not null,
    boardID number not null,
    replyContent varchar(200) not null,
    replyTo number,
    CONSTRAINT reply_pk PRIMARY key(replyID),
    CONSTRAINT siteUserID_fk FOREIGN key(siteUserID) REFERENCES siteUserInfo(siteUserID),
    CONSTRAINT boardID_fk FOREIGN key(boardID) REFERENCES board(boardID)
);

create table saltTable(
    saltKey varchar(100) not null primary key
);
