import unittest

from app import validar_datos_producto


class ValidarDatosProductoTests(unittest.TestCase):
    def test_eliminar_espacios_y_formato_valido(self):
        errores = validar_datos_producto({
            "codigo": "  P900  ",
            "nombre": "  Teclado Mecánico  ",
            "precio": " 50000 ",
            "categoria": "  Periféricos  ",
        })
        self.assertEqual([], errores)

    def test_campos_vacios(self):
        errores = validar_datos_producto({
            "codigo": "",
            "nombre": "   ",
            "precio": "",
            "categoria": "",
        })
        self.assertIn("El código del producto es obligatorio.", errores)
        self.assertIn("El nombre del producto es obligatorio.", errores)
        self.assertIn("El precio del producto es obligatorio.", errores)
        self.assertIn("La categoría es obligatoria.", errores)

    def test_precio_mayor_que_cero(self):
        errores = validar_datos_producto({
            "codigo": "P002",
            "nombre": "Mouse",
            "precio": "0",
            "categoria": "Accesorios",
        })
        self.assertIn("El precio debe ser mayor que cero.", errores)

    def test_codigo_duplicado(self):
        errores = validar_datos_producto({
            "codigo": "P001",
            "nombre": "Mouse",
            "precio": "10000",
            "categoria": "Accesorios",
        })
        self.assertIn("El código del producto ya existe.", errores)

    def test_codigo_minimo_cinco_caracteres(self):
        errores = validar_datos_producto({
            "codigo": "P01",
            "nombre": "Mouse",
            "precio": "10000",
            "categoria": "Accesorios",
        })
        self.assertIn("El código debe tener al menos 5 caracteres.", errores)

    def test_nombre_minimo_cinco_caracteres(self):
        errores = validar_datos_producto({
            "codigo": "P005",
            "nombre": "Hola",
            "precio": "10000",
            "categoria": "Accesorios",
        })
        self.assertIn("El nombre debe tener al menos 5 caracteres.", errores)

    def test_formato_codigo(self):
        errores = validar_datos_producto({
            "codigo": "ABC123",
            "nombre": "Teclado",
            "precio": "50000",
            "categoria": "Periféricos",
        })
        self.assertIn("El código debe tener el formato P001.", errores)

    def test_precio_extremadamente_alto(self):
        errores = validar_datos_producto({
            "codigo": "P010",
            "nombre": "Monitor",
            "precio": "6000000",
            "categoria": "Periféricos",
        })
        self.assertIn("El precio no puede ser mayor a 5000000.", errores)

    def test_nombre_demasiado_largo(self):
        errores = validar_datos_producto({
            "codigo": "P011",
            "nombre": "x" * 101,
            "precio": "10000",
            "categoria": "Accesorios",
        })
        self.assertIn("El nombre no puede exceder los 100 caracteres.", errores)


if __name__ == "__main__":
    unittest.main()
