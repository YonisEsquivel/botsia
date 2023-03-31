-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.30 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para dbbotsia
CREATE DATABASE IF NOT EXISTS `dbbotsia` /*!40100 DEFAULT CHARACTER SET armscii8 COLLATE armscii8_bin */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbbotsia`;

-- Volcando estructura para tabla dbbotsia.config_emas
CREATE TABLE IF NOT EXISTS `config_emas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idsettings` int NOT NULL,
  `periods` int NOT NULL,
  `colors` varchar(15) CHARACTER SET armscii8 COLLATE armscii8_bin DEFAULT NULL,
  `decimals` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idsettings` (`idsettings`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla dbbotsia.config_emas: ~2 rows (aproximadamente)
INSERT INTO `config_emas` (`id`, `idsettings`, `periods`, `colors`, `decimals`) VALUES
	(1, 1, 14, 'white', 0),
	(2, 2, 14, 'white', 0);

-- Volcando estructura para tabla dbbotsia.config_smas
CREATE TABLE IF NOT EXISTS `config_smas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idsettings` int NOT NULL,
  `periods` int NOT NULL,
  `colors` varchar(15) COLLATE armscii8_bin DEFAULT NULL,
  `decimals` float DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idsettings` (`idsettings`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla dbbotsia.config_smas: ~6 rows (aproximadamente)
INSERT INTO `config_smas` (`id`, `idsettings`, `periods`, `colors`, `decimals`) VALUES
	(1, 1, 15, 'green', 0),
	(2, 1, 25, 'yellow', 0),
	(3, 1, 50, 'blue', 0),
	(4, 2, 15, 'green', 2),
	(5, 2, 25, 'yellow', 0),
	(6, 2, 50, 'blue', 0);

-- Volcando estructura para tabla dbbotsia.settings
CREATE TABLE IF NOT EXISTS `settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `periodo_graph` int NOT NULL DEFAULT '0',
  `longitud_graph` int NOT NULL DEFAULT '0',
  `interval_klines` varchar(3) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla dbbotsia.settings: ~1 rows (aproximadamente)
INSERT INTO `settings` (`id`, `periodo_graph`, `longitud_graph`, `interval_klines`) VALUES
	(1, 200, 150, '5m');

-- Volcando estructura para tabla dbbotsia.settingsymbols
CREATE TABLE IF NOT EXISTS `settingsymbols` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbols` varchar(50) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `decimals` float NOT NULL DEFAULT '0',
  `porcent_profit` float NOT NULL DEFAULT '0',
  `periodo_trend` int NOT NULL DEFAULT '0',
  `periodo_momentum` int NOT NULL DEFAULT '0',
  `period_rsi` int NOT NULL DEFAULT '0',
  `decimal_rsi` float NOT NULL DEFAULT '0',
  `color_rsi` varchar(15) CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `porcent_over_sma` float NOT NULL DEFAULT '0',
  `porcent_low_sma` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- Volcando datos para la tabla dbbotsia.settingsymbols: ~2 rows (aproximadamente)
INSERT INTO `settingsymbols` (`id`, `symbols`, `decimals`, `porcent_profit`, `periodo_trend`, `periodo_momentum`, `period_rsi`, `decimal_rsi`, `color_rsi`, `porcent_over_sma`, `porcent_low_sma`) VALUES
	(1, 'BTCUSDT', 0.8, 0.7, 14, 14, 14, 0.2, 'orange', 0.002, 0.002),
	(2, 'BNBUSDT', 0.2, 0.7, 14, 14, 14, 0.2, 'orange', 0.002, 0.002);

-- Volcando estructura para tabla dbbotsia.spot_entry_points
CREATE TABLE IF NOT EXISTS `spot_entry_points` (
  `id` int NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) COLLATE armscii8_bin NOT NULL DEFAULT '0',
  `price` varchar(50) COLLATE armscii8_bin NOT NULL DEFAULT '0',
  `emas` varchar(200) CHARACTER SET armscii8 COLLATE armscii8_bin DEFAULT '',
  `smas` varchar(200) CHARACTER SET armscii8 COLLATE armscii8_bin DEFAULT '',
  `action` char(5) COLLATE armscii8_bin NOT NULL DEFAULT '0',
  `strategy` varchar(200) CHARACTER SET armscii8 COLLATE armscii8_bin DEFAULT '0',
  `porcent_low_over_sma` float NOT NULL DEFAULT '0',
  `date_time` datetime NOT NULL,
  `status` char(1) COLLATE armscii8_bin NOT NULL DEFAULT 'O',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla dbbotsia.spot_response_order
CREATE TABLE IF NOT EXISTS `spot_response_order` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_entry_point` int DEFAULT '0',
  `id_orden_open` int DEFAULT '0',
  `response` text CHARACTER SET armscii8 COLLATE armscii8_bin NOT NULL,
  `date_response` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla dbbotsia.spot_trading_open
CREATE TABLE IF NOT EXISTS `spot_trading_open` (
  `orderId` int NOT NULL AUTO_INCREMENT,
  `id_entry_point_open` int NOT NULL DEFAULT '0',
  `id_entry_point_close` int NOT NULL DEFAULT '0',
  `symbol` varchar(10) COLLATE armscii8_bin NOT NULL DEFAULT '0',
  `open` varchar(50) COLLATE armscii8_bin NOT NULL DEFAULT '0',
  `close` varchar(50) CHARACTER SET armscii8 COLLATE armscii8_bin DEFAULT '0',
  `usdt_open` float NOT NULL DEFAULT '0',
  `usdt_close` float DEFAULT '0',
  `quantity` varchar(50) COLLATE armscii8_bin NOT NULL DEFAULT '0',
  `profit` float DEFAULT '0',
  `date_time_open` datetime NOT NULL,
  `date_time_close` datetime DEFAULT NULL,
  `status` char(1) COLLATE armscii8_bin NOT NULL DEFAULT 'O',
  `comment` text COLLATE armscii8_bin,
  PRIMARY KEY (`orderId`) USING BTREE,
  KEY `id_entry_point_open` (`id_entry_point_open`),
  KEY `id_entry_point_close` (`id_entry_point_close`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=armscii8 COLLATE=armscii8_bin;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
