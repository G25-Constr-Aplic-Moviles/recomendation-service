# Recommendation Service API

## Descripción

El **Recommendation Service API** es una API construida con Flask que recomienda restaurantes a los usuarios basándose en su historial de visitas. El sistema extrae las tres modas de los restaurantes más visitados por el usuario y sugiere dos restaurantes adicionales por cada tipo de cocina de los restaurantes más frecuentados.

## Endpoints

### 1. Obtener recomendaciones de restaurantes para un usuario

- **Ruta**: `/recommend/<user_id>`
- **Método**: `GET`
- **Descripción**: Este endpoint retorna una lista de recomendaciones de 6 restaurantes basados en los restaurantes más frecuentados por el usuario.

#### Proceso:

1. Se consulta el historial de visitas del usuario haciendo una petición a `https://history-service-7d9c8283d538.herokuapp.com/history/{user_id}`.
2. Se calculan los 3 restaurantes más visitados por el usuario (moda de `restaurant_id`).
3. Para cada uno de estos restaurantes, se hace una petición al endpoint `https://restaurantservice-375afbe356dc.herokuapp.com/restaurant/{restaurant_id}` para obtener el atributo `cuisine_type`.
4. Con cada `cuisine_type`, se consulta la lista de restaurantes similares en `https://restaurantservice-375afbe356dc.herokuapp.com/restaurant/list/{cuisine_type}`.
5. Finalmente, se seleccionan aleatoriamente 2 restaurantes por cada tipo de cocina, resultando en un total de 6 restaurantes que se retornan al usuario.
