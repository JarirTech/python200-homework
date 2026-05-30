Part 1: Warmup -- Check for Understanding
Answer each question in your own words in warmup_08.md. A sentence or two is enough for most questions -- you are demonstrating that you understood the concept, not writing an essay. Try to do this without AI assistance.
Cloud Concepts
These questions are based on the Cloud Overview lesson.
Cloud Concepts Question 1
What is the core economic model of cloud computing, and how does it differ from owning your own servers?
The core economic model of cloud computing is pay as you go. You only pay for what you use. If you need more compute or more resources you only need to do a simple click and you can scale vertically or horizontally as you need.
Cloud Concepts Question 2
What is the difference between vertical scaling and horizontal scaling? Give a concrete example of when you might choose each.
Vertical scaling when you scale on your current virtual machine(Ec2). You can add more memory, more storage, cpu…
Horizontal scaling when you deploy and add more machines responding to a current or a future increase and high demand on your website or app.
Then, for the three scenarios below, write one sentence saying which type of scaling applies and why.
A web app that normally handles 1,000 users per day suddenly needs to handle 100,000 after a viral product launch.
Horizontal scaling will be better because there is huge increase in the number of users. Deploying many machines will be a good choice.
A data scientist's model training job is running too slowly, and they want a machine with a faster GPU and more RAM.
In this case a vertical scaling will be enough, because the data scientist only need more gpu and ram and can have that by scaling vertically.
A data pipeline that processes 10 files per run now needs to process 10,000 files per run, and the work can be split across machine
	Horizontal scaling will be the best choice here as long as the work can be split across machines so adding more machines will be a good option.

Cloud Concepts Question 3
Before writing your definitions, classify each item in the list below as IaaS, PaaS, or SaaS. One sentence of reasoning is enough for each.
SaaS:
Gmail
GitHub Codespaces
Iaas:
Azure Virtual Machines
AWS S3 (Simple Storage Service)
 PaaS:
Snowflake
Azure App Service


IaaS: is a kind of cloud service where the cloud provider provision infrastructures as a resource for the user. As a developer or user I will be responsible for deploying my application, and responsible for the security of my application . An example is AWS Ec2 which you chose the type of operating system, the size of RAM, cpu and storage
PaaS: is a cloud service when the cloud provider provide all necessary infrastructures and platform to run your application or software. The provider manage the infrastructure, but you bring your own code. An example is Azure app service which is a platform for hosting web applications.
SaaS:


Software as a service is cloud service where the cloud provider provides every thing for you you only manage your security and your data. Everything else managed by the provider. An example is facebook, Turbo Tax service
Cloud Concepts Question 4
What is a managed data platform like Databricks or Snowflake, and how does it differ from using a cloud provider like Azure directly? What do you gain, and what do you give up?
managed data platform like Databricks or Snowflake take a different approach:  they pre-wire the pieces for you, optimizing specifically for data and analytics workloads. 
provisions and manages cloud resources on your behalf. This makes it much faster to get started with large-scale data processing or machine learning, at the cost of some flexibility and, potentially higher costs. 
Cloud Concepts Question 5
The lesson names two situations where the cloud is probably not the right choice. What are they?
The cloud isn't the right tool for every problem.
The cloud is likely not the right choice if your dataset fits on a single machine or if you lack massive compute demands, making local processing faster and cheaper for initial prototypes. Additionally, the steep learning curve and potential for high costs make it unsuitable when quick, simple, and inexpensive solutions are needed for smaller tasks.


Azure Basics
These questions are based on the Getting Started with Azure lesson.
Azure Basics Question 1
What is the difference between an Azure subscription and a resource group? Which one is yours alone, and which one does CTD share?
An Azure subscription is the main billing and management account that owns all the resources in an organization. CTD shares one subscription for the entire course, and all student resources are created inside it.
A resource group is a smaller container inside the subscription that organizes related cloud resources together, like a project folder or sandbox. Each student has their own personal resource group with the storage infrastructure already set up for Cloud Shell.


I use a resource group alone and I use a shared one subscription under CTD 
Azure Basics Question 2
Azure Cloud Shell is ephemeral by default. What does that mean in practice, and what does your course setup use to make it persistent?
It means that your work will be lost whenever your session ends or you close the terminal. The storage is not permanent.
The course setup a cloud drive for  storage so everything will be stored in that drive like a network shared drive.
Azure Basics Question 3
What is the difference between your SSH private key and your SSH public key? Which one gets uploaded to the remote systems you want to connect to, and why is that safe?
Both keys are saved in the cloud drive how ever you keep the private key  secretly, and never been shared, always on your drive and you only upload to the remote systems the public key.
This is safe because the public key cannot be used to recreate the private key. When you connect, the server checks that your private key matches the uploaded public key, allowing secure login without exposing your secret key. 
Azure Basics Question 4
Run the following command in Cloud Shell without the --output table flag:
az account show


{
  "environmentName": "AzureCloud",
  "homeTenantId": "0f040ddd-301f-4665-8677-7b21f129d605",
  "id": "4e07c58c-751e-4765-b40c-632b9ee6fe6e",
  "isDefault": true,
  "managedByTenants": [],
  "name": "CTD Nonprofit Sponsorship",
  "state": "Enabled",
  "tenantId": "0f040ddd-301f-4665-8677-7b21f129d605",
  "user": {
    "cloudShellID": true,
    "name": "live.com#bjarir001@gmail.com",
    "type": "user"
  }
}


Paste the output into your answer. Then describe in one sentence what changes when you add --output table.


The output was on the json format then when added --output table the display is clear, easy to read and understand.
