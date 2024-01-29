from odoo import api, fields, models
from amadeus import Client, ResponseError
import logging

_logger = logging.getLogger(__name__)


class AmadeusExample(models.Model):
    _name = "amadeus.example"

    # Añade los campos necesarios
    location_id = fields.Char(string="Location ID")
    location_type = fields.Char(string="Location Type")
    location_subtype = fields.Char(string="Location Subtype")
    name = fields.Char(string="Location Name")
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")
    lgbtq = fields.Integer(string="LGBTQ Safety Score")
    medical = fields.Integer(string="Medical Safety Score")
    overall = fields.Integer(string="Overall Safety Score")
    physical_harm = fields.Integer(string="Physical Harm Safety Score")
    political_freedom = fields.Integer(string="Political Freedom Safety Score")
    theft = fields.Integer(string="Theft Safety Score")
    women = fields.Integer(string="Women Safety Score")

    amadeus = Client(
        client_id="6TzonemPmQYwuxuZl1Og9A2sJTNLcqNE", client_secret="q2qn4ag5xbcPwADt"
    )

    def get_safety_info(self, latitude, longitude):
        try:
            # Obtiene información de seguridad para una ubicación en Barcelona
            response = self.amadeus.safety.safety_rated_locations.get(
                latitude=latitude, longitude=longitude
            )
            return response.data
        except ResponseError as error:
            _logger.error("Amadeus ResponseError: %s", error)
            return False

    def get_flights(self):
        try:
            # Obtiene ofertas de vuelos; puedes ajustar los parámetros según sea necesario
            response = self.amadeus.shopping.flight_offers_search.get(
                originLocationCode="BCN",
                destinationLocationCode="MAD",
                departureDate="2024-08-01",
                adults=1,
            )
            flights_data = response.data
            for flight in flights_data:
                self.create(
                    {
                        # Mapea los campos de Amadeus con los campos de tu modelo Odoo
                        # Tendrás que ajustar estos campos según la estructura de tu modelo y los datos que devuelve Amadeus
                    }
                )
            return True
        except ResponseError as error:
            _logger.error("Amadeus ResponseError: %s", error)
            return False

    # ... resto de tu modelo ...

    def fetch_safety_info(self):
        try:
            # Suponiendo que tienes métodos para obtener las credenciales y la latitud/longitud
            latitude, longitude = self._get_location_coordinates()
            response = self.amadeus.safety.safety_rated_locations.get(latitude=latitude, longitude=longitude)
            for item in response.data:
                self.create({
                    'location_id': item['id'],
                    'location_type': item['type'],
                    'location_subtype': item['subType'],
                    'name': item['name'],
                    'latitude': item['geoCode']['latitude'],
                    'longitude': item['geoCode']['longitude'],
                    'lgbtq': item['safetyScores']['lgbtq'],
                    'medical': item['safetyScores']['medical'],
                    'overall': item['safetyScores']['overall'],
                    'physical_harm': item['safetyScores']['physicalHarm'],
                    'political_freedom': item['safetyScores']['politicalFreedom'],
                    'theft': item['safetyScores']['theft'],
                    'women': item['safetyScores']['women'],
                })
            return True
        except ResponseError as error:
            _logger.error('Amadeus ResponseError: %s', error)
            return False
