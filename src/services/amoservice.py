from datetime import datetime, time, timedelta
import re
from zoneinfo import ZoneInfo
import requests
# from src.config import BASE_URL, HEADERS, PHONE_FIELD_ID, TRIAL_DATETIME_FIELD_ID

ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImU4YzAwMzI3ZDAxYjhkMDJkZTI0ODg0MTVjMmY2NWEzOGZlYTZlMjIzNTE3NDRlYmQ3MjVjM2JkOTYxZGJlZjllMDZiNjUwMGJhZmMxNzgzIn0.eyJhdWQiOiI3YWE2MWViMy1jMTMzLTQ3MDEtYTY3NC00N2UwMGNiNWE1MGQiLCJqdGkiOiJlOGMwMDMyN2QwMWI4ZDAyZGUyNDg4NDE1YzJmNjVhMzhmZWE2ZTIyMzUxNzQ0ZWJkNzI1YzNiZDk2MWRiZWY5ZTA2YjY1MDBiYWZjMTc4MyIsImlhdCI6MTc3OTA4ODg4NiwibmJmIjoxNzc5MDg4ODg2LCJleHAiOjE3OTg3NjE2MDAsInN1YiI6IjEyOTA2NTQ2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMyNjI4MDYyLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiN2Q4ODQ1MWQtYzIyYS00OWQ4LWIzODEtNzEwMmJkMjUzMzAyIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.BuTKJh8_p_3UXx5YHuylUjdLP-oJbL_rFOWFh7GLUzpp3rpFq143lOYYrEUKX3vwN6KjQaCU27MD1Nwh4DjDVgCdhfiw46r4TAvFg4azcMrNoOyrTslaFMjv55kRGBUgFBP_vJ69-oTT5AYfkkpvCaEZC1VwAEC1ecYbBUuIGGvrMNmuxPU-hnbYL0aFVbu6e4RAgjg-JF2XieE9HTKfm7YldMQv23HmrdkJZO1uTxOc03S9vEKE_-hXRhwW_S9-Xvlf4ZNMkr7oa2FeQ_1VgwI6XCcBtYizzmaZyTkjm4vNlniyR6oHNWjbl72X5k1ULhdrUddqm_HNCOkXSKtIoQ"
BASE_URL = "https://makebeatschool.amocrm.ru"
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}
PHONE_FIELD_ID = 3371021
# TRIAL_DATETIME_FIELD_ID = 3372431
TRIAL_DATETIME_FIELD_ID = 3401955 

TZ = ZoneInfo("Europe/Oslo")

def _normalize_phone(phone: str) -> str:
    return re.sub(r"\D+", "", phone or "")

def _parse_group_name(value: str) -> datetime | None:
    try:
        d, t = value.strip().split()
        return datetime(int(d[4:8]), int(d[2:4]), int(d[0:2]), int(t[0:2]), int(t[2:4]), tzinfo=TZ)
    except Exception:
        return None

def _ts_to_dt(value):
    try:
        return datetime.fromtimestamp(int(value), tz=TZ)
    except Exception:
        return None

def get_trial_datetime_by_phone(phone: str) -> tuple[datetime, bool]:
    phone = _normalize_phone(phone)
    fallback_dt = datetime.combine((datetime.now(TZ) + timedelta(days=1)).date(), time(16, 0), tzinfo=TZ)
    resp = requests.get(f"{BASE_URL}/api/v4/contacts", headers=HEADERS, params={"query": phone, "with": "leads"}, timeout=20)
    resp.raise_for_status()
    contacts = resp.json().get("_embedded", {}).get("contacts", [])
    if not contacts: return fallback_dt, False
    contact = contacts[0]
    lead_id = next((l.get("id") for l in contact.get("_embedded", {}).get("leads", []) if l.get("id")), None)
    if not lead_id: return fallback_dt, False
    lead_resp = requests.get(f"{BASE_URL}/api/v4/leads/{lead_id}", headers=HEADERS, params={"with": "catalog_elements"}, timeout=20)
    lead_resp.raise_for_status()
    catalog_elements = lead_resp.json().get("_embedded", {}).get("catalog_elements", [])
    if not catalog_elements: return fallback_dt, False
    catalog_element_id = catalog_elements[0].get("id")
    if not catalog_element_id: return fallback_dt, False
    resp = requests.get(f"{BASE_URL}/api/v4/catalogs/12278/elements/{catalog_element_id}", headers=HEADERS, timeout=20)
    resp.raise_for_status()
    catalog_data = resp.json()
    for f in catalog_data.get("custom_fields_values", []):
        if f.get("field_name") == "Дата и время занятия":
            values = f.get("values") or []
            if values and values[0].get("value") is not None:
                dt = _ts_to_dt(values[0]["value"])
                return (dt, True) if dt else (fallback_dt, False)
    dt = _parse_group_name(catalog_data.get("name", ""))
    return (dt, True) if dt else (fallback_dt, False)


