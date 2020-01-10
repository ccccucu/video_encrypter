-- MySQL dump 10.13  Distrib 8.0.18, for osx10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: video_encrypter
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `distribut_videos`
--

DROP TABLE IF EXISTS `distribut_videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `distribut_videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【分发单位】id',
  `video_id` int(11) NOT NULL DEFAULT '0' COMMENT '视频表的id',
  `video_uuid` varchar(255) NOT NULL DEFAULT '' COMMENT '视频；对应视频编号',
  `organization_id` int(11) NOT NULL COMMENT '单位id；对应单位id，若为“0”则表示所有单位均可下载',
  `organization_account` varchar(255) NOT NULL DEFAULT '' COMMENT '单位；对应单位编码，若为“ALL”则表示所有单位均可下载',
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  `updated_by` varchar(255) NOT NULL DEFAULT '',
  `created_by` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `download_logs`
--

DROP TABLE IF EXISTS `download_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `login_logs`
--

DROP TABLE IF EXISTS `login_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `organizations`
--

DROP TABLE IF EXISTS `organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `videos`
--

DROP TABLE IF EXISTS `videos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `videos` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '【视频】id',
  `uuid` varchar(255) NOT NULL DEFAULT '' COMMENT '编号；唯一，UUID，同时也是文件名，原始问价、加密我呢见、缩略图、加密密钥分别存放在不同文件夹内',
  `title` varchar(255) NOT NULL DEFAULT '' COMMENT '标题；',
  `upload_organization_id` int(11) NOT NULL COMMENT '上传单位id；对应单位id',
  `upload_admin_id` int(11) NOT NULL DEFAULT '0' COMMENT '上传管理员di；对应管理员id',
  `allow_play_time` timestamp NOT NULL COMMENT '播放时限；该日期的24点前允许播放',
  `original_file_size` float NOT NULL DEFAULT '0' COMMENT '原始文件大小；字节为单位',
  `encrypt_file_size` bigint(20) NOT NULL DEFAULT '0' COMMENT '加密后文件大小；字节为单位，与原始文件相同文件名',
  `release_allow` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否发布',
  `secret_key` varchar(255) NOT NULL DEFAULT '' COMMENT '密钥',
  `release_time` timestamp NOT NULL COMMENT '发布时间',
  `delete_admin_id` int(11) DEFAULT '0' COMMENT '删除管理员id；对应管理员id',
  `thumb_filename` varchar(255) NOT NULL DEFAULT '' COMMENT '缩略图名字',
  `updated_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL COMMENT '上传时间',
  `updated_by` varchar(255) NOT NULL DEFAULT '' COMMENT '删除管理员；对应管理员用户名',
  `created_by` varchar(255) NOT NULL DEFAULT '' COMMENT '上传管理员；对应管理员用户名',
  `release_admin_id` int(11) DEFAULT '0' COMMENT '发布管理员id；对应管理员id',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '是否删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `watermark_logs`
--

DROP TABLE IF EXISTS `watermark_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-10 14:56:24
