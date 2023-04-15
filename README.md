# LampTest

Установка

pip3 install -i https://test.pypi.org/simple/ example-package-lamp==0.0.6

Запуск
```
from example_package_lamp import start
import time


if __name__ == '__main__':
    while True:
        start(host='127.0.0.1', port=9999)
        time.sleep(2)
 ```
