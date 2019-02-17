# autoilr

Command line interface to MIT's Auto-ILR system found at: https://auto-ilr.ll.mit.edu/instant/

## Getting Started

The only non-standard Python requirment is the requests library.

### Prerequisites

You get get requests with pip

```
pip install requests
```

### Installing

If you want to import it and use it in your own scripts you can install it with

```
pip install git+https://github.com/bmswens/autoilr
```

If you want to use it as a command line tool, you can clone it to the directory you want to use it out of

```
git clone https://github.com/bmswens/autoilr
```

## Use

In your own code:
```
import autoilr.autoilr as autoilr

text = "This is some text in the English Language."

level = autoilr.get_level(text, "English")
```

Command line (using multiple files):
```
python autoilr.py -f Chinese-Simplified 孙子兵法.txt 西游记.txt 孔乙己.txt
```

## Authors

* **Brandon Swenson** - *Initial work* - [bmswens](https://github.com/bmswens)

See also the list of [contributors](https://github.com/bmswens/autoilr/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* MIT - creating the website this utilizes
* DLI - for teaching me a language that I now avoid
