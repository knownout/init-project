# Create projects from your own templates

*Read this in other languages:* [Russian](README.ru-RU.md), English *(current)*

**Init-projects** is a program written in Python for quickly creating 
projects based on your own templates

The purpose of this script is to make both the creation of projects 
and templates as easy as possible. With init-project, in order to create 
your template, you will need:
1. Create a configuration file *init-project.json* at 
the root of your project
2. Add the "files" key to this file and give it the following value:

```json5
{
    // ... other options
    "files": {
        // ... other files
        "path/to/file.ext": {
            "variable-name": "variable-value"
        },
        // other files ...
    },
    // other options ...
}
```

3. Additional variables can be created using the "define" key 
(an example is given below)
4. To use a variable inside a configuration file, simply replace 
the value of the file variable with *#VariableName*

### Available variables

All keys that are in the configuration file (except "define" and "files") 
will be converted into variables in the following way: 
"version" -> "#TemplateVersion". Thus, if you specify "#TemplateVersion" 
as the value of a file variable, the value of the 
"version" key will be used

Exceptions: 
- The "author" key will be converted to *#Author* instead of 
*#TemplateAuthor*. This is because the *#Author* variable can be 
set both inside the template configuration file and inside the 
program configuration file, and the TemplateAuthor name is not 
very suitable here.
- The key "template" will be converted to *#TemplateName* 
because the name *#TemplateTemplate* doesn't look good

With the "define" key in the template configuration file, you can 
create your own variables. The names of these variables will 
not be transformed, but they must be specified (in the "define" section) 
without a hash mark:
```json5
{
    // ...
    "define": {
        "MyCustomVariable": "This is my custom variable",
        "MyCustomAuthor": "Made by #Author"
    }
    // ...
}
```

### Templates
In order for the program to create new projects from your templates, 
replace the necessary values in the files (such as package.json,
manifest.json, index.html, etc.) with the variable names from the 
"files" section. As an example, let's add a variable 
to the package.json file

```json5
// Before
{
    // ... some things
    "name": "app-name",
    // other things ...
}
```
```json5
// After
{
    // ... some things
    "name": "@application-name",
    // other things ...
}
```

To make everything work, the specified variable must also be set in 
the "files" section of the template configuration file *(init-project.json)*
```json5
{
    // ...
    "files": {
        // ... some other files
        "package.json": {
            "@application-name": "#ApplicationName"
        },
        // ...
    }
}
```

### Notes
- If a variable is set in the "files" section, but the program 
could not find it either in the "define" section or in the file 
itself, the user will be prompted to enter the variable value manually

- If the "author" variable is specified in the config.json file 
(script configuration file, created automatically), then it will replace 
the "author" variable from the template configuration file

- The "default-author" variable from the config.json file will 
only be used if the "author" variable is not set in either the 
script config file or the template config file

re-knownout - https://github.com/re-knownout/
<br />
knownout@hotmail.com