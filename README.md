## uLauncher

Wii U download, decrypt and play helper

- [x] download
- [ ] decrypt
- [ ] launch

### Requirements

`db.json`: a database list of games, with the following format:

```json
[
    {
        "titleID": "123123123",
        "titleKey": "123123123",
        "name": "Game Title 1",
        "region": "USA"
    },
    {
        "titleID": "123123",
        "titleKey": "123123123",
        "name": "Game Title 2",
        "region": "EUR"
    },
    ...
]
```
Once you have that, copy it into the `ulauncher/` folder

[FunKiiU](https://github.com/llakssz/FunKiiU): copy FunKiiU.py into the `ulauncher/` folder

[CDecrypt-Release](https://github.com/MisterSirCode/CDecrypt-Release): copy `CDecrypt_v2.0b.exe`, `libeay32.dll` and `msvcr120d.dll` files into the `ulauncher/` folder

### How to run

Run it via

    python main.py

Your games will be in the `ulauncher/install/` directory.

### Testing

Tested on Windows 11, your mileage may vary significantly.