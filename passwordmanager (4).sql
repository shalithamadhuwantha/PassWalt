-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 06, 2025 at 04:19 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `passwordmanager`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
CREATE TABLE IF NOT EXISTS `accounts` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `service_name` varchar(100) NOT NULL,
  `account_user` varchar(100) NOT NULL,
  `password_enc` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `date_added` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `user_id`, `service_name`, `account_user`, `password_enc`, `created_at`, `date_added`) VALUES
(3, 2, 'smg', 'admin2', 'gAAAAABotfLo_OwqlnRCGDRxah-08Grozoiu5ofE6Z9qidhpsiQnl2lbjzzrWR3w-lzzbcg9AOQZPnq1xN95amKfYvoMbIQgwQ==', '2025-09-02 00:54:24', '2025-09-01 19:24:24'),
(4, 5, 'my facebook', 'admin2', 'gAAAAABou7kgmLv137DxsfsLHd-MhTWgOcWgE6xerwWqdA8TKzwZWYWyTrt-s0G4ysfKB9n4OzXlnlCATnhhrR_CfWZRGm4DnA==', '2025-09-06 10:01:28', '2025-09-06 04:31:28'),
(5, 5, 'my gmail', 'test@email.com', 'gAAAAABou7lFdyzdEcklQV3W5zrLzC-VRx13lB96_t49kqoS-CXVcgfF1ukXs6vfeDORbRpqUIaXV_E5b2iN8ZN5N7OQJt9x0A==', '2025-09-06 10:02:05', '2025-09-06 04:32:05');

-- --------------------------------------------------------

--
-- Table structure for table `loginmonitor`
--

DROP TABLE IF EXISTS `loginmonitor`;
CREATE TABLE IF NOT EXISTS `loginmonitor` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `login_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `device_info` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `loginmonitor`
--

INSERT INTO `loginmonitor` (`log_id`, `user_id`, `login_time`, `ip_address`, `status`, `device_info`) VALUES
(26, 2, '2025-09-06 10:08:38', '127.0.0.1', 'Success', NULL),
(25, 2, '2025-09-06 10:07:57', '127.0.0.1', 'Success', NULL),
(24, 2, '2025-09-06 10:06:19', '127.0.0.1', 'Failed', NULL),
(23, 2, '2025-09-06 10:06:07', '127.0.0.1', 'Failed', NULL),
(22, 5, '2025-09-06 09:59:54', '127.0.0.1', 'Success', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `passwordlogs`
--

DROP TABLE IF EXISTS `passwordlogs`;
CREATE TABLE IF NOT EXISTS `passwordlogs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `action` varchar(50) NOT NULL,
  `account_id` int DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  KEY `user_id` (`user_id`),
  KEY `account_id` (`account_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `master_pass` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `master_pass`, `email`, `created_at`) VALUES
(2, 'admin', '$2a$12$Vy3P4jMDLLDlvRqKehr55OSKVfTKU4BC4TsedRPJYVG.IJXvir96C', 'bbsmgamage@gmail.com', '2025-09-02 00:53:23'),
(5, 'shalitha2', '$2b$12$fmOpjaIzMnuVOfkJloFwvOx7gnR.zMkHx0mKDVQaLTsv47mHa4bFG', 'bbsmgamageuni@gmail.com', '2025-09-06 09:59:39');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
