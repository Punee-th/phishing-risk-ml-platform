# Phishing URL Risk ML Platform

A machine-learning system that analyses lexical URL characteristics and estimates whether a submitted URL resembles phishing or legitimate URLs.

The project includes URL canonicalisation, reproducible feature extraction, a trained Random Forest model, automated testing and a FastAPI inference service.

> This system is a research prototype and should not be treated as a standalone production security control.

## Key Features

- URL-only prediction without downloading webpage content
- 13 reproducible lexical URL features
- Domain-grouped evaluation on previously unseen domains
- URL canonicalisation to reduce formatting sensitivity
- Random Forest classification model
- FastAPI prediction service
- Interactive Swagger documentation
- Automated unit, integration and API tests
- Versioned model and metadata

## Important Dataset Finding

Initial experiments produced near-perfect test performance. Further investigation found that 31,744 root-level URLs ending in a trailing slash were labelled as phishing, while no legitimate observation used this pattern.

The model therefore learned a dataset-specific shortcut: adding a harmless trailing slash could reverse a prediction.

For example:

```text
https://www.adelaide.edu.au  → legitimate
https://www.adelaide.edu.au/ → phishing