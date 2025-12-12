-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-12-2025 a las 03:46:38
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_baron_rojo`
--
CREATE DATABASE IF NOT EXISTS `bd_baron_rojo` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `bd_baron_rojo`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detail_order`
--

CREATE TABLE `detail_order` (
  `id_detail_order` int(11) NOT NULL,
  `amount` int(3) NOT NULL,
  `id_product` int(11) NOT NULL,
  `id_order` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detail_order`
--

INSERT INTO `detail_order` (`id_detail_order`, `amount`, `id_product`, `id_order`) VALUES
(1, 5, 1, 1),
(2, 1, 12, 1),
(3, 10, 1, 2),
(4, 1, 11, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingredients`
--

CREATE TABLE `ingredients` (
  `id_ingredients` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `measurement_unit` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ingredients`
--

INSERT INTO `ingredients` (`id_ingredients`, `name`, `measurement_unit`) VALUES
(1, 'Tortilla de harina', 'u'),
(2, 'Tortilla de maiz', 'u'),
(3, 'Carne asada', 'g'),
(4, 'Carne adobada', 'g'),
(5, 'Queso', 'g');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingredients_details`
--

CREATE TABLE `ingredients_details` (
  `id_ingredientsdetail` int(11) NOT NULL,
  `id_ingredients` int(11) NOT NULL,
  `id_product` int(11) NOT NULL,
  `quantity` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ingredients_details`
--

INSERT INTO `ingredients_details` (`id_ingredientsdetail`, `id_ingredients`, `id_product`, `quantity`) VALUES
(34, 2, 2, 1),
(35, 4, 2, 30),
(36, 1, 3, 1),
(37, 3, 3, 75),
(40, 2, 5, 1),
(41, 3, 5, 20),
(42, 5, 5, 15),
(58, 2, 1, 1),
(59, 3, 1, 30),
(60, 1, 8, 1),
(61, 4, 8, 75),
(62, 5, 8, 50),
(63, 1, 7, 1),
(64, 3, 7, 75),
(65, 5, 7, 50),
(67, 1, 9, 2),
(68, 3, 9, 100),
(69, 4, 9, 100),
(77, 2, 6, 1),
(78, 4, 6, 20),
(79, 5, 6, 15),
(84, 2, 10, 10),
(85, 3, 10, 75),
(86, 4, 10, 75),
(87, 5, 10, 30),
(88, 1, 4, 1),
(89, 4, 4, 75);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orders`
--

CREATE TABLE `orders` (
  `id_order` int(11) NOT NULL,
  `date` date NOT NULL,
  `total` double(10,2) NOT NULL,
  `costumer_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `orders`
--

INSERT INTO `orders` (`id_order`, `date`, `total`, `costumer_name`) VALUES
(1, '2025-12-10', 115.00, 'Armando'),
(2, '2025-12-10', 225.00, 'Enrique');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id_product` int(11) NOT NULL,
  `product_name` varchar(20) NOT NULL,
  `products_category` varchar(15) NOT NULL,
  `unit_price` double(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id_product`, `product_name`, `products_category`, `unit_price`) VALUES
(1, 'Taco de asada', 'Alimentos', 20.00),
(2, 'Taco de adobada', 'Alimentos', 20.00),
(3, 'Burro de asada', 'Alimentos', 65.00),
(4, 'Burro de adobada', 'Alimentos', 65.00),
(5, 'Volcan de asada', 'Alimentos', 25.00),
(6, 'Volcan de adobada', 'Alimentos', 25.00),
(7, 'Gringa de asada', 'Alimentos', 80.00),
(8, 'Gringa de adobada', 'Alimentos', 80.00),
(9, 'El BB', 'Especiales', 140.00),
(10, 'Alambre el baron', 'Especiales', 125.00),
(11, 'Refresco', 'Bebida', 25.00),
(12, 'Agua natural', 'Bebida', 15.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id_user` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` text NOT NULL,
  `creation_date` date NOT NULL,
  `delete_date` date NOT NULL,
  `status` tinyint(1) NOT NULL,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id_user`, `username`, `password`, `creation_date`, `delete_date`, `status`, `role`) VALUES
(1, 'admin', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2025-11-14', '0000-00-00', 1, 'Administrador'),
(2, 'Carlos', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2025-12-07', '0000-00-00', 1, 'Administrador'),
(3, 'Jose', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2025-12-07', '2025-12-07', 0, 'Empleado'),
(19, 'Emi', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2025-12-10', '0000-00-00', 1, 'Empleado'),
(20, 'Cardiel', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', '2025-12-10', '0000-00-00', 1, 'Empleado'),
(21, 'Mauricio', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2025-12-10', '2025-12-10', 0, 'Administrador'),
(23, 'Luis', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', '2025-12-10', '0000-00-00', 1, 'Empleado');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `detail_order`
--
ALTER TABLE `detail_order`
  ADD PRIMARY KEY (`id_detail_order`),
  ADD KEY `id_producto` (`id_product`,`id_order`),
  ADD KEY `id_orden` (`id_order`);

--
-- Indices de la tabla `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`id_ingredients`);

--
-- Indices de la tabla `ingredients_details`
--
ALTER TABLE `ingredients_details`
  ADD PRIMARY KEY (`id_ingredientsdetail`),
  ADD KEY `id_ingredients` (`id_ingredients`),
  ADD KEY `id_product` (`id_product`);

--
-- Indices de la tabla `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id_order`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id_product`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `detail_order`
--
ALTER TABLE `detail_order`
  MODIFY `id_detail_order` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `id_ingredients` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `ingredients_details`
--
ALTER TABLE `ingredients_details`
  MODIFY `id_ingredientsdetail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=114;

--
-- AUTO_INCREMENT de la tabla `orders`
--
ALTER TABLE `orders`
  MODIFY `id_order` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id_product` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detail_order`
--
ALTER TABLE `detail_order`
  ADD CONSTRAINT `detail_order_ibfk_1` FOREIGN KEY (`id_order`) REFERENCES `orders` (`id_order`),
  ADD CONSTRAINT `detail_order_ibfk_2` FOREIGN KEY (`id_product`) REFERENCES `products` (`id_product`);

--
-- Filtros para la tabla `ingredients_details`
--
ALTER TABLE `ingredients_details`
  ADD CONSTRAINT `ingredients_details_ibfk_2` FOREIGN KEY (`id_ingredients`) REFERENCES `ingredients` (`id_ingredients`),
  ADD CONSTRAINT `ingredients_details_ibfk_3` FOREIGN KEY (`id_product`) REFERENCES `products` (`id_product`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
