select B.boardid, C.siteusername, A.replyContent, D.siteusername
from reply A
    inner join board B on A.boardid = B.boardid
    inner join siteuserinfo C on A.siteuserid = C.siteuserid
    left outer join siteuserinfo D on A.replyto = D.siteuserid
where B.boardid = 3;
    
select * from board;

insert into reply values(replyidseq.nextval, 28, 3, 'test2', 28);
commit;