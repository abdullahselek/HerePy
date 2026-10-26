import json
from pathlib import Path
from unittest.mock import AsyncMock, patch, sentinel

import httpx2

ASYNC_SUCCESS = {
    "items": [],
    "evStations": [],
    "results": [],
    "Res": {
        "Stations": {},
        "Coverage": {},
        "NextDepartures": {},
        "MultiNextDepartures": {},
        "Connections": {"Connection": []},
        "LocalCoverage": {},
    },
    "TracePoints": [],
    "observations": {},
    "forecasts": {},
    "dailyForecasts": {},
    "hourlyForecasts": {},
    "astronomy": {},
    "alerts": {},
    "nwsAlerts": {},
    "departure": {},
    "arrival": {},
    "isolines": {},
    "TRAFFIC_ITEMS": [],
    "RWS": [],
    "Response": {},
    "routes": [],
    "matrix": {"numOrigins": 1, "numDestinations": 1, "travelTimes": [1]},
    "matrixId": "matrix",
    "status": "accepted",
    "statusUrl": "https://example.com/status",
}


async def assert_async_get_cases(test_case, api, cases, response_type, fixture=None, payload=None):
    if fixture is not None:
        with Path(f"testdata/models/{fixture}").open(encoding="utf-8") as file:
            payload = json.load(file)
    if payload is None:
        payload = ASYNC_SUCCESS

    async with api:
        client = api._get_async_client()
        for case in cases:
            method_name, arguments = case[:2]
            case_response_type = case[2] if len(case) > 2 else response_type
            case_payload = payload
            if len(case) > 3:
                with Path(f"testdata/models/{case[3]}").open(encoding="utf-8") as file:
                    case_payload = json.load(file)
            with (
                test_case.subTest(method=method_name),
                patch.object(
                    client,
                    "get",
                    new=AsyncMock(return_value=httpx2.Response(200, json=case_payload)),
                ) as get,
            ):
                with patch.object(case_response_type, "new_from_jsondict", return_value=sentinel.response):
                    if method_name == "async_calculate_route" and hasattr(api, "_get_response_with_short_route"):
                        with patch.object(api, "_get_response_with_short_route", return_value=sentinel.response):
                            result = await getattr(api, method_name)(*arguments)
                    else:
                        result = await getattr(api, method_name)(*arguments)
                test_case.assertIs(result, sentinel.response)
                get.assert_awaited_once()


async def assert_async_get_error_case(test_case, api, method_name, arguments, payload, error_type):
    if isinstance(payload, str):
        with Path(f"testdata/models/{payload}").open(encoding="utf-8") as file:
            payload = json.load(file)
    async with api:
        client = api._get_async_client()
        with patch.object(client, "get", new=AsyncMock(return_value=httpx2.Response(200, json=payload))) as get:
            with test_case.assertRaises(error_type):
                await getattr(api, method_name)(*arguments)
        get.assert_awaited_once()
