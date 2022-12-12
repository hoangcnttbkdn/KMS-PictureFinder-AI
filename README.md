# KMS-PictureFinder-AI
```
In this version, Service AI provide 3 main feature:
- Find person in picture with the face (InsightFace)
- Find person in picture with BIB code (PaddleOCR)
- Find person in picture with Clothes (Openpifpaf + Histogram comparison)
```

## Result
### Find with BIB code
![](./assets/images/bib-findor.jpg)
### Find with clothes
![](./assets/images/clothe-findor.jpg)
### Find with face
![](./assets/images/face-findor.jpg)

(replace the link youtube + "/sddefault.jpg" to get the maximum resolution thumbnail)

![Watch the video](https://img.youtube.com/vi/nTQUwghvy5Q/maxresdefault.jpg)](https://youtu.be/nTQUwghvy5Q)

## Architecture

* **Current version**
![](./assets/images/architect_1.png)

* **The next version**
![](./assets/images/architect_2.png)

## Version 1.0.0

## Install and setup environment:

Local env:
`make install`

Docker version:
`make dc-up`

## Run:
- `make run`
