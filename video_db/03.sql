ALTER TABLE `admins` DROP COLUMN `organization_account`;
ALTER TABLE `users` DROP COLUMN `organization_account`;
ALTER TABLE `login_logs` DROP COLUMN `user_account`;
ALTER TABLE `distribut_videos` MODIFY COLUMN `video_id`  int(11) NOT NULL DEFAULT 0 COMMENT '视频表的id' AFTER `id`;
ALTER TABLE `distribut_videos` DROP COLUMN `video_uuid`, DROP COLUMN `video_title`, DROP COLUMN `organization_account`;
ALTER TABLE `videos` DROP COLUMN `upload_organization_account`, DROP COLUMN `release_admin_user_account`;
ALTER TABLE `watermark_logs`
CHANGE COLUMN `video_uuid` `video_id`  int(11) NOT NULL DEFAULT 0 COMMENT '视频id 所需的uuid从video对象中取' AFTER `watermark`,
CHANGE COLUMN `organization_account` `organization_id`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '单位id；单位编码从organization对象中取' AFTER `video_id`,
CHANGE COLUMN `user_uuid` `user_id`  varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户id；对应用户编号从user对象中取' AFTER `organization_id`;
ALTER TABLE `watermark_logs`
MODIFY COLUMN `organization_id`  int(11) NOT NULL DEFAULT 0 COMMENT '单位id；单位编码从organization对象中取' AFTER `video_id`,
MODIFY COLUMN `user_id`  int(11) NOT NULL DEFAULT 0 COMMENT '用户id；对应用户编号从user对象中取' AFTER `organization_id`;
ALTER TABLE `download_logs`
DROP COLUMN `organization_account`,
DROP COLUMN `download_user_account`,
CHANGE COLUMN `video_uuid` `video_id`  int(11) NOT NULL DEFAULT 0 COMMENT '视频id；视频编号从video对象中取得' AFTER `id`,
MODIFY COLUMN `organization_id`  int(11) NOT NULL COMMENT '单位id' AFTER `video_id`,
MODIFY COLUMN `download_user_id`  int(11) NOT NULL COMMENT '下载者id' AFTER `organization_id`;
ALTER TABLE `login_logs` ADD COLUMN `login_role`  varchar(255) NOT NULL DEFAULT '' COMMENT '登录校色：“admin“ 或 ”user“' AFTER `user_id`;
ALTER TABLE `videos`
CHANGE COLUMN `upload_admin_user_id` `upload_admin_id`  int(11) NOT NULL DEFAULT 0 COMMENT '上传管理员di；对应管理员id' AFTER `upload_organization_id`,
CHANGE COLUMN `release_admin_user_id` `release_admin_id`  int(11) NULL DEFAULT 0 COMMENT '发布管理员id；对应管理员id' AFTER `release_allow`,
CHANGE COLUMN `delete_admin_user_id` `delete_admin_id`  int(11) NULL DEFAULT 0 COMMENT '删除管理员id；对应管理员id' AFTER `release_time`;