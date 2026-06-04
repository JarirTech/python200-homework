#Part 1: Warmup

## --- Azure Authentication --- 
# ---- Azure Authentication Question 1-------

#When you run a Python script locally that uses DefaultAzureCredential, it relies on your existing Azure authentication 
# session to sign in. Before running the script, you must first run the az login command to authenticate with Azure.

#When a DefaultAzureCredential instance is created, it tries several authentication methods in a specific order 
# and uses the first one that succeeds. These methods include environment variables, managed identities
#  (for Azure-hosted resources), Azure CLI credentials from your az login session, and other developer 
# authentication tools. If it detects a valid Azure CLI login session, it automatically uses those credentials 
# to authenticate your application.

#***************************************************************************************
# -----Azure Authentication Question 2-------------------

#why can't a deployed pipeline (running on an Azure VM or container) use az login for authentication? 
# What does it use instead, and why does the same Python code work without changes?

#A deployed pipeline cannot use az login because there is no  human around to run az login. 
# Instead, it uses a Managed Identity provided by Azure through Microsoft Entra ID.

#The same Python code works without changes because DefaultAzureCredential automatically chooses the best 
# authentication method. Locally, it uses the az login session, and in Azure, it uses the Managed Identity.
#*********************************************************************************
#------Azure Authentication Question 3--------

#You run a script that creates a DefaultAzureCredential and immediately gets an AuthenticationError. In a comment block,
#  describe the two most likely causes and how you would diagnose each.
#1. The most likely cause is that you have not run az login to authenticate with Azure. To diagnose this, you can check
#  if you have an active Azure CLI session by running ***az account show*** in your terminal. If it returns an error or shows 
# no active subscriptions, you need to run az login.
#2. Another likely cause is that your Azure CLI session has expired or is not properly configured.
#  To diagnose this, you can run ***az account list*** to see if your subscriptions are listed and if you have 
# the correct permissions. If you see an error or no subscriptions, you may need to re-authenticate with az login
#  or check your Azure CLI configuration.
#**************************************************************************************
#----------------Blob Storage---------
#----------------Blob Storage Question 1--------------------

# describe the three-level hierarchy of Azure Blob Storage in your own words. Give a concrete analogy that maps each level to 
# something familiar (a filesystem, a filing cabinet, etc.).

#Azure Blob Storage has a three-level hierarchy: Storage Account, Container, and Blob.

#Azure Blob Storage has three levels: the storage account, containers, and blobs. A storage account is like
#  a filing cabinet, containers are like folders inside the cabinet, and blobs are the individual files stored 
# in those folders. 

#*********************************************************************************************************
#----------Blob Storage Question 2-------

#For each scenario below, write one sentence in a comment block saying whether you would use Blob Storage or 
# a relational database (like Azure SQL), and why.

#A REST API returns a JSON payload each hour. You need to store the raw responses for reprocessing later.

# I will use Blob storage because the returned raw output is a json payload no need for strectured data and relational database is not needed.  
#
#Your pipeline produces a table of 50 million customer transactions that your analytics team queries by date
#  range and customer ID every day.
#
# I will use a relational database because the data is structured and needs to be queried by date range and customer ID, 
# which is more efficient in a relational database than in Blob Storage.

#A computer vision model produces image embeddings as NumPy arrays. You need to save them between pipeline runs.

# I will use Blob Storage because the image embeddings are unstructured data and can be efficiently stored as 
# binary files in Blob Storage.
#****************************************************************************************
# ----Blob Storage Question 3------------------------------------------------------

#Write a function list_container(container_client) that prints the name and size (in bytes) of every blob in the container,
#  one per line. The function should take a ContainerClient object as its only argument and return nothing.

def list_container(container_client):
    blobs = container_client.list_blobs()
    for blob in blobs:
        print(f"{blob.name}: {blob.size} bytes")

#*********************************************************************************

#---------------Blob Storage Question 4------------
#Write a function upload_text(container_client, blob_name, text) that encodes a Python string as
#  UTF-8 and uploads it as a blob, overwriting any existing blob with the same name. The function should
#  take a ContainerClient, a blob name string, and a text string, and return nothing.
def upload_text(container_client, blob_name, text):
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(text.encode('utf-8'), overwrite=True)
    