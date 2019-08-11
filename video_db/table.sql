/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : video_encrypter

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2019-08-11 21:15:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for distribut_videos
-- ----------------------------
DROP TABLE IF EXISTS `distribut_videos`;
CREATE TABLE `distribut_videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【分发单位】id',
  `video_id` int(11) NOT NULL DEFAULT '0' COMMENT '视频表的id',
  `organization_id` int(11) NOT NULL COMMENT '单位id；对应单位id，若为“0”则表示所有单位均可下载',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for download_logs
-- ----------------------------
DROP TABLE IF EXISTS `download_logs`;
CREATE TABLE `download_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【下载记录】id',
  `video_id` int(11) NOT NULL DEFAULT '0' COMMENT '视频id；视频编号从video对象中取得',
  `organization_id` int(11) NOT NULL COMMENT '单位id',
  `download_user_id` int(11) NOT NULL COMMENT '下载者id',
  `created_at` timestamp NULL DEFAULT NULL COMMENT '下载开始时间',
  `updated_at` timestamp NULL DEFAULT NULL COMMENT '下载结束时间',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for login_logs
-- ----------------------------
DROP TABLE IF EXISTS `login_logs`;
CREATE TABLE `login_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【登录日志】id',
  `user_id` int(11) NOT NULL COMMENT '用户id；管理员或用户的id',
  `login_role` varchar(255) NOT NULL DEFAULT '' COMMENT '登录校色：“admin“ 或 ”user“',
  `login_type` varchar(255) NOT NULL DEFAULT '' COMMENT '登录类型；三个客户端软件：分发管理，下载，水印提取',
  `login_ip` varchar(255) NOT NULL DEFAULT '' COMMENT '登录IP',
  `success` tinyint(1) NOT NULL COMMENT '是否成功',
  `failure_reason` varchar(255) NOT NULL DEFAULT '' COMMENT '失败原因；无此用户，密码不匹配，IP不匹配',
  `created_at` timestamp NULL DEFAULT NULL COMMENT '登录时间',
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for organizations
-- ----------------------------
DROP TABLE IF EXISTS `organizations`;
CREATE TABLE `organizations` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【单位】id',
  `account` varchar(255) NOT NULL COMMENT '单位变码；唯一，00表示总部，00XX表示下属单位，依次类推',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT '单位名称',
  `responsible_name` varchar(255) NOT NULL DEFAULT '' COMMENT '单位负责人姓名',
  `responsible_phone` varchar(255) NOT NULL DEFAULT '' COMMENT '单位负责人电话',
  `organization_duty_phone` varchar(255) NOT NULL DEFAULT '' COMMENT '单位值班电话',
  `father_organization_id` int(11) NOT NULL COMMENT '父单位id',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【用户】id',
  `uuid` varchar(255) NOT NULL DEFAULT '' COMMENT '用户编号；唯一，UUID',
  `account` varchar(255) NOT NULL COMMENT '账号',
  `password` varchar(255) NOT NULL DEFAULT '' COMMENT '密码；SHA-256',
  `role` varchar(255) NOT NULL DEFAULT '' COMMENT '角色权限["admin","user"], 管理员和用户都用这一张表',
  `ip` varchar(255) NOT NULL DEFAULT '' COMMENT 'IP；绑定IP地址',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT '姓名',
  `organization_id` int(11) NOT NULL COMMENT '单位id；对应单位id',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for videos
-- ----------------------------
DROP TABLE IF EXISTS `videos`;
CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【视频】id',
  `uuid` varchar(255) NOT NULL DEFAULT '' COMMENT '编号；唯一，UUID，同时也是文件名，原始问价、加密我呢见、缩略图、加密密钥分别存放在不同文件夹内',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT '标题；',
  `upload_organization_id` int(11) NOT NULL DEFAULT '0' COMMENT '上传单位id；对应单位id',
  `upload_admin_id` int(11) NOT NULL DEFAULT '0' COMMENT '上传管理员di；对应管理员id',
  `allow_play_time` timestamp NOT NULL COMMENT '播放时限；该日期的24点前允许播放',
  `original_file_size` bigint(20) NOT NULL DEFAULT '0' COMMENT '原始文件大小；字节为单位',
  `encrypt_file_size` bigint(20) NOT NULL DEFAULT '0' COMMENT '加密后文件大小；字节为单位，与原始文件相同文件名',
  `release_allow` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否发布',
  `release_admin_id` int(11) DEFAULT '0' COMMENT '发布管理员id；对应管理员id',
  `release_time` timestamp NOT NULL COMMENT '发布时间',
  `delete_admin_id` int(11) DEFAULT '0' COMMENT '删除管理员id；对应管理员id',
  `secret_key` varchar(255) NOT NULL DEFAULT '' COMMENT '密钥',
  `created_at` timestamp NULL DEFAULT NULL COMMENT '上传时间',
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '' COMMENT '删除管理员；对应管理员用户名',
  `created_by` varchar(255) NOT NULL DEFAULT '' COMMENT '上传管理员；对应管理员用户名',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for watermark_logs
-- ----------------------------
DROP TABLE IF EXISTS `watermark_logs`;
CREATE TABLE `watermark_logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【水印记录】id',
  `watermark` varchar(255) NOT NULL DEFAULT '' COMMENT '水印',
  `video_id` int(11) NOT NULL DEFAULT '0' COMMENT '视频id 所需的uuid从video对象中取',
  `organization_id` int(11) NOT NULL DEFAULT '0' COMMENT '单位id；单位编码从organization对象中取',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户id；对应用户编号从user对象中取',
  `ip` varchar(255) NOT NULL DEFAULT '' COMMENT 'IP',
  `time` timestamp NOT NULL COMMENT '时间',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
