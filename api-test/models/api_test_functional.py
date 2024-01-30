from odoo import models, fields, api
from odoo.exceptions import UserError
import amadeus
from amadeus import Client, ResponseError


class AmadeusExample(models.Model):
    _name = "amadeus.example"

    departure_date = fields.Char(string="Fecha de Salida")
    price_total = fields.Float(string="Precio total")

    def obtener_vuelos(self, codigo_origen="MAD", codigo_destino="NYC"):
        amadeus_client = amadeus.Client(
            client_id="nT2gsA6YR4YBZVKUgzX76VdfHmjMH3WP",
            client_secret="sFxY0IU2aMsyaMnc",
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

                self.create(
                    {
                        "departure_date": fecha_salida,
                        "price_total": float(precio),
                    }
                )

        except amadeus.ResponseError as error:
            raise UserError("Error")
