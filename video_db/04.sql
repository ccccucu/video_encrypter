ALTER TABLE `users`
ADD COLUMN `role`  varchar(255) NOT NULL DEFAULT '' COMMENT '角色权限[\"admin\",\"user\"], 管理员和用户都用这一张表' AFTER `password`;

DROP TABLE `admins` ;

