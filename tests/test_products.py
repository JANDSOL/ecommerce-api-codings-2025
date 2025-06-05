from fastapi.testclient import (
    TestClient,
)  # Importa cliente para hacer requests HTTP a la app FastAPI en tests
from main import app  # Importa la aplicación FastAPI definida en main.py

# Ruta del servicio que queremos "mockear" (sustituir temporalmente) durante los tests
path_to_service = "services.product_service.ProductService"

# Crea un cliente de pruebas que usará la app FastAPI para hacer peticiones simuladas
client = TestClient(app)


# Test para cuando no hay productos en la base de datos (lista vacía)
def test_get_products_empty_list(monkeypatch):
    # Definimos una función mock que simula que list_products siempre devuelve lista vacía
    def mock_list_products(*args, **kwargs):
        return []

    # Con monkeypatch reemplazamos la función original por la mock durante este test
    monkeypatch.setattr(path_to_service + ".list_product", mock_list_products)

    # Hacemos una petición GET al endpoint real de productos
    response = client.get("/api/v1/products/")

    # Comprobamos que la respuesta tenga código HTTP 200 (OK)
    assert response.status_code == 200

    # Comprobamos que el contenido JSON de la respuesta sea una lista vacía (como esperábamos)
    assert response.json() == []


# Test para cuando hay productos disponibles, simulamos la respuesta del servicio con datos concretos
def test_get_products_with_data(monkeypatch):
    # Definimos un mock que retorna una lista con un producto con datos específicos
    def mock_list_products(*args, **kwargs):
        return [
            {
                "id": 1,
                "title": "Producto X",
                "image": "/uploaded/images/xyz.jpg",
                "seller_full_name": "Ana López",
                "price": 29.99,
                "rating": 4.0,
            }
        ]

    # Reemplazamos el método list_products con nuestro mock para este test
    monkeypatch.setattr(path_to_service + ".list_product", mock_list_products)

    # Ejecutamos la petición GET al endpoint de productos
    response = client.get("/api/v1/products/")

    # Validamos que la respuesta tenga código HTTP 200 OK
    assert response.status_code == 200

    # Guardamos la respuesta JSON para validaciones posteriores
    data = response.json()

    # Validamos que la respuesta sea una lista
    assert isinstance(data, list)

    # Validamos que la lista tenga un solo producto
    assert len(data) == 1

    # Validamos que el título del producto sea el esperado "Producto X"
    assert data[0]["title"] == "Producto X"


# Test para validar que el endpoint maneja mal las query params inválidas correctamente
def test_get_products_invalid_query_params():
    # Hacemos una petición GET con parámetros query inválidos (no enteros) para page y limit-per-page
    response = client.get("/api/v1/products/?page=abc&limit-per-page=xyz")

    # Validamos que la respuesta sea un error 422 (Unprocessable Entity) generado por FastAPI
    assert response.status_code == 422

    # Guardamos el cuerpo JSON de la respuesta para validar detalles del error
    body = response.json()

    # Validamos que el body tiene una clave "detail" (que contiene info sobre el error)
    assert "detail" in body

    # Validamos que "detail" sea una lista (FastAPI reporta errores de validación como lista)
    assert isinstance(body["detail"], list)

    # Extraemos los campos que generaron error de validación (page y limit-per-page)
    error_fields = {err["loc"][-1] for err in body["detail"]}

    # Comprobamos que entre esos campos están "page" y "limit-per-page"
    assert "page" in error_fields
    assert "limit-per-page" in error_fields
