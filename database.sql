SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_bot_config
-- ----------------------------
DROP TABLE IF EXISTS `tb_bot_config`;
CREATE TABLE `tb_bot_config`  (
  `current_qq` bigint(20) NOT NULL COMMENT '机器人QQ',
  `master_qq` bigint(20) NULL DEFAULT NULL COMMENT '主人QQ',
  PRIMARY KEY (`current_qq`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of tb_bot_config
-- ----------------------------
INSERT INTO `tb_bot_config` VALUES (123456, 10001);
-- ----------------------------
-- Table structure for tb_friendlist
-- ----------------------------
DROP TABLE IF EXISTS `tb_friendlist`;
CREATE TABLE `tb_friendlist`  (
  `FriendUin` bigint(20) NOT NULL,
  `IsRemark` tinyint(1) NULL DEFAULT NULL,
  `NickName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `OnlineStr` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `Remark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `Status` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`FriendUin`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tb_good_morning
-- ----------------------------
DROP TABLE IF EXISTS `tb_good_morning`;
CREATE TABLE `tb_good_morning`  (
  `uin` bigint(20) NOT NULL,
  `nick_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `group_id` bigint(20) NULL DEFAULT NULL,
  `group_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `model` int(11) NULL DEFAULT NULL,
  `time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`uin`) USING BTREE,
  INDEX `tb_good_morning_Idx_Time`(`time`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tb_group_member
-- ----------------------------
DROP TABLE IF EXISTS `tb_group_member`;
CREATE TABLE `tb_group_member`  (
  `GroupUin` bigint(20) NOT NULL,
  `MemberUin` bigint(20) NOT NULL,
  `Age` int(11) NULL DEFAULT NULL,
  `AutoRemark` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `CreditLevel` int(11) NULL DEFAULT NULL,
  `Email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `FaceId` int(11) NULL DEFAULT NULL,
  `Gender` int(11) NULL DEFAULT NULL,
  `GroupAdmin` int(11) NULL DEFAULT NULL,
  `GroupCard` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `JoinTime` int(11) NULL DEFAULT NULL,
  `LastSpeakTime` int(11) NULL DEFAULT NULL,
  `MemberLevel` int(11) NULL DEFAULT NULL,
  `Memo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `NickName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `ShowName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `SpecialTitle` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `Status` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`GroupUin`, `MemberUin`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tb_trooplist
-- ----------------------------
DROP TABLE IF EXISTS `tb_trooplist`;
CREATE TABLE `tb_trooplist`  (
  `GroupId` bigint(20) NOT NULL,
  `GroupMemberCount` int(11) NULL DEFAULT NULL,
  `GroupName` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `GroupNotice` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `GroupOwner` bigint(20) NULL DEFAULT NULL,
  `GroupTotalCount` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`GroupId`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
