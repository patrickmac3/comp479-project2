# Project Setup

## Setup

1. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**

    - **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    - **On Unix or macOS:**
        ```bash
        source venv/bin/activate
        ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

You can run the project in two ways:

### 1. Run `main.py`

```bash
python main.py --limit {limit} --k {k} --top {top} 
```

This command will build the index with a specified `limit` on the number of terms and save the index and mapper to the given paths. Once the index is built and saved, it will cluster the data into `k` clusters and display the `top n` vocabulary terms for each cluster.

Note, the index will be built and saved in the `index/` directory.

The default values for each parameter are: 
- `limit`: 50
- `k`: 7
- `top`: 20


### 2. Build the index

```bash
python build_index.py --limit {limit}
```

This command will only build the index.

Note, the index will be built and saved in the `index/` directory.
The default values for each parameter are: 
- `limit`: 50

### 3. Run the clustering process

```bash
python clustering.py --k {number_of_clusters} --top {top_n_terms_per_cluster} -
```

This command runs the clustering process with `k` clusters and displays the `top` n terms for each cluster. 

Note: when only executing the clustering, the index and mapper used are from the `index_main/` directory. 

The default values for each parameter are: 
- `k`: 7
- `top`: 20


# Project Demo

- `clustering`: directory containing the results from clustering with k=3 and k=6
- `clustering_faculty_department`: directory containing the clustering results from k = number of faculties (7) and k = number of departments (49)
- `index_main`: directory containing a compiled index and the document url to id mapper. 