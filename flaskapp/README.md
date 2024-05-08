### README para la API de Gestión del Carrito

#### Descripción General
Esta API ofrece un conjunto de puntos de acceso para gestionar un carrito de compras en una plataforma de comercio electrónico, utilizando Redis como almacén de datos en el backend. Los usuarios pueden añadir elementos a su carrito, obtener el contenido del carrito y eliminar su carrito.


#### Uso de la API
- **Agregar al Carrito**
  - **POST** `/cart`
  - Carga útil: `{ "user_id": "123", "item_id": "item123", "quantity": 2 }`
  - Añade un artículo al carrito del usuario. Si la cantidad es cero o negativa, se elimina el artículo del carrito.

- **Obtener Carrito**
  - **GET** `/cart`
  - Carga útil: `{ "user_id": "123" }`
  - Recupera el contenido del carrito del usuario.

- **Eliminar Carrito**
  - **DELETE** `/cart`
  - Carga útil: `{ "user_id": "123" }`
  - Elimina el carrito del usuario.

#### Notas
- La aplicación utiliza un hilo separado para limpiar los carritos antiguos no utilizados si exceden un límite predefinido.
