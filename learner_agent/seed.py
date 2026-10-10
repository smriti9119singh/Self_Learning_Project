TOPICS = {
    "Python fundamentals": {
        "objective": "Use variables, collections, functions, loops, and comprehensions to solve small problems.",
        "tags": "python variables lists dictionaries functions loops comprehensions beginner programming",
        "activity": "Write a function that filters and summarizes a list of scores.",
    },
    "Data handling with pandas": {
        "objective": "Load, inspect, clean, transform, and summarize tabular data with pandas.",
        "tags": "python pandas dataframe data cleaning missing values groupby csv data analysis",
        "activity": "Load a CSV, handle missing values, then group rows and calculate a mean.",
    },
    "Machine learning basics": {
        "objective": "Explain supervised learning, features, labels, training, and evaluation.",
        "tags": "machine learning supervised features labels classification regression training evaluation",
        "activity": "Sketch a small classification pipeline and identify its feature and label.",
    },
    "Model evaluation": {
        "objective": "Choose suitable metrics and use validation data to estimate generalization.",
        "tags": "machine learning metrics accuracy precision recall f1 validation test overfitting",
        "activity": "Compare accuracy and recall for an imbalanced classification example.",
    },
    "Generative AI and prompting": {
        "objective": "Write clear prompts, understand model limitations, and check generated answers.",
        "tags": "generative ai llm prompt context hallucination language model tokens",
        "activity": "Improve a vague prompt by adding context, a task, and an output format.",
    },
    "Agentic AI and tools": {
        "objective": "Describe how an agent plans, chooses tools, observes results, and continues safely.",
        "tags": "agentic ai agents tools planning observation loop function calling workflow",
        "activity": "Design a two-step agent workflow and specify its input, tool, and stopping condition.",
    },
}

