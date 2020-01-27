from google.oauth2 import id_token
from google.auth.transport import requests
import requests as py_requests
import config
from filoModules.Models.LogicReturn import LogicReturn as m_LogicReturn


class SocialsLogic:
    @staticmethod
    def fb_verify_access_token(access_token) -> m_LogicReturn:
        resp = py_requests.get(
            f"https://graph.facebook.com/app/?access_token={access_token}")

        j_resp = resp.json()
        if "error" in j_resp:
            return m_LogicReturn.f_error_msg( j_resp['error'])
        if j_resp['name'] != "Findlock":
            return m_LogicReturn.f_error_msg( "Access token is not from findlock!")
        return m_LogicReturn.f_success_msg( "Valid access token!")

    @staticmethod
    def verify_token_id(google_token_id, client_id):
        idinfo = id_token.verify_oauth2_token(
            google_token_id, requests.Request())
        if idinfo['aud'] != config.get_gcid():
            return m_LogicReturn.f_error_msg( "Could not verify audience.")

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return m_LogicReturn.f_error_msg( "Wrong issuer!")

        # returns user id
        return m_LogicReturn.f_success("Verified!", addon_data=idinfo['sub'])
