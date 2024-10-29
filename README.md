# Information Retrieval System using ElasticSearch

The objective of this project is to develop an ad-hoc information retrieval system using the [ElasticSearch API](https://www.elastic.co). The ultimate goal is to implement various methods for analyzing and indexing document and query content, allowing for a comparative evaluation of different approaches in Spanish.

The following approaches have been implemented:

- **Base Approach**: Implements the default analyzer for Spanish, including lowercase conversion, removal of stopwords (using the Snowball-provided list), and a simple stemmer (sourced from Jacques Savoy’s resources).

- **Custom Stopwords**: Modifies the base approach to use a custom list of stopwords from the file `vacias.txt`. This file contains terms that appear in more than 20% of the documents.

- **Snowball Lemmatizer**: Replaces the base stemmer with the Snowball lemmatizer for Spanish.

- **Retrieval Model Change**: Modifies the default retrieval model. ElasticSearch’s latest versions use the BM25 model by default; here, it is changed to DFR (Divergence From Randomness).

### Test Collection

The Spanish test collection has been sourced from the CLEF conference materials, comprising:
- 15,000 documents,
- 25 queries
- the associated relevance judgments

The documents and queries are provided in XML files (`efe01.xml` to `efe10.xml` and `topics.xml`). Relevance judgments are in TREC format, located in `qrels.txt`. These files should ideally be in the `files` directory; however, due to privacy and compliance restrictions, they cannot be publicly shared.

### Evaluation of Results

The `trec_eval.exe` tool is used to evaluate the retrieval results. `trec_eval` is the standard tool used by the TREC community for evaluating ad-hoc retrieval runs, given a results file and a standard set of judged results.

"""