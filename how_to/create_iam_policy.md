# Configuring IAM Policy for AWS Lambda Function
 
 ## IAM Policy
 1. Select the Identity and Access Management (IAM) Service
 2. Under Access Management > Select **Policies**
   <img src="source/images/iam/IAM_1.PNG" width=30% height=30%> 
 
 3. Select **Create Policy**
   <img src="source/images/iam/IAM_2.png" width=90% height=90%>
   
 4. Within the Visual Editor, Select the **Choose a service**
 
 5. Search **Lambda**
 
 <img src="source/images/iam/IAM_3.png" width=70% height=70%>
 
 6. Under the **Actions** Pane, Expand **Write** and Select &#x2611;**InvokeFunction**

<img src="source/images/iam/IAM_4.png" width=80% height=80%>


 8. Under **Resources** Pane, Select the &#x2611; **Any in this account**
 
 
 > **__NOTE:__** This will be modified later for fine-grained permissions
 
 <img src="source/images/iam/IAM_5.png" width=80% height=80%>
 
 8. Select **Next: Tags**
 9. Add a tag if you would like, e.g. **Key = Lambda | Value: InvokeFunction**
 10. Select **Next: Review**
 11. Input values for **Name** and **Description**
 12. Select **Create policy**
