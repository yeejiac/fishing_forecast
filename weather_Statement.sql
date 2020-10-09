-- --------------------------------------------------------
-- 主機:                           127.0.0.1
-- 伺服器版本:                        10.5.5-MariaDB - mariadb.org binary distribution
-- 伺服器作業系統:                      Win64
-- HeidiSQL 版本:                  11.0.0.5919
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 傾印 weather_data 的資料庫結構
CREATE DATABASE IF NOT EXISTS `weather_data` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `weather_data`;

-- 傾印  資料表 weather_data.tide_table 結構
CREATE TABLE IF NOT EXISTS `tide_table` (
  `index` bigint(20) DEFAULT NULL,
  `DISTRICT` text DEFAULT NULL,
  `DAY` text DEFAULT NULL,
  `TIME` text DEFAULT NULL,
  `Wx` text DEFAULT NULL,
  `WinDir` text DEFAULT NULL,
  `WindSpeed` text DEFAULT NULL,
  `WaveHeight` text DEFAULT NULL,
  `WaveType` text DEFAULT NULL,
  KEY `ix_tide_Table_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 取消選取資料匯出。

-- 傾印  資料表 weather_data.weather_table 結構
CREATE TABLE IF NOT EXISTS `weather_table` (
  `index` bigint(20) DEFAULT NULL,
  `CITY` text DEFAULT NULL,
  `DISTRICT` text DEFAULT NULL,
  `GEOCODE` text DEFAULT NULL,
  `DAY` text DEFAULT NULL,
  `TIME` text DEFAULT NULL,
  `T` text DEFAULT NULL,
  `TD` text DEFAULT NULL,
  `RH` text DEFAULT NULL,
  `WD` text DEFAULT NULL,
  `Wind` text DEFAULT NULL,
  `Wx` text DEFAULT NULL,
  `PoP12h` text DEFAULT NULL,
  KEY `ix_weather_Table_index` (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 取消選取資料匯出。

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
