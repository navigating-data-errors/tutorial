# Hands-on Notebooks for the Tutorial on Navigating Data Errors in ML Pipelines

Links: **[[🌐 Tutorial Website](https://navigating-data-errors.github.io/)]** **[[👀 Review Slides](https://navigating-data-errors.github.io/pdf/navigating-data-errors-review-slides.pdf)]** **[[📜 Tutorial Paper](https://deem.berlin/pdf/icde-tutorial-navigating-data-errors-in-ml-pipelines.pdf)]**

The goal of this tutorial is to **showcase different notions of data importance**, based on the [DataScope](https://github.com/easeml/datascope) library. The notebooks revolve around a **toy problem of classifying the sentiment of recommendation letters**.

## Accessing the Tutorial Notebooks

We provide several notebooks walking you through several data debugging scenarios.

### Part 1: Data Errors

We begin by detailling how to leverage data importance to **identify impactful label errors** in the data.

 * https://colab.research.google.com/github/navigating-data-errors/tutorial/blob/main/navigating_data_errors_tutorial_part1_data_errors.ipynb

### Part 2a: Tracing Data Errors through Pipelines

We extend the previous notebook with a complex feature encoding pipeline, and show that we can **trace data errors through these pipelines** easily too. 

* https://colab.research.google.com/github/navigating-data-errors/tutorial/blob/main/navigating_data_errors_tutorial_part2a_with_pipeline.ipynb

### Part 2b: Tracing Data Errors through Pipelines with Dataframe Operations

We extend our example use case with dataframe operations, and show that we can **trace data errors through these relational operations** as well.

* https://colab.research.google.com/github/navigating-data-errors/tutorial/blob/main/navigating_data_errors_tutorial_part2b_with_dataframes.ipynb


## Frequently Asked Questions

### Can I run the notebooks locally?

Yes, after cloning the repo and entering the repo directory, run the following commands:

```bash
make shell
make setup
make jupyter
```

**Note:** The `make setup` command installs all the Python dependencies and needs to be run only the first time you set up the repository.
