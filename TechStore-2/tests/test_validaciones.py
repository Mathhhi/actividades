import unittest

from app import validar_datos_producto


class ValidarDatosProductoTests(unittest.TestCase):
    def test_codigo_solo_numeros(self):
        errores = validar_datos_producto({
            "codigo": "ABC123",
            "nombre": "Teclado",
            "precio": "50000",
            "categoria": "Periféricos",
        })
        self.assertIn("El código del producto solo debe contener números.", errores)

    def test_precio_no_negativo(self):
        errores = validar_datos_producto({
            "codigo": "123",
            "nombre": "Teclado",
            "precio": "-100",
            "categoria": "Periféricos",
        })
        self.assertIn("El precio no puede ser negativo.", errores)

    def test_nombre_no_acepta_numeros(self):
        errores = validar_datos_producto({
            "codigo": "123",
            "nombre": "Teclado 123",
            "precio": "50000",
            "categoria": "Periféricos",
        })
        self.assertIn("El nombre no debe contener números.", errores)

    def test_precio_con_formato_invalido(self):
        errores = validar_datos_producto({
            "codigo": "123",
            "nombre": "Teclado",
            "precio": "1e3",
            "categoria": "Periféricos",
        })
        self.assertIn("El precio debe ser un número válido.", errores)

    def test_datos_validos(self):
        errores = validar_datos_producto({
            "codigo": "123",
            "nombre": "Teclado Mecánico",
            "precio": "50000",
            "categoria": "Periféricos",
        })
        self.assertEqual([], errores)


if __name__ == "__main__":
    unittest.main()
