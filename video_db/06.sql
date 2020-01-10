ALTER TABLE videos ADD thumb_filename varchar(255) DEFAULT '' NOT NULL COMMENT '缩略图名字';
ALTER TABLE videos
  MODIFY COLUMN thumb_filename varchar(255) NOT NULL DEFAULT '' COMMENT '缩略图名字' AFTER delete_admin_id,
  MODIFY COLUMN deleted_at timestamp COMMENT '是否删除' AFTER release_admin_id,
  MODIFY COLUMN created_at timestamp COMMENT '上传时间' AFTER updated_at;
  ALTER TABLE videos MODIFY original_file_size float(11) NOT NULL DEFAULT '0' COMMENT '原始文件大小；字节为单位';