# TZ = ZoneInfo("Europe/Oslo")
# def _normalize_phone(phone: str) -> str:
#     return re.sub(r"\D+", "", phone or "")

# def _parse_group_name(value: str) -> datetime | None:
#     try:
#         date_part, time_part = value.strip().split()
#         dt = datetime(
#             int(date_part[4:8]),
#             int(date_part[2:4]),
#             int(date_part[0:2]),
#             int(time_part[0:2]),
#             int(time_part[2:4]),
#             tzinfo=TZ
#         )
#         return dt
#     except Exception:
#         return None

# def get_trial_datetime_by_phone(phone: str) -> tuple[datetime, bool]:
#     phone = _normalize_phone(phone)
#     fallback_dt = datetime.combine((datetime.now(TZ) + timedelta(days=1)).date(), time(16, 0), tzinfo=TZ )
#     url = f"{BASE_URL}/api/v4/contacts"
#     resp = requests.get( url, headers=HEADERS,
#         params={ "query": phone, "with": "leads", },
#         timeout=20,
#     )
#     resp.raise_for_status()
#     data = resp.json()
#     print("data1", data)
#     print()
#     contacts = data.get("_embedded", {}).get("contacts", [])
#     if not contacts:
#         return fallback_dt, False
#     contact = contacts[0]
#     leads = contact.get("_embedded", {}).get("leads", [])
#     if not leads: return fallback_dt, False
#     lead_id = leads[0].get("id")
#     lead_url = f"{BASE_URL}/api/v4/leads/{lead_id}"
#     lead_resp = requests.get( lead_url, headers=HEADERS,
#         params={"with": "catalog_elements"},
#         timeout=20, )
#     lead_resp.raise_for_status()
#     lead_data = lead_resp.json()
#     print("data2", lead_data)
#     print()
#     catalog_elements = lead_data.get("_embedded", {}).get("catalog_elements", [])
#     if catalog_elements:
#         catalog_element_id = catalog_elements[0].get("id")
#         url = f"{BASE_URL}/api/v4/catalogs/12278/elements/{catalog_element_id}"
#         resp = requests.get(url, headers=HEADERS, timeout=20)
#         resp.raise_for_status()
#         catalog_data = resp.json()
#         print("data3", catalog_data)
#         print()
#         group_dt = _parse_group_name(catalog_data.get("name"))
#         return ((group_dt, True) if group_dt else (fallback_dt, False))
#     return fallback_dt, True


# def get_trial_datetime_by_phone(phone: str) -> tuple[datetime, bool]:
#     phone = _normalize_phone(phone)
#     fallback_dt = datetime.combine( (datetime.now(TZ) + timedelta(days=1)).date(),
#         time(16, 0), tzinfo=TZ )
#     url = f"{BASE_URL}/api/v4/contacts"
#     resp = requests.get(
#         url, headers=HEADERS,
#         params={ "query": phone, "with": "leads", },
#         timeout=20,
#     )
#     resp.raise_for_status()
#     data = resp.json()
#     contacts = data.get("_embedded", {}).get("contacts", [])
#     if not contacts:
#         return fallback_dt, False
#     contact = contacts[0]
#     custom_fields = contact.get("custom_fields_values") or []
#     for field in custom_fields:
#         if field.get("field_id") == TRIAL_DATETIME_FIELD_ID:
#             values = field.get("values") or []
#             if not values:
#                 break
#             trial_dt = _parse_trial_value(values[0].get("value"))
#             if trial_dt is not None:
#                 return trial_dt, True
#     return fallback_dt, False

# тест телефон 89521082823
# группа 21-05-2026 19-00
phone_test = "89521082823"
print(get_trial_datetime_by_phone(phone_test))