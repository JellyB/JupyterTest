/*
Navicat MySQL Data Transfer

Source Server         : 电脑本地数据库
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2017-12-23 19:55:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for iask_answers
-- ----------------------------
DROP TABLE IF EXISTS `iask_answers`;
CREATE TABLE `iask_answers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `qId` varchar(255) DEFAULT NULL,
  `ansContent` varchar(2000) DEFAULT NULL,
  `questionId` varchar(255) DEFAULT NULL,
  `ansAuthor` varchar(255) DEFAULT NULL,
  `postDate` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `isGood` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2402 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for iask_questions
-- ----------------------------
DROP TABLE IF EXISTS `iask_questions`;
CREATE TABLE `iask_questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `questionId` varchar(255) DEFAULT NULL,
  `qcontent` varchar(255) DEFAULT NULL,
  `qusAuthor` varchar(255) DEFAULT NULL,
  `postDate` timestamp NULL DEFAULT NULL,
  `ansCount` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=868 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_meizitu_proxy_ip
-- ----------------------------
DROP TABLE IF EXISTS `t_meizitu_proxy_ip`;
CREATE TABLE `t_meizitu_proxy_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=289 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_meizitu_tags_url
-- ----------------------------
DROP TABLE IF EXISTS `t_meizitu_tags_url`;
CREATE TABLE `t_meizitu_tags_url` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `next_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=686 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_meizitu_tag_html_urls
-- ----------------------------
DROP TABLE IF EXISTS `t_meizitu_tag_html_urls`;
CREATE TABLE `t_meizitu_tag_html_urls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) DEFAULT NULL,
  `html_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=868 DEFAULT CHARSET=utf8;
