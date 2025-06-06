## Examples

### Image Example:

The example [export_image_and_display.py](export_image_and_display.py) exports the data as an image and displays with the [Pillow](https://github.com/python-pillow/Pillow) library. 
Install Pillow and run the example:

```sh
python3 -m pip install --upgrade Pillow
python3 examples/export_image_and_display.py
```
#### Output:

<img src="../resource/Spectrogram.jpeg" alt="Spectrogram Output" width="500">

### CSV Example:

The example [export_CSV_and_print.py](export_CSV_and_print.py) exports the data as a CSV file and prints it in the console:

```sh
python3 examples/export_CSV_and_print.py
```
#### Output:
```
['TIME', 'DURATION', 'VALUE']
['0.0000000000', '0.0000000000', '-0.000031']
['0.0000226757', '0.0000000000', '0.000000']
['0.0000453515', '0.0000000000', '0.000000']
...
```

### Multiple Types Example:

The example [export_multiple_types.py](export_multiple_types.py) exports the data as JPEG, CSV and JSON files to the **examples/exports/multiple** folder.

```sh
python3 examples/export_multiple_types.py
```
