from flask import Response, request
from apicore import api, Http501Exception, Http403Exception


@api.route('/oas/test/', methods=['POST'])
@api.validate
def aosTest():
    """
    common_responses:
        400:
         description: Invalid request
        401:
          description: Authentification required
        406:
          description: Nothing to send maching Access-* headers
        500:
          description: Server internal error
    ---
      tags:
        - transation
      summary: Perfom a transaction by using a code
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - amount
                - code
              properties:
                amount:
                  title: Montant en Francs CFA à dépenser chez le commerçant
                  type: number
                  example: 35000.00
                code:
                  title: Code du destinataire utilisé pour la transaction
                  type: string
                  example: 35-768-99
        required: true
      responses:
        201:
          description: Created
          content:
            application/json:
              schema:
                type: object
                properties:
                  uuid:
                    title: Unique identifier of the created transaction
                    type: string
                    format: uuid
                    example: 59f226c110cd249a8d4a7fd7
        403:
          description: Max amount exceeded
        404:
            description: Invalid code
    """
    return "OK!!"
