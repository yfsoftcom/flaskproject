## v2.0(2020-02-28)

Feature:
- [ ] set redis server store mode.

- [x] support hd video address
- [x] support the user system
  - [x] login/logout
  - [x] save to the redis, use the hash `userinfo` include the fields: `username, nickname, email, password, salt, createAt, loginAt, loginIp`
  - [x] register

- [x] favorite list
  - [x] save the users' favorite list, use the hash `favorite:$(username)` include the fields: `username, createAt, vid, title, cover, href`