QUIZZES = {
    "Python fundamentals": [
        {"question": "What does list comprehension [x * 2 for x in [1, 2, 3]] produce?", "options": ["[2, 4, 6]", "[1, 2, 3, 2]", "[1, 4, 9]", "An error"], "answer": "[2, 4, 6]", "explanation": "The expression x * 2 is evaluated once for every item in the list."},
        {"question": "Which Python structure stores key-value pairs?", "options": ["tuple", "set", "dictionary", "string"], "answer": "dictionary", "explanation": "A dictionary maps unique keys to values, for example {'name': 'Asha'}."},
        {"question": "What does range(3) produce when used in a for loop?", "options": ["0, 1, 2", "1, 2, 3", "0, 1, 2, 3", "Only 3"], "answer": "0, 1, 2", "explanation": "range(3) starts at zero and stops before three."},
        {"question": "What is the value of len({'a': 1, 'b': 2})?", "options": ["1", "2", "3", "An error"], "answer": "2", "explanation": "len() on a dictionary returns the number of keys."},
        {"question": "Which keyword sends a value back from a function?", "options": ["yield", "return", "break", "pass"], "answer": "return", "explanation": "return exits the function and provides its result to the caller."},
    ],
    "Data handling with pandas": [
        {"question": "Which pandas method gives a quick summary of numeric columns?", "options": ["describe()", "rename()", "append()", "sort_index()"], "answer": "describe()", "explanation": "DataFrame.describe() reports statistics such as count, mean, and quartiles."},
        {"question": "Which pandas method can detect missing values?", "options": ["isna()", "isupper()", "tolist()", "merge()"], "answer": "isna()", "explanation": "isna() returns a Boolean mask indicating missing values."},
        {"question": "How do you select the 'price' column from a DataFrame named df?", "options": ["df['price']", "df.price()", "df->price", "select(df, price)"], "answer": "df['price']", "explanation": "Square bracket indexing is the standard way to select a DataFrame column by its label."},
        {"question": "What does df.dropna() do by default?", "options": ["Removes rows with missing values", "Fills missing values with zero", "Renames missing columns", "Sorts missing values first"], "answer": "Removes rows with missing values", "explanation": "By default, dropna removes rows that contain at least one missing value."},
        {"question": "Which operation summarizes values for each category?", "options": ["groupby()", "head()", "astype()", "to_csv()"], "answer": "groupby()", "explanation": "groupby() splits rows into groups so you can aggregate each group."},
    ],
    "Machine learning basics": [
        {"question": "In supervised learning, what is a label?", "options": ["The target value the model learns to predict", "A random training row", "The optimizer", "A chart title"], "answer": "The target value the model learns to predict", "explanation": "Training examples pair features with known target labels or values."},
        {"question": "Which task predicts a continuous number?", "options": ["Regression", "Clustering", "Classification", "Tokenization"], "answer": "Regression", "explanation": "Regression estimates numeric values such as prices or temperatures."},
        {"question": "In a spam classifier, which is an example of a feature?", "options": ["The email's word counts", "Whether the email is spam", "The model's final accuracy", "The test set size"], "answer": "The email's word counts", "explanation": "Features are input measurements used by the model. Spam/not spam is the label."},
        {"question": "What is classification used to predict?", "options": ["A category or class", "A continuous measurement only", "A database schema", "A training duration"], "answer": "A category or class", "explanation": "Classification predicts discrete classes such as 'spam' or 'not spam'."},
        {"question": "Why should data be split before fitting preprocessing steps?", "options": ["To prevent information from the test set leaking into training", "To make all labels identical", "To increase the number of test rows", "To remove the need for evaluation"], "answer": "To prevent information from the test set leaking into training", "explanation": "Fit preprocessing only on training data, then apply it to held-out data to avoid leakage."},
    ],
    "Model evaluation": [
        {"question": "Why keep a test set separate from training?", "options": ["To estimate performance on unseen data", "To make training faster by deleting labels", "To guarantee perfect accuracy", "To create more features"], "answer": "To estimate performance on unseen data", "explanation": "A held-out test set helps estimate how well a model generalizes."},
        {"question": "For rare positive cases, which metric often matters more than accuracy alone?", "options": ["Recall", "Row count", "Training loss only", "Feature name"], "answer": "Recall", "explanation": "Recall measures the fraction of actual positives found; accuracy can hide missed rare cases."},
        {"question": "What does precision measure?", "options": ["The share of predicted positives that are truly positive", "The share of all negatives correctly rejected", "The total number of training examples", "The model's training time"], "answer": "The share of predicted positives that are truly positive", "explanation": "Precision is true positives divided by all predicted positives."},
        {"question": "What is a validation set commonly used for?", "options": ["Selecting model settings during development", "Reporting final performance after every tuning decision", "Replacing all training labels", "Storing production predictions"], "answer": "Selecting model settings during development", "explanation": "Validation data supports model selection; preserve the test set for a final, less biased estimate."},
        {"question": "A model scores very highly on training data but poorly on unseen data. What is a likely issue?", "options": ["Overfitting", "Under-sampling the test metric", "Perfect generalization", "Feature scaling success"], "answer": "Overfitting", "explanation": "A large train–test gap often signals that the model has memorized training-specific patterns."},
    ],
    "Generative AI and prompting": [
        {"question": "What is a useful way to reduce ambiguity in a prompt?", "options": ["Specify context, task, and desired format", "Remove all context", "Ask several unrelated tasks at once", "Request an answer without constraints"], "answer": "Specify context, task, and desired format", "explanation": "Clear context and output requirements help guide generation and make answers easier to check."},
        {"question": "What is a hallucination in an LLM response?", "options": ["A confident-sounding unsupported or incorrect claim", "A model update", "A type of database index", "An evaluation split"], "answer": "A confident-sounding unsupported or incorrect claim", "explanation": "Generated content can sound plausible while being false, so important claims need verification."},
        {"question": "What does grounding a response mean?", "options": ["Providing relevant evidence or context for the response", "Increasing model temperature", "Removing the user question", "Training without data"], "answer": "Providing relevant evidence or context for the response", "explanation": "Grounding gives the model useful source material to base its answer on."},
        {"question": "What is the purpose of a system instruction?", "options": ["Set the model's role and response guidelines", "Store the conversation permanently", "Guarantee factual accuracy", "Replace all user context"], "answer": "Set the model's role and response guidelines", "explanation": "System instructions guide behavior and format but do not guarantee correctness."},
        {"question": "Why should an important generated answer be checked?", "options": ["The model can produce plausible but incorrect claims", "All generated text is copied from a verified source", "Checking always makes the model forget", "Prompts cannot affect outputs"], "answer": "The model can produce plausible but incorrect claims", "explanation": "Language models can make mistakes, so consequential claims should be checked against reliable material."},
    ],
    "Agentic AI and tools": [
        {"question": "What makes a tool useful to an AI agent?", "options": ["It lets the agent take a defined action and observe a result", "It guarantees the agent is always correct", "It removes the need to check permissions", "It turns every output into training data"], "answer": "It lets the agent take a defined action and observe a result", "explanation": "Agents can select tools, inspect their outputs, and use those observations in a next step."},
        {"question": "Why should an agent have a stopping condition?", "options": ["To bound the workflow and avoid unending tool loops", "To prevent it from using context", "To make its answer random", "To remove the user goal"], "answer": "To bound the workflow and avoid unending tool loops", "explanation": "A clear stopping rule keeps agent workflows finite and easier to inspect."},
        {"question": "In a tool-using agent loop, what should happen after a tool returns?", "options": ["The agent should inspect the result before choosing its next step", "The result should always be ignored", "The agent should call every available tool", "The result should be treated as guaranteed truth"], "answer": "The agent should inspect the result before choosing its next step", "explanation": "Observing tool output lets the agent decide whether it has enough information or needs another action."},
        {"question": "What is a benefit of giving an agent a narrow tool interface?", "options": ["It limits actions to defined capabilities", "It guarantees correct reasoning", "It removes the need for input validation", "It lets the model edit any file"], "answer": "It limits actions to defined capabilities", "explanation": "A narrow interface makes an agent easier to reason about, constrain, and audit."},
        {"question": "When should an agent ask the user instead of guessing?", "options": ["When required information is missing or ambiguous", "Whenever a tool returns any result", "Only after an infinite loop", "Never; agents should always guess"], "answer": "When required information is missing or ambiguous", "explanation": "Clarifying material uncertainty is safer and more useful than acting on a guess."},
    ],
}
