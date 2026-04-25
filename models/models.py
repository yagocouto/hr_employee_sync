import requests
import logging
import json
from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class HrEmployeeSync(models.Model):
    _inherit = "hr.employee"

    def action_buscar_api(self):
        self.ensure_one()

        if not self.work_email:
            raise UserError("Informe o email antes de efetuar a buscar.")

        url = f"https://randomuser.me/api/?seed={self.work_email}"

        try:
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                raise Exception("Erro na API")

            data = response.json()
            user = data["results"][0]

            full_name = f"{user['name']['first']} {user['name']['last']}"

            self.write(
                {
                    "name": full_name,
                    "mobile_phone": user.get("cell"),
                    "private_phone": user.get("phone"),
                    "private_email": user.get("email"),
                    "sex": user.get("gender"),
                }
            )

            _logger.info(
                "Resposta completa da API:\n%s",
                json.dumps(data, indent=4, ensure_ascii=False),
            )

        except Exception as e:
            raise Exception(f"Erro ao buscar API: {str(e)}")
