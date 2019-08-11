ALTER TABLE `watermark_logs`
MODIFY COLUMN `time`  timestamp NULL COMMENT '时间' AFTER `ip`;

