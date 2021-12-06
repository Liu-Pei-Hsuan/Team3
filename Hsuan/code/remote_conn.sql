# 建立使用者帳號
create user pei@localhost;
create user 'pei2'@'%' identified by "012276";
grant all on my_db.* to 'pei2'@'%';

use mysql;
select * from user;
SHOW tables;


create user 'CFI101'@'%' identified by "team3";
grant all PRIVILEGES on project.* to 'CFI101'@'%';
FLUSH PRIVILEGES;

GRANT ALL PRIVILEGES ON project.* to 'CFI101'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;