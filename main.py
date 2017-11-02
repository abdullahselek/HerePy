import herepy

def main():
    api = herepy.GeocoderApi('DemoAppId01082013GAL', 'AJKnXv84fjrb0KIHawS0Tg', 20)
    data = {'searchtext': '200 S Mathilda Sunnyvale CA', 'app_id': api._app_id, 'app_code': api._app_code}
    print herepy.Utils.build_url(api._base_url, extra_params=data)
    response = api.free_form('200 S Mathilda Sunnyvale CA')
    print response

main()
