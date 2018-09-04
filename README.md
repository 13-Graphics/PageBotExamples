# PageBotExamples

## What is this project about?

The [PageBotExamples](https://github.com/TypeNetwork/PageBotExamples) project aims to be a central location for many good examples of PageBot documents, for a wide range of use-cases. The primary kind of contents are Python scripts, and any resources they include, which depend on the [TypeNetwork/PageBot](https://github.com/TypeNetwork/PageBot) Python library.

## Examples to be expected

Examples of PageBot generated documents are in the range of:

* Books
* TypeSpecimens
* Magazines
* Newspapers
* Portfolios
* Posters
* Thesis
* Websites

## History

During the early stages of PageBot development, many structural changes were made. The last major one began in November 2017, when the connection to the [DrawBot app](http://drawbot.com) became optional and other drawing environments became also possible, such as [Flat](https://github.com/xxyxyz/flat/).

This was done by adding a `Context` object, which made many of the examples break. Currently we are still working to make them compatible with the latest PageBot version and run again.

To avoid confusion, only the working examples will be published in this repository, for now leaving it more empty than intended.

## Repository

In well written PageBot scripts, the `_export` folder is automatically generated.

The `.gitignore` file has been set up to prevent these `_export` folders from being committed to this repository.

This way, locally generated documents will not be uploaded to GitHub automatically.

The `_local` folders are also ignored, and can be used for changes to scripts that are not yet working, for example.
