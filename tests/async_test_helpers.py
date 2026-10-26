import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx2


async def assert_async_get_cases(test_case, api, cases, response_type, fixture=None):
    async with api:
        client = api._get_async_client()
        for case in cases:
            method_name, arguments = case[:2]
            case_response_type = case[2] if len(case) > 2 else response_type
            case_fixture = case[3] if len(case) > 3 else fixture
            if case_fixture is None:
                raise ValueError(f"No response fixture specified for {method_name}.")
            with Path(f"testdata/models/{case_fixture}").open(encoding="utf-8") as file:
                case_payload = json.load(file)
            with (
                test_case.subTest(method=method_name),
                patch.object(
                    client,
                    "get",
                    new=AsyncMock(return_value=httpx2.Response(200, json=case_payload)),
                ) as get,
            ):
                result = await getattr(api, method_name)(*arguments)
                test_case.assertIsInstance(result, case_response_type)
                test_case.assertTrue(result)
                get.assert_awaited_once()
                test_case.assertTrue(get.await_args.args[0].startswith("https://"))
                test_case.assertEqual(get.await_args.kwargs["timeout"], api._timeout)
                test_case.assertTrue(result.as_dict())


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
