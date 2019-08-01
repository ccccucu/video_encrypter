/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : video_encrypter

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2019-08-01 15:10:31
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【系统管理员】id',
  `account` varchar(255) NOT NULL COMMENT '用户名；唯一',
  `password` varchar(255) NOT NULL COMMENT '密码；SHA-256',
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `organization_account` varchar(255) NOT NULL COMMENT '单位；对应单位编码',
  `create_time` timestamp NOT NULL COMMENT '创建日期',
  `delete_time` timestamp NULL DEFAULT NULL COMMENT '删除日期',
  `disable` tinyint(1) NOT NULL COMMENT '是否禁用',
  `using` tinyint(1) NOT NULL COMMENT '是否删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('1', 'admin', '123456', '总管理员', '00', '2019-08-01 11:47:26', '2019-08-01 11:48:08', '0', '1');

-- ----------------------------
-- Table structure for distribut_video
-- ----------------------------
DROP TABLE IF EXISTS `distribut_video`;
CREATE TABLE `distribut_video` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【分发单位】id',
  `video_uuid` varchar(255) NOT NULL COMMENT '视频；对应视频编号',
  `organization_account` varchar(255) NOT NULL COMMENT '单位；对应单位编码，若为“ALL”则表示所有单位均可下载',
  `using` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of distribut_video
-- ----------------------------

-- ----------------------------
-- Table structure for download_log
-- ----------------------------
DROP TABLE IF EXISTS `download_log`;
CREATE TABLE `download_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【下载记录】id',
  `video_uuid` varchar(255) NOT NULL COMMENT '视频；对应视频编号',
  `organization_account` varchar(255) NOT NULL COMMENT '单位；对应单位编码',
  `download_user_account` varchar(255) NOT NULL COMMENT '下载用户；对应用户账号',
  `download_begin_time` timestamp NOT NULL COMMENT '开始时间',
  `download_end_time` timestamp NOT NULL COMMENT '结束时间',
  `using` tinyint(1) NOT NULL COMMENT '是否删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of download_log
-- ----------------------------

-- ----------------------------
-- Table structure for login_log
-- ----------------------------
DROP TABLE IF EXISTS `login_log`;
CREATE TABLE `login_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【登录日志】id',
  `user_account` varchar(255) NOT NULL COMMENT '用户名；管理员或用户名(admin或user的user_id字段)',
  `login_type` varchar(255) NOT NULL COMMENT '登录类型；三个客户端软件：分发管理，下载，水印提取',
  `login_time` timestamp NOT NULL COMMENT '登录时间',
  `login_ip` varchar(255) NOT NULL COMMENT '登录IP',
  `success` tinyint(1) NOT NULL COMMENT '是否成功',
  `failure_reason` tinyint(1) NOT NULL COMMENT '失败原因；无此用户，密码不匹配，IP不匹配',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of login_log
-- ----------------------------

-- ----------------------------
-- Table structure for organization
-- ----------------------------
DROP TABLE IF EXISTS `organization`;
CREATE TABLE `organization` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【单位】id',
  `account` varchar(255) NOT NULL COMMENT '单位变码；唯一，00表示总部，00XX表示下属单位，依次类推',
  `name` varchar(255) NOT NULL COMMENT '单位名称',
  `responsible_name` varchar(255) NOT NULL COMMENT '单位负责人姓名',
  `responsible_phone` int(40) NOT NULL COMMENT '单位负责人电话',
  `organization_duty_phone` int(40) NOT NULL COMMENT '单位值班电话',
  `father_organization_id` varchar(255) NOT NULL COMMENT '父单位id',
  `using` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of organization
-- ----------------------------
INSERT INTO `organization` VALUES ('1', '00', '总部', '负责人1', '1325546', '4654654', '00', '1');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【用户】id',
  `uuid` varchar(255) NOT NULL COMMENT '用户编号；唯一，UUID',
  `account` varchar(255) NOT NULL COMMENT '账号',
  `password` varchar(255) NOT NULL COMMENT '密码；SHA-256',
  `ip` varchar(255) NOT NULL COMMENT 'IP；绑定IP地址',
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `organization_account` varchar(255) NOT NULL COMMENT '单位；对应单位编码',
  `using` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user
-- ----------------------------

-- ----------------------------
-- Table structure for video
-- ----------------------------
DROP TABLE IF EXISTS `video`;
CREATE TABLE `video` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【视频】id',
  `uuid` varchar(255) NOT NULL COMMENT '编号；唯一，UUID，同时也是文件名，原始问价、加密我呢见、缩略图、加密密钥分别存放在不同文件夹内',
  `title` varchar(255) NOT NULL COMMENT '标题；',
  `upload_organization_account` varchar(255) NOT NULL COMMENT '上传单位；对应单位编码',
  `upload_admin_user_account` varchar(255) NOT NULL COMMENT '上传管理员；对应管理员用户名',
  `upload_time` timestamp NOT NULL COMMENT '上传时间',
  `allow_play_time` timestamp NOT NULL COMMENT '播放时限；该日期的24点前允许播放',
  `original_file_size` bigint(20) NOT NULL COMMENT '原始文件大小；字节为单位',
  `encrypt_file_size` bigint(20) NOT NULL COMMENT '加密后文件大小；字节为单位，与原始文件相同文件名',
  `release_allow` tinyint(1) NOT NULL COMMENT '是否发布',
  `release_admin_user_account` varchar(255) NOT NULL DEFAULT '' COMMENT '发布管理员；对应管理员用户名',
  `release_time` timestamp NOT NULL COMMENT '发布时间',
  `delete_admin_user_account` varchar(255) NOT NULL COMMENT '删除管理员；对应管理员用户名',
  `delete_time` timestamp NOT NULL COMMENT '删除时间',
  `secret_key` varchar(255) NOT NULL COMMENT '密钥',
  `using` tinyint(1) NOT NULL COMMENT '是否删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of video
-- ----------------------------

-- ----------------------------
-- Table structure for watermark_log
-- ----------------------------
DROP TABLE IF EXISTS `watermark_log`;
CREATE TABLE `watermark_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【水印记录】id',
  `watermark` varchar(255) NOT NULL COMMENT '水印',
  `video_uuid` varchar(255) NOT NULL COMMENT '视频；对应视频编号',
  `organization_account` varchar(255) NOT NULL COMMENT '单位；对应单位编码',
  `user_uuid` varchar(255) NOT NULL COMMENT '用户；对应用户编号',
  `ip` varchar(255) NOT NULL COMMENT 'IP',
  `time` timestamp NOT NULL COMMENT '时间',
  `using` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of watermark_log
-- ----------------------------
