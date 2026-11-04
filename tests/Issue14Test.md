**Test:**



def test\_issue\_14():

&#x20;   links = \[

&#x20;       {"id": 1, "favorite": False, "created\_at": "2026-09-03"},

&#x20;       {"id": 2, "favorite": True, "created\_at": "2026-09-01"},

&#x20;       {"id": 3, "favorite": True, "created\_at": "2026-09-02"},

&#x20;   ]

&#x20;   assert \[x\["id"] for x in favorites\_first(links)] == \[3, 2, 1]



**Results:**



**C:\\Users\\lifes\\OneDrive\\Desktop\\Assignment 5\\LinkVaulterSEF26-JesusM>python -m pytest -v -k test\_issue\_14**

**================================================= test session starts =================================================**

**platform win32 -- Python 3.14.7, pytest-9.2.0, pluggy-1.7.0 -- C:\\Python314\\python.exe**

**cachedir: .pytest\_cache**

**rootdir: C:\\Users\\lifes\\OneDrive\\Desktop\\Assignment 5\\LinkVaulterSEF26-JesusM**

**configfile: pyproject.toml**

**testpaths: tests**

**collected 33 items / 32 deselected / 1 selected**



**tests/test\_issues.py::test\_issue\_14 PASSED                                                                       \[100%]**



**========================================== 1 passed, 32 deselected in 0.23s ===========================================**

