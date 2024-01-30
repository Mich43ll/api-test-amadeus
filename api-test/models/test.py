import amadeus


def obtener_vuelos(codigo_origen, codigo_destino):
    amadeus_client = amadeus.Client(
        client_id="nT2gsA6YR4YBZVKUgzX76VdfHmjMH3WP", client_secret="sFxY0IU2aMsyaMnc"
    )

    try:
        response = amadeus_client.shopping.flight_offers_search.get(
            originLocationCode=codigo_origen,
            destinationLocationCode=codigo_destino,
            departureDate="2024-03-02",
            adults=1,
        )

        vuelos = response.data

        for vuelo in vuelos:
            precio = vuelo["price"]["total"]
            fecha_salida = vuelo["itineraries"][0]["segments"][0]["departure"]["at"]
            aerolinea = vuelo["itineraries"][0]["segments"][0]["operating"][
                "carrierCode"
            ]
            if not aerolinea: 
                aerolinea = "No encontrada"

            print(f"Fecha de salida: {fecha_salida}")
            print(f"Precio: {precio}")
            print(f"Aerolínea: {aerolinea}")
            print()

    except amadeus.ResponseError as error:
        print(error)


obtener_vuelos("MAD", "NYC")
