

#-----------------Part 1: Warmup-------------------

#----LLMs as Transform
#-----LLMs as Transform Question 1-------------

#use an LLM or deterministic code
#1. Parse the string "Jan 5th, 2024" into an ISO date format like "2024-01-05".

#I will use deterministic code to parse the string "Jan 5th, 2024" into an ISO date format. Because coding is better in
#parsing iso date than LLM

# 2. Classify a customer support ticket -- "my card was charged twice" -- into one of: billing, technical, or general.

# I will use LLM because LLM is good and better choice whith classification.  
# These require reading comprehension and judgment -- a regex cannot reliably do them.

#3. Calculate the average of a list of numbers.

# I will use deterministic code to calculate the average of a list of numbers.
#  Because coding is better in calculating arithmetic operations and average than LLM 

#4. Extract the company name from a freeform job title like "Sr. Data Eng @ Acme Corp (contract)".

# I will use LLM because  extraction is another strong fit for LLM than code.
# 
#  
# 5. Determine whether a product review is more than 100 words long.

# I will use deterministic code to determine whether a product review is more than 100 words long.
# Because coding is better in counting words than LLM.
#********************************************************************************************************
#-------LLMs as Transform Question 2-------------------------------------------

#In a comment block, explain what problem this creates downstream in a pipeline, and rewrite the prompt so it produces output
#  that is easy to parse and store reliably.
system = "Summarize this product review in a few sentences."

# The problem with this prompt is that it is open-ended and can produce a wide variety of outputs, 
# making it difficult to parse and store reliably in a downstream pipeline. 
# The output should be easy to parse without ambiguity.

system = "Summarize this product review in a few sentences. reply in json format with a single key 'summary' and the value being the summary of the review."

#********************************************************************************************

#-----LLMs as Transform Question 3----------------------------

#Your dataset has 50,000 records and you need to run a classification call for each one using gpt-4o-mini. In a comment block, answer:
# If each call takes 1 second on average, how long would sequential processing take?
# What is one practical strategy to handle this more efficiently at scale, without changing models?

# If each call takes 1 second on average, sequential processing for 50,000 records would take 13.89 hours
# Batch API will be a good practical strategy to handle this more efficiently at scale, without changing models.

#****************************************************************************************

# ---------------------Azure OpenAI-------
#-------------Azure OpenAI Question 1-----------

# An organization might use Azure OpenAI instead of calling the OpenAI API directly because: 
# With Azure OpenAI, requests stay inside Azure's infrastructure in the opposit of 
# OpenAI API, your data leaves your organization's infrastructure and travels to OpenAI's servers.
# Another reason is Azure OpenAI centralizes IT operations by consolidating AI and cloud expenses onto a single, predictable 
# invoice while managing support directly through Microsoft.

#-------------Azure OpenAI Question 2----


# When switching from openAI to AzureOpenAI, the client initialization takes three Azure-specific parameters:
# 1. azure_endpoint: This is the URL endpoint for the Azure OpenAI service. 
# 
# 2. azure-api-key: This is the API key provided by Azure to authenticate and authorize access to the Azure OpenAI service.
#
# 3. api_version: This specifies the version of the Azure OpenAI API to use.

#****************************************************************************************

#-----Azure OpenAI Question 3--------------------




# The model parameter in chat.completions.create() takes a deployment name. In Azure OpenAI, you do not call 
# a model directly -- you call a named deployment that your organization's admin created and configured.
#  The deployment name is chosen by whoever set up the resource.