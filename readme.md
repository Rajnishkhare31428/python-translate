## Project Brief

```
 This project includes two scripts written in python

 "html_processor.py": An script to convert plain text found inside html files to interpolation syntax and generates JSON file which can further be translated to different languages in order to make an angular application multilingual.

 Say for an instance input html is as below
"
<span>
 First Name
</span>
<span>
 Last Name
</span>
"

Html is converted as below:
"
<span>
 {{ 'firstName' | translate }}
</span>
<span>
 {{ 'lastName' | translate }}
</span>
"

Json created looks like:
{
    "firstName": "First Name",
    "lastName": "Last Name",
}

Now here comes the role of second script

 "translate.py": A Python script to translate JSON file to any or multiple language.

 This scripts takes json file in a language and converts it to other language while keys being preserved

 Input Json:
{
    "firstName": "First Name",
    "lastName": "Last Name",
}

Output Json:
{
    "firstName": "पहला नाम",
    "lastName": "अंतिम नाम",
}



```

## How to use the "Json Generator Script"

* Run "html_processor.py"
* Input your project's complete json file path.
* Input your angular application source(src directory) path.
* Hurray! All html file plain text in converted to interpolation syntax with a translate pipe
* Also "en.json" file is generated

## How to use Json Translate script

* Configure translation-config.json file which looks like below

    {
        "source_language": "en",
        "target_languages": [
            "hi",
            "es",
            "zh"
        ],
        "input_file": "D:\\LearnAngular\\Multilingual-Demo\\src\\assets\\lang-file\\en.json",
        "output_path": "D:\\LearnAngular\\Multilingual-Demo\\src\\assets\\lang-file"
    }
    
* set source_language code
* Put codes of language to which you want your project to be translated into in target_languages array.
* Mention your source json file path in input_file
* Mention output directory where all converted json will be created
* Congrates your angular application is converted to multiple languages within a few minutes