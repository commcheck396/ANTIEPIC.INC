### Data Cleaning and Processing

#### Data Overview

The provided dataset consists of five JSON files:

1. **`australian_user_reviews.json`**: This dataset contains user information and their corresponding reviews:
   - Includes user ID, name, profile URL, and all reviews posted by the user. Each review contains details such as the game reviewed, review date, whether it was recommended, the review text, and counts of helpful or funny reactions.

2. **`australian_users_items.json`**: This dataset contains user inventories, i.e., the items in their game libraries:
   - Includes user ID, name, profile URL, and all games in the user's library. Each game entry contains details like game ID, name, recent playtime (last two weeks), and total playtime.

3. **`bundle_data.json`**: This dataset contains information about game bundles and their components:
   - Includes bundle ID, name, original price, discounted price, URL, and details about the games within the bundle, such as game ID, name, genre, URL, and discounted price.

4. **`steam_games.json`**: This dataset contains information about games available on Steam:
   - Includes game ID, name, developer, publisher, genres, tags, positive rating percentage, URL, release date, price, and other detailed attributes.

For our project, we selected **`steam_games.json`**, **`australian_users_items.json`**, and **`australian_user_reviews.json`** as the primary datasets for data processing and analysis.

#### Challenges Encountered

During the data cleaning and processing phase, we encountered several challenges:

1. **JSON Syntax Issues**  
   The datasets had significant syntax issues that violated JSON standards, particularly with inconsistent usage of quotes:
   - Most elements used single quotes instead of the required double quotes, making it impossible for standard JSON parsers to process the files.
   - Some elements contained both single and double quotes, relying on escape characters, which further complicated parsing.
   - Other minor issues included improper boolean formatting (e.g., `True`/`False` instead of `true`/`false`) and incorrect use of commas for separation.

2. **Large Dataset Size**  
   Some datasets exceeded 500MB, with one surpassing 3GB. Loading such large files entirely into memory for training or analysis was impractical. Simple sampling exacerbated the issue by introducing **cross-dataset sampling inconsistency**:
   - User reviews and game details were stored in separate files. Sampling a subset from one file often resulted in reviews for games that lacked corresponding information in the other file, leading to uncorrelated data and reduced utility.

#### Solutions Implemented

1. **Handling JSON Syntax Issues**  
   Initially, we attempted to use third-party libraries such as `json5` or `demjson` to address the syntax issues. While these libraries successfully parsed the files, they were extremely slow, taking nearly a minute to read just a thousand records. This was far below our performance expectations.

2. **Conditional Sampling**  
   To address both performance and inconsistency issues, we explored a conditional sampling approach:
   - We first sampled a subset of users, identified the games they reviewed, and then sampled data from related datasets to retain only relevant users and games.  
   - However, this approach required significant data reduction, which resulted in the loss of valuable information.

3. **Custom Parser and Preprocessing**  
   Ultimately, we developed a custom parser to preprocess and trim the datasets:
   - The parser normalized the syntax by fixing quote inconsistencies, handling escape sequences, and resolving boolean formatting and comma issues.
   - Irrelevant or unused information was removed during preprocessing.
   - After preprocessing, we used a standard JSON library for efficient data loading, enabling us to process nearly the entire dataset with excellent performance.

#### Data Transformation

Using the cleaned datasets, we constructed two primary data structures:

1. **`game_details` Dictionary**  
   - **Key**: Game ID  
   - **Value**: A dictionary containing game developer and tag information.  
   - Only includes games with valid IDs.  
   - Example structure:  
     ```json
     {
       "game_id": {
         "developer": "Developer Name",
         "tags": ["Tag1", "Tag2"]
       }
     }
     ```

2. **`user_data_map` Dictionary**  
   - **Key**: User ID  
   - **Value**: A dictionary with two main sub-dictionaries: `reviews` and `items`.  
     - **`reviews` Sub-Dictionary**:  
       - **Key**: Game ID  
       - **Value**: User review details, including review date and recommendation status.  
     - **`items` Sub-Dictionary**:  
       - **Key**: Game ID  
       - **Value**: User’s game information, including total playtime and recent playtime.  
   - Example structure:  
     ```json
     {
       "user_id": {
         "reviews": {
           "game_id": {
             "review_date": "YYYY-MM-DD",
             "recommended": true
           }
         },
         "items": {
           "game_id": {
             "total_playtime": 100,
             "recent_playtime": 5
           }
         }
       }
     }
     ```