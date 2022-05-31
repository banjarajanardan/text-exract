# Document Parser Documentation

#### Contents
- [Environment Setup](#1-environment-setup)
- [Overview](#2-overview)

## 1. Environment Setup

Recommended Linux, python 3.8.10

### 1.1 Setting Up Environment
* create virtual environment
    * virtualenv venv --python=python3.8
* activate virtual environment
    * . ./venv/bin/activate (linux)
    * . ./venv/Scripts/activate (windows)
* EasyOcr installation (https://www.analyticsvidhya.com/blog/2021/06/text-detection-from-images-using-easyocr-hands-on-guide/)
    * pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu (linux)
    * pip install torch torchvision torchaudio (windows/mac)
* pip install -r app/requirements.txt

### 1.2 Running Server
* . ./runserver.sh (linux)
    * runs gunicorn server
* . ./runserver_windows.sh (windows/linux)
    * runs flask development server

### 1.3 Testing
* import `WeWrite.postman_collection.json` to postman
* send request to `text_extract` collection to extract text from pdf, image, docx and text files

## 2. Overview
### 2.1 Find Answer In Passage
Api: ` POST http://127.0.0.1:8000/api/v1/extract/text/`
```
POST /api/v1/extract/text/
Content-Type: multipart/form-data
Header: {token: <TOKEN>}
FormData: {files: <FILES>}
```
| Parameter       | Type     | Required?  | Description  |
| -------------   |----------|------------|--------------|
| `TOKEN`         | string   | required   | Static token to authorize the request |
| `FILES`         | file     | required   | File form which text is to be extracted. Supported format `.pdf`, `.jpg`, `.jpeg`, `.png`, `.tif`, `.tiff`, `.docx`, `.txt`. Multiple files of different types are supported in a single request. |

Response of a successful request
```
{
    "data": " Your Name 123 Your Street Your City, ST 12345 (123) 456-7890 no_reply@example.com 4th September 20XX Ronny Reader CEO, Company Name 123 Address St  Anytown, ST 12345 Dear Ms. Reader, Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan. Nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet doming id quod mazim placerat facer possim assum. Typi non habent claritatem insitam; est usus legentis in iis qui facit eorum claritatem. Investigationes demonstraverunt lectores legere me lius quod ii legunt saepius. Sincerely,    Your Name\nA Simple PDF File This is a small demonstration .pdf file - just for use in the Virtual Mechanics tutorials. More text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. Boring, zzzzz. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. Even more. Continued on page 2 ...\nSimple PDF File 2 ...continued from page 1. Yet more text. And more text. And more text. And more text. And more text. And more text. And more text. And more text. Oh, how boring typing this stuff. But not as boring as watching paint dry. And more text. And more text. And more text. And more text. Boring. More, a little more text. The end, and just as well.",
    "error": "",
    "message": "",
    "status": "success",
    "status_code": 200
}
```

| Parameter       | Type     | Description  |
| -------------   |----------|--------------|
| `DATA`          | string   | Text of each file separated by `\n` |
| `ERROR`         | string   | Error code in case request is unsuccessful |
| `MESSAGE`       | string   | Description of error in case request is unsuccessful |
| `STATUS`        | string   | `success` if request is successful else `fail` |
| `STATUS_CODE`   | int      | HTTP response status code. Eg: 200 for success, 401 for unauthorized. |