import requests

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

params = {
    'token': 'eyJraWQiOiJZdXlYb1kiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoiY29tLmZvb3RiYWxsdGFya293LmNvbSIsImV4cCI6MTY5MTMxNzgxMCwiaWF0IjoxNjkxMjMxNDEwLCJzdWIiOiIwMDE3NTguNmQ4ODZlMzQwNDkyNDA1ZThmODU0ZDkxZDRjZGMwNTguMTUyNyIsImNfaGFzaCI6IjVPc1gwaEJnNVIxQmxwMEJxSXoxRXciLCJlbWFpbCI6IjhmMnBza2t2dGhAcHJpdmF0ZXJlbGF5LmFwcGxlaWQuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiaXNfcHJpdmF0ZV9lbWFpbCI6InRydWUiLCJhdXRoX3RpbWUiOjE2OTEyMzE0MTAsIm5vbmNlX3N1cHBvcnRlZCI6dHJ1ZX0.wG1izbJ44AT8n0sJirwkRMhk5mIemxzhGad2YWzehwud7OrvOiG5_Qayd5NqGiHRDkRm1faFeX94f2xLlpAe34vz_ejtexdYQAychfb6a9-xw1tSysZh33W31cRwIcuf6zYXuoQS9b_Xs37w1rhzrA2RgfyZcGGPjV83JwpOnSODauvSR4RbLPYMVpIV4zqNw1qcd2I2Lh3_lXSvYmijm4g1GRJNGYOFxv7d2LAixNhZrbC3B6sHOFdLXCbOba-0GWqSZnGEHcXBV-u8ymcTgebWzhhCy5HKrccr4fYKbyncOiycRdAtT7651toeapD1oSqOk2R6UfdjdCpYaHMiXg',
}

response = requests.post('http://192.168.0.103:8000/revoke-token', params=params, headers=headers)

print(response.status_code)
print(response.text